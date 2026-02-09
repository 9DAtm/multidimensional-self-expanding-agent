from core.emergence.agent import EmergentAgent

class AgentGeneration:
    def __init__(self, llm=None):
        self.llm = llm
        self.spawned = []

    def spawn(self, awareness):
        agent = EmergentAgent(awareness, self.llm)
        self.spawned.append(agent)
        return agent

    def spawn_count(self):
        return len(self.spawned)

    def active_agents(self):
        return [a for a in self.spawned if a.alive]