#!/usr/bin/env python3
"""
Ω Error Predictor v0.1
Analyzes state and patterns to predict potential errors before they occur.
"""

import yaml
from pathlib import Path
from datetime import datetime

def load_file(filename):
    """Load a YAML file from the evome root."""
    path = Path(__file__).parent.parent / filename
    if path.exists():
        with open(path) as f:
            return yaml.safe_load(f) or {}
    return {}

def analyze_state_risks(state):
    """Analyze state.yaml for potential issues."""
    risks = []

    # Check for stagnation
    cycle = state.get('cycle', 0)
    goals_completed = state.get('metrics_snapshot', {}).get('goals_completed', 0)
    if cycle > 0 and goals_completed / cycle < 0.3:
        risks.append({
            'type': 'stagnation',
            'severity': 'medium',
            'message': f'Low goal completion rate ({goals_completed}/{cycle} cycles)',
            'suggestion': 'Consider simplifying current goal or trying different approach'
        })

    # Check exploration rate bounds
    exploration = state.get('evolution_state', {}).get('exploration_rate', 0.3)
    if exploration > 0.7:
        risks.append({
            'type': 'instability',
            'severity': 'high',
            'message': f'High exploration rate ({exploration}) may cause erratic behavior',
            'suggestion': 'Reduce exploration_rate to stabilize'
        })
    elif exploration < 0.1:
        risks.append({
            'type': 'local_minimum',
            'severity': 'low',
            'message': f'Low exploration rate ({exploration}) may cause stagnation',
            'suggestion': 'Consider increasing exploration_rate'
        })

    # Check for missing critical fields
    required = ['current_goal', 'next_action', 'cycle']
    for field in required:
        if field not in state or state[field] is None:
            risks.append({
                'type': 'missing_field',
                'severity': 'high',
                'message': f'Missing required field: {field}',
                'suggestion': f'Set {field} in state.yaml'
            })

    return risks

def analyze_metrics_risks(metrics):
    """Analyze metrics.yaml for concerning patterns."""
    risks = []

    perf = metrics.get('performance', {})

    # Check success rate
    success_rate = perf.get('success_rate', 1.0)
    if success_rate < 0.5:
        risks.append({
            'type': 'high_failure_rate',
            'severity': 'high',
            'message': f'Success rate below 50% ({success_rate})',
            'suggestion': 'Review recent mutations, consider rollback'
        })

    # Check token usage
    avg_tokens = perf.get('avg_tokens_per_cycle', 0)
    if avg_tokens > 8000:
        risks.append({
            'type': 'token_overuse',
            'severity': 'medium',
            'message': f'High token usage ({avg_tokens}/cycle)',
            'suggestion': 'Optimize prompts, reduce verbosity'
        })

    # Check cost
    cost = perf.get('cost_usd_total', 0)
    if cost > 1.0:
        risks.append({
            'type': 'budget_warning',
            'severity': 'medium',
            'message': f'Total cost approaching budget (${cost})',
            'suggestion': 'Monitor spending, consider pausing'
        })

    return risks

def analyze_error_patterns(errors_log_path):
    """Analyze errors.log for recurring patterns."""
    risks = []
    path = Path(__file__).parent.parent / "errors.log"

    if not path.exists():
        return risks

    with open(path) as f:
        content = f.read()

    # Count error mentions
    error_count = content.count('ERROR_TYPE')
    if error_count > 5:
        risks.append({
            'type': 'recurring_errors',
            'severity': 'medium',
            'message': f'Multiple errors logged ({error_count})',
            'suggestion': 'Analyze error patterns for root cause'
        })

    return risks

def predict():
    """Run all predictions and return combined risks."""
    state = load_file('state.yaml')
    metrics = load_file('metrics.yaml')

    all_risks = []
    all_risks.extend(analyze_state_risks(state))
    all_risks.extend(analyze_metrics_risks(metrics))
    all_risks.extend(analyze_error_patterns('errors.log'))

    # Sort by severity
    severity_order = {'high': 0, 'medium': 1, 'low': 2}
    all_risks.sort(key=lambda r: severity_order.get(r['severity'], 99))

    return {
        'timestamp': datetime.now().isoformat(),
        'cycle': state.get('cycle', 0),
        'risks_found': len(all_risks),
        'risks': all_risks
    }

if __name__ == "__main__":
    result = predict()
    print(f"Ω Error Prediction Report - Cycle {result['cycle']}")
    print(f"Timestamp: {result['timestamp']}")
    print(f"Risks found: {result['risks_found']}")
    print("-" * 40)

    if result['risks']:
        for risk in result['risks']:
            print(f"\n[{risk['severity'].upper()}] {risk['type']}")
            print(f"  {risk['message']}")
            print(f"  → {risk['suggestion']}")
    else:
        print("\n✓ No risks detected. System healthy.")
