#!/bin/bash
# Quick progress snapshot without clearing screen

CYCLE=$(grep "^cycle:" state.yaml 2>/dev/null | awk '{print $2}')
SWE_ATTEMPTED=$(grep "attempted:" external_validation/external_metrics.yaml 2>/dev/null | head -1 | awk '{print $2}')
SWE_PASSED=$(grep "passed:" external_validation/external_metrics.yaml 2>/dev/null | head -1 | awk '{print $2}')
LAST_ACTION=$(tail -1 outcomes.log 2>/dev/null | cut -d'|' -f2 | xargs)

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Ω Cycle $CYCLE | SWE-Bench: $SWE_PASSED/$SWE_ATTEMPTED | Last: $LAST_ACTION"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
tail -3 loop.log 2>/dev/null | grep -E "CYCLE|COMPLETE|ERROR" | tail -1
