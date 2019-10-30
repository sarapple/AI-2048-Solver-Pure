from random import randint
from BaseAI import BaseAI
from PlayerAIHelper import PlayerAIHelper

class PlayerAI(BaseAI):
  def getMove(self, grid):
    return PlayerAIHelper.determineBestMove(grid)
