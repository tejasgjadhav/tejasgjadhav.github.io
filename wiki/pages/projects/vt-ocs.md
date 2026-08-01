---
title: VT-OCS — volatility-targeted ORB-CPPI system
type: project
tags: [trading, orb, cppi, turtle, nse, paper-trading]
created: 2026-08-01
updated: 2026-08-01
sources: [~/files/vt-ocs/README.md, ~/files/vt-ocs/docs/agent-workflow.md]
---

Three-layer NSE equity system at `~/files/vt-ocs`, pushed to
`github.com/tejasgjadhav/vt-ocs`: **ORB signals → Turtle sizing → CPPI overlay**. Written
as the first response to an SCMHRD brief (Vipul Khandekar, 2026-07-05), separate from
[[institutional-trader]], which trades index and stock options rather than cash equity.

State as of 2026-07: paper engine built and live-capable (`88adb01`), launchd-deployed via
`deploy/com.sayali.vtocs.engine.plist`, with an as-built Mermaid agent workflow in
`docs/agent-workflow.md`. **The README still says "DESIGN PHASE, no code" — that line is
stale; trust the commits.**

Design points that survived from the brief:
- The Nifty 500 is not really 500 tradable names. Hard pre-filter at ADV ≥ ₹25 crore and no
  price band tighter than 20% leaves a working universe of roughly 150–250.
- **The 5% monthly target is an aspirational design goal, not a probability.** The CPPI
  floor structurally limits but cannot eliminate losses beyond 5% in gap-downs, lower
  circuits, or broker outages. This is the same honesty discipline recorded in
  [[capital-curve-verdict]] for the options book.
