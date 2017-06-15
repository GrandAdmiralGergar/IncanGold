'''
Created on May 20, 2017

@author: Gregory
'''
from incanGold.agent.Agent import Agent
from incanGold.GameState import TURN_BACK, GO_FORWARD
from random import random

class InverseRiskAgent(Agent):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        super(InverseRiskAgent, self).__init__()
        self.name = "InverseRiskAgent"
    
    def decide(self, gameState):
        '''
        Returns true if the agent goes forward, 
        returns false if the agent turns back
        '''
        if random() < gameState.round().probabilityOfNextCardEndingRound():
            return TURN_BACK
        else:
            return GO_FORWARD