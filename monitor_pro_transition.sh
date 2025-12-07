#!/bin/bash
# Monitor Pro transition progress
watch -n 10 '
echo "=== Ω Pro Transition Monitor ==="
echo ""
echo "Current Cycle: $(grep "^cycle:" state.yaml | cut -d: -f2)"
echo "Current Goal: $(grep "^current_goal:" state.yaml | cut -d: -f2-)"
echo ""
echo "Pending Feedbacks:"
ls -1 feedback/*.md 2>/dev/null | grep -E "009|010|011" | wc -l
echo ""
echo "Latest Loop Activity:"
tail -5 loop.log | grep -E "CYCLE|feedback|Pro"
'
