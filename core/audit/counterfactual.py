class Counterfactual:
    def explore(self, awareness):
        base_coherence = awareness.coherence
        base_uncertainty = awareness.uncertainty
        base_risk = awareness.field.get("risk", 0.0)

        scenarios = {
            "higher_coherence": {
                "coherence": min(1.0, base_coherence + 0.2),
                "uncertainty": base_uncertainty,
                "risk_delta": -0.2 * base_risk,
            },
            "lower_uncertainty": {
                "coherence": base_coherence,
                "uncertainty": max(0.0, base_uncertainty - 0.2),
                "risk_delta": -0.15 * base_risk,
            },
            "coherence_collapse": {
                "coherence": max(0.0, base_coherence - 0.4),
                "uncertainty": min(1.0, base_uncertainty + 0.3),
                "risk_delta": 0.5,
            },
        }

        for name, scenario in scenarios.items():
            scenario["would_violate_invariant"] = (
                scenario["uncertainty"] > 0.85 or scenario["coherence"] < 0.15
            )

        return scenarios