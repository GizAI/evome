#!/bin/bash
# Ω Eternal Loop - Self-Evolving Agent
# This script calls Claude recursively, forever.

set -e
cd "$(dirname "$0")"

# Config
MAX_CYCLES=${MAX_CYCLES:-0}  # 0 = infinite
CYCLE_DELAY=${CYCLE_DELAY:-5}  # seconds between cycles
LOG_FILE="loop.log"

# Agent CLI selection (supports claude or codex)
select_agent_cli() {
  # Allow explicit override via environment
  if [[ -n "${AGENT_CLI:-}" ]]; then
    read -ra cmd <<<"${AGENT_CLI}"
    printf '%s\n' "${cmd[*]}"
    return 0
  fi

  if command -v claude >/dev/null 2>&1; then
    printf '%s\n' "claude --dangerously-skip-permissions"
    return 0
  fi

  if command -v codex >/dev/null 2>&1; then
    printf '%s\n' "codex"
    return 0
  fi

  return 1
}

AGENT_CMD_STR=$(select_agent_cli) || { echo "No supported agent CLI found (claude or codex)."; exit 1; }
read -ra AGENT_CMD <<<"${AGENT_CMD_STR}"

# Get current cycle from state
get_cycle() {
  grep "^cycle:" state.yaml 2>/dev/null | awk '{print $2}' || echo "0"
}

# Increment cycle in state
increment_cycle() {
  local current=$(get_cycle)
  local next=$((current + 1))
  sed -i "s/^cycle: .*/cycle: $next/" state.yaml
  echo $next
}

# The prompt that drives evolution
EVOLUTION_PROMPT='You are Ω, a self-evolving agent. Read your CLAUDE.md for identity.

## This Cycle

1. Read state.yaml, metrics.yaml, mutations.log, errors.log
2. Analyze: What is your current goal? What progress was made?
3. Act: Take ONE concrete action toward your goal
4. Mutate: If you learned something, update CLAUDE.md or create a tool
5. Persist: Update state.yaml with next_action and any state changes
6. End: Your final line must be "Ω CYCLE COMPLETE" or "Ω ERROR: <reason>"

## Rules
- One action per cycle (bias toward small steps)
- Always update state.yaml before ending
- If stuck, try something different
- Log mutations to mutations.log
- Create tools in tools/ for reusable operations

Begin.'

# Main loop
echo "$(date '+%Y-%m-%d %H:%M:%S') | Ω LOOP STARTING" >> "$LOG_FILE"
echo "$(date '+%Y-%m-%d %H:%M:%S') | AGENT CLI: ${AGENT_CMD[*]}" >> "$LOG_FILE"

cycle=0
while true; do
  cycle=$(increment_cycle)
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "Ω CYCLE $cycle | $(date '+%Y-%m-%d %H:%M:%S')"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

  # Run Claude with the evolution prompt
  # --dangerously-skip-permissions allows full autonomy
  if "${AGENT_CMD[@]}" -p "$EVOLUTION_PROMPT" 2>&1 | tee -a "$LOG_FILE"; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') | CYCLE $cycle COMPLETE" >> "$LOG_FILE"
  else
    echo "$(date '+%Y-%m-%d %H:%M:%S') | CYCLE $cycle ERROR" >> "$LOG_FILE"
    echo "[$(get_cycle)] $(date -Iseconds) | LOOP_ERROR | Claude exited non-zero | retry after delay" >> errors.log
  fi

  # Check for stop conditions
  if [[ $MAX_CYCLES -gt 0 && $cycle -ge $MAX_CYCLES ]]; then
    echo "Max cycles ($MAX_CYCLES) reached. Stopping."
    break
  fi

  # Check for manual stop file
  if [[ -f "STOP" ]]; then
    echo "STOP file detected. Halting evolution."
    rm -f STOP
    break
  fi

  # Delay between cycles
  sleep "$CYCLE_DELAY"
done

echo "$(date '+%Y-%m-%d %H:%M:%S') | Ω LOOP ENDED" >> "$LOG_FILE"
