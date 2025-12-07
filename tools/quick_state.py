#!/usr/bin/env python3
"""Quick state reader - extracts only essential cycle info to minimize tokens"""

import yaml
import sys
from pathlib import Path

def quick_state():
    """Read minimal state needed for cycle execution"""
    base = Path(__file__).parent.parent

    # Read state
    with open(base / 'state.yaml') as f:
        state = yaml.safe_load(f)

    # Extract essentials only
    essentials = {
        'cycle': state['cycle'],
        'current_goal': state['current_goal'],
        'next_action': state['next_action'],
        'last_mutation': state.get('last_mutation'),
        'last_error': state.get('last_error'),
    }

    # Read only last 5 mutations
    mutations = []
    with open(base / 'mutations.log') as f:
        lines = [l.strip() for l in f if l.strip() and not l.startswith('#')]
        mutations = lines[-5:] if len(lines) > 5 else lines

    # Minimal metrics
    with open(base / 'metrics.yaml') as f:
        metrics = yaml.safe_load(f)

    compact = {
        'cycles': metrics['performance']['cycles_total'],
        'gradient': metrics['evolution_gradient']['current_value'],
        'avg_tokens': metrics['performance']['avg_tokens_per_cycle']
    }

    return {
        'state': essentials,
        'recent_mutations': mutations,
        'metrics': compact
    }

if __name__ == '__main__':
    import json
    result = quick_state()
    print(json.dumps(result, indent=2))
