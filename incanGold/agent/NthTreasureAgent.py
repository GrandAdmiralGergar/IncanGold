'''
Created on May 20, 2017

@author: Gregory
'''
from incanGold.agent.Agent import Agent
from incanGold.GameState import TURN_BACK, GO_FORWARD

class NthTreasureAgent(Agent):
    '''
    classdocs
    '''


    def __init__(self, treasureCards):
        '''
        Constructor
        '''
        super(NthTreasureAgent, self).__init__(treasureCards)
        self.treasureCards = treasureCards
        self.name = "NthTreasureAgent"
    
    def decide(self, gameState):
        '''
        Returns true if the agent goes forward, 
        returns false if the agent turns back
        '''
        if 15 - gameState.round().deck.treasureCardsLeft() >= self.treasureCards:
            return TURN_BACK
        else:
            return GO_FORWARD