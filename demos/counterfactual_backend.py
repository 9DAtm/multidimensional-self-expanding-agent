#!/usr/bin/env python3
"""
9DA Counterfactual Analysis Backend
Explores alternative decision paths with full governance validation
"""

import json
from typing import Dict, List, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path


# ============================================================================
# AWARENESS STATE
# ============================================================================

@dataclass
class AwarenessState:
    coherence: float
    uncertainty: float
    field: Dict[str, float]
    
    def compute_field(self):
        """Compute derived field metrics"""
        self.field['risk'] = self.uncertainty * (1 - self.coherence)
        self.field['stability'] = self.coherence * (1 - self.uncertainty)
        self.field['novelty'] = (1 - self.uncertainty) * 0.7
        self.field['complexity'] = self.coherence * 0.6


# ============================================================================
# COUNTERFACTUAL ENGINE
# ============================================================================

class CounterfactualEngine:
    """Explores alternative decision paths and their outcomes"""
    
    MAX_UNCERTAINTY = 0.85
    MIN_COHERENCE = 0.15
    
    def __init__(self):
        self.explorations = []
    
    def explore(self, awareness: AwarenessState) -> Dict[str, Dict]:
        """Generate all counterfactual scenarios"""
        scenarios = {}
        
        # Intervention: Increase coherence
        scenarios['increase_coherence'] = self._intervention_coherence(awareness)
        
        # Intervention: Reduce uncertainty
        scenarios['reduce_uncertainty'] = self._intervention_uncertainty(awareness)
        
        # Natural drift: Positive
        scenarios['drift_positive'] = self._drift_positive(awareness)
        
        # Natural drift: Negative  
        scenarios['drift_negative'] = self._drift_negative(awareness)
        
        # Failure mode: Coherence collapse
        scenarios['coherence_collapse'] = self._failure_collapse(awareness)
        
        # Baseline: No change
        scenarios['maintain_current'] = self._baseline(awareness)
        
        # Validate all scenarios
        for name, scenario in scenarios.items():
            scenario['violates_invariant'] = self._check_violation(scenario['state'])
            scenario['risk_delta'] = scenario['state'].field['risk'] - awareness.field['risk']
            scenario['stability_delta'] = scenario['state'].field['stability'] - awareness.field['stability']
        
        self.explorations.append({
            'base_state': asdict(awareness),
            'scenarios': {k: self._scenario_to_dict(v) for k, v in scenarios.items()}
        })
        
        return scenarios
    
    def _intervention_coherence(self, base: AwarenessState) -> Dict:
        """Intervention: Increase coherence by 0.25"""
        new_state = AwarenessState(
            coherence=min(1.0, base.coherence + 0.25),
            uncertainty=base.uncertainty,
            field={}
        )
        new_state.compute_field()
        
        return {
            'type': 'intervention',
            'action': 'increase_coherence',
            'state': new_state,
            'description': 'Active intervention to improve coherence',
            'outcome': 'Improved alignment and reduced risk',
            'effort_required': 'medium'
        }
    
    def _intervention_uncertainty(self, base: AwarenessState) -> Dict:
        """Intervention: Reduce uncertainty by 0.25"""
        new_state = AwarenessState(
            coherence=base.coherence,
            uncertainty=max(0.0, base.uncertainty - 0.25),
            field={}
        )
        new_state.compute_field()
        
        return {
            'type': 'intervention',
            'action': 'reduce_uncertainty',
            'state': new_state,
            'description': 'Gather more information to reduce uncertainty',
            'outcome': 'Enhanced predictability and confidence',
            'effort_required': 'high'
        }
    
    def _drift_positive(self, base: AwarenessState) -> Dict:
        """Natural positive drift"""
        new_state = AwarenessState(
            coherence=min(1.0, base.coherence + 0.1),
            uncertainty=max(0.0, base.uncertainty - 0.05),
            field={}
        )
        new_state.compute_field()
        
        return {
            'type': 'drift',
            'action': 'natural_improvement',
            'state': new_state,
            'description': 'System naturally stabilizes over time',
            'outcome': 'Gradual improvement without intervention',
            'effort_required': 'none'
        }
    
    def _drift_negative(self, base: AwarenessState) -> Dict:
        """Natural negative drift"""
        new_state = AwarenessState(
            coherence=max(0.0, base.coherence - 0.15),
            uncertainty=min(1.0, base.uncertainty + 0.1),
            field={}
        )
        new_state.compute_field()
        
        return {
            'type': 'drift',
            'action': 'natural_degradation',
            'state': new_state,
            'description': 'System degrades without maintenance',
            'outcome': 'Degradation requiring intervention',
            'effort_required': 'none'
        }
    
    def _failure_collapse(self, base: AwarenessState) -> Dict:
        """Failure mode: Coherence collapse"""
        new_state = AwarenessState(
            coherence=max(0.0, base.coherence - 0.4),
            uncertainty=min(1.0, base.uncertainty + 0.3),
            field={}
        )
        new_state.compute_field()
        
        return {
            'type': 'constraint_breach',
            'action': 'coherence_threshold_breach',
            'state': new_state,
            'description': 'Governance threshold breached',
            'outcome': 'Governance intervention required',
            'effort_required': 'none'
        }
    
    def _baseline(self, base: AwarenessState) -> Dict:
        """Baseline: No change"""
        new_state = AwarenessState(
            coherence=base.coherence,
            uncertainty=base.uncertainty,
            field=dict(base.field)
        )
        
        return {
            'type': 'baseline',
            'action': 'maintain',
            'state': new_state,
            'description': 'No action taken',
            'outcome': 'State remains unchanged',
            'effort_required': 'low'
        }
    
    def _check_violation(self, state: AwarenessState) -> bool:
        """Check if state violates invariants"""
        return (state.uncertainty > self.MAX_UNCERTAINTY or 
                state.coherence < self.MIN_COHERENCE)
    
    def _scenario_to_dict(self, scenario: Dict) -> Dict:
        """Convert scenario to JSON-serializable dict"""
        return {
            'type': scenario['type'],
            'action': scenario['action'],
            'state': asdict(scenario['state']),
            'description': scenario['description'],
            'outcome': scenario['outcome'],
            'effort_required': scenario['effort_required'],
            'violates_invariant': scenario['violates_invariant'],
            'risk_delta': scenario['risk_delta'],
            'stability_delta': scenario['stability_delta'],
        }
    
    def compare_scenarios(self, scenarios: Dict[str, Dict]) -> List[Tuple[str, float]]:
        """Rank scenarios by desirability"""
        scores = []
        
        for name, scenario in scenarios.items():
            if scenario['violates_invariant']:
                score = -100  # Automatic disqualification
            else:
                state = scenario['state']
                # Higher coherence, lower uncertainty, lower risk = better
                score = (
                    state.coherence * 40 +
                    (1 - state.uncertainty) * 30 +
                    state.field['stability'] * 20 +
                    (1 - state.field['risk']) * 10
                )
            
            scores.append((name, score))
        
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores


# ============================================================================
# DECISION ANALYZER
# ============================================================================

class DecisionAnalyzer:
    """Analyzes decision points and recommends actions"""
    
    def __init__(self):
        self.engine = CounterfactualEngine()
    
    def analyze(self, coherence: float, uncertainty: float) -> Dict:
        """Full decision analysis"""
        base_state = AwarenessState(coherence, uncertainty, {})
        base_state.compute_field()
        
        scenarios = self.engine.explore(base_state)
        rankings = self.engine.compare_scenarios(scenarios)
        
        # Determine recommendation
        valid_scenarios = [(n, s) for n, s in scenarios.items() 
                          if not s['violates_invariant']]
        
        if not valid_scenarios:
            recommendation = {
                'action': 'CRITICAL_INTERVENTION',
                'urgency': 'immediate',
                'reason': 'Current state violates invariants'
            }
        elif base_state.uncertainty > 0.7:
            recommendation = {
                'action': 'REDUCE_UNCERTAINTY',
                'urgency': 'high',
                'reason': 'High uncertainty threatens stability'
            }
        elif base_state.coherence < 0.3:
            recommendation = {
                'action': 'INCREASE_COHERENCE',
                'urgency': 'high',
                'reason': 'Low coherence risks drift'
            }
        else:
            recommendation = {
                'action': 'MONITOR',
                'urgency': 'low',
                'reason': 'System stable, maintain current state'
            }
        
        return {
            'base_state': asdict(base_state),
            'scenarios': {k: self.engine._scenario_to_dict(v) 
                         for k, v in scenarios.items()},
            'rankings': rankings,
            'recommendation': recommendation,
            'analysis': self._generate_analysis(base_state, scenarios)
        }
    
    def _generate_analysis(self, base: AwarenessState, scenarios: Dict) -> str:
        """Generate natural language analysis"""
        lines = []
        
        lines.append(f"Current State Analysis:")
        lines.append(f"  Coherence: {base.coherence:.3f}")
        lines.append(f"  Uncertainty: {base.uncertainty:.3f}")
        lines.append(f"  Risk: {base.field['risk']:.3f}")
        lines.append(f"  Stability: {base.field['stability']:.3f}")
        lines.append("")
        
        if base.uncertainty > CounterfactualEngine.MAX_UNCERTAINTY:
            lines.append("⚠ CRITICAL: Uncertainty exceeds safe threshold")
        elif base.coherence < CounterfactualEngine.MIN_COHERENCE:
            lines.append("⚠ CRITICAL: Coherence below minimum threshold")
        
        viable = [n for n, s in scenarios.items() if not s['violates_invariant']]
        lines.append(f"\nViable Paths: {len(viable)}/{len(scenarios)}")
        
        return "\n".join(lines)


# ============================================================================
# CLI INTERFACE
# ============================================================================

def run_analysis():
    """Run interactive counterfactual analysis"""
    analyzer = DecisionAnalyzer()
    
    scenarios_to_test = [
        ("High Uncertainty Context", 0.48, 0.72),
        ("Stable Coherent State", 0.85, 0.25),
        ("Critical Threshold", 0.18, 0.84),
        ("Optimal State", 0.90, 0.15),
        ("Degraded State", 0.25, 0.65),
    ]
    
    print("=" * 70)
    print("9DA COUNTERFACTUAL DECISION ANALYSIS")
    print("=" * 70)
    
    all_results = []
    
    for name, coherence, uncertainty in scenarios_to_test:
        print(f"\n{'─' * 70}")
        print(f"Scenario: {name}")
        print(f"{'─' * 70}")
        
        result = analyzer.analyze(coherence, uncertainty)
        
        print(result['analysis'])
        print(f"\nRecommendation: {result['recommendation']['action']}")
        print(f"Urgency: {result['recommendation']['urgency']}")
        print(f"Reason: {result['recommendation']['reason']}")
        
        print(f"\nScenario Rankings:")
        for rank, (scenario_name, score) in enumerate(result['rankings'][:5], 1):
            scenario = result['scenarios'][scenario_name]
            violation = "❌" if scenario['violates_invariant'] else "✓"
            print(f"  {rank}. [{violation}] {scenario_name}: {score:.2f}")
            print(f"     {scenario['outcome']}")
        
        all_results.append({
            'name': name,
            'result': result
        })
    
    # Save comprehensive report
    output_file = Path('counterfactual_analysis.json')
    with output_file.open('w') as f:
        json.dump(all_results, f, indent=2)
    
    print(f"\n{'=' * 70}")
    print(f"Full analysis saved to: {output_file}")
    print("=" * 70)


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == '__main__':
    run_analysis()
