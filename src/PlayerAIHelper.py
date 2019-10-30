import time
import math
import operator
import functools
import sys
from random import randint

from Heuristics import Heuristics
from Displayer import Displayer

displayer = Displayer()
timeLimit = 0.15

class PlayerAIHelper:
  @staticmethod
  def getWeights():
    return [
      float(sys.argv[1]),
      float(sys.argv[2]),
      float(sys.argv[3]),
      float(sys.argv[4]),
      float(sys.argv[5]),
    ]

  @staticmethod
  def getCurrentTime():
    return time.clock()
  
  @staticmethod
  def getRandomMove(grid):
    moves = grid.getAvailableMoves()
    return moves[randint(0, len(moves) - 1)] if moves else None

  @staticmethod
  def getValueOfGrid(grid):
    weights = PlayerAIHelper.getWeights()

    heuristics = [
      weights[0] * Heuristics.monotonicity(grid),
      weights[1] * Heuristics.smoothness(grid),
      weights[2] * Heuristics.emptiness(grid),
      weights[3] * Heuristics.preferHighValues(grid),
      weights[4] * Heuristics.preferHighMaxValue(grid),
    ]

    return (
      functools.reduce(operator.add, heuristics, 0)
    )

  @staticmethod
  def determineBestMove(grid):
    startTime = PlayerAIHelper.getCurrentTime()
    depthLimit = 1
    timeLeft = timeLimit
    currentMove = 0

    # uncomment the below line to just return random move
    # return PlayerAIHelper.getRandomMove(grid)

    while (timeLeft > 0):
      try:
        _, move = PlayerAIHelper.getPlayersBestMove(grid, 0, depthLimit, timeLeft)
        currentMove = move
        depthLimit += 1
        timeLeft = timeLimit - (Helpers.getCurrentTime() - startTime) 

      except:
        timeLeft = 0

    return currentMove
  
  @staticmethod
  def throwIfOutOfTime(timeLeft):
    if (timeLeft <= 0):
      raise Exception("OUT_OF_TIME") # exit out of this we ran out of time while iterative deepening
  
  @staticmethod
  def getComputersBestMove(currentGrid, depth, depthLimit, timeLeft):
    startTime = PlayerAIHelper.getCurrentTime()
    cells = currentGrid.getAvailableCells()

    PlayerAIHelper.throwIfOutOfTime(timeLeft)

    if len(cells) == 0 or depth >= depthLimit:
      return (PlayerAIHelper.getValueOfGrid(currentGrid), None)

    minimalValue = math.inf # Track the lowest value (some number of the children will be lower than this)
    minimalMove = cells[0]

    for move in cells:
      for tileValue in [2, 4]:
        gridCopy = currentGrid.clone()
        gridCopy.insertTile(move, tileValue)

        playersBestScoreGivenChoice, _ = PlayerAIHelper.getPlayersBestMove(
          gridCopy,
          depth + 1,
          depthLimit,
          timeLeft - (PlayerAIHelper.getCurrentTime() - startTime),
        )

        if playersBestScoreGivenChoice < minimalValue: # If true, we found a value lower than the other children (so far), go this route
          minimalValue = playersBestScoreGivenChoice
          minimalMove = move

    return (minimalValue, minimalMove)

  @staticmethod
  def getPlayersBestMove(currentGrid, depth, depthLimit, timeLeft):
    startTime = PlayerAIHelper.getCurrentTime()
    moves = currentGrid.getAvailableMoves() # get available moves given currentGrid

    PlayerAIHelper.throwIfOutOfTime(timeLeft)

    if len(moves) == 0 or depth >= depthLimit:
      return (PlayerAIHelper.getValueOfGrid(currentGrid), None)

    maximalValue = -math.inf # Track the highest value of the minimums provided by the children
    maximalMove = None

    for move in moves:
      gridCopy = currentGrid.clone()
      gridCopy.move(move)

      computersBestScoreGivenChoice, _ = PlayerAIHelper.getComputersBestMove(
        gridCopy,
        depth + 1,
        depthLimit,
        timeLeft - (PlayerAIHelper.getCurrentTime() - startTime),
      )

      if computersBestScoreGivenChoice > maximalValue: # If true, we found a value greater than the other children (so far), go this route
        maximalValue = computersBestScoreGivenChoice
        maximalMove = move

    return (maximalValue, maximalMove)