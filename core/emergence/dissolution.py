class Dissolution:
    def __init__(self):
        self.dissolved_residues = []

    def dissolve(self, agent):
        residue = agent.dissolve()
        self.dissolved_residues.append(residue)
        return residue

    def total_dissolved(self):
        return len(self.dissolved_residues)

    def last_residue(self):
        if self.dissolved_residues:
            return self.dissolved_residues[-1]
        return None