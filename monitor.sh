#!/bin/bash
# Real-time monitoring dashboard for Ω evolution

clear
echo "╔════════════════════════════════════════════════════════════╗"
echo "║          Ω EVOLUTION MONITOR - Live Dashboard             ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Function to display metrics
show_metrics() {
    # Current cycle
    CYCLE=$(grep "^cycle:" state.yaml 2>/dev/null | awk '{print $2}' || echo "0")

    # SWE-Bench progress
    SWE_ATTEMPTED=$(grep "attempted:" external_validation/external_metrics.yaml 2>/dev/null | head -1 | awk '{print $2}' || echo "0")
    SWE_PASSED=$(grep "passed:" external_validation/external_metrics.yaml 2>/dev/null | head -1 | awk '{print $2}' || echo "0")

    # Recent outcome
    LAST_OUTCOME=$(tail -1 outcomes.log 2>/dev/null | grep -o 'score: [0-9.]*' | awk '{print $2}' || echo "0")

    # Feedback pending
    FEEDBACK_COUNT=$(ls -1 feedback/*.md 2>/dev/null | grep -v TEMPLATE | wc -l)

    # Tools created
    TOOL_COUNT=$(ls -1 tools/*.py 2>/dev/null | wc -l)

    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📊 CURRENT STATUS"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  Cycle:              $CYCLE"
    echo "  Last Outcome:       $LAST_OUTCOME"
    echo "  Tools:              $TOOL_COUNT"
    echo "  Pending Feedback:   $FEEDBACK_COUNT"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🎯 SWE-BENCH PROGRESS (Target: 80/300)"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  Attempted:          $SWE_ATTEMPTED / 300"
    echo "  Passed:             $SWE_PASSED / 300"

    if [ "$SWE_ATTEMPTED" -gt 0 ]; then
        SUCCESS_RATE=$(awk "BEGIN {printf \"%.1f\", ($SWE_PASSED/$SWE_ATTEMPTED)*100}")
        echo "  Success Rate:       $SUCCESS_RATE%"

        # Progress bar
        PROGRESS=$(awk "BEGIN {printf \"%.0f\", ($SWE_PASSED/80)*100}")
        BARS=$(($PROGRESS / 5))
        printf "  Progress [80]:      ["
        for i in $(seq 1 20); do
            if [ $i -le $BARS ]; then
                printf "█"
            else
                printf "░"
            fi
        done
        printf "] $PROGRESS%%\n"
    else
        echo "  Success Rate:       N/A"
        echo "  Progress [80]:      [░░░░░░░░░░░░░░░░░░░░] 0%"
    fi

    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📝 RECENT ACTIVITY (Last 5 lines)"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    tail -5 loop.log 2>/dev/null | sed 's/^/  /'
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "💡 Press Ctrl+C to exit monitor (loop continues)"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}

# Main loop
while true; do
    show_metrics
    sleep 10
    clear
done
