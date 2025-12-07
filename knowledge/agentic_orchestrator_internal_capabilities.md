# Internal Orchestrator Pivot (CrewAI/LangGraph not needed)

- Human feedback: rely on native Codex/Ω capabilities instead of external orchestrators (CrewAI, LangGraph).
- Available primitives: introspect, gap_analyzer, research_pipeline, web_search, prompt_distiller, tool_composer, auto_repair, token_optimizer, optimization_suite.
- Strengths: fast tool chaining, RL goal selection, token-efficient prompts, error prediction/repair.
- Immediate plan: design an internal orchestrator flow using existing tools (no external frameworks), focusing on research + synthesis pipelines with self-repair.
- Next step idea: blueprint pipeline (goal selection → gap analysis → research_pipeline/web_search → prompt_distiller → tool_composer → outcome logging/auto_repair) and test on agentic tooling topic.
