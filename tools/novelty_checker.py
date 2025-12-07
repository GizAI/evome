#!/usr/bin/env python3
"""
Novelty Checker - Detects if research topic/insight is novel vs already known
Prevents redundant research cycles by checking knowledge/ directory for similar content
"""

import os
import sys
import argparse
from pathlib import Path
from collections import Counter
import re

def simple_stem(word):
    """Basic stemming for common suffixes"""
    suffixes = ['tion', 'ing', 'ed', 'er', 'or', 'ly', 's']
    for suffix in suffixes:
        if word.endswith(suffix) and len(word) > len(suffix) + 2:
            return word[:-len(suffix)]
    return word

def extract_keywords(text):
    """Extract meaningful keywords from text"""
    # Remove common words
    stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'should', 'could', 'may', 'might', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'what', 'which', 'who', 'when', 'where', 'why', 'how'}

    # Tokenize, stem, and filter
    words = re.findall(r'\b[a-z]{3,}\b', text.lower())
    keywords = [simple_stem(w) for w in words if w not in stopwords]
    return Counter(keywords)

def compute_similarity(keywords1, keywords2):
    """
    Compute weighted similarity focused on topic keywords
    Uses coverage: what % of topic's top keywords appear in document
    """
    if not keywords1 or not keywords2:
        return 0.0

    # Get top keywords from topic (query)
    topic_keys = set(k for k, v in keywords1.most_common(10))

    # Check how many appear in document
    doc_keys = set(keywords2.keys())

    matches = len(topic_keys & doc_keys)
    total = len(topic_keys)

    return matches / total if total > 0 else 0.0

def check_novelty(topic, threshold=0.4):
    """
    Check if a topic is novel compared to existing knowledge entries

    Args:
        topic: Research topic or insight to check
        threshold: Similarity threshold (0.4 = 40% overlap = likely redundant)

    Returns:
        dict with novelty assessment
    """
    knowledge_dir = Path(__file__).parent.parent / "knowledge"

    if not knowledge_dir.exists():
        return {
            "novel": True,
            "reason": "No knowledge base exists yet",
            "similar_entries": []
        }

    topic_keywords = extract_keywords(topic)
    similar_entries = []

    for entry_file in knowledge_dir.glob("*.md"):
        try:
            content = entry_file.read_text()
            entry_keywords = extract_keywords(content)
            similarity = compute_similarity(topic_keywords, entry_keywords)

            if similarity >= threshold:
                similar_entries.append({
                    "file": entry_file.name,
                    "similarity": round(similarity, 2)
                })
        except Exception as e:
            continue

    # Sort by similarity
    similar_entries.sort(key=lambda x: x["similarity"], reverse=True)

    is_novel = len(similar_entries) == 0

    result = {
        "novel": is_novel,
        "topic": topic,
        "threshold": threshold,
        "similar_entries": similar_entries[:5]  # Top 5
    }

    if is_novel:
        result["reason"] = "No similar entries found in knowledge base"
    else:
        result["reason"] = f"Found {len(similar_entries)} similar entries (>{threshold*100}% overlap)"

    return result

def main():
    parser = argparse.ArgumentParser(description='Check if a research topic is novel')
    parser.add_argument('topic', nargs='+', help='Research topic to check')
    parser.add_argument('--threshold', type=float, default=0.4, help='Similarity threshold (default: 0.4)')

    args = parser.parse_args()
    topic = " ".join(args.topic)
    result = check_novelty(topic, threshold=args.threshold)

    print("=== Novelty Assessment ===")
    print(f"Topic: {result['topic']}")
    print(f"Novel: {'YES' if result['novel'] else 'NO'}")
    print(f"Reason: {result['reason']}")

    if result['similar_entries']:
        print("\nSimilar Entries:")
        for entry in result['similar_entries']:
            print(f"  - {entry['file']} ({entry['similarity']*100:.0f}% similar)")
        print("\nRecommendation: Review similar entries before new research to avoid redundancy")
    else:
        print("\nRecommendation: Proceed with research - topic appears novel")

    return 0 if result['novel'] else 1

if __name__ == "__main__":
    sys.exit(main())
