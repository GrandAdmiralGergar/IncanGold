'''
Created on May 20, 2017

@author: Gregory
'''
from incanGold.agent.Agent import Agent
from incanGold.GameState import TURN_BACK, GO_FORWARD

class ChancesOfDyingAgent(Agent):
    '''
    classdocs
    '''


    def __init__(self, threshold=0.15):
        '''
        Constructor
        '''
        super(ChancesOfDyingAgent, self).__init__(threshold)
        self.threshold = threshold
        self.name = "ChancesOfDyingAgent"
    
    def decide(self, gameState):
        '''
        Returns true if the agent goes forward, 
        returns false if the agent turns back
        '''
        if gameState.round().probabilityOfNextCardEndingRound() > self.threshold:
            return TURN_BACK
        else:
            return GO_FORWARD