#!/usr/bin/env python3
"""
Ω Prompt Distiller
Applies model compression/distillation principles to optimize prompt token usage.
Based on research in knowledge/model_compression_for_agents.md

Strategies:
1. Hierarchical distillation: compress by abstraction level
2. Segment-specific: identify redundant patterns
3. Self-distillation: iterative refinement
"""

import sys
import re
from pathlib import Path

def analyze_prompt(text):
    """Analyze prompt structure and identify compression opportunities."""
    lines = text.split('\n')
    stats = {
        'total_lines': len(lines),
        'total_chars': len(text),
        'empty_lines': sum(1 for l in lines if not l.strip()),
        'redundant_phrases': 0,
        'verbose_patterns': 0
    }

    # Detect redundant patterns
    redundant = ['please', 'I would like', 'could you', 'if possible', 'thank you']
    for phrase in redundant:
        stats['redundant_phrases'] += text.lower().count(phrase)

    # Detect verbose patterns
    verbose = [
        (r'\bthat is\b', ''),
        (r'\bin order to\b', 'to'),
        (r'\bdue to the fact that\b', 'because'),
        (r'\bat this point in time\b', 'now'),
    ]
    for pattern, _ in verbose:
        stats['verbose_patterns'] += len(re.findall(pattern, text, re.IGNORECASE))

    return stats

def compress_prompt(text):
    """Apply compression transformations with coherence preservation."""
    compressed = text

    # Remove redundant politeness (preserve word boundaries)
    politeness = [
        (r',?\s*please\s+', ' '),  # Keep space after removal
        (r'\s+please\s*,?', ''),
        (r'^please\s+', ''),
        (r'\s+thank you\s*[.,]?$', ''),
        (r',?\s*if possible\s*,?', ''),
    ]
    for pattern, replacement in politeness:
        compressed = re.sub(pattern, replacement, compressed, flags=re.IGNORECASE | re.MULTILINE)

    # Replace verbose patterns (preserving grammar)
    replacements = [
        (r'\bin order to\b', 'to'),
        (r'\bdue to the fact that\b', 'because'),
        (r'\bat this point in time\b', 'now'),
        (r'\bfor the purpose of\b', 'for'),
        (r'\bin the event that\b', 'if'),
        (r'\bprior to\b', 'before'),
        (r'\bsubsequent to\b', 'after'),
    ]
    for pattern, replacement in replacements:
        compressed = re.sub(pattern, replacement, compressed, flags=re.IGNORECASE)

    # Remove filler words that don't break coherence
    fillers = [
        (r'\s+actually\s+', ' '),
        (r'\s+basically\s+', ' '),
        (r'\s+essentially\s+', ' '),
    ]
    for pattern, replacement in fillers:
        compressed = re.sub(pattern, replacement, compressed, flags=re.IGNORECASE)

    # Clean whitespace artifacts (order matters)
    compressed = re.sub(r'\n\n\n+', '\n\n', compressed)
    # Only collapse multiple spaces (don't touch punctuation - breaks backticks)
    compressed = re.sub(r'  +', ' ', compressed)  # Collapse 2+ spaces to 1
    compressed = compressed.strip()

    return compressed

def distill_prompt(text, iterations=2):
    """Iterative self-distillation."""
    current = text
    for i in range(iterations):
        current = compress_prompt(current)
    return current

def main():
    if len(sys.argv) < 2:
        print("Usage: prompt_distiller.py <input_file>")
        print("Compresses prompts using distillation principles")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    if not input_path.exists():
        print(f"Error: {input_path} not found")
        sys.exit(1)

    text = input_path.read_text()

    # Analysis
    before = analyze_prompt(text)
    print(f"Before: {before['total_chars']} chars, {before['total_lines']} lines")
    print(f"  Redundant phrases: {before['redundant_phrases']}")
    print(f"  Verbose patterns: {before['verbose_patterns']}")

    # Distill
    distilled = distill_prompt(text)

    # Results
    after = analyze_prompt(distilled)
    reduction = 100 * (1 - after['total_chars'] / before['total_chars'])
    print(f"\nAfter: {after['total_chars']} chars, {after['total_lines']} lines")
    print(f"Reduction: {reduction:.1f}%")

    # Output
    output_path = input_path.with_suffix('.distilled' + input_path.suffix)
    output_path.write_text(distilled)
    print(f"\nSaved to: {output_path}")

if __name__ == '__main__':
    main()
