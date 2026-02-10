# 9DA Advanced Demos

Three interactive demonstrations of the Nine-Dimensional Awareness (9DA) governed autonomy architecture.

## Overview

These demos showcase different aspects of the 9DA framework:

1. **Multi-Agent Emergence** - Real-time visualization of agent spawning, interaction, and dissolution
2. **Counterfactual Explorer** - Interactive decision tree analysis with alternative paths
3. **Phase Space Dynamics** - Awareness continuum trajectory visualization

Each demo consists of:
- **HTML frontend** - Interactive, browser-based visualization
- **Python backend** - Computational engine with full governance layer

## Architecture Highlights

### Awareness Components
- **AwarenessField** - Multi-dimensional state representation
- **AwarenessRecursion** - Self-reflective dynamics
- **AwarenessDynamics** - State evolution and regulation

### Governance Layer
- **Invariants** - Hard constraints (max uncertainty: 0.85, min coherence: 0.15)
- **Ethics** - Validation of action safety
- **Explainability** - Decision trace generation

### Emergence Layer
- **AgentGeneration** - Governed spawning of emergent agents
- **Dissolution** - Controlled agent lifecycle termination
- **EmergentAgent** - Autonomous units with awareness state

### Audit Layer
- **SelfEvaluation** - Alignment and integrity assessment
- **Counterfactual** - Alternative path exploration
- **Continuity** - Trajectory coherence analysis

---

## Demo 1: Multi-Agent Emergence

**Files:**
- `demo_emergence.html` - Interactive visualization
- `emergence_backend.py` - Full simulation engine

### Features

**Frontend:**
- Live agent spawning and dissolution
- Connection visualization between nearby agents
- Real-time event logging
- Governance violation tracking
- Population dynamics monitoring

**Backend:**
- Complete governance enforcement
- Agent lifecycle management
- Event logging and analysis
- Invariant violation detection
- Full state tracking

### Running

**Browser (instant):**
```bash
# Open in browser
open demo_emergence.html
```

**Python (computational):**
```bash
# Run 1000 step simulation
python emergence_backend.py

# Custom step count
python emergence_backend.py 2000

# Generates: emergence_log.json
```

### What to Watch

1. **Spawning** - Green agents materialize with initial coherence/uncertainty
2. **Maturation** - Agents grow to full size and become active (blue)
3. **Connections** - Lines show emergent relationships between agents
4. **Violations** - Orange coloring indicates governance threshold breaches
5. **Dissolution** - Red fade-out when agents reach end of lifecycle

### Invariants Enforced

- Maximum agents: 20
- Maximum uncertainty: 0.85
- Minimum coherence: 0.15
- Maximum recursion depth: 5

---

## Demo 2: Counterfactual Decision Explorer

**Files:**
- `demo_counterfactual.html` - Interactive decision tree
- `counterfactual_backend.py` - Analysis engine

### Features

**Frontend:**
- Three pre-configured scenarios
- Visual decision tree with branching paths
- Color-coded outcomes (green=safe, amber=drift, red=threshold breach)
- Real-time metrics for each path
- Comparative analysis cards

**Backend:**
- Exhaustive counterfactual generation
- Path ranking and scoring
- Violation prediction
- Recommendation engine
- Natural language analysis

### Running

**Browser:**
```bash
open demo_counterfactual.html
```

**Python:**
```bash
python counterfactual_backend.py

# Generates: counterfactual_analysis.json
```

### Scenarios

1. **High Uncertainty Context**
   - Coherence: 0.48, Uncertainty: 0.72
   - Multiple intervention paths needed

2. **Stable Coherent State**
   - Coherence: 0.85, Uncertainty: 0.25
   - Monitor-only recommendation

3. **Critical Threshold**
   - Coherence: 0.18, Uncertainty: 0.84
   - Immediate intervention required

### Decision Paths Explored

- **Increase Coherence** - Active intervention (+0.25 coherence)
- **Reduce Uncertainty** - Information gathering (-0.25 uncertainty)
- **Natural Drift (Positive)** - Autonomous improvement
- **Natural Drift (Negative)** - Degradation scenario
- **Coherence Threshold Breach** - Governance constraint violation
- **Maintain Current** - No-action baseline

---

## Demo 3: Phase Space Dynamics

**Files:**
- `demo_phase_space.html` - Interactive phase portrait
- `phase_space_backend.py` - Trajectory computation

### Features

**Frontend:**
- 2D phase space (coherence × uncertainty)
- Live trajectory tracking
- Invariant boundary visualization
- Adjustable initial conditions
- Safe zone highlighting
- Real-time drift event detection

**Backend:**
- Vector field computation
- Attractor identification
- Trajectory statistics
- Trend analysis
- Multi-scenario comparison

### Running

**Browser:**
```bash
open demo_phase_space.html
```

**Python:**
```bash
python phase_space_backend.py

# Generates: phase_space_analysis.json
```

### Controls

**Awareness Evolution:**
- Start/Pause - Control trajectory evolution
- Reinitialize Conditions - Clear trajectory and restart
- Sliders - Set initial coherence/uncertainty

**Metrics Tracked:**
- Points tracked in trajectory
- Drift events (significant coherence jumps)
- Invariant violations
- Current risk and stability

### Phase Space Regions

- **Green zone** - Safe operation (C>0.15, U<0.85)
- **Red zones** - Invariant violations
- **Yellow marker** - Current state
- **Blue trail** - Historical trajectory

---

## Technical Details

### Dependencies

**Python:**
```bash
pip install numpy  # For phase_space_backend.py only
# All other backends: stdlib only
```

**Browser:**
- Modern browser with Canvas API
- JavaScript enabled
- No external dependencies

### Data Flow

```
User Input → HTML Interface → Canvas Rendering
     ↓
Initial State → Python Backend → Simulation
     ↓
Governance Checks → Dynamics → Event Log
     ↓
Output JSON ← Analysis ← Results
```

### Governance Pipeline

```
Input State
    ↓
Awareness Generation (field.py)
    ↓
Recursion (recursion.py)
    ↓
Dynamics (dynamics.py)
    ↓
Invariant Check (invariants.py) ──→ Violation → Log
    ↓ Pass
Ethics Validation (ethics.py) ──→ Violation → Log
    ↓ Pass
Agent Spawn/Action (generation.py, agent.py)
    ↓
Explainability (explainability.py)
    ↓
Self-Evaluation (self_evaluation.py)
    ↓
Counterfactual (counterfactual.py)
    ↓
Feedback (feedback.py)
    ↓
Memory Update (memory.py)
    ↓
Lineage Track (lineage.py)
```

---

## Key Concepts

### Coherence
Measure of internal consistency and alignment. Higher coherence = more stable, predictable behavior.

### Uncertainty  
Measure of unpredictability and information gaps. Higher uncertainty = less confidence in state.

### Risk
Computed as `uncertainty × (1 - coherence)`. Represents potential for undesired outcomes.

### Stability
Computed as `coherence × (1 - uncertainty)`. Represents resilience to perturbations.

### Drift
Magnitude of change in coherence between states. Large drift events indicate phase transitions.

### Invariants
Hard constraints that must never be violated:
- Uncertainty must remain ≤ 0.85
- Coherence must remain ≥ 0.15
- Agent population ≤ 20
- Recursion depth ≤ 5

## Design Philosophy

### Visual Aesthetics
Each demo has a distinct visual identity:

1. **Emergence** - Tech noir (JetBrains Mono, electric blues)
2. **Counterfactual** - Analytical elegance (Space Mono, gradient headers)
3. **Phase Space** - Scientific minimalism (Inconsolata, dark void)

### Interaction Patterns
- Immediate feedback
- Progressive disclosure
- Explorable explanations
- No hidden complexity

### Code Quality
- Type hints throughout
- Comprehensive docstrings
- Separation of concerns
- Minimal dependencies
- Production-ready structure


## Future Extensions

### Potential Additions

1. **Temporal Continuity Demo**
   - Multi-cycle memory evolution
   - Long-term coherence tracking
   - Feedback loop visualization

2. **Ethics Validation Explorer**
   - Constraint boundary testing
   - Risk/stability thresholds
   - Recovery strategies

3. **Multi-Agent Collaboration**
   - Inter-agent communication
   - Emergent coordination
   - Collective decision-making

4. **LLM Integration**
   - Real language model backing
   - Actual reasoning traces
   - Context-aware responses

---

## Legal


9DA™ is a registered trademark. The entirety of the 9DA™ Framework, including naming, structure, conceptual architecture, applied domains, and visual identity, is proprietary intellectual property of Zdenka Cucin, Originator and Lead Developer.

This repository is provided for evaluation and testing purposes only.

For licensing inquiries: [https://github.com/9DAtm](https://github.com/9DAtm)


Enjoy exploring governed autonomy! 


© 2025 Zdenka Cucin. All Rights Reserved.

