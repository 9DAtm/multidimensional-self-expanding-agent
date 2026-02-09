class EmergentAgent:
    def __init__(self, awareness, llm=None):
        self.awareness = awareness
        self.llm = llm
        self.alive = True

    async def act(self, context):
        if self.llm and self.llm.enabled:
            prompt = (
                f"You are an emergent cognitive agent.\n"
                f"Awareness field: {self.awareness.field}\n"
                f"Coherence: {self.awareness.coherence}\n"
                f"Uncertainty: {self.awareness.uncertainty}\n"
                f"Context: {context}\n"
                f"Analyze the situation and provide structured findings."
            )
            llm_response = await self.llm.complete(prompt)
            return {
                "awareness_field": self.awareness.field,
                "context_keys": list(context.keys()),
                "llm_response": llm_response,
            }

        return {
            "awareness_field": self.awareness.field,
            "context_keys": list(context.keys()),
        }

    def dissolve(self):
        self.alive = False
        residue = {
            "final_coherence": self.awareness.coherence,
            "final_uncertainty": self.awareness.uncertainty,
            "final_field": dict(self.awareness.field),
        }
        self.awareness = None
        return residue