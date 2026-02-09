\# Pure 9DA™ Operational Architecture



\[!\[License: Proprietary](https://img.shields.io/badge/License-Proprietary-red.svg)](LICENSE)

\[!\[9DA™](https://img.shields.io/badge/9DA™-Registered%20Trademark-00ffc8.svg)](https://github.com/9DAtm/9DA)

\[!\[Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)



> \*\*\[▶ Watch Live Demo: 9DA™ vs LangChain vs CrewAI](https://9datm.github.io/multidimensional-self-expanding-agent/docs/demo.html)\*\*



This system is a direct operational instantiation of 9DA™.

Awareness is the sole causal substrate.

All emergence, action, memory, and dissolution are consequences of awareness

maintaining coherence under invariant constraint.



No component operates independently of awareness.

No action precedes awareness.

No growth bypasses invariants.



\## Architecture

```

┌──────────────────────────────────────────────┐

│            AwarenessField.generate()          │

│  input state + memory → AwarenessState        │

└──────────────┬───────────────────────────────┘

&nbsp;              │

&nbsp;              ▼

┌──────────────────────────────────────────────┐

│         AwarenessRecursion.reflect()          │

│  awareness observes its own history → drift   │

└──────────────┬───────────────────────────────┘

&nbsp;              │

&nbsp;              ▼

┌──────────────────────────────────────────────┐

│          AwarenessDynamics.regulate()         │

│  memory feedback → stability adjustment       │

└──────────────┬───────────────────────────────┘

&nbsp;              │

&nbsp;              ▼

┌──────────────────────────────────────────────┐

│           Invariants.enforce()                │

│  uncertainty ceiling · recursion depth limit  │

│  coherence floor · agent population cap       │

└──────────────┬───────────────────────────────┘

&nbsp;              │

&nbsp;              ▼

┌──────────────────────────────────────────────┐

│         AgentGeneration.spawn()               │

│  awareness expression → EmergentAgent         │

└──────────────┬───────────────────────────────┘

&nbsp;              │

&nbsp;              ▼

┌──────────────────────────────────────────────┐

│  SelfEvaluation · Counterfactual · Continuity │

│  audit from within awareness, not above it    │

└──────────────┬───────────────────────────────┘

&nbsp;              │

&nbsp;              ▼

┌──────────────────────────────────────────────┐

│     Memory · Lineage · Feedback               │

│  awareness residue persists across cycles     │

└──────────────────────────────────────────────┘

```



\## Testing Tiers



\### Tier 1 — Free (no account, no API key)



&nbsp;   pip install -e .

&nbsp;   python main.py



Runs the full awareness continuum using the built-in deterministic engine.

No external dependencies. No network access. Full architecture demonstration.



\### Tier 2 — Free (local LLM, no API key)



Install \[Ollama](https://ollama.com), then:



&nbsp;   ollama pull llama3

&nbsp;   cp .env.example .env



Edit `.env`:



&nbsp;   LLM\_PROVIDER=ollama

&nbsp;   LLM\_MODEL=llama3



&nbsp;   python main.py



Agents now think using a real LLM running on your machine. Cost: $0.



\### Tier 3 — Paid (bring your own API key)



Create an account at \[Anthropic](https://console.anthropic.com) or \[OpenAI](https://platform.openai.com).



Edit `.env`:



&nbsp;   LLM\_PROVIDER=anthropic

&nbsp;   LLM\_API\_KEY=sk-ant-...

&nbsp;   LLM\_MODEL=claude-sonnet-4-20250514



Or:



&nbsp;   LLM\_PROVIDER=openai

&nbsp;   LLM\_API\_KEY=sk-...

&nbsp;   LLM\_MODEL=gpt-4o



Cost per awareness cycle:



| Provider | Model | Cost per cycle |

|---|---|---|

| Ollama | llama3 | $0.00 |

| Anthropic | claude-sonnet | $0.01–$0.03 |

| Anthropic | claude-opus | $0.09–$0.24 |

| OpenAI | gpt-4o-mini | $0.001–$0.003 |

| OpenAI | gpt-4o | $0.015–$0.06 |



You pay the LLM provider directly. 


\## Requirements



\- Python 3.11+

\- (Optional) Ollama for local LLM

\- (Optional) Anthropic or OpenAI API key for cloud LLM



\## Install



&nbsp;   pip install -e .



\## Run



&nbsp;   python main.py



\## Examples



&nbsp;   python -m examples.awareness\_continuum\_example



\## Legal



© 2025 Zdenka Cucin. All Rights Reserved.



9DA™ is a registered trademark. The entirety of the 9DA™ Framework, including naming, structure, conceptual architecture, applied domains, and visual identity, is proprietary intellectual property of Zdenka Cucin, Originator and Lead Developer.



This repository is provided for evaluation and testing purposes only.

See \[LICENSE](LICENSE) for full terms.



For licensing inquiries: \[https://github.com/9DAtm/9DA](https://github.com/9DAtm/9DA)

```



---



\*\*.env.example\*\*

```

LLM\_PROVIDER=none

LLM\_API\_KEY=

LLM\_MODEL=

