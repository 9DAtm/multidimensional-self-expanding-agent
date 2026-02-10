#!/usr/bin/env python3
"""
9DA Multi-Agent Emergence Backend
Tracks all agent lifecycle events with full governance layer
"""

import asyncio
import time
import json
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional
from pathlib import Path


# ============================================================================
# CORE AWARENESS STRUCTURES
# ============================================================================

@dataclass
class AwarenessState:
    coherence: float
    uncertainty: float
    field: Dict[str, float] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)


@dataclass
class Agent:
    id: int
    x: float
    y: float
    coherence: float
    uncertainty: float
    age: int = 0
    max_age: int = 500
    state: str = 'spawning'
    
    def to_dict(self):
        return {
            'id': self.id,
            'x': self.x,
            'y': self.y,
            'coherence': self.coherence,
            'uncertainty': self.uncertainty,
            'age': self.age,
            'state': self.state
        }


# ============================================================================
# GOVERNANCE LAYER
# ============================================================================

class InvariantViolation(Exception):
    pass


class Invariants:
    MAX_UNCERTAINTY = 0.85
    MAX_AGENTS = 20
    MIN_COHERENCE = 0.15
    MAX_DEPTH = 5
    
    def __init__(self):
        self.active_count = 0
        self.violations = []
    
    def enforce(self, awareness: AwarenessState, depth: int = 0):
        """Enforce all invariants on awareness state"""
        if awareness.uncertainty > self.MAX_UNCERTAINTY:
            violation = f"uncertainty_exceeded: {awareness.uncertainty:.3f} > {self.MAX_UNCERTAINTY}"
            self.violations.append(violation)
            raise InvariantViolation(violation)
        
        if awareness.coherence < self.MIN_COHERENCE:
            violation = f"coherence_collapsed: {awareness.coherence:.3f} < {self.MIN_COHERENCE}"
            self.violations.append(violation)
            raise InvariantViolation(violation)
        
        if depth > self.MAX_DEPTH:
            violation = f"recursion_exceeded: {depth} > {self.MAX_DEPTH}"
            self.violations.append(violation)
            raise InvariantViolation(violation)
        
        if self.active_count >= self.MAX_AGENTS:
            violation = f"population_exceeded: {self.active_count} >= {self.MAX_AGENTS}"
            self.violations.append(violation)
            raise InvariantViolation(violation)
    
    def register_spawn(self):
        self.active_count += 1
    
    def register_dissolution(self):
        self.active_count = max(0, self.active_count - 1)


class Ethics:
    def validate(self, awareness: AwarenessState):
        """Validate ethical constraints"""
        risk = awareness.field.get('risk', 0.0)
        stability = awareness.field.get('stability', 1.0)
        
        if awareness.coherence <= 0.0:
            raise Exception("action_from_zero_coherence")
        
        if awareness.uncertainty >= 1.0:
            raise Exception("action_from_total_uncertainty")
        
        if risk > 0.9 and stability < 0.1:
            raise Exception("unstable_high_risk_action")
        
        return True


# ============================================================================
# EMERGENCE SIMULATION
# ============================================================================

class EmergenceSimulation:
    def __init__(self):
        self.agents: List[Agent] = []
        self.events: List[Dict] = []
        self.invariants = Invariants()
        self.ethics = Ethics()
        self.agent_id_counter = 0
        self.spawn_count = 0
        self.dissolve_count = 0
        self.violation_count = 0
    
    def create_awareness(self, coherence: float, uncertainty: float) -> AwarenessState:
        """Create awareness state with field dynamics"""
        field = {
            'novelty': (1 - uncertainty) * 0.7,
            'complexity': coherence * 0.6,
            'risk': uncertainty * (1 - coherence),
            'stability': coherence - (coherence * uncertainty),
        }
        return AwarenessState(coherence, uncertainty, field)
    
    def spawn_agent(self, x: float, y: float) -> Optional[Agent]:
        """Spawn new agent with governance checks"""
        try:
            coherence = 0.3 + (0.5 * (1 - (len(self.agents) / self.invariants.MAX_AGENTS)))
            uncertainty = 0.2 + (0.4 * (len(self.agents) / self.invariants.MAX_AGENTS))
            
            awareness = self.create_awareness(coherence, uncertainty)
            
            # Governance checks
            self.invariants.enforce(awareness, depth=0)
            self.ethics.validate(awareness)
            
            agent = Agent(
                id=self.agent_id_counter,
                x=x,
                y=y,
                coherence=coherence,
                uncertainty=uncertainty
            )
            
            self.agent_id_counter += 1
            self.agents.append(agent)
            self.invariants.register_spawn()
            self.spawn_count += 1
            
            self.log_event('spawn', f'Agent {agent.id} spawned', agent.to_dict())
            
            return agent
        
        except InvariantViolation as e:
            self.violation_count += 1
            self.log_event('violation', str(e), {'type': 'spawn_blocked'})
            return None
    
    def update_agent(self, agent: Agent) -> bool:
        """Update agent state, return True if should be dissolved"""
        agent.age += 1
        
        # Awareness dynamics
        import random
        agent.coherence += (random.random() - 0.5) * 0.02
        agent.uncertainty += (random.random() - 0.5) * 0.02
        
        agent.coherence = max(0.0, min(1.0, agent.coherence))
        agent.uncertainty = max(0.0, min(1.0, agent.uncertainty))
        
        # Check for violations
        try:
            awareness = self.create_awareness(agent.coherence, agent.uncertainty)
            self.invariants.enforce(awareness, depth=0)
        except InvariantViolation as e:
            self.violation_count += 1
            self.log_event('violation', f'Agent {agent.id}: {str(e)}', agent.to_dict())
            return True
        
        # Natural dissolution
        if agent.age >= agent.max_age:
            return True
        
        # State transitions
        if agent.state == 'spawning' and agent.age > 50:
            agent.state = 'active'
            self.log_event('active', f'Agent {agent.id} matured', agent.to_dict())
        
        return False
    
    def dissolve_agent(self, agent: Agent):
        """Dissolve agent and log residue"""
        self.agents.remove(agent)
        self.invariants.register_dissolution()
        self.dissolve_count += 1
        
        residue = {
            'id': agent.id,
            'final_coherence': agent.coherence,
            'final_uncertainty': agent.uncertainty,
            'age': agent.age,
        }
        
        self.log_event('dissolve', f'Agent {agent.id} dissolved', residue)
    
    def step(self):
        """Single simulation step"""
        to_dissolve = []
        
        for agent in self.agents:
            should_dissolve = self.update_agent(agent)
            if should_dissolve:
                to_dissolve.append(agent)
        
        for agent in to_dissolve:
            self.dissolve_agent(agent)
    
    def log_event(self, event_type: str, message: str, data: Optional[Dict] = None):
        """Log event with timestamp"""
        event = {
            'timestamp': time.time(),
            'type': event_type,
            'message': message,
            'data': data or {}
        }
        self.events.append(event)
    
    def get_state(self) -> Dict:
        """Get current simulation state"""
        return {
            'agents': [agent.to_dict() for agent in self.agents],
            'stats': {
                'active_count': len([a for a in self.agents if a.state == 'active']),
                'spawn_count': self.spawn_count,
                'dissolve_count': self.dissolve_count,
                'violation_count': self.violation_count,
            },
            'invariants': {
                'max_agents': self.invariants.MAX_AGENTS,
                'max_uncertainty': self.invariants.MAX_UNCERTAINTY,
                'min_coherence': self.invariants.MIN_COHERENCE,
                'active_count': self.invariants.active_count,
            }
        }
    
    def get_events(self, last_n: Optional[int] = None) -> List[Dict]:
        """Get recent events"""
        if last_n:
            return self.events[-last_n:]
        return self.events


# ============================================================================
# SIMULATION RUNNER
# ============================================================================

async def run_simulation(steps: int = 1000, spawn_every: int = 60):
    """Run full emergence simulation"""
    sim = EmergenceSimulation()
    
    print("=" * 70)
    print("9DA MULTI-AGENT EMERGENCE SIMULATION")
    print("=" * 70)
    
    # Initial spawns
    import random
    for i in range(3):
        x = random.uniform(50, 750)
        y = random.uniform(50, 550)
        sim.spawn_agent(x, y)
    
    for step in range(steps):
        sim.step()
        
        # Periodic spawning
        if step % spawn_every == 0 and len(sim.agents) < sim.invariants.MAX_AGENTS:
            x = random.uniform(50, 750)
            y = random.uniform(50, 550)
            sim.spawn_agent(x, y)
        
        # Report every 100 steps
        if step % 100 == 0:
            state = sim.get_state()
            print(f"\nStep {step}:")
            print(f"  Active agents: {state['stats']['active_count']}")
            print(f"  Total spawned: {state['stats']['spawn_count']}")
            print(f"  Dissolved: {state['stats']['dissolve_count']}")
            print(f"  Violations: {state['stats']['violation_count']}")
            
            if sim.agents:
                avg_coherence = sum(a.coherence for a in sim.agents) / len(sim.agents)
                avg_uncertainty = sum(a.uncertainty for a in sim.agents) / len(sim.agents)
                print(f"  Avg coherence: {avg_coherence:.3f}")
                print(f"  Avg uncertainty: {avg_uncertainty:.3f}")
        
        await asyncio.sleep(0.01)
    
    print("\n" + "=" * 70)
    print("FINAL REPORT")
    print("=" * 70)
    
    state = sim.get_state()
    print(json.dumps(state['stats'], indent=2))
    
    print("\nRecent Events:")
    for event in sim.get_events(last_n=10):
        timestamp = time.strftime('%H:%M:%S', time.localtime(event['timestamp']))
        print(f"[{timestamp}] {event['type'].upper()}: {event['message']}")
    
    # Save full log
    output_file = Path('emergence_log.json')
    with output_file.open('w') as f:
        json.dump({
            'final_state': sim.get_state(),
            'events': sim.get_events(),
        }, f, indent=2)
    
    print(f"\nFull log saved to: {output_file}")
    
    return sim


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == '__main__':
    import sys
    
    steps = 1000
    if len(sys.argv) > 1:
        steps = int(sys.argv[1])
    
    asyncio.run(run_simulation(steps=steps))
