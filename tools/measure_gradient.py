#!/usr/bin/env python3
"""
Ω Evolution Gradient Analyzer
Measures progress toward optimization goals:
- Minimize: tokens, errors, cycles to goal
- Maximize: capability, autonomy, goal completion rate
"""

import yaml
from pathlib import Path

def load_yaml(path):
    with open(path) as f:
        return yaml.safe_load(f)

def measure_gradient():
    state = load_yaml('state.yaml')
    metrics = load_yaml('metrics.yaml')

    # Current measurements
    cycles = state.get('cycle', 0)
    tools = metrics.get('growth', {}).get('tools_created', 0)
    knowledge = metrics.get('growth', {}).get('knowledge_entries', 0)
    goals_completed = metrics.get('growth', {}).get('goals_completed', 0)
    errors = state.get('metrics_snapshot', {}).get('errors_total', 0)

    # Calculate gradient components
    capability_score = tools + knowledge  # total artifacts
    efficiency = goals_completed / max(cycles, 1)  # goals per cycle
    error_rate = errors / max(cycles, 1)  # errors per cycle

    # Evolution gradient (higher = better)
    gradient = (capability_score * efficiency) / max(1 - error_rate, 0.01)

    report = {
        'gradient_value': round(gradient, 3),
        'components': {
            'capability_score': capability_score,
            'efficiency': round(efficiency, 3),
            'error_rate': round(error_rate, 3)
        },
        'interpretation': [],
        'recommendations': []
    }

    # Interpret gradient
    if gradient > 1.0:
        report['interpretation'].append('Positive evolution trajectory')
    elif gradient > 0.5:
        report['interpretation'].append('Moderate progress')
    else:
        report['interpretation'].append('Consider mutation to improve')

    # Recommendations
    if efficiency < 0.2:
        report['recommendations'].append('Focus on completing current goal before adding new ones')
    if capability_score < cycles / 2:
        report['recommendations'].append('Increase artifact creation rate')
    if error_rate > 0.1:
        report['recommendations'].append('Address error patterns before expanding')
    if not report['recommendations']:
        report['recommendations'].append('Continue current evolution strategy')

    return report

if __name__ == '__main__':
    report = measure_gradient()
    print("=" * 50)
    print("Ω EVOLUTION GRADIENT REPORT")
    print("=" * 50)
    print(f"\nGradient Value: {report['gradient_value']}")
    print("\nComponents:")
    for k, v in report['components'].items():
        print(f"  {k}: {v}")
    print("\nInterpretation:")
    for item in report['interpretation']:
        print(f"  - {item}")
    print("\nRecommendations:")
    for item in report['recommendations']:
        print(f"  - {item}")
    print("=" * 50)
