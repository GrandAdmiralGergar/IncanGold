'''
Created on May 11, 2017

@author: Gregory
'''
from incanGold.Round import Round
import logging
logger = logging.getLogger(__name__)

TURN_BACK = False
GO_FORWARD = True
ROUNDS_IN_GAME = 5

class GameState():
    '''
    Tracks the state of the game by containing each of the (up to) five played
    rounds and the scores of each agent up to this point. Is copied and passed
    to each agent for decision making
    '''


    def __init__(self, playerCount):
        '''
        Constructor
        '''
        self.playerCount = playerCount
        self.treasureValues = [0] * playerCount
        self.currentRound = 0
        self.rounds = []
        for i in range(0, ROUNDS_IN_GAME):
            self.rounds.append(Round(i, playerCount))
    
    def setRound(self, roundNumber):
        self.currentRound = roundNumber
        return self.round()
    
    def round(self):
        return self.rounds[self.currentRound]
    
    def awardTreasure(self, round):
        for i in range(0, self.playerCount):
            self.treasureValues[i] += self.rounds[round].roundTreasureValues[i]