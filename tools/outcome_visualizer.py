#!/usr/bin/env python3
"""
Ω Outcome Visualizer
Analyzes outcomes.log to track RL performance trends
"""

import re
from collections import defaultdict
from datetime import datetime

def parse_outcomes(log_path='outcomes.log'):
    """Parse outcomes.log and extract metrics"""
    data = {
        'total': 0,
        'by_action': defaultdict(lambda: {'count': 0, 'success': 0, 'avg_score': 0.0}),
        'scores': [],
        'timeline': []
    }

    with open(log_path) as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue

            # Parse: [CYCLE] TIMESTAMP | ACTION | RESULT | SCORE | NOTES
            match = re.match(r'\[(\d+)\] ([^\|]+) \| ([^\|]+) \| ([^\|]+) \| ([\d.]+) \| (.+)', line)
            if match:
                cycle, timestamp, action, result, score, notes = match.groups()
                cycle = int(cycle)
                score = float(score)

                data['total'] += 1
                data['scores'].append(score)
                data['timeline'].append((cycle, action, score))

                action = action.strip()
                data['by_action'][action]['count'] += 1
                if result.strip() == 'success':
                    data['by_action'][action]['success'] += 1
                data['by_action'][action]['avg_score'] += score

    # Calculate averages
    for action in data['by_action']:
        count = data['by_action'][action]['count']
        data['by_action'][action]['avg_score'] /= count
        data['by_action'][action]['success_rate'] = data['by_action'][action]['success'] / count

    return data

def visualize():
    """Display outcomes analysis"""
    data = parse_outcomes()

    print(f"Ω OUTCOMES ANALYSIS")
    print(f"=" * 50)
    print(f"Total outcomes: {data['total']}")

    if data['scores']:
        avg_score = sum(data['scores']) / len(data['scores'])
        print(f"Average score: {avg_score:.2f}")
        print()

    print("Performance by action type:")
    print("-" * 50)
    for action, stats in sorted(data['by_action'].items()):
        print(f"{action:20} | count: {stats['count']:2} | success: {stats['success_rate']*100:5.1f}% | avg: {stats['avg_score']:.2f}")

    print()
    print("Recent timeline:")
    print("-" * 50)
    for cycle, action, score in data['timeline'][-5:]:
        bar = '█' * int(score * 10)
        print(f"[{cycle:4}] {action:20} {score:.1f} {bar}")

    print()

    # Insight
    if data['by_action']:
        best = max(data['by_action'].items(), key=lambda x: x[1]['avg_score'])
        print(f"Best action: {best[0]} (avg {best[1]['avg_score']:.2f})")

if __name__ == '__main__':
    visualize()
