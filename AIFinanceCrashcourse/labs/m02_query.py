"""Module 2 lab, step 2: search ChromaDB with LlamaIndex, then let Claude write the answer.

    python m02_query.py "What are the main risk factors?"
    python m02_query.py "..." --top-k 8 --retrieve-only
    python m02_query.py "..." --print-prompt     # print the full prompt to paste into any free AI chat
"""

import argparse
import os
import sys
from pathlib import Path

import chromadb
from llama_index.core import PromptTemplate, Settings, VectorStoreIndex
from llama_index.core.postprocessor import SimilarityPostprocessor
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore

sys.path.insert(0, str(Path(__file__).resolve().parent))
from m02_claude_llm import ClaudeCLI  # noqa: E402

HERE = Path(__file__).resolve().parent
DB_PATH = HERE / "chroma_db"
COLLECTION = "medline_s1"
EMBED_MODEL = "BAAI/bge-small-en-v1.5"

ANSWER_PROMPT = PromptTemplate(
    "You are reading extracts from the Medline Inc. Form S-1 registration statement\n"
    "filed with the SEC on October 28, 2025. Each extract is labelled with the PDF\n"
    "page it came from.\n"
    "\n"
    "Extracts:\n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "\n"
    "Answer the question using only these extracts. Cite the page number after every\n"
    "fact, like (p. 44). If the extracts do not contain the answer, say so plainly and\n"
    "name what is missing. Do not use anything you know about Medline from elsewhere.\n"
    "\n"
    "Question: {query_str}\n"
    "Answer: "
)


def build_index() -> VectorStoreIndex:
    if not DB_PATH.exists():
        raise SystemExit("No database found. Run m02_ingest.py first.")
    Settings.embed_model = HuggingFaceEmbedding(model_name=EMBED_MODEL)
    client = chromadb.PersistentClient(path=str(DB_PATH))
    collection = client.get_collection(COLLECTION)
    vector_store = ChromaVectorStore(chroma_collection=collection)
    return VectorStoreIndex.from_vector_store(vector_store)


def pick_llm(use_api: bool, model: str):
    if use_api:
        if not os.environ.get("ANTHROPIC_API_KEY"):
            raise SystemExit("--api needs ANTHROPIC_API_KEY in the environment.")
        from llama_index.llms.anthropic import Anthropic

        return Anthropic(model=model)
    return ClaudeCLI(model=model)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("question")
    parser.add_argument("--top-k", type=int, default=6)
    parser.add_argument("--min-score", type=float, default=0.0)
    parser.add_argument("--model", default="claude-opus-5")
    parser.add_argument("--api", action="store_true", help="use the Anthropic API instead of the CLI")
    parser.add_argument("--retrieve-only", action="store_true", help="show chunks, skip the LLM")
    parser.add_argument("--print-prompt", action="store_true", help="print the assembled prompt instead of calling a model")
    args = parser.parse_args()

    index = build_index()

    # Step 1. Retrieve. The question is embedded with the same model as the
    # chunks, and Chroma returns the nearest ones.
    retriever = index.as_retriever(similarity_top_k=args.top_k)
    nodes = retriever.retrieve(args.question)
    if args.min_score > 0:
        nodes = SimilarityPostprocessor(similarity_cutoff=args.min_score).postprocess_nodes(nodes)

    print(f"\nRetrieved {len(nodes)} chunks for: {args.question}\n")
    for i, node in enumerate(nodes, 1):
        page = node.metadata.get("page_label", "?")
        preview = " ".join(node.get_content().split())[:180]
        print(f"  {i}. page {page}  score {node.score:.3f}  {preview} ...")

    if args.retrieve_only:
        return
    if args.print_prompt:
        # The free route: the retrieval ran on your laptop, so paste this into any chat you already use.
        context = "\n\n".join(
            f"[page {n.metadata.get('page_label', '?')}]\n{n.get_content().strip()}" for n in nodes
        )
        print(ANSWER_PROMPT.format(context_str=context, query_str=args.question))
        return
    if not nodes:
        print("\nNothing cleared the score cutoff, so there is nothing to answer from.")
        return

    # Step 2. Claude writes the answer from those chunks only.
    Settings.llm = pick_llm(args.api, args.model)
    engine = index.as_query_engine(
        similarity_top_k=args.top_k,
        text_qa_template=ANSWER_PROMPT,
        response_mode="compact",
    )
    print("\nAsking Claude ...\n")
    response = engine.query(args.question)
    print(str(response))

    pages = sorted({n.metadata.get("page_label", "?") for n in response.source_nodes})
    print(f"\nSources: pages {', '.join(pages)}")


if __name__ == "__main__":
    main()
