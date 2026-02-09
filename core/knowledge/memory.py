import time

class Memory:
    def __init__(self):
        self.state = {}
        self.snapshots = []

    def update(self, awareness):
        self.state["coherence"] = awareness.coherence
        self.state["uncertainty"] = awareness.uncertainty
        self.state["field"] = dict(awareness.field)
        self.state["last_updated"] = time.time()

        self.snapshots.append({
            "coherence": awareness.coherence,
            "uncertainty": awareness.uncertainty,
            "field": dict(awareness.field),
            "timestamp": time.time(),
        })

    def recall(self, n=1):
        return self.snapshots[-n:] if self.snapshots else []

    def depth(self):
        return len(self.snapshots)