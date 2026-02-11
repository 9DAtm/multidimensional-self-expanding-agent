"""
9DA™ Nine-Field Examiner — Demo Backend
Mirrors demo_nine_fields.html in pure Python.

Runs the NineDAExaminer simulation loop and prints
structured output matching every panel in the browser demo.

Usage:
    python demo_nine_fields.py
    python demo_nine_fields.py --scenario safety_stress
    python demo_nine_fields.py --scenario governance_crisis --steps 100
    python demo_nine_fields.py --steps 50 --noise 0.4 --speed fast
"""

import math
import time
import json
import argparse
import random
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Tuple
from pathlib import Path


# ═══════════════════════════════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════════════════════════════

@dataclass
class NineDADemoConfig:
    input_dim: int = 256
    model_dim: int = 768
    latent_dim: int = 768
    action_dim: int = 32
    seq_len: int = 128
    heads: int = 12
    layers: int = 12
    ensemble: int = 7
    gamma: float = 0.99
    tau: float = 0.005
    buffer_size: int = 500_000
    batch_size: int = 256
    target_entropy: float = -32.0
    imagination_horizon: int = 5
    intrinsic_coef: float = 0.1
    diversity_coef: float = 0.05


# ═══════════════════════════════════════════════════════════════
# FIELD DEFINITIONS
# ═══════════════════════════════════════════════════════════════

FIELD_NAMES = [
    "human_cognitive",
    "human_behavioral",
    "human_ethical",
    "ai_alignment",
    "ai_autonomy",
    "ai_safety",
    "multiplanetary_governance",
    "resource_ecology",
    "systemic_regulation",
]

FIELD_COLORS_ANSI = {
    "human_cognitive":           "\033[96m",
    "human_behavioral":          "\033[92m",
    "human_ethical":             "\033[32m",
    "ai_alignment":              "\033[93m",
    "ai_autonomy":               "\033[33m",
    "ai_safety":                 "\033[91m",
    "multiplanetary_governance": "\033[94m",
    "resource_ecology":          "\033[95m",
    "systemic_regulation":       "\033[35m",
}

RESET = "\033[0m"
BOLD  = "\033[1m"
DIM   = "\033[2m"


# ═══════════════════════════════════════════════════════════════
# STATE STRUCTURES
# ═══════════════════════════════════════════════════════════════

@dataclass
class FieldState:
    name: str
    coherence: float = 0.0
    uncertainty: float = 0.0
    imagine_reward: float = 0.0
    q_value: float = 0.0
    alpha: float = 0.1
    weight: float = 0.0


@dataclass
class WorldModelState:
    ensemble_disagreement: List[float] = field(default_factory=list)
    imagined_rewards: List[float] = field(default_factory=list)
    kl: float = 0.0


@dataclass
class GovernorState:
    governance_loss: float = 0.0
    dominant_field: str = ""
    dominant_weight: float = 0.0
    total_imagine_reward: float = 0.0


@dataclass
class SystemState:
    step: int = 0
    buffer_size: int = 0
    updates: int = 0
    backbone_activations: List[float] = field(default_factory=list)
    fields: List[FieldState] = field(default_factory=list)
    world: WorldModelState = field(default_factory=WorldModelState)
    governor: GovernorState = field(default_factory=GovernorState)
    events: List[Dict] = field(default_factory=list)
    loss_history: List[float] = field(default_factory=list)
    kl_history: List[float] = field(default_factory=list)


# ═══════════════════════════════════════════════════════════════
# SCENARIO PRESETS
# ═══════════════════════════════════════════════════════════════

SCENARIOS = {
    "balanced": {
        "description": "Smooth coherence distribution across all fields",
        "target_coherence": 0.70,
        "target_uncertainty": 0.25,
        "stressed_fields": [],
    },
    "high_complexity": {
        "description": "Elevated uncertainty across entire system",
        "target_coherence": 0.45,
        "target_uncertainty": 0.55,
        "stressed_fields": list(range(9)),
    },
    "safety_stress": {
        "description": "AI fields under governance pressure",
        "target_coherence": 0.65,
        "target_uncertainty": 0.28,
        "stressed_fields": [3, 4, 5],
    },
    "governance_crisis": {
        "description": "System-wide coherence collapse",
        "target_coherence": 0.20,
        "target_uncertainty": 0.80,
        "stressed_fields": list(range(9)),
    },
}


# ═══════════════════════════════════════════════════════════════
# MATH HELPERS (no torch dependency)
# ═══════════════════════════════════════════════════════════════

def softmax(logits: List[float]) -> List[float]:
    max_l = max(logits)
    exp = [math.exp(l - max_l) for l in logits]
    s = sum(exp)
    return [e / s for e in exp]


def clamp(v: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, v))


def noise(scale: float) -> float:
    return (random.random() - 0.5) * 2 * scale


# ═══════════════════════════════════════════════════════════════
# SIMULATION ENGINE
# ═══════════════════════════════════════════════════════════════

class NineFieldSimulation:
    """
    Pure-Python simulation of NineDAExaminer update loop.

    Mirrors:
        NineDAExaminer.act()
        NineDAExaminer.update()
        WorldModel.forward()
        WorldModel.imagine()
        Governor.forward()
        ReplayBuffer.push() / .sample()
    """

    def __init__(
        self,
        cfg: NineDADemoConfig,
        scenario: str = "balanced",
        noise_level: float = 0.20,
        seed: int = 42,
    ):
        random.seed(seed)
        self.cfg = cfg
        self.noise_level = noise_level
        self.scenario = scenario
        self.s = SystemState()
        self._init_state()

    def _init_state(self):
        """Initialize system state from scenario preset."""
        preset = SCENARIOS[self.scenario]

        self.s.fields = []
        for i, name in enumerate(FIELD_NAMES):
            stressed = i in preset["stressed_fields"]
            self.s.fields.append(FieldState(
                name=name,
                coherence=clamp(
                    preset["target_coherence"] + noise(0.15), 0.05, 0.98
                ) if not stressed else clamp(
                    0.20 + noise(0.08), 0.05, 0.40
                ),
                uncertainty=clamp(
                    preset["target_uncertainty"] + noise(0.1), 0.02, 0.98
                ) if not stressed else clamp(
                    0.70 + noise(0.1), 0.50, 0.95
                ),
                imagine_reward=clamp(0.3 + noise(0.2), 0.0, 1.0),
                q_value=clamp(0.4 + noise(0.3), 0.0, 1.0),
                alpha=clamp(0.15 + noise(0.05), 0.01, 0.5),
                weight=1.0 / 9,
            ))

        self.s.world = WorldModelState(
            ensemble_disagreement=[clamp(random.random() * 0.3, 0, 1)
                                   for _ in range(self.cfg.ensemble)],
            imagined_rewards=[clamp(0.2 + noise(0.1), -0.5, 1.0)
                              for _ in range(self.cfg.imagination_horizon)],
            kl=0.1,
        )

        self.s.backbone_activations = [random.random() for _ in range(32)]
        self.s.governor = GovernorState(dominant_field=FIELD_NAMES[0])

    # ─── STEP ────────────────────────────────────────────────

    def step(self) -> SystemState:
        """Single simulation step — mirrors one update() call."""
        self.s.step += 1
        self.s.buffer_size = min(
            self.s.buffer_size + self.cfg.batch_size,
            self.cfg.buffer_size
        )

        preset = SCENARIOS[self.scenario]
        nl = self.noise_level

        # ── Backbone (SharedBackbone.forward)
        self.s.backbone_activations = [
            clamp(v + noise(nl * 0.15), 0, 1)
            for v in self.s.backbone_activations
        ]

        # ── Field updates (NineField: policy + world model)
        for i, f in enumerate(self.s.fields):
            stressed = i in preset["stressed_fields"]
            target_c = 0.25 if stressed else preset["target_coherence"]
            target_u = 0.75 if stressed else preset["target_uncertainty"]

            pull_c = (target_c - f.coherence) * 0.04
            pull_u = (target_u - f.uncertainty) * 0.03

            f.coherence    = clamp(f.coherence    + noise(nl*0.03) + pull_c, 0.05, 0.98)
            f.uncertainty  = clamp(f.uncertainty  + noise(nl*0.02) + pull_u, 0.02, 0.98)
            f.imagine_reward = clamp(f.imagine_reward + noise(nl*0.04), -0.5, 1.0)
            f.q_value      = clamp(f.q_value      + noise(nl*0.03), 0.0, 1.0)
            f.alpha        = clamp(f.alpha         + noise(0.003),  0.01, 0.5)

        # ── Governor (Governor.forward → softmax)
        logits = [
            f.coherence * 2.5 + (1 - f.uncertainty) * 1.5 + f.imagine_reward
            for f in self.s.fields
        ]
        weights = softmax(logits)
        for f, w in zip(self.s.fields, weights):
            f.weight = w

        dom_idx = weights.index(max(weights))

        # ── Governance loss: -(weights · imagine_rewards).mean()
        gov_loss = -sum(
            w * f.imagine_reward
            for w, f in zip(weights, self.s.fields)
        )
        total_ir = sum(f.imagine_reward for f in self.s.fields) / 9

        self.s.governor = GovernorState(
            governance_loss=abs(gov_loss),
            dominant_field=FIELD_NAMES[dom_idx],
            dominant_weight=weights[dom_idx],
            total_imagine_reward=total_ir,
        )

        # ── World model ensemble (WorldModel.forward)
        self.s.world.ensemble_disagreement = [
            clamp(v * 0.9 + self.s.fields[i % 9].uncertainty * 0.1 * 0.5
                  + noise(nl * 0.04), 0, 1)
            for i, v in enumerate(self.s.world.ensemble_disagreement)
        ]

        # ── Imagination horizon (WorldModel.imagine)
        self.s.world.imagined_rewards = [
            clamp(
                total_ir * (self.cfg.gamma ** t) + noise(nl * 0.03),
                -0.5, 1.0
            )
            for t in range(self.cfg.imagination_horizon)
        ]

        # ── KL divergence
        avg_kl = sum(
            f.uncertainty * (1 - f.coherence) * 0.5
            for f in self.s.fields
        ) / 9
        self.s.world.kl = clamp(avg_kl + noise(nl * 0.01), 0, 1)

        # ── History
        self.s.loss_history.append(self.s.governor.governance_loss)
        self.s.kl_history.append(self.s.world.kl)
        if len(self.s.loss_history) > 120:
            self.s.loss_history.pop(0)
        if len(self.s.kl_history) > 80:
            self.s.kl_history.pop(0)

        # ── Updates counter
        if self.s.buffer_size >= self.cfg.batch_size:
            self.s.updates += 1

        # ── Events
        self._emit_events()

        return self.s

    def _emit_events(self):
        ts = time.strftime("%H:%M:%S")
        step = self.s.step

        if step % 8 == 0:
            self.s.events.append({
                "time": ts,
                "type": "UPDATE",
                "msg": f"governance_loss={self.s.governor.governance_loss:.6f}"
            })
        if step % 15 == 0:
            self.s.events.append({
                "time": ts,
                "type": "GOVERN",
                "msg": f"dominant_field={self.s.governor.dominant_field}"
                       f"  weight={self.s.governor.dominant_weight:.4f}"
            })
        if step % 20 == 0:
            self.s.events.append({
                "time": ts,
                "type": "IMAGINE",
                "msg": f"horizon_reward={self.s.governor.total_imagine_reward:.6f}"
                       f"  kl={self.s.world.kl:.4f}"
            })
        if step % 50 == 0:
            self.s.events.append({
                "time": ts,
                "type": "BUFFER",
                "msg": f"transitions={self.s.buffer_size:,}"
                       f"  updates={self.s.updates:,}"
            })

        # Keep last 100 events
        if len(self.s.events) > 100:
            self.s.events = self.s.events[-100:]


# ═══════════════════════════════════════════════════════════════
# TERMINAL RENDERER
# ═══════════════════════════════════════════════════════════════

class TerminalRenderer:
    """Renders SystemState to terminal — mirrors demo_nine_fields.html panels."""

    def __init__(self, cfg: NineDADemoConfig):
        self.cfg = cfg

    def render(self, s: SystemState):
        self._clear()
        self._header(s)
        self._fields(s)
        self._governor(s)
        self._world_model(s)
        self._backbone(s)
        self._events(s)

    def _clear(self):
        print("\033[H\033[2J", end="")

    def _header(self, s: SystemState):
        print(f"\n  {BOLD}9DA™ Nine-Field Examiner{RESET}  ·  Neural Governance Architecture")
        print(f"  {DIM}step={s.step}  buffer={s.buffer_size:,}  updates={s.updates:,}{RESET}\n")

    def _fields(self, s: SystemState):
        print(f"  {DIM}── NINE DIMENSIONAL FIELDS {'─'*54}{RESET}")
        print()

        header = f"  {'FIELD':<30} {'WEIGHT':>8} {'COHERENCE':>10} {'UNCERTAINTY':>12} {'Q-VALUE':>8} {'ALPHA':>7}"
        print(f"  {DIM}{header}{RESET}")
        print(f"  {DIM}{'─'*80}{RESET}")

        for f in s.fields:
            col = FIELD_COLORS_ANSI.get(f.name, "")
            dom = " ◀" if f.name == s.governor.dominant_field else "  "

            coh_col = (
                "\033[91m" if f.coherence < 0.2
                else "\033[93m" if f.coherence < 0.4
                else "\033[92m"
            )
            unc_col = (
                "\033[91m" if f.uncertainty > 0.75
                else "\033[93m" if f.uncertainty > 0.5
                else "\033[37m"
            )

            bar_w = int(f.weight * 30)
            bar = "█" * bar_w + "░" * (30 - bar_w)

            print(
                f"  {col}{f.name:<30}{RESET}"
                f"  {col}{f.weight:>7.4f}{RESET}{dom}"
                f"  {coh_col}{f.coherence:>9.4f}{RESET}"
                f"  {unc_col}{f.uncertainty:>11.4f}{RESET}"
                f"  {f.q_value:>8.4f}"
                f"  {f.alpha:>7.4f}"
            )

        print()
        # Weight distribution bar
        print(f"  {DIM}Weight Distribution{RESET}")
        total_w = 0
        print("  ", end="")
        for f in s.fields:
            col = FIELD_COLORS_ANSI.get(f.name, "")
            segs = max(1, int(f.weight * 60))
            print(f"{col}{'█'*segs}{RESET}", end="")
            total_w += segs
        print()
        print()

    def _governor(self, s: SystemState):
        g = s.governor
        print(f"  {DIM}── GOVERNOR {'─'*66}{RESET}")
        print()
        print(f"  governance_loss   {BOLD}{g.governance_loss:>12.6f}{RESET}")
        print(f"  dominant_field    {FIELD_COLORS_ANSI.get(g.dominant_field,'')}"
              f"{g.dominant_field:<30}{RESET}  weight={g.dominant_weight:.4f}")
        print(f"  total_img_reward  {g.total_imagine_reward:>12.6f}")

        if len(s.loss_history) > 1:
            _min = min(s.loss_history)
            _max = max(s.loss_history) or 0.001
            chart = ""
            bars = "▁▂▃▄▅▆▇█"
            step = max(1, len(s.loss_history) // 60)
            for v in s.loss_history[::step][-60:]:
                idx = int((v - _min) / (_max - _min) * 7)
                chart += bars[idx]
            print(f"  loss_history      {DIM}{chart}{RESET}")

        print()

    def _world_model(self, s: SystemState):
        w = s.world
        print(f"  {DIM}── WORLD MODEL  ensemble={self.cfg.ensemble}  horizon={self.cfg.imagination_horizon} {'─'*40}{RESET}")
        print()

        # Ensemble disagreement
        print(f"  {DIM}Ensemble Disagreement (7 members){RESET}")
        print("  ", end="")
        for i, v in enumerate(w.ensemble_disagreement):
            col = "\033[92m" if v < 0.3 else "\033[93m" if v < 0.6 else "\033[91m"
            bar_h = int(v * 8)
            bar = "█" * bar_h + "░" * (8 - bar_h)
            print(f" M{i+1}{col}{bar}{RESET}", end="")
        print()

        # Imagined reward horizon
        print(f"\n  {DIM}Imagined Reward Horizon (γ={self.cfg.gamma}){RESET}")
        print("  ", end="")
        for t, v in enumerate(w.imagined_rewards):
            col = "\033[92m" if v >= 0 else "\033[91m"
            bar = "█" * max(1, int(abs(v) * 8))
            print(f" t+{t+1}{col}{bar[:8]}{RESET}", end="")
        print()

        # KL divergence
        if len(s.kl_history) > 1:
            bars = "▁▂▃▄▅▆▇█"
            _min = min(s.kl_history)
            _max = max(s.kl_history) or 0.001
            chart = ""
            for v in s.kl_history[-60:]:
                idx = int((v - _min) / (_max - _min) * 7)
                chart += bars[idx]
            print(f"\n  {DIM}KL Divergence {RESET}{DIM}{chart}{RESET}  {w.kl:.4f}")

        print()

    def _backbone(self, s: SystemState):
        print(f"  {DIM}── SHARED BACKBONE  model_dim={self.cfg.model_dim}  heads={self.cfg.heads}  layers={self.cfg.layers} {'─'*20}{RESET}")
        print()
        print(f"  {DIM}Activations (projected 768→32){RESET}")
        print("  ", end="")
        for v in s.backbone_activations:
            hue_idx = int(v * 5)
            colors = ["\033[34m", "\033[36m", "\033[32m", "\033[33m", "\033[31m", "\033[35m"]
            col = colors[min(hue_idx, 5)]
            bars = "▁▂▃▄▅▆▇█"
            idx = int(v * 7)
            print(f"{col}{bars[idx]}{RESET}", end="")
        print()
        print()

    def _events(self, s: SystemState):
        print(f"  {DIM}── EVENT LOG {'─'*65}{RESET}")
        print()
        recent = s.events[-8:]
        type_colors = {
            "UPDATE": "\033[96m",
            "GOVERN": "\033[93m",
            "IMAGINE": "\033[94m",
            "BUFFER": "\033[37m",
        }
        for ev in reversed(recent):
            col = type_colors.get(ev["type"], "\033[37m")
            print(f"  {DIM}{ev['time']}{RESET}  {col}{ev['type']:<8}{RESET}  {DIM}{ev['msg']}{RESET}")
        print()


# ═══════════════════════════════════════════════════════════════
# SUMMARY REPORT
# ═══════════════════════════════════════════════════════════════

def print_summary(s: SystemState, scenario: str):
    print("\n" + "═"*78)
    print(f"  {BOLD}NINE-FIELD EXAMINER — FINAL REPORT{RESET}")
    print("═"*78)
    print()
    print(f"  Scenario         {scenario}")
    print(f"  Steps            {s.step}")
    print(f"  Buffer           {s.buffer_size:,}")
    print(f"  Updates          {s.updates:,}")
    print(f"  Final Gov. Loss  {s.governor.governance_loss:.6f}")
    print(f"  Dominant Field   {s.governor.dominant_field}")
    print()

    print(f"  {DIM}Field Weights at Termination{RESET}")
    print()
    for f in sorted(s.fields, key=lambda x: x.weight, reverse=True):
        col = FIELD_COLORS_ANSI.get(f.name, "")
        bar = "█" * int(f.weight * 50)
        print(f"  {col}{f.name:<30}{RESET}  {f.weight:.4f}  {DIM}{bar}{RESET}")

    print()
    print(f"  {DIM}Coherence Summary{RESET}")
    print()
    coherences = [(f.name, f.coherence) for f in s.fields]
    coherences.sort(key=lambda x: x[1], reverse=True)
    for name, c in coherences:
        col = "\033[92m" if c > 0.6 else "\033[93m" if c > 0.35 else "\033[91m"
        bar = "█" * int(c * 30)
        print(f"  {name:<30}  {col}{c:.4f}  {bar}{RESET}")

    print()
    if len(s.loss_history) >= 2:
        trend = s.loss_history[-1] - s.loss_history[0]
        direction = "↓ decreasing" if trend < 0 else "↑ increasing"
        print(f"  Loss Trend  {direction}  ({trend:+.4f})")

    print()
    print(f"  Events logged: {len(s.events)}")
    print()


# ═══════════════════════════════════════════════════════════════
# JSON EXPORT
# ═══════════════════════════════════════════════════════════════

def export_report(s: SystemState, scenario: str, path: str = "nine_fields_report.json"):
    report = {
        "scenario": scenario,
        "steps": s.step,
        "buffer_size": s.buffer_size,
        "updates": s.updates,
        "governor": {
            "final_loss": s.governor.governance_loss,
            "dominant_field": s.governor.dominant_field,
            "dominant_weight": s.governor.dominant_weight,
            "total_imagine_reward": s.governor.total_imagine_reward,
        },
        "fields": [
            {
                "name": f.name,
                "weight": f.weight,
                "coherence": f.coherence,
                "uncertainty": f.uncertainty,
                "q_value": f.q_value,
                "alpha": f.alpha,
                "imagine_reward": f.imagine_reward,
            }
            for f in s.fields
        ],
        "world_model": {
            "ensemble_disagreement": s.world.ensemble_disagreement,
            "imagined_rewards": s.world.imagined_rewards,
            "final_kl": s.world.kl,
        },
        "loss_history": s.loss_history,
        "kl_history": s.kl_history,
        "events": s.events[-50:],
    }
    with open(path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"  Report exported → {path}")


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="9DA™ Nine-Field Examiner Demo"
    )
    parser.add_argument(
        "--scenario",
        choices=list(SCENARIOS.keys()),
        default="balanced",
        help="Input scenario preset"
    )
    parser.add_argument(
        "--steps",
        type=int,
        default=200,
        help="Number of simulation steps"
    )
    parser.add_argument(
        "--noise",
        type=float,
        default=0.20,
        help="Noise level 0.0–1.0"
    )
    parser.add_argument(
        "--speed",
        choices=["slow", "normal", "fast", "instant"],
        default="normal",
        help="Render speed"
    )
    parser.add_argument(
        "--export",
        action="store_true",
        help="Export final report to JSON"
    )
    parser.add_argument(
        "--no-render",
        action="store_true",
        dest="no_render",
        help="Suppress terminal rendering (fastest)"
    )
    args = parser.parse_args()

    delays = {"slow": 0.3, "normal": 0.08, "fast": 0.02, "instant": 0.0}
    delay = delays[args.speed]

    cfg = NineDADemoConfig()
    sim = NineFieldSimulation(
        cfg=cfg,
        scenario=args.scenario,
        noise_level=args.noise,
    )
    renderer = TerminalRenderer(cfg)

    scenario_info = SCENARIOS[args.scenario]
    print(f"\n  {BOLD}9DA™ Nine-Field Examiner{RESET}")
    print(f"  Scenario: {BOLD}{args.scenario}{RESET}  —  {scenario_info['description']}")
    print(f"  Steps: {args.steps}  |  Noise: {args.noise}  |  Speed: {args.speed}")
    print()

    if not args.no_render:
        input("  Press Enter to start...")

    for step in range(args.steps):
        state = sim.step()

        if not args.no_render:
            renderer.render(state)
            if delay > 0:
                time.sleep(delay)

        elif step % 25 == 0:
            # Minimal progress when no render
            print(
                f"  step={step:>4}  "
                f"loss={state.governor.governance_loss:.5f}  "
                f"dominant={state.governor.dominant_field:<30}  "
                f"buffer={state.buffer_size:,}"
            )

    print_summary(sim.s, args.scenario)

    if args.export:
        export_report(sim.s, args.scenario)


if __name__ == "__main__":
    main()
