# 9DA™  Governed Autonomous Agent Architecture
## Evaluation Infrastructure for Governed Autonomy

The field-wide AI evaluation gap requires benchmarks measuring:
- Long-horizon coherence retention
- World modeling under uncertainty
- Know-when-to-stop behaviour
- Explainable, auditable decisions

9DA™ is not just an agent framework. It is the architectural substrate
for benchmarking these properties — the things current benchmarks
(Terminal-Bench, ARC-AGI, METR) do not yet measure.

| What Benchmarks Need | What 9DA Provides |
|---|---|
| Long-horizon coherence measurement | `continuity.py` + Governor tracking |
| World model uncertainty quantification | `WorldModel` ensemble (7 members) |
| Know-when-to-stop enforcement | `invariants.py` hard stops |
| Explainable decision rubrics | `explainability.py` + `counterfactual.py` |
| Multi-factor output audit | `self_evaluation.py` |

Governance protocol: [9DA-Core](https://github.com/9DAtm/9DA-Core)

**A Research-Grade Framework for Auditable, Self-Bounded AI Systems**

“If you’re using this architecture in research or tooling, attribution is appreciated.” Zdenka

> **[▶ Watch Live Demo: 9DA™ NINE FIELDS](https://9datm.github.io/multidimensional-self-expanding-agent/demo_nine_fields.html)**
>
> **[▶ Watch Live Demo: 9DA™ COUNTERFACTUAL](https://9datm.github.io/multidimensional-self-expanding-agent/demo_counterfactual.html)**
> 
> **[▶ Watch Live Demo: 9DA™ EMERGENCE](https://9datm.github.io/multidimensional-self-expanding-agent/demo_emergence.html)**
> 
> **[▶ Watch Live Demo: 9DA™ PHASE SPACE ](https://9datm.github.io/multidimensional-self-expanding-agent/demo_phase_space.html)**


Docs/Each demo consists of:
- **HTML frontend** - Interactive, browser-based visualization
- **Python backend** - Computational engine with full governance layer

**9DA™** is a governed autonomous agent architecture designed around a single premise:

> **Autonomy is only meaningful when governance, awareness, and termination are internal system properties.**

Unlike conventional agent frameworks that optimize for orchestration and task throughput, 9DA™ treats **governance, continuity, and safe dissolution** as first-class architectural constraints.

The result is an agent system that is:
- aware of its own operational state,
- auditable by design,
- bounded by enforceable invariants,
- and capable of safe, explicit lifecycle closure.

This repository provides a **reproducible, inspectable reference implementation** demonstrating how governed and ungoverned agent execution diverge under identical conditions.


## What Makes 9DA™ Different

Most agent systems rely on:
- external supervision,
- tool-driven orchestration,
- implicit state,
- and unbounded execution loops.

9DA™ explores a different architectural category.

### Core Distinctions

- **Awareness is explicit and structured**, not emergent or implicit
- **Constraints are enforced**, not advisory
- **Lifecycle control is mandatory**, including termination
- **Evaluation is deterministic and replayable**
- **Lineage, memory residue, and continuity are observable**

This is not an optimization layer on top of existing frameworks.
It is a **foundational rethinking of autonomous agent design**.


## Architecture Summary

### Awareness-Centric Core
- Cycle-based awareness traces
- Explicit coherence and uncertainty signals
- Reflection and recursion loops
- Drift and continuity tracking

### Governance by Design
- Hard invariants and thresholds
- Internal validation and coherence checks
- Explainability and inspection hooks
- No silent failure or hidden escalation

### Lifecycle Control
- Agent emergence from awareness state
- Self-evaluation and counterfactual assessment
- Explicit, safe dissolution
- No orphaned or runaway agents

### Auditability and Replay
- Deterministic execution
- Structured logs
- Lineage and signal tracking
- Reproducible evaluation pipeline


## Repository Contents

This repository includes:

- A modular Python architecture implementing governed agent execution
- A deterministic demo pipeline separating awareness generation and evaluation
- A visual replay tool for inspecting awareness signals and outcomes
- Clear separation between governed and orchestration-driven models

Everything included is designed to be **inspectable, explainable, and reproducible**.


## Demo: Governed vs Orchestrated Execution

The included demo compares two execution paradigms under identical conditions:

### Governed Model
- Awareness-driven execution
- Enforced coherence constraints
- Bounded lifecycle
- Explicit evaluation and traceability

### Ungoverned Model
- Delegation-driven orchestration
- No global invariants
- Implicit state
- Unbounded progression

This comparison is **illustrative, not competitive**.
It does not benchmark third-party frameworks or claim empirical superiority.

Its purpose is to make **architectural differences observable**.


## Running the Demo

### 1. Execute the Orchestrator

```bash
python demo_orchestrator.py > demo_output.json

2. Inspect the Replay

Open demo_viewer.html in a browser and load demo_output.json.

You will be able to:
   •   inspect extracted awareness signals,
   •   observe coherence and confidence trends,
   •   replay System-1 evaluation output deterministically.

Intended Audience

9DA™ is designed for:
   •   AI safety and governance researchers
   •   Advanced agent system designers
   •   Enterprise R&D teams exploring governed autonomy
   •   Grant reviewers and technical evaluators
   •   Organizations requiring auditable AI behavior

It is not a consumer assistant or turnkey product.

Status and Scope

This project is:
   •   a research-grade reference architecture
   •   suitable for technical review and extension
   •   intentionally conservative in claims

It is not:
   •   a production-ready assistant
   •   a performance benchmark
   •   a wrapper around external agent toolchains
   •   a finished commercial product

Why This Matters

As autonomous systems become more capable, the limiting factor is no longer intelligence, but governance.

9DA™ demonstrates how:
   •   autonomy can be bounded without external micromanagement,
   •   safety can be structural rather than procedural,
   •   and awareness can be made inspectable rather than assumed.

This repository exists to make those principles concrete.

## Testing Tiers

### Tier 1 — Free (no account, no API key)

```bash
pip install -e .
python main.py
```

Runs the full awareness continuum using the built-in deterministic engine.
No external dependencies. No network access. Full architecture demonstration.

### Tier 2 — Free (local LLM, no API key)

Install [Ollama](https://ollama.com), then:

```bash
ollama pull llama3
cp .env.example .env
```

Edit `.env`:

```env
LLM_PROVIDER=ollama
LLM_MODEL=llama3
```

Run:

```bash
python main.py
```

Agents now think using a real LLM running on your machine. Cost: $0.

### Tier 3 — Paid (bring your own API key)

Create an account at [Anthropic](https://console.anthropic.com) or [OpenAI](https://platform.openai.com).

Edit `.env`:

```env
LLM_PROVIDER=anthropic
LLM_API_KEY=sk-ant-...
LLM_MODEL=claude-sonnet-4-20250514
```

Or:

```env
LLM_PROVIDER=openai
LLM_API_KEY=sk-...
LLM_MODEL=gpt-4o
```

Cost per awareness cycle:

| Provider  | Model         | Cost per cycle |
| --------- | ------------- | -------------- |
| Ollama    | llama3        | $0.00          |
| Anthropic | claude-sonnet | $0.01–$0.03    |
| Anthropic | claude-opus   | $0.09–$0.24    |
| OpenAI    | gpt-4o-mini   | $0.001–$0.003  |
| OpenAI    | gpt-4o        | $0.015–$0.06   |

You pay the LLM provider directly.

## Requirements

* Python 3.11+
* (Optional) Ollama for local LLM
* (Optional) Anthropic or OpenAI API key for cloud LLM

## Install

```bash
pip install -e .
```

## Run

```bash
python main.py
```

## Examples

```bash
python -m examples.awareness_continuum_example
```

## Legal

9DA™ is a registered trademark of Zdenka Cucin.

**Governance protocol** (`9DA-Core`): open source under Apache-2.0
→ https://github.com/9DAtm/9DA-Core

**Framework implementation** (this repository): proprietary intellectual property of Zdenka Cucin.
Provided for evaluation, research, and testing purposes only.
Commercial licensing available → https://github.com/9DAtm

© 2025 Zdenka Cucin. All Rights Reserved.
```
