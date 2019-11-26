import time
import math
import operator
import functools
import sys
from random import randint

from Displayer import Displayer

displayer = Displayer()
timeLimit = 0.15

actionDic = {
    0: "UP",
    1: "DOWN",
    2: "LEFT",
    3: "RIGHT"
}

class HeuristicsHelper:
  @staticmethod
  def getNeighborInDirection(grid, startPos, move):
    xNeighbor, yNeighbor = startPos

    if actionDic[move] == "UP":
      xNeighbor -= 1
    elif actionDic[move] == "DOWN":
      xNeighbor += 1
    elif actionDic[move] == "LEFT":
      yNeighbor -= 1
    elif actionDic[move] == "RIGHT":
      yNeighbor += 1

    if (xNeighbor >= 0 and xNeighbor <= 3 and yNeighbor >= 0 and yNeighbor <= 3):
      neighborValue = grid.getCellValue((xNeighbor, yNeighbor))

      if (neighborValue != None and neighborValue > 0):
        return (neighborValue, (xNeighbor, yNeighbor))

    return (None, None)

  @staticmethod
  def getMonotinicityCounter(grid, pos):
    x, y = pos # One of these should be None
    runner = 0
    counter = {
      "up": 0,
      "down": 0,
      "same": 0
    }
    prevTileValue = 0

    while (runner < 4):
      currentPos = (x, runner) if y == None else (runner, y)
      currentTileValue = grid.getCellValue(currentPos)
      if (currentTileValue <= 0):
        pass # blank, keep moving
      else:
        if (prevTileValue > 0): # compare with a previous one if already set
          if (prevTileValue < currentTileValue): # number is increasing
            counter["up"] += math.log2(currentTileValue) - math.log2(prevTileValue)
          elif (prevTileValue > currentTileValue): # number is decreasing
            counter["down"] += math.log2(prevTileValue) - math.log2(currentTileValue)
          else:
            counter["same"] += 1
          
        prevTileValue = currentTileValue
      runner += 1
    
    return counter

  @staticmethod
  def getMean(items):
    if (len(items) == 0): return 0

    return functools.reduce(operator.add, items, 0) / len(items)

  @staticmethod
  def getPointValueOfTiles(grid):
    totalPointValue = 0
    occupiedCells = 0

    for x in range(0, 4):
      for y in range(0, 4):
        tileValue = grid.getCellValue((x, y))
        if (tileValue > 0):
          occupiedCells += 1
          totalPointValue = totalPointValue + tileValue
    
    return (totalPointValue, occupiedCells)
