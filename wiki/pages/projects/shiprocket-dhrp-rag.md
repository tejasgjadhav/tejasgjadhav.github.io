---
title: Shiprocket DHRP RAG — a teaching build on a real prospectus
type: project
tags: [rag, llamaindex, chromadb, codex, teaching, finance]
created: 2026-08-23
updated: 2026-08-23
sources: [~/files/.claude/worktrees/shiprocket-dhrp-rag-setup-ddaf84/shiprocket-rag]
---

A retrieval-augmented question-answering system over Shiprocket's draft red herring prospectus, built
on 22 August 2026. [[tejas-jadhav]] asked for it step by step because he teaches this build to
students, so the constraint that shaped every choice was that it has to run for free and it has to be
reproducible on a student's own machine. It is the worked example behind the RAG half of Module 2 on
[[aifinance]].

The document is the prospectus Shiprocket filed with SEBI, which runs to 543 pages. LlamaIndex loads
it and splits it, a local embedding model turns each chunk into a vector, and ChromaDB stores the
result as 885 chunks taking 31 megabytes on disk. A question then goes through the same embedding
model, Chroma returns the nearest chunks, and the Codex command-line tool writes an answer from them
and cites the page it came from.

The pipeline was proven rather than assumed. Asking what the main risk factors are returned the risk
factors cross-reference from page 39, the financial risk management note from page 377 and the price
risk section from page 417, and all three are genuine prospectus text.

No API key appears anywhere in it. The embedding model runs locally on the processor after a
one-off download of about 130 megabytes, and the answer step runs on his existing ChatGPT login
through the Codex tool. That matters for teaching, because his students do not have paid
subscriptions.

Three environment notes came out of the build. The machine's system Python is 3.9, which is too old,
so the project creates its environment with `uv`, which needs no administrator rights. A gitignore
keeps the virtual environment, the database and the PDF out of the repository. And the shell working
directory resets between commands here, so every script needs an absolute path or the run starts from
the wrong folder.

The project sits on a worktree branch rather than on the main branch of [[files-repo]], so it will
not be found by looking in the repository root.
