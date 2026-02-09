# Pure 9DA™ Operational Architecture

[![License: Proprietary](https://img.shields.io/badge/License-Proprietary-red.svg)](LICENSE)
[![9DA™](https://img.shields.io/badge/9DA™-Registered%20Trademark-00ffc8.svg)](https://github.com/9DAtm/9DA)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)

> **[▶ Watch Live Demo: 9DA™ vs LangChain vs CrewAI](https://9datm.github.io/multidimensional-self-expanding-agent/9da-live-demo.html)**

This system is a direct operational instantiation of 9DA™.

Awareness is the sole causal substrate.
All emergence, action, memory, and dissolution are consequences of awareness maintaining coherence under invariant constraint.

No component operates independently of awareness.
No action precedes awareness.
No growth bypasses invariants.

## Architecture

```
┌──────────────────────────────────────────────┐
│            AwarenessField.generate()          │
│  input state + memory → AwarenessState        │
└──────────────┬───────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────┐
│         AwarenessRecursion.reflect()          │
│  awareness observes its own history → drift   │
└──────────────┬───────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────┐
│          AwarenessDynamics.regulate()         │
│  memory feedback → stability adjustment       │
└──────────────┬───────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────┐
│           Invariants.enforce()                │
│  uncertainty ceiling · recursion depth limit  │
│  coherence floor · agent population cap       │
└──────────────┬───────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────┐
│              Ethics.validate()                │
│  blocks unstable or unsafe action             │
└──────────────┬───────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────┐
│         AgentGeneration.spawn()               │
│  awareness expression → EmergentAgent         │
└──────────────┬───────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────┐
│  SelfEvaluation · Counterfactual · Continuity │
│  audit from within awareness, not above it    │
└──────────────┬───────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────┐
│     Memory · Lineage · Feedback               │
│  awareness residue persists across cycles     │
└──────────────┬───────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────┐
│          Dissolution.dissolve()               │
│  agent is retired; residue is retained        │
└──────────────────────────────────────────────┘
```

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

© 2025 Zdenka Cucin. All Rights Reserved.

9DA™ is a registered trademark. The entirety of the 9DA™ Framework, including naming, structure, conceptual architecture, applied domains, and visual identity, is proprietary intellectual property of Zdenka Cucin, Originator and Lead Developer.

This repository is provided for evaluation and testing purposes only.
See [LICENSE](LICENSE) for full terms.

For licensing inquiries: [https://github.com/9DAtm](https://github.com/9DAtm)
