'''
Created on May 13, 2017

@author: Gregory
'''
from incanGold.agent.Agent import Agent
import random
import logging
from incanGold.GameState import GO_FORWARD, TURN_BACK

logger = logging.getLogger(__name__)

class RandomAgent(Agent):
    '''
    classdocs
    '''

    def __init__(self, weight=0.8):
        '''
        Constructor
        '''
        super(RandomAgent, self).__init__(weight)
        self.weight = weight
        self.name = "RandomAgent"
    
    def decide(self, gameState):
        if random.random() <= self.weight:
            return GO_FORWARD
        else:
            return TURN_BACK