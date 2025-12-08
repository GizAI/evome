#!/bin/bash
# Ω Evome - Self-Evolving Agent Controller
# Usage: evome {start|stop|restart|status|log|feed}

EVOME_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$EVOME_DIR"

# Config
MAX_CYCLES=${MAX_CYCLES:-0}
CYCLE_DELAY=${CYCLE_DELAY:-5}
CYCLE_TIMEOUT=${CYCLE_TIMEOUT:-3600}
LOG_FILE="loop.log"
STDERR_LOG="loop.stderr.log"
LOCK_FILE=".loop.lock"

# Agent CLI selection
select_agent_cli() {
  if [[ -n "${AGENT_CLI:-}" ]]; then
    printf '%s\n' "${AGENT_CLI}"
    return 0
  fi
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

get_cycle() {
  grep "^cycle:" state.yaml 2>/dev/null | awk '{print $2}' || echo "0"
}

increment_cycle() {
  local current=$(get_cycle)
  local next=$((current + 1))
  sed -i "s/^cycle: .*/cycle: $next/" state.yaml
  echo $next
}

get_pid() {
  [[ -f "$LOCK_FILE" ]] && cat "$LOCK_FILE" 2>/dev/null
}

is_running() {
  local pid=$(get_pid)
  [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null
}

# Evolution prompt
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

run_agent_once() {
  local exit_code=0

  AGENT_CMD_STR=$(select_agent_cli) || { echo "No agent CLI found"; return 1; }
  read -ra AGENT_CMD <<<"${AGENT_CMD_STR}"

  # Use script to capture all output with proper TTY handling
  # script -q -c "command" /dev/null captures output without needing a real terminal
  if [[ "${AGENT_CMD[0]}" == "codex" ]]; then
    script -q -c "timeout $CYCLE_TIMEOUT ${AGENT_CMD[*]} -C '$(pwd)' '$EVOLUTION_PROMPT'" /dev/null 2>&1 | tee -a "$LOG_FILE"
    exit_code=${PIPESTATUS[0]}
  else
    script -q -c "timeout $CYCLE_TIMEOUT ${AGENT_CMD[*]} -p '$EVOLUTION_PROMPT'" /dev/null 2>&1 | tee -a "$LOG_FILE"
    exit_code=${PIPESTATUS[0]}
  fi

  # Timeout returns 124
  if [[ $exit_code -eq 124 ]]; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') | ⚠️  TIMEOUT after ${CYCLE_TIMEOUT}s" | tee -a "$LOG_FILE"
  fi

  return $exit_code
}

cleanup() {
  echo "$(date '+%Y-%m-%d %H:%M:%S') | 🛑 Signal: $1" | tee -a "$LOG_FILE"
  # Kill child processes (timeout and claude)
  pkill -P $$ 2>/dev/null || true
  rm -f "$LOCK_FILE"
  echo "$(date '+%Y-%m-%d %H:%M:%S') | ✋ Cleanup complete" >> "$LOG_FILE"
  exit 0
}

do_loop() {
  if is_running; then
    echo "ERROR: Already running (PID: $(get_pid))"
    exit 1
  fi
  [[ -f "$LOCK_FILE" ]] && rm -f "$LOCK_FILE"
  echo $$ > "$LOCK_FILE"

  trap "cleanup SIGTERM" SIGTERM
  trap "cleanup SIGINT" SIGINT
  trap "cleanup EXIT" EXIT

  echo "$(date '+%Y-%m-%d %H:%M:%S') | Ω LOOP STARTING (PID: $$)" >> "$LOG_FILE"

  while true; do
    local cycle=$(increment_cycle)
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Ω CYCLE $cycle | $(date '+%Y-%m-%d %H:%M:%S')"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    set +e
    run_agent_once
    local exit_code=$?
    set -e

    if [[ $exit_code -eq 0 ]]; then
      echo "$(date '+%Y-%m-%d %H:%M:%S') | ✅ CYCLE $cycle COMPLETE" >> "$LOG_FILE"
    else
      echo "$(date '+%Y-%m-%d %H:%M:%S') | ❌ CYCLE $cycle ERROR ($exit_code)" >> "$LOG_FILE"
    fi

    [[ $MAX_CYCLES -gt 0 && $cycle -ge $MAX_CYCLES ]] && break
    [[ -f "STOP" ]] && { rm -f STOP; break; }
    sleep "$CYCLE_DELAY"
  done

  echo "$(date '+%Y-%m-%d %H:%M:%S') | 🏁 Ω LOOP ENDED" >> "$LOG_FILE"
}

cmd_start() {
  if is_running; then
    echo "Ω already running (PID: $(get_pid))"
    return 1
  fi
  echo "Starting Ω..."
  nohup "$0" _loop >> "$LOG_FILE" 2>&1 &
  sleep 1
  if is_running; then
    echo "Ω started (PID: $(get_pid))"
  else
    echo "Failed to start"
    return 1
  fi
}

cmd_stop() {
  if ! is_running; then
    echo "Ω not running"
    [[ -f "$LOCK_FILE" ]] && rm -f "$LOCK_FILE"
    return 0
  fi
  local pid=$(get_pid)
  echo "Stopping Ω (PID: $pid)..."
  kill -TERM "$pid" 2>/dev/null
  for i in {1..10}; do
    sleep 0.5
    kill -0 "$pid" 2>/dev/null || { echo "Ω stopped"; return 0; }
  done
  echo "Force killing..."
  kill -9 "$pid" 2>/dev/null || true
  rm -f "$LOCK_FILE"
  echo "Ω stopped"
}

cmd_restart() {
  cmd_stop
  sleep 1
  cmd_start
}

cmd_status() {
  if is_running; then
    local pid=$(get_pid)
    local cycle=$(get_cycle)
    local goal=$(grep "^current_goal:" state.yaml 2>/dev/null | cut -d'"' -f2 | head -c 60)
    echo "Ω RUNNING"
    echo "  PID: $pid"
    echo "  Cycle: $cycle"
    echo "  Goal: $goal"
  else
    echo "Ω STOPPED"
    [[ -f "$LOCK_FILE" ]] && echo "  (stale lock file exists)"
  fi
}

cmd_log() {
  local lines=${1:-50}
  tail -n "$lines" "$LOG_FILE"
}

cmd_feed() {
  local msg="$*"
  if [[ -z "$msg" ]]; then
    echo "Usage: evome feed <message>"
    return 1
  fi
  local filename="feedback/$(date +%s)-manual.md"
  echo -e "# Manual Feedback\n\n**Date**: $(date)\n\n$msg" > "$filename"
  echo "Feedback saved: $filename"
}

# Main
case "${1:-}" in
  start)   cmd_start ;;
  stop)    cmd_stop ;;
  restart) cmd_restart ;;
  status)  cmd_status ;;
  log)     cmd_log "${2:-50}" ;;
  feed)    shift; cmd_feed "$@" ;;
  _loop)   do_loop ;;
  *)
    echo "Usage: evome {start|stop|restart|status|log [n]|feed <msg>}"
    exit 1
    ;;
esac
