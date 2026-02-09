class SelfEvaluation:
    def __init__(self):
        self.evaluations = []

    def evaluate(self, output, awareness):
        risk = awareness.field.get("risk", 0.0)
        stability = awareness.field.get("stability", 0.0)
        drift = awareness.field.get("drift", 0.0)

        alignment = awareness.coherence * (1.0 - risk)
        integrity = max(0.0, stability - drift)

        result = {
            "coherent": awareness.coherence > 0.5,
            "confidence": 1.0 - awareness.uncertainty,
            "alignment": round(alignment, 4),
            "integrity": round(integrity, 4),
            "risk": round(risk, 4),
            "drift": round(drift, 4),
            "action_required": alignment < 0.4 or integrity < 0.2,
        }

        self.evaluations.append(result)
        return result

    def average_alignment(self):
        if not self.evaluations:
            return 0.0
        return sum(e["alignment"] for e in self.evaluations) / len(self.evaluations)

    def summary(self):
        return {
            "total_evaluations": len(self.evaluations),
            "average_alignment": round(self.average_alignment(), 4),
            "action_required_count": sum(1 for e in self.evaluations if e["action_required"]),
        }