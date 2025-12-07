#!/bin/bash
# Continuous monitoring - updates every 15 seconds

cd /home/user/evome

echo "Starting Ω Evolution Monitor..."
echo "Monitoring 20 cycles in background"
echo "Press Ctrl+C to stop monitoring (loop continues)"
echo ""

while true; do
    ./progress_snapshot.sh
    echo ""
    echo "Next update in 15 seconds..."
    sleep 15
    clear
done
