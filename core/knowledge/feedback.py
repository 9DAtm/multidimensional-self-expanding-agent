class Feedback:
    def apply(self, memory, awareness):
        memory["feedback"] = awareness.coherence
        memory["feedback_delta"] = awareness.coherence - memory.get("coherence", awareness.coherence)
        memory["feedback_drift"] = awareness.field.get("drift", 0.0)
        memory["feedback_stability"] = awareness.field.get("stability", 0.0)
        return memory

    def is_positive(self, memory):
        return memory.get("feedback_delta", 0.0) >= 0.0

    def requires_correction(self, memory):
        return (
            memory.get("feedback_delta", 0.0) < -0.2
            or memory.get("feedback_drift", 0.0) > 0.3
        )