from core.awareness.state import AwarenessState

class AwarenessField:
    def generate(self, input_state: dict, memory: dict) -> AwarenessState:
        coherence = input_state.get("coherence", 1.0)
        uncertainty = 1.0 - input_state.get("confidence", 1.0)

        field = {
            "novelty": input_state.get("novelty", 0.0) * (1 - uncertainty),
            "complexity": input_state.get("complexity", 0.0) * coherence,
            "risk": uncertainty * (1 - coherence),
            "memory_pressure": memory.get("coherence", 0.0),
        }

        return AwarenessState(field, coherence, uncertainty)