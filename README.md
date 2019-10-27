# Agent to intelligently play 2048


## Author
Sara Wong @sarapple

## Course from edx
ColumbiaX: CSMM.101x
Artificial Intelligence (AI)

## The Task

Create a PlayerAI that will play 2048 as if the computer generating the random block each turn is an adversarial opponent (that is, minimize the PlayerAI's outcome).

The better the PlayerAI performs, the higher the score. 

Rules:
```
Your Player AI will be pitted against the standard Computer AI for a total of 10 games, and the maximum tile value of each game will be recorded. Among the 10 runs, we pick and average top 5 maximum tile values. Based on the average of these 5 maximum tile values, your submission will be assessed out of a total of 100 points.
```

Pre-existing files are provided beforehand to provide a skeleton, that are all read-only. A new file, `PlayerAI.py`, will be created and this will contain the solution. Given the code is run as-is without any added improvements, it will perform no better than if moves are played at random 0/100.  Improvements will be added to the file `PlayerAI.py` with the end goal of helping the Player AI reach a max tile of 2048 (or more) each run of the game. A time limit of 0.2 seconds (in CPU time) should be enforced on the decision making process of the player AI for each move. Helper methods are allowed to be defined in a separate file.

## Pre-existing files (provided)
- Read-only: `GameManager.py`. This is the driver program that loads your Computer AI and Player AI, and begins a game where they compete with each other. See below on how to execute this program.
- Read-only: `Grid.py`. This module defines the Grid object, along with some useful operations: move(), getAvailableCells(), insertTile(), and clone(), which you may use in your code. These are available to get you started, but they are by no means the most efficient methods available. If you wish to strive for better performance, feel free to ignore these and write your own helper methods in a separate file.
- Read-only: `BaseAI.py`. This is the base class for any AI component. All AIs inherit from this module, and implement the getMove() function, which takes a Grid object as parameter and returns a move (there are different "moves" for different AIs).
- Read-only: `ComputerAI.py`. This inherits from BaseAI. The getMove() function returns a computer action that is a tuple (x, y) indicating the place you want to place a tile.
- Read-only: `BaseDisplayer.py` and `Displayer.py`. These print the grid.

## Possible heuristics to consider (provided)
- the absolute value of tiles,
- the difference in value between adjacent tiles,
- the potential for merging of similar tiles,
- the ordering of tiles across rows, columns, and diagonals
- research on existing heuristics is encouraged

## To Run
To run the code, execute the game manager like so:

```python
python3 GameManager.py
```

# Tasks
- Run it, set up env, confirm score of 0/100
- Implement minimax
- Alpha-beta pruning
- Heuristics with weights