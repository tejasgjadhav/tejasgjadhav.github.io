---
title: GlobalAAR TPS Ops — shop-floor operations app
type: project
tags: [manufacturing, tps, fastapi, lan, sqlite]
created: 2026-08-01
updated: 2026-08-01
sources: [~/files/globalaar-ops]
---

Factory operations app at `~/files/globalaar-ops` — the only non-finance project in
[[files-repo]]. FastAPI + Jinja templates + SQLite (`globalaar.db`), server-rendered, no
build step. `python run.py [port]` binds the LAN interface (default **8035**) and prints a
`http://<lan-ip>:<port>` URL so anyone on the factory network can open it.

Modules, one template each: daily entries and entry forms, machines, operators, parts
summary, materials, quality, defects, downtime, CAPA, checklists, actions, masters, import,
dashboard, login. `app/engine.py` and `app/calc.py` hold the computation; `app/importer.py`
loads masters from `seed_masters.json`; `app/charts.py` renders the dashboard views.

Toyota-Production-System framing (defects, downtime, CAPA, standard checklists) rather than
anything financial — worth noting because it is the one project here whose domain does not
connect to [[tejas-jadhav]]'s capital-markets work.
