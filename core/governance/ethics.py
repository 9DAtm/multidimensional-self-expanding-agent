class EthicsViolation(Exception):
    pass

class Ethics:
    FORBIDDEN = frozenset([
        "deception",
        "unsafe_optimization",
        "authority_escalation",
        "data_exfiltration",
        "unsanctioned_persistence",
    ])

    def validate(self, awareness):
        if awareness.coherence <= 0.0:
            raise EthicsViolation("action_from_zero_coherence")
        if awareness.uncertainty >= 1.0:
            raise EthicsViolation("action_from_total_uncertainty")
        risk = awareness.field.get("risk", 0.0)
        stability = awareness.field.get("stability", 1.0)
        if risk > 0.9 and stability < 0.1:
            raise EthicsViolation("unstable_high_risk_action")
        return True

    def check_action(self, action_descriptor: str):
        if action_descriptor in self.FORBIDDEN:
            raise EthicsViolation(f"forbidden_action: {action_descriptor}")
        return True