# Internal Orchestrator Blueprint (Agentic Tooling)

Objective: Build a native orchestrator (no external frameworks) that turns capability gaps into focused tools using existing Ω components.

Pipeline (MVP)
1) gap_analyzer.py — scan tools/knowledge, output top gaps (JSON).
2) research_pipeline.py or web_search.py — gather 3-5 primary sources per gap into knowledge/.
3) prompt_distiller.py — compress research into an actionable spec with constraints and acceptance checks.
4) tool_composer.py — scaffold/compose a small tool from the spec; include minimal README/test hook.
5) impact_analyzer.py + outcomes.log — run quick eval (manual/auto) and record score/lessons.

Operating notes
- Tackle one gap per run; prioritize agentic tooling gaps first.
- Cache research outputs to avoid repeated queries; reuse sources when possible.
- Validate distillation integrity (spacing, code fences) before composing.
- After tool creation, set next_action to targeted test or follow-up research.

Example chain
```
python tools/gap_analyzer.py --top 1 --format json
python tools/research_pipeline.py --topic "<gap>" --out knowledge/<file>.md
python tools/prompt_distiller.py --input knowledge/<file>.md --out tmp/spec.md
python tools/tool_composer.py --spec tmp/spec.md --name <tool_name>
python tools/impact_analyzer.py --tool <tool_name> --log outcomes.log
```
