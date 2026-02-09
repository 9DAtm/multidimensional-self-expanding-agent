import asyncio
from core.awareness.field import AwarenessField
from core.awareness.recursion import AwarenessRecursion
from core.awareness.dynamics import AwarenessDynamics
from core.governance.invariants import Invariants
from core.governance.ethics import Ethics
from core.governance.explainability import Explainability
from core.emergence.generation import AgentGeneration
from core.emergence.dissolution import Dissolution
from core.audit.self_evaluation import SelfEvaluation
from core.audit.counterfactual import Counterfactual
from core.audit.continuity import Continuity
from core.knowledge.memory import Memory
from core.knowledge.lineage import Lineage
from core.knowledge.feedback import Feedback

async def run():
    field = AwarenessField()
    recursion = AwarenessRecursion()
    dynamics = AwarenessDynamics()
    invariants = Invariants()
    ethics = Ethics()
    explainability = Explainability()
    generator = AgentGeneration()
    dissolution = Dissolution()
    auditor = SelfEvaluation()
    counterfactual = Counterfactual()
    continuity = Continuity()
    memory = Memory()
    lineage = Lineage()
    feedback = Feedback()

    history = []

    scenarios = [
        {"confidence": 0.45, "novelty": 0.8, "complexity": 0.7, "coherence": 0.6},
        {"confidence": 0.85, "novelty": 0.3, "complexity": 0.4, "coherence": 0.9},
        {"confidence": 0.3, "novelty": 0.9, "complexity": 0.85, "coherence": 0.35},
    ]

    print("=" * 60)
    print("PURE 9DA™ AWARENESS CONTINUUM")
    print("=" * 60)

    for i, input_state in enumerate(scenarios):
        depth = len(history)

        awareness = field.generate(input_state, memory.state)
        awareness = recursion.reflect(awareness, history)
        awareness = dynamics.regulate(awareness, memory.state)

        invariants.enforce(awareness, depth)
        ethics.validate(awareness)

        invariants.register_spawn()
        agent = generator.spawn(awareness)
        output = await agent.act(input_state)

        explanation = explainability.explain_decision(awareness, output)
        audit = auditor.evaluate(output, awareness)
        alternatives = counterfactual.explore(awareness)

        memory.update(awareness)
        lineage.track(memory.state)
        feedback.apply(memory.state, awareness)

        history.append(awareness)

        residue = dissolution.dissolve(agent)
        invariants.register_dissolution()

        cont = continuity.assess(history)

        print(f"\n--- Cycle {i + 1} ---")
        print(f"  Field: {awareness.field}")
        print(f"  Coherence: {awareness.coherence}")
        print(f"  Uncertainty: {awareness.uncertainty}")
        print(f"  Audit: {audit}")
        print(f"  Continuity: {cont}")
        print(f"  Counterfactual scenarios: {list(alternatives.keys())}")
        print(f"  Dissolved residue coherence: {residue['final_coherence']}")
        print(f"  Memory depth: {memory.depth()}")
        print(f"  Lineage length: {lineage.length()}")
        print(f"  Feedback positive: {feedback.is_positive(memory.state)}")

    print(f"\n{'=' * 60}")
    print("CONTINUUM REPORT")
    print(f"{'=' * 60}")
    print(f"  Total cycles: {len(history)}")
    print(f"  Audit summary: {auditor.summary()}")
    print(f"  Continuity: {continuity.assess(history)}")
    print(f"  Coherence lineage: {lineage.coherence_history()}")
    print(f"  Agents spawned: {generator.spawn_count()}")
    print(f"  Agents dissolved: {dissolution.total_dissolved()}")
    print(f"  Invariant status: {invariants.status}")
    print(f"  Explainability trace count: {len(explainability.full_trace())}")

if __name__ == "__main__":
    asyncio.run(run())