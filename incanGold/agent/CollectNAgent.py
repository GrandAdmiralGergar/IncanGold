'''
Created on May 20, 2017

@author: Gregory
'''
from incanGold.agent.Agent import Agent
from incanGold.GameState import TURN_BACK, GO_FORWARD

class CollectNAgent(Agent):
    '''
    classdocs
    '''


    def __init__(self, minRoundValue):
        '''
        Constructor
        '''
        super(CollectNAgent, self).__init__(minRoundValue)
        self.minRoundValue = minRoundValue
        self.name = "CollectNAgent"
    
    def decide(self, gameState):
        '''
        Returns true if the agent goes forward, 
        returns false if the agent turns back
        '''
        if gameState.round().roundTreasureValues[self.player_id] >= self.minRoundValue:
            return TURN_BACK
        else:
            return GO_FORWARD