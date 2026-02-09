class InvariantViolation(Exception):
    pass

class Invariants:
    MAX_UNCERTAINTY = 0.85
    MAX_DEPTH = 5
    MIN_COHERENCE = 0.15
    MAX_AGENTS = 20

    def __init__(self):
        self.active_agents = 0

    def enforce(self, awareness, depth):
        if awareness.uncertainty > self.MAX_UNCERTAINTY:
            raise InvariantViolation("uncertainty_exceeded")
        if depth > self.MAX_DEPTH:
            raise InvariantViolation("recursion_exceeded")
        if awareness.coherence < self.MIN_COHERENCE:
            raise InvariantViolation("coherence_collapsed")
        if self.active_agents >= self.MAX_AGENTS:
            raise InvariantViolation("agent_population_exceeded")

    def register_spawn(self):
        self.active_agents += 1
        if self.active_agents > self.MAX_AGENTS:
            self.active_agents -= 1
            raise InvariantViolation("agent_population_exceeded")

    def register_dissolution(self):
        self.active_agents = max(0, self.active_agents - 1)

    @property
    def status(self):
        return {
            "active_agents": self.active_agents,
            "capacity_remaining": self.MAX_AGENTS - self.active_agents,
        }