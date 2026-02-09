class Lineage:
    def __init__(self):
        self.chain = []

    def track(self, memory):
        entry = {
            "keys": list(memory.keys()),
            "coherence": memory.get("coherence", None),
            "uncertainty": memory.get("uncertainty", None),
            "step": len(self.chain),
        }
        self.chain.append(entry)
        return entry

    def full_lineage(self):
        return list(self.chain)

    def coherence_history(self):
        return [e["coherence"] for e in self.chain if e["coherence"] is not None]

    def length(self):
        return len(self.chain)