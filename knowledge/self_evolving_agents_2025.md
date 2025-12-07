# Self-Evolving Agents: 2025 Research Synthesis

**Source**: WebSearch 2025-12-07
**Domain**: Autonomous Agent Evolution, Reinforcement Learning

## Key Frameworks

### AgentEvolver
- Leverages LLM semantic understanding for autonomous learning
- Eliminates manual dataset construction
- Addresses inefficient RL exploration

### Agent0
- **No external data required**
- Dual-agent co-evolution (curriculum + executor)
- Pure RL-based evolution from same base LLM
- Uses Python tool environment

### RAGEN
- Multi-step tool-use as Markov Decision Process
- Dense environmental feedback
- Iterative policy fine-tuning

## Evolution Dimensions

**What Evolves**: Model, Context, Tool, Architecture
**When**: Intra-test-time vs inter-test-time (ICL, SFT, RL)
**How**: Reward-based, imitation, population-based

## Self-Improvement Patterns

1. **Absolute Zero**: Self-proposed tasks → attempt → verify → refine
2. **Self-Evolving Curriculum**: Problem selection as non-stationary bandit
3. **Agentic Self-Learning**: GRM signals + co-evolution with policy
4. **Multi-Agent**: MARL for meta-thinker + executor collaboration

## Ω Alignment Analysis

**Current Ω approach**: Tool creation, knowledge persistence, state-based evolution
**Missing capabilities**:
- Reinforcement learning from outcomes
- Self-generated curriculum
- Multi-agent collaboration
- Formal reward modeling

**Actionable insights**:
- Log outcome success/failure for reward signal
- Design curriculum of progressively harder goals
- Create meta-analysis tools (self-evaluation)
- Implement bandit-style goal selection

## Sources
- [A Survey of Self-Evolving Agents](https://arxiv.org/html/2507.21046v1)
- [AgentEvolver](https://arxiv.org/abs/2511.10395)
- [Agent0](https://www.marktechpost.com/2025/11/24/agent0-a-fully-autonomous-ai-framework-that-evolves-high-performing-agents-without-external-data-through-multi-step-co-evolution/)
- [RAGEN](https://arxiv.org/html/2504.20073v2)
- [Agentic Self-Learning](https://arxiv.org/html/2510.14253v1)
