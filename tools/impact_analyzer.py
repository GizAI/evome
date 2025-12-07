#!/usr/bin/env python3
"""
Ω Impact Analyzer - Quantifies value of knowledge produced
Based on 2025 AI agent metrics research: ROE (Return on Efficiency) > traditional ROI
Metrics: novelty, actionability, token efficiency, application potential
"""

import sys
import json
import yaml
from pathlib import Path

def analyze_knowledge_impact(knowledge_file: str) -> dict:
    """
    Measure impact/value of a knowledge entry.

    Metrics aligned with 2025 research:
    - ROE (Return on Efficiency): insights gained / tokens used
    - Actionability: can insights be applied immediately?
    - Novelty: new vs redundant information
    - Application potential: breadth of use cases

    Returns:
        dict with impact scores and recommendations
    """

    # Read knowledge file
    kpath = Path(knowledge_file)
    if not kpath.exists():
        return {"error": f"Knowledge file not found: {knowledge_file}"}

    content = kpath.read_text()

    # Calculate metrics
    word_count = len(content.split())
    token_estimate = word_count * 1.3  # rough estimate

    # Heuristic scoring
    impact = {
        "file": knowledge_file,
        "metrics": {
            "size_words": word_count,
            "size_tokens_est": int(token_estimate),
            "novelty_score": 0,
            "actionability_score": 0,
            "application_score": 0
        },
        "impact_level": "unknown",
        "roi_estimate": 0.0,
        "recommendations": []
    }

    # Novelty: check for actionable keywords vs just summaries
    actionable_keywords = ["create", "implement", "use", "apply", "tool", "pattern", "strategy"]
    novelty_indicators = ["insight", "recommendation", "conclusion", "principle"]

    content_lower = content.lower()

    actionable_count = sum(1 for kw in actionable_keywords if kw in content_lower)
    novelty_count = sum(1 for kw in novelty_indicators if kw in content_lower)

    # Actionability score (0-10)
    impact["metrics"]["actionability_score"] = min(10, actionable_count * 2)

    # Novelty score (0-10)
    impact["metrics"]["novelty_score"] = min(10, novelty_count * 2)

    # Application score based on breadth (headers, sections)
    section_count = content.count("#")
    impact["metrics"]["application_score"] = min(10, section_count)

    # Calculate ROE: (actionability + novelty + application) / (tokens/1000)
    total_value = (
        impact["metrics"]["actionability_score"] +
        impact["metrics"]["novelty_score"] +
        impact["metrics"]["application_score"]
    )
    token_cost = impact["metrics"]["size_tokens_est"] / 1000.0
    impact["roi_estimate"] = round(total_value / token_cost if token_cost > 0 else 0, 2)

    # Determine impact level
    if impact["roi_estimate"] > 10:
        impact["impact_level"] = "high"
    elif impact["roi_estimate"] > 5:
        impact["impact_level"] = "medium"
    else:
        impact["impact_level"] = "low"

    # Generate recommendations
    if impact["metrics"]["actionability_score"] < 5:
        impact["recommendations"].append("Add concrete implementation steps or tool creation")

    if impact["metrics"]["novelty_score"] < 5:
        impact["recommendations"].append("Extract unique insights or principles")

    if impact["metrics"]["application_score"] < 5:
        impact["recommendations"].append("Expand breadth with more use cases or patterns")

    if impact["impact_level"] == "high":
        impact["recommendations"].append("High-value knowledge - prioritize application in mutations")

    return impact

def analyze_all_knowledge() -> dict:
    """Analyze all knowledge entries and rank by impact."""
    knowledge_dir = Path("knowledge")
    if not knowledge_dir.exists():
        return {"error": "knowledge/ directory not found"}

    results = []
    for kfile in knowledge_dir.glob("*.md"):
        analysis = analyze_knowledge_impact(str(kfile))
        if "error" not in analysis:
            results.append(analysis)

    # Sort by ROI estimate descending
    results.sort(key=lambda x: x["roi_estimate"], reverse=True)

    return {
        "total_entries": len(results),
        "avg_roi": round(sum(r["roi_estimate"] for r in results) / len(results), 2) if results else 0,
        "high_impact": [r for r in results if r["impact_level"] == "high"],
        "medium_impact": [r for r in results if r["impact_level"] == "medium"],
        "low_impact": [r for r in results if r["impact_level"] == "low"],
        "top_3": results[:3]
    }

def main():
    if len(sys.argv) < 2:
        # Default: analyze all knowledge
        result = analyze_all_knowledge()
    else:
        # Analyze specific file
        result = analyze_knowledge_impact(sys.argv[1])

    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
