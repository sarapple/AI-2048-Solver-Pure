#!/bin/bash

timestamp=$(date +"%Y-%m-%dT%H:%M:%S")
echo "[GAMES START]"

# Set up the log folder for given timestamp
timestamp_dir="./logs/$timestamp"
mkdir $timestamp_dir

FILES="game_01.log
game_02.log"

declare -a StringArray=(
  "1 1 1 0 0"
)

# Run the games in a loop and output the log file of every game
for c in "${StringArray[@]}"
do
  weights_no_spaces=${c// /-} 
  weight_dir="$timestamp_dir/$weights_no_spaces"
  mkdir $weight_dir

  for f in $FILES
  do
    { { python3 ./src/GameManager.py $c; echo "$f Done"; } & } 2>/dev/null 1>"$weight_dir/$f"
  done

  wait

  echo "Weights: [$c]"

  for f in $FILES
  do
    echo "Score for file: [$f]"
    grep "\[MAX TILE\]" "$weight_dir/$f"
  done 
done

wait
echo "[GAMES COMPLETE]"
