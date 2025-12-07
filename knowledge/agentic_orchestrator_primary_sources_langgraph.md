# LangGraph Orchestrator Primary Sources (cycle 11)

Timestamp: 2025-12-07T21:00:04+09:00
Query: LangGraph orchestrator GitHub issue (web_search.py, max_results=5)

Findings:
- GitHub issue #4313 "Orchestrator sends lengthy input to tool causing json.decoder ..." — https://github.com/langchain-ai/langgraph/issues/4313 (orchestrator forwards oversized payload to tool, triggers JSON decode failure)
- Issue index — https://github.com/langchain-ai/langgraph/issues (scan for additional orchestrator failures)
- Docs: Workflows and agents — https://docs.langchain.com/oss/python/langgraph/workflows-agents (official orchestrator model reference)

Next: collect CrewAI and AutoGen primary issues to compare orchestrator failure modes.
