import time

class Explainability:
    def __init__(self):
        self.traces = []

    def explain(self, awareness):
        entry = {
            "field": dict(awareness.field),
            "coherence": awareness.coherence,
            "uncertainty": awareness.uncertainty,
            "timestamp": time.time(),
        }
        self.traces.append(entry)
        return entry

    def explain_decision(self, awareness, action_output):
        entry = {
            "field_at_decision": dict(awareness.field),
            "coherence": awareness.coherence,
            "uncertainty": awareness.uncertainty,
            "action_keys": list(action_output.keys()),
            "dominant_dimension": max(awareness.field, key=awareness.field.get) if awareness.field else None,
            "timestamp": time.time(),
        }
        self.traces.append(entry)
        return entry

    def full_trace(self):
        return list(self.traces)