import time
import math
import operator
import functools
import sys
from Heuristics import Heuristics
from Displayer import Displayer

displayer = Displayer()
timeLimit = 0.2

actionDic = {
    0: "UP",
    1: "DOWN",
    2: "LEFT",
    3: "RIGHT"
}
weights = [
  float(sys.argv[1]),
  float(sys.argv[2]),
  float(sys.argv[3]),
]

class PlayerAIHelper:
  @staticmethod
  def getCurrentTime():
    return time.clock()
  
  @staticmethod
  def getValueOfGrid(grid, printVal = False):
    heuristics = [
      weights[0] * Heuristics.monotonicity(grid),
      weights[1] * Heuristics.mergeability(grid),
      weights[2] * Heuristics.emptiness(grid),
    ]

    return (
      functools.reduce(operator.add, heuristics, 0)
    )

  @staticmethod
  def determineBestMove(grid):
    endTime = PlayerAIHelper.getCurrentTime() + timeLimit 
    depthLimit = 2
    currentMove = 0

    # uncomment the below line to just return random move
    # return PlayerAIHelper.getRandomMove(grid)

    while (PlayerAIHelper.getCurrentTime() < endTime):
      try:
        _, move = PlayerAIHelper.getPlayersBestMove(grid, 0, depthLimit, endTime, -1 * math.inf, math.inf)
        currentMove = move
        depthLimit += 1

      except:
        pass

    return currentMove
  
  @staticmethod
  def throwIfOutOfTime(endTime):
    timeLeft = endTime - PlayerAIHelper.getCurrentTime()

    if (timeLeft <= 0):
      raise Exception("OUT_OF_TIME") # exit out of this we ran out of time while iterative deepening
  
  @staticmethod
  def getComputersBestMove(currentGrid, depth, depthLimit, endTime, alpha, beta):
    cells = currentGrid.getAvailableCells()

    PlayerAIHelper.throwIfOutOfTime(endTime)

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
          endTime,
          alpha,
          beta
        )

        if playersBestScoreGivenChoice < minimalValue: # If true, we found a value lower than the other children (so far), go this route
          minimalValue = playersBestScoreGivenChoice
          minimalMove = move

        beta = min(minimalValue, beta)

        if alpha >= beta:
          break

    return (minimalValue, minimalMove)

  @staticmethod
  def getPlayersBestMove(currentGrid, depth, depthLimit, endTime, alpha, beta):
    moves = currentGrid.getAvailableMoves() # get available moves given currentGrid
 
    PlayerAIHelper.throwIfOutOfTime(endTime)

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
        endTime,
        alpha,
        beta
      )

      if computersBestScoreGivenChoice > maximalValue: # If true, we found a value greater than the other children (so far), go this route
        maximalValue = computersBestScoreGivenChoice
        maximalMove = move
      
      alpha = max(maximalValue, alpha)

      if alpha >= beta:
        break
      
    return (maximalValue, maximalMove)