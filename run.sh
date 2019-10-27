#!/bin/bash

timestamp=$(date +"%Y-%m-%dT%H:%M:%S")
echo "[GAMES START]"

# Set up the log folder for given timestamp
timestamp_dir="./logs/$timestamp"
mkdir $timestamp_dir

FILES="game_01.log
game_02.log"

# Run the games in a loop and output the log file of every game
for f in $FILES
do
  { { python3 ./src/GameManager.py; echo "$f Done"; } & } 2>/dev/null 1>"./logs/$timestamp/$f"
done

wait

echo "[GAMES COMPLETE]"

# Display scores
for f in $FILES
do
  echo "Score for $f"
  grep "\[MAX TILE\]" "./logs/$timestamp/$f"
done
