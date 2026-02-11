# demo_nine_fields.html

Nine-Field Examiner — interactive browser demo of the `NineDAExaminer` neural governance architecture.

---

## What It Is

A real-time visualization of the full 9DA™ neural engine running in the browser. Every panel maps directly to a component in the Python architecture. No simplifications. No metaphors. The actual structure, simulated.

---

## Architecture Map

| Demo Panel | Python Component |
|---|---|
| Nine Field Cards | `NineField` × 9 inside `nn.ModuleDict` |
| Backbone Activation Bar | `SharedBackbone` → `TransformerEncoder` → `LayerNorm` |
| Cross-Attention Arcs | `Governor` → `nn.MultiheadAttention` |
| Governor Node + Weights | `Governor.forward()` → `F.softmax(logits)` |
| Governance Loss | `-(weights * imagination_rewards).mean()` |
| Ensemble Bars (7 members) | `WorldModel` with `cfg.ensemble=7` |
| Imagined Reward Horizon | `WorldModel.imagine()` with `horizon=5` |
| KL Divergence | `-0.5 * sum(1 + logvar - mu² - exp(logvar))` |
| Loss History Chart | `governor_opt.step()` per update cycle |
| Event Log | Training loop events: update / govern / imagine / buffer |

---

## Field Definitions

```
F01  human_cognitive          — Human reasoning and perception
F02  human_behavioral         — Human action and decision patterns  
F03  human_ethical            — Human moral and value systems
F04  ai_alignment             — AI goal alignment with human intent
F05  ai_autonomy              — AI independent decision capacity
F06  ai_safety                — AI harm prevention and constraint
F07  multiplanetary_governance — Governance across distributed systems
F08  resource_ecology         — Resource allocation and sustainability
F09  systemic_regulation      — Cross-system regulatory coherence
```

---

## Controls

### Scenario
Pre-configured input states that stress different parts of the architecture.

| Scenario | Description | Fields Affected |
|---|---|---|
| Balanced Input | Smooth coherence distribution | All fields stable |
| High Complexity | Elevated uncertainty across system | All fields degraded |
| Safety Stress Test | AI fields under pressure | F04 F05 F06 |
| Governance Crisis | System-wide coherence collapse | All fields critical |

### Speed
Controls simulation tick rate from 1 (2000ms/step) to 10 (16ms/step).

### Noise
Injects stochastic perturbation into field dynamics. Mirrors real gradient noise during training. Range 0.00–1.00.

### Buttons
- **Run Examiner** — starts continuous simulation loop
- **Step** — single step when paused
- **Reinitialize Conditions** — full reset to initial state

---

## Panel Reference

### Nine Dimensional Fields

Each card shows:

```
weight      — governor softmax output for this field
coherence   — internal state consistency (green > 0.5, red < 0.2)
uncertainty — inverse of confidence (orange > 0.5, red > 0.75)
q-value     — critic estimate from QNetwork
```

The card with the highest governor weight glows and is marked as dominant field.

Weight bar fills proportionally to softmax output. All 9 bars sum to 1.0.

---

### Backbone State · Attention Flow · Field Activations

Three layers in one canvas:

**Activation heatmap (top bar)**
Represents `SharedBackbone` output projected from `model_dim=768` to 32 display units. Color maps activation magnitude: cool = low, warm = high.

**Governor node (center)**
The `Governor` module. Lines to each field node are weighted by `F.softmax` output — thicker line = higher weight assigned to that field.

**Field nodes (bottom row)**
Node radius scales with governor weight. Inner fill radius scales with coherence. Outer arc shows weight percentage. Cross-attention arcs between fields represent the `MultiheadAttention` cross-field dependencies.

---

### Governor · Field Weights

**Large number** — current `governance_loss` value.

Computed as:
```
governance_loss = -(weights × imagination_rewards).mean()
```

Mirrors the exact loss used in `governor_opt.zero_grad()` → `governance_loss.backward()` → `governor_opt.step()`.

**Loss History chart** — rolling window of last 120 steps. Downward trend = governor learning to assign weight to higher-reward fields.

**Stats:**
```
Updates        — number of gradient steps taken (buffer >= batch_size)
Buffer         — replay buffer transitions stored (max 500K)
Dominant Field — field with highest softmax weight this step
Imagine Rew.   — mean imagined reward across all fields this step
```

---

### Ensemble Disagreement · World Model Uncertainty

Bar chart for all 7 ensemble members in `WorldModel`.

Each bar = disagreement magnitude for one member (`cfg.ensemble=7`).

High disagreement = high epistemic uncertainty = world model is unsure about this transition. Governor should reduce weight on fields with high ensemble disagreement.

Color: green = low disagreement, red = high disagreement.

---

### Imagined Reward · Horizon Rollout

Bar chart for 5 imagination steps (`cfg.imagination_horizon=5`).

Each bar = `WorldModel.imagine()` output at that step using `gamma=0.99` discount.

```
t+1  t+2  t+3  t+4  t+5
```

Green bar = positive imagined reward. Red bar = negative (penalized path). Decay across horizon reflects `gamma` discounting.

---

### KL Divergence · Latent Space Compression

Rolling line chart.

KL divergence from `WorldModel.forward()`:
```python
kl = -0.5 * sum(1 + logvar - mu² - exp(logvar))
```

High KL = latent space is expanding (model learning new structure). Low KL = latent space compressed and stable.

---

### System Event Log

Streams four event types:

```
UPDATE   — governance_loss value after governor step
GOVERN   — dominant field at this step
IMAGINE  — mean horizon reward across all fields
BUFFER   — replay buffer size milestone
```

---

## Relationship to Python Source

```python
# Python: NineDAExaminer.act()
state = self.backbone(x)
field_states = []
for name in self.field_names:
    action, _ = self.fields[name].policy(state)
    field_states.append(state)
weights = self.governor(field_states)
final_action = (weights.unsqueeze(-1) * stacked_actions).sum(1)

# Demo equivalent:
# → backbone activation bar updates
# → each field card updates coherence/uncertainty
# → governor weights update all 9 bars
# → dominant field highlights
```

```python
# Python: NineDAExaminer.update()
for name in self.field_names:
    imagination_reward = field.world.imagine(
        state.detach(), field.policy, self.cfg.imagination_horizon
    )
    imagination_rewards.append(imagination_reward)

governance_loss = -(weights * stacked_rewards.mean(-1)).mean()
self.governor_opt.zero_grad()
governance_loss.backward()
self.governor_opt.step()

# Demo equivalent:
# → imagined reward horizon bars update
# → governance_loss number updates
# → loss history chart extends
```

---

## Config Reference

All simulation parameters match `NineDAConfig`:

```
input_dim           256
model_dim           768
latent_dim          768
action_dim          32
seq_len             128
heads               12
layers              12
ensemble            7
gamma               0.99
tau                 0.005
imagination_horizon 5
buffer_size         500,000
batch_size          256
target_entropy      -32.0
```

---

## Running

Open in any modern browser. No server. No dependencies. No install.

```bash
open demo_nine_fields.html
```

To run the actual Python architecture:

```bash
pip install -e .
python main.py
```

---

## Files

```
demo_nine_fields.html        ← This demo (browser)
main.py                      ← Full Python execution with LLM
core/
├── awareness/               ← AwarenessField, State, Dynamics
├── governance/              ← Invariants, Ethics, Explainability
├── emergence/               ← NineField, Policy, QNetwork, WorldModel
└── audit/                   ← SelfEvaluation, Counterfactual, Continuity
```

---

## Legal

© 2025 Zdenka Cucin. All Rights Reserved.
9DA™ is a registered trademark.
For licensing: [https://github.com/9DAtm](https://github.com/9DAtm)
