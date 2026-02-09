class AwarenessRecursion:
    def reflect(self, state, history):
        if history:
            state.field["drift"] = abs(
                state.coherence - history[-1].coherence
            )
        else:
            state.field["drift"] = 0.0
        return state