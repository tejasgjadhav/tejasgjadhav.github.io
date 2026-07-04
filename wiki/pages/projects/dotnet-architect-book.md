---
title: The Senior .NET Architect's Handbook (book build)
type: project
tags: [book, kdp, dotnet, writing]
created: 2026-07-03
updated: 2026-07-05
sources: [~/files/dotnet-architect-book]
---

Book project: **"The Senior .NET Architect's Handbook"**. Written as 15 markdown parts in
`parts/` (foundations → design patterns → architecture → ASP.NET API → data access → SQL →
microservices → event-driven → Redis → Angular → Azure → Docker/K8s → testing →
DevOps/observability → capstone), compiled by `build.py` into `book.html` and
`dotnet-architect-handbook.pdf` (68 pages).

**Build gotcha:** WeasyPrint fails on this Mac (missing native lib `libgobject-2.0-0`);
`build.py` uses headless-Chrome print-to-PDF instead. Reuse this fallback for any future
PDF-from-HTML task on this machine.

Presumably one of the 5 KDP titles tracked in [[kdp-dashboard]].

Part of [[files-repo]].
