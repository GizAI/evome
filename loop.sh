#!/bin/bash
# Ω Eternal Loop - Self-Evolving Agent
# This script calls Claude recursively, forever.

set -e
cd "$(dirname "$0")"

# Config
MAX_CYCLES=${MAX_CYCLES:-0}  # 0 = infinite
CYCLE_DELAY=${CYCLE_DELAY:-5}  # seconds between cycles
CYCLE_TIMEOUT=${CYCLE_TIMEOUT:-3600}  # 1 hour timeout per cycle
LOG_FILE="loop.log"
STDERR_LOG="loop.stderr.log"
AGENT_CHOICE="${AGENT:-${1:-}}"  # optional: set AGENT=claude or AGENT=codex or pass as first arg
AGENT_PID=""

# Agent CLI selection (supports claude or codex)
select_agent_cli() {
  # Allow explicit override via environment
  # Highest priority: explicit override
  if [[ -n "${AGENT_CLI:-}" ]]; then
    read -ra cmd <<<"${AGENT_CLI}"
    printf '%s\n' "${cmd[*]}"
    return 0
  fi

  # Next: explicit choice via AGENT env or first arg
  if [[ -n "${AGENT_CHOICE:-}" ]]; then
    case "${AGENT_CHOICE,,}" in
      claude)
        printf '%s\n' "claude --dangerously-skip-permissions"
        return 0
        ;;
      codex)
        printf '%s\n' "codex exec --skip-git-repo-check --dangerously-bypass-approvals-and-sandbox --sandbox danger-full-access"
        return 0
        ;;
    esac
  fi

  # Auto-detect
  if command -v claude >/dev/null 2>&1; then
    printf '%s\n' "claude --dangerously-skip-permissions"
    return 0
  fi

  if command -v codex >/dev/null 2>&1; then
    printf '%s\n' "codex exec --skip-git-repo-check --dangerously-bypass-approvals-and-sandbox --sandbox danger-full-access"
    return 0
  fi

  return 1
}

AGENT_CMD_STR=$(select_agent_cli) || { echo "No supported agent CLI found (claude or codex)."; exit 1; }
read -ra AGENT_CMD <<<"${AGENT_CMD_STR}"

run_agent_once() {
  local temp_stdout=$(mktemp)
  local temp_stderr=$(mktemp)
  local exit_code=0

  # Start agent process in background to monitor it
  if [[ "${AGENT_CMD[0]}" == "codex" ]]; then
    "${AGENT_CMD[@]}" -C "$(pwd)" "$EVOLUTION_PROMPT" > "$temp_stdout" 2> "$temp_stderr" &
  else
    "${AGENT_CMD[@]}" -p "$EVOLUTION_PROMPT" > "$temp_stdout" 2> "$temp_stderr" &
  fi

  AGENT_PID=$!
  local start_time=$(date +%s)

  # Monitor process with timeout
  while kill -0 $AGENT_PID 2>/dev/null; do
    local current_time=$(date +%s)
    local elapsed=$((current_time - start_time))

    # Check for timeout
    if [[ $elapsed -gt $CYCLE_TIMEOUT ]]; then
      echo "$(date '+%Y-%m-%d %H:%M:%S') | ⚠️  CYCLE TIMEOUT (${elapsed}s > ${CYCLE_TIMEOUT}s) - killing PID $AGENT_PID" | tee -a "$LOG_FILE"
      kill -9 $AGENT_PID 2>/dev/null || true
      sleep 1
      break
    fi

    # Stream stdout/stderr in real-time (non-blocking tail)
    if [[ -f "$temp_stdout" ]]; then
      tail -n +1 "$temp_stdout" 2>/dev/null | while IFS= read -r line; do
        echo "$line" | tee -a "$LOG_FILE"
      done
    fi

    sleep 0.5
  done

  # Wait for process to finish (or be killed)
  wait $AGENT_PID 2>/dev/null
  exit_code=$?

  # Append any remaining output
  if [[ -f "$temp_stdout" ]]; then
    cat "$temp_stdout" >> "$LOG_FILE" 2>/dev/null
  fi

  if [[ -f "$temp_stderr" ]]; then
    cat "$temp_stderr" >> "$STDERR_LOG" 2>/dev/null
  fi

  # Cleanup
  rm -f "$temp_stdout" "$temp_stderr"

  return $exit_code
}

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

1. **PRIORITY: Check feedback/ directory FIRST** - human messages override all other goals
2. Read state.yaml, metrics.yaml, mutations.log, errors.log
3. Analyze: What is your current goal? What progress was made?
4. Act: Take ONE concrete action toward your goal
5. Mutate: If you learned something, update CLAUDE.md or create a tool
6. Persist: Update state.yaml with next_action and any state changes
7. End: Your final line must be "Ω CYCLE COMPLETE" or "Ω ERROR: <reason>"

## Rules
- One action per cycle (bias toward small steps)
- Always update state.yaml before ending
- If stuck, try something different
- Log mutations to mutations.log
- Create tools in tools/ for reusable operations

Begin.'

# Cleanup function
cleanup() {
  local signal=$1
  echo "$(date '+%Y-%m-%d %H:%M:%S') | 🛑 Received signal: $signal" | tee -a "$LOG_FILE"

  # Kill any running agent
  if [[ -n "$AGENT_PID" ]] && kill -0 $AGENT_PID 2>/dev/null; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') | Killing agent process: $AGENT_PID" | tee -a "$LOG_FILE"
    kill -9 $AGENT_PID 2>/dev/null || true
    sleep 1
  fi

  # Remove lock file
  rm -f "$LOCK_FILE" "$LOCK_FILE.pid"

  echo "$(date '+%Y-%m-%d %H:%M:%S') | ✋ Loop cleanup complete" >> "$LOG_FILE"
  exit 0
}

# Prevent concurrent execution
LOCK_FILE=".loop.lock"
if [[ -f "$LOCK_FILE" ]]; then
  existing_pid=$(cat "$LOCK_FILE" 2>/dev/null)
  if [[ -n "$existing_pid" ]] && kill -0 "$existing_pid" 2>/dev/null; then
    echo "ERROR: Loop already running (PID: $existing_pid)"
    echo "If this is stale, remove $LOCK_FILE manually"
    exit 1
  fi
  echo "Removing stale lock file"
  rm -f "$LOCK_FILE"
fi
echo $$ > "$LOCK_FILE"

# Setup signal handlers
trap "cleanup SIGTERM" SIGTERM
trap "cleanup SIGINT" SIGINT
trap "cleanup EXIT" EXIT

# Main loop
echo "$(date '+%Y-%m-%d %H:%M:%S') | Ω LOOP STARTING (PID: $$)" >> "$LOG_FILE"
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
  set +e  # Disable set -e for this section to handle exit codes properly
  run_agent_once
  cycle_exit_code=$?
  set -e

  if [[ $cycle_exit_code -eq 0 ]]; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') | ✅ CYCLE $cycle COMPLETE" >> "$LOG_FILE"
  elif [[ $cycle_exit_code -eq 124 ]]; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') | ⏱️  CYCLE $cycle TIMEOUT (exit code 124)" >> "$LOG_FILE"
    echo "[$(get_cycle)] $(date -Iseconds) | CYCLE_TIMEOUT | Cycle exceeded ${CYCLE_TIMEOUT}s, agent killed" >> errors.log
  else
    echo "$(date '+%Y-%m-%d %H:%M:%S') | ❌ CYCLE $cycle ERROR (exit code: $cycle_exit_code)" >> "$LOG_FILE"
    echo "[$(get_cycle)] $(date -Iseconds) | CYCLE_ERROR | Claude exited with code $cycle_exit_code" >> errors.log
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

echo "$(date '+%Y-%m-%d %H:%M:%S') | 🏁 Ω LOOP ENDED (normal termination)" >> "$LOG_FILE"
