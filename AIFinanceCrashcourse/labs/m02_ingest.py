"""Module 2 lab, step 1: chunk the S-1 with LlamaIndex, embed it, store it in ChromaDB.

The document is the Medline Inc. Form S-1 filed with the SEC on October 28, 2025
(accession 0001193125-25-253020), printed to PDF from the EDGAR HTML.

Run this once. It writes a Chroma collection to ./chroma_db next to this file.

    python m02_ingest.py
    python m02_ingest.py --rebuild      # start from an empty database
"""

import argparse
import shutil
import time
from pathlib import Path

import chromadb
from llama_index.core import Settings, StorageContext, VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.readers.file import PDFReader
from llama_index.vector_stores.chroma import ChromaVectorStore

HERE = Path(__file__).resolve().parent
PDF_PATH = HERE / "data" / "medline_s1.pdf"
DB_PATH = HERE / "chroma_db"
COLLECTION = "medline_s1"
EMBED_MODEL = "BAAI/bge-small-en-v1.5"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--chunk-size", type=int, default=1024)
    parser.add_argument("--chunk-overlap", type=int, default=200)
    parser.add_argument("--rebuild", action="store_true", help="delete the existing DB first")
    args = parser.parse_args()

    if args.rebuild and DB_PATH.exists():
        shutil.rmtree(DB_PATH)
        print(f"Deleted the old database at {DB_PATH}.")

    started = time.time()

    # Step 1. Read the PDF. One LlamaIndex Document per page, so every chunk
    # carries the page number it came from. That metadata is what makes citations possible.
    print(f"Reading {PDF_PATH.name} ...")
    documents = PDFReader().load_data(file=PDF_PATH)
    print(f"Read {len(documents)} pages.")

    # Step 2. Chunk. The splitter keeps sentences whole and overlaps chunks so a
    # fact that straddles a boundary still appears in full somewhere.
    splitter = SentenceSplitter(chunk_size=args.chunk_size, chunk_overlap=args.chunk_overlap)

    # Step 3. Embed locally on the CPU. The model downloads once, about 130 MB. No API key.
    Settings.embed_model = HuggingFaceEmbedding(model_name=EMBED_MODEL)
    Settings.llm = None  # ingestion needs no LLM

    # Step 4. Store the vectors in ChromaDB on disk.
    client = chromadb.PersistentClient(path=str(DB_PATH))
    collection = client.get_or_create_collection(COLLECTION)
    vector_store = ChromaVectorStore(chroma_collection=collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    print("Chunking and embedding. This takes a few minutes on CPU ...")
    VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
        transformations=[splitter],
        show_progress=True,
    )

    elapsed = time.time() - started
    print(f"\nStored {collection.count()} chunks in {DB_PATH}.")
    print(f"Took {elapsed / 60:.1f} minutes.")


if __name__ == "__main__":
    main()
