import functools
import operator
import math
from Displayer import Displayer
from HeuristicsHelper import HeuristicsHelper

displayer = Displayer()

class Heuristics:
  @staticmethod
  def emptiness(grid):
    emptyCells = len(grid.getAvailableCells())
    return emptyCells / 15

  @staticmethod
  def monotonicity(grid):
    changeAcrossColumns = 0
    changeAcrossRows = 0
    counterNoChange = 0
    counterChange = 0

    # vertical
    for y in range(0, 4):
      counter = HeuristicsHelper.getMonotinicityCounter(grid, (None, y))
      changeAcrossColumns += counter["up"]
      changeAcrossColumns -= counter["down"]
      counterNoChange += counter["same"]
      counterChange += counter["up"] + counter["down"] + counter["same"]

    # horizontal
    for x in range(0, 4):
      counter = HeuristicsHelper.getMonotinicityCounter(grid, (x, None))
      changeAcrossRows += counter["up"]
      changeAcrossRows -= counter["down"]
      counterNoChange += counter["same"]
      counterChange += counter["up"] + counter["down"] + counter["same"]

    return (abs(changeAcrossColumns) + abs(changeAcrossRows) + counterNoChange) / counterChange

  @staticmethod
  def mergeability(grid):
    mergeableTiles = 0
    comparisons = 0
    for y in range(0, 4):
      for x in range(0, 4):
        tileValue = grid.getCellValue((x, y))
        if (tileValue > 0): 
          for move in range(0, 4):
            neighborValue, _ = HeuristicsHelper.getNeighborInDirection(grid, (x, y), move)

            if (neighborValue != None):
              comparisons += 1
              diff = tileValue - neighborValue
              if (diff == 0):
                mergeableTiles += 1
    
    return mergeableTiles / comparisons if (comparisons > 0) else 0
