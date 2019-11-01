import functools
import operator
import math

class Heuristics:
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

  @staticmethod
  def preferHighMaxValue(grid):
    totalPoints, _ = Heuristics.getPointValueOfTiles(grid)
    return grid.getMaxTile() / totalPoints

  
  @staticmethod
  def preferHighValues(grid):
    occupiedTiles = 0
    maxTile = grid.getMaxTile()
    tileValues = []

    for x in range(0, 4):
      for y in range(0, 4):
        tileValue = grid.getCellValue((x, y))
        if (tileValue > 0):
          occupiedTiles = occupiedTiles + 1
          tileValues.append(tileValue)

    return functools.reduce(operator.add, tileValues, 0) / (maxTile * occupiedTiles)

  @staticmethod
  def emptiness(grid):
    emptyCells = len(grid.getAvailableCells())
    return emptyCells / 15

  @staticmethod
  def getMean(items):
    if (len(items) == 0): return 0

    return functools.reduce(operator.add, items, 0) / len(items)

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
  def monotonicity(grid):
    changeAcrossColumns = 0
    changeAcrossRows = 0
    counterSame = 0
    counterChange = 0

    # vertical
    for y in range(0, 4):
      counter = Heuristics.getMonotinicityCounter(grid, (None, y))
      changeAcrossColumns += counter["up"]
      changeAcrossColumns -= counter["down"]
      counterSame += counter["same"]
      counterChange += counter["up"] + counter["down"] + counter["same"]

    # horizontal
    for x in range(0, 4):
      counter = Heuristics.getMonotinicityCounter(grid, (x, None))
      changeAcrossRows += counter["up"]
      changeAcrossRows -= counter["down"]
      counterSame += counter["same"]
      counterChange += counter["up"] + counter["down"] + counter["same"]

    totalY = abs(changeAcrossColumns)
    totalX = abs(changeAcrossRows)

    return (totalY + totalX + counterSame) / counterChange

  @staticmethod
  def smoothness(grid):
    allStdDev = []
    for y in range(0, 4):
      for x in range(0, 4):
        tileValue = grid.getCellValue((x, y))
        if (tileValue == None): tileValue = 0
        squaredDiffs = []

        for neighbor in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
          x, y = neighbor
          if (x >= 0 and x <= 3 and y >= 0 and y <= 3):
            neighborValue = grid.getCellValue(neighbor)
            if (neighborValue == None): neighborValue = 0
            diff = tileValue - neighborValue
            squaredDiffs.append(diff * diff)

        meanOfSquaredDiffs = Heuristics.getMean(squaredDiffs)
        stdDev = math.sqrt(meanOfSquaredDiffs)
        allStdDev.append(stdDev)

    meanOfAllStdDev = Heuristics.getMean(allStdDev)
  
    # invert to lower stddev is better
    return 1 / (meanOfAllStdDev if meanOfAllStdDev > 0 else 1)
  