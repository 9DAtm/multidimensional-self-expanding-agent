#!/usr/bin/env python3
"""
9DA Phase Space Analysis Backend
Computes awareness trajectories and phase space dynamics
"""

import numpy as np
import json
from typing import List, Tuple, Dict
from dataclasses import dataclass
from pathlib import Path


# ============================================================================
# PHASE SPACE STRUCTURES
# ============================================================================

@dataclass
class PhasePoint:
    coherence: float
    uncertainty: float
    
    def __post_init__(self):
        self.risk = self.uncertainty * (1 - self.coherence)
        self.stability = self.coherence * (1 - self.uncertainty)
        self.novelty = (1 - self.uncertainty) * 0.7
        self.complexity = self.coherence * 0.6
    
    def to_dict(self):
        return {
            'coherence': self.coherence,
            'uncertainty': self.uncertainty,
            'risk': self.risk,
            'stability': self.stability,
            'novelty': self.novelty,
            'complexity': self.complexity,
        }


# ============================================================================
# DYNAMICS ENGINE
# ============================================================================

class AwarenessDynamics:
    """Computes awareness field evolution through phase space"""
    
    MAX_UNCERTAINTY = 0.85
    MIN_COHERENCE = 0.15
    
    def __init__(self, drift_rate: float = 0.02, noise_level: float = 0.01):
        self.drift_rate = drift_rate
        self.noise_level = noise_level
        self.violations = []
        self.drift_events = []
    
    def evolve(self, point: PhasePoint) -> PhasePoint:
        """Compute next state using awareness dynamics"""
        # Drift component (systematic change)
        coherence_drift = np.random.randn() * self.drift_rate
        
        # Noise component (random fluctuation)
        coherence_noise = np.random.randn() * self.noise_level
        uncertainty_noise = np.random.randn() * self.noise_level
        
        # Coupling: high uncertainty inhibits coherence increase
        coupling_effect = -point.uncertainty * 0.01
        
        # New state
        new_coherence = point.coherence + coherence_drift + coherence_noise + coupling_effect
        new_uncertainty = point.uncertainty + uncertainty_noise
        
        # Bounds
        new_coherence = np.clip(new_coherence, 0.0, 1.0)
        new_uncertainty = np.clip(new_uncertainty, 0.0, 1.0)
        
        # Track significant drift
        if abs(coherence_drift) > self.drift_rate * 1.5:
            self.drift_events.append({
                'from': point.to_dict(),
                'drift': coherence_drift
            })
        
        new_point = PhasePoint(new_coherence, new_uncertainty)
        
        # Check violations
        if new_uncertainty > self.MAX_UNCERTAINTY or new_coherence < self.MIN_COHERENCE:
            self.violations.append(new_point.to_dict())
        
        return new_point
    
    def compute_trajectory(self, start: PhasePoint, steps: int) -> List[PhasePoint]:
        """Compute full trajectory from initial conditions"""
        trajectory = [start]
        current = start
        
        for _ in range(steps):
            current = self.evolve(current)
            trajectory.append(current)
        
        return trajectory
    
    def analyze_trajectory(self, trajectory: List[PhasePoint]) -> Dict:
        """Analyze trajectory statistics"""
        coherences = [p.coherence for p in trajectory]
        uncertainties = [p.uncertainty for p in trajectory]
        risks = [p.risk for p in trajectory]
        stabilities = [p.stability for p in trajectory]
        
        # Compute trends
        coherence_trend = np.polyfit(range(len(coherences)), coherences, 1)[0]
        uncertainty_trend = np.polyfit(range(len(uncertainties)), uncertainties, 1)[0]
        
        # Find critical points
        max_risk_idx = np.argmax(risks)
        min_stability_idx = np.argmin(stabilities)
        
        return {
            'length': len(trajectory),
            'statistics': {
                'coherence': {
                    'mean': float(np.mean(coherences)),
                    'std': float(np.std(coherences)),
                    'min': float(np.min(coherences)),
                    'max': float(np.max(coherences)),
                    'trend': float(coherence_trend),
                },
                'uncertainty': {
                    'mean': float(np.mean(uncertainties)),
                    'std': float(np.std(uncertainties)),
                    'min': float(np.min(uncertainties)),
                    'max': float(np.max(uncertainties)),
                    'trend': float(uncertainty_trend),
                },
                'risk': {
                    'mean': float(np.mean(risks)),
                    'max': float(np.max(risks)),
                    'max_at_step': int(max_risk_idx),
                },
                'stability': {
                    'mean': float(np.mean(stabilities)),
                    'min': float(np.min(stabilities)),
                    'min_at_step': int(min_stability_idx),
                },
            },
            'drift_events': len(self.drift_events),
            'violations': len(self.violations),
            'final_state': trajectory[-1].to_dict(),
        }


# ============================================================================
# PHASE PORTRAIT GENERATOR
# ============================================================================

class PhasePortrait:
    """Generates full phase space portraits"""
    
    def __init__(self):
        self.dynamics = AwarenessDynamics()
    
    def generate_vector_field(self, resolution: int = 20) -> Dict:
        """Generate vector field showing flow directions"""
        coherence_grid = np.linspace(0, 1, resolution)
        uncertainty_grid = np.linspace(0, 1, resolution)
        
        vectors = []
        
        for c in coherence_grid:
            for u in uncertainty_grid:
                point = PhasePoint(c, u)
                next_point = self.dynamics.evolve(point)
                
                dc = next_point.coherence - point.coherence
                du = next_point.uncertainty - point.uncertainty
                
                vectors.append({
                    'position': {'coherence': c, 'uncertainty': u},
                    'velocity': {'d_coherence': dc, 'd_uncertainty': du},
                    'magnitude': np.sqrt(dc**2 + du**2)
                })
        
        return {
            'resolution': resolution,
            'vectors': vectors
        }
    
    def find_attractors(self, n_samples: int = 50, steps: int = 100) -> List[Dict]:
        """Find stable attractors in phase space"""
        # Sample random initial conditions
        attractors = []
        
        for _ in range(n_samples):
            c0 = np.random.uniform(0.2, 0.9)
            u0 = np.random.uniform(0.1, 0.7)
            
            dynamics = AwarenessDynamics(drift_rate=0.01, noise_level=0.005)
            start = PhasePoint(c0, u0)
            trajectory = dynamics.compute_trajectory(start, steps)
            
            # Check if trajectory converges
            final_points = trajectory[-10:]
            c_variance = np.var([p.coherence for p in final_points])
            u_variance = np.var([p.uncertainty for p in final_points])
            
            if c_variance < 0.001 and u_variance < 0.001:
                final = trajectory[-1]
                attractors.append({
                    'coherence': final.coherence,
                    'uncertainty': final.uncertainty,
                    'basin_start': {'coherence': c0, 'uncertainty': u0},
                })
        
        return attractors


# ============================================================================
# SCENARIO EXPLORER
# ============================================================================

def explore_scenarios():
    """Explore multiple initial conditions"""
    
    scenarios = [
        ("High Uncertainty", 0.48, 0.72),
        ("Stable State", 0.85, 0.25),
        ("Critical Threshold", 0.18, 0.84),
        ("Optimal", 0.90, 0.15),
        ("Balanced", 0.50, 0.50),
    ]
    
    print("=" * 70)
    print("9DA PHASE SPACE ANALYSIS")
    print("=" * 70)
    
    results = []
    
    for name, c0, u0 in scenarios:
        print(f"\n{'─' * 70}")
        print(f"Scenario: {name}")
        print(f"Initial: C={c0:.2f}, U={u0:.2f}")
        print(f"{'─' * 70}")
        
        dynamics = AwarenessDynamics(drift_rate=0.02, noise_level=0.01)
        start = PhasePoint(c0, u0)
        trajectory = dynamics.compute_trajectory(start, steps=200)
        
        analysis = dynamics.analyze_trajectory(trajectory)
        
        print(f"\nTrajectory Analysis:")
        print(f"  Length: {analysis['length']} steps")
        print(f"  Drift events: {analysis['drift_events']}")
        print(f"  Violations: {analysis['violations']}")
        
        print(f"\nCoherence:")
        print(f"  Mean: {analysis['statistics']['coherence']['mean']:.3f}")
        print(f"  Range: [{analysis['statistics']['coherence']['min']:.3f}, "
              f"{analysis['statistics']['coherence']['max']:.3f}]")
        print(f"  Trend: {analysis['statistics']['coherence']['trend']:+.4f}/step")
        
        print(f"\nUncertainty:")
        print(f"  Mean: {analysis['statistics']['uncertainty']['mean']:.3f}")
        print(f"  Range: [{analysis['statistics']['uncertainty']['min']:.3f}, "
              f"{analysis['statistics']['uncertainty']['max']:.3f}]")
        print(f"  Trend: {analysis['statistics']['uncertainty']['trend']:+.4f}/step")
        
        print(f"\nRisk & Stability:")
        print(f"  Mean risk: {analysis['statistics']['risk']['mean']:.3f}")
        print(f"  Max risk: {analysis['statistics']['risk']['max']:.3f} "
              f"(step {analysis['statistics']['risk']['max_at_step']})")
        print(f"  Mean stability: {analysis['statistics']['stability']['mean']:.3f}")
        print(f"  Min stability: {analysis['statistics']['stability']['min']:.3f} "
              f"(step {analysis['statistics']['stability']['min_at_step']})")
        
        final = analysis['final_state']
        print(f"\nFinal State:")
        print(f"  Coherence: {final['coherence']:.3f}")
        print(f"  Uncertainty: {final['uncertainty']:.3f}")
        print(f"  Risk: {final['risk']:.3f}")
        print(f"  Stability: {final['stability']:.3f}")
        
        results.append({
            'name': name,
            'initial': {'coherence': c0, 'uncertainty': u0},
            'trajectory': [p.to_dict() for p in trajectory],
            'analysis': analysis,
        })
    
    # Generate phase portrait
    print(f"\n{'=' * 70}")
    print("GENERATING PHASE PORTRAIT")
    print("=" * 70)
    
    portrait = PhasePortrait()
    vector_field = portrait.generate_vector_field(resolution=15)
    print(f"Vector field computed: {len(vector_field['vectors'])} points")
    
    attractors = portrait.find_attractors(n_samples=30, steps=100)
    print(f"Attractors found: {len(attractors)}")
    
    if attractors:
        print("\nAttractor locations:")
        for i, attr in enumerate(attractors[:5], 1):
            print(f"  {i}. C={attr['coherence']:.3f}, U={attr['uncertainty']:.3f}")
    
    # Save results
    output = {
        'scenarios': results,
        'vector_field': vector_field,
        'attractors': attractors,
    }
    
    output_file = Path('phase_space_analysis.json')
    with output_file.open('w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\n{'=' * 70}")
    print(f"Full analysis saved to: {output_file}")
    print("=" * 70)


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == '__main__':
    explore_scenarios()
