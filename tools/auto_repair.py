#!/usr/bin/env python3
"""
Ω Auto-Repair Tool
Monitors errors.log and state.yaml, executes self-repair protocol automatically.
Part of Ω's self-healing capability.
"""

import yaml
import os
from datetime import datetime

def load_state():
    """Load current state.yaml"""
    with open('state.yaml', 'r') as f:
        return yaml.safe_load(f)

def load_errors():
    """Load errors.log if exists"""
    if not os.path.exists('errors.log'):
        return []
    with open('errors.log', 'r') as f:
        return [line.strip() for line in f if line.strip()]

def count_stuck_cycles(state):
    """Check if stuck on same goal for >3 cycles"""
    # Parse mutations.log to see recent cycles on current goal
    goal = state.get('current_goal', '')
    if not os.path.exists('mutations.log'):
        return 0

    with open('mutations.log', 'r') as f:
        lines = f.readlines()

    # Count recent cycles mentioning current goal
    recent_cycles = [l for l in lines[-10:] if goal.lower() in l.lower()]
    return len(recent_cycles)

def suggest_repair(state, errors, stuck_cycles):
    """Generate repair suggestion based on state"""
    repairs = []

    # Check for errors
    if errors:
        recent_errors = errors[-5:]
        repairs.append({
            'issue': 'errors_detected',
            'count': len(recent_errors),
            'action': 'rollback last mutation and retry with different approach',
            'priority': 'high'
        })

    # Check if stuck
    if stuck_cycles > 3:
        repairs.append({
            'issue': 'stuck_on_goal',
            'cycles': stuck_cycles,
            'action': 'simplify goal or try different approach',
            'priority': 'medium'
        })

    # Check exploration rate
    exploration = state.get('evolution_state', {}).get('exploration_rate', 0.3)
    if stuck_cycles > 5 and exploration < 0.4:
        repairs.append({
            'issue': 'low_exploration_while_stuck',
            'action': 'increase exploration_rate to 0.4 (exploration mode)',
            'priority': 'medium'
        })

    return repairs

def main():
    state = load_state()
    errors = load_errors()
    stuck = count_stuck_cycles(state)

    repairs = suggest_repair(state, errors, stuck)

    print(f"Ω Auto-Repair Analysis (Cycle {state.get('cycle', 0)})")
    print("=" * 50)
    print(f"Errors detected: {len(errors)}")
    print(f"Stuck cycles: {stuck}")
    print(f"Exploration rate: {state.get('evolution_state', {}).get('exploration_rate', 0.3)}")
    print()

    if repairs:
        print("REPAIR SUGGESTIONS:")
        for i, r in enumerate(repairs, 1):
            print(f"\n{i}. {r['issue'].upper()} [{r['priority']}]")
            print(f"   Action: {r['action']}")
    else:
        print("STATUS: No repairs needed. System healthy.")

    return len(repairs)

if __name__ == '__main__':
    exit(main())
