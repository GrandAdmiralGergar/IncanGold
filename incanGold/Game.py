'''
Created on May 11, 2017

@author: Gregory
'''
from incanGold.GameState import GameState, TURN_BACK, ROUNDS_IN_GAME
import copy
import logging
from random import randint, choice, shuffle

logger = logging.getLogger(__name__)

MIN_PLAYERS = 3
MAX_PLAYERS = 7

class Game():
    '''
    classdocs
    '''
    def __init__(self, id, agentPool):
        '''
        Constructor
        '''
        logger.info("Creating game...")
        self.id = id
        self.round = 0
        self.playerCount = randint(MIN_PLAYERS,MAX_PLAYERS)
        self.players = self.players = agentPool.getNAgents(self.playerCount)
        self.gameState = GameState(len(self.players))
    
    def simulateRound(self, roundNumber):
        round = self.gameState.setRound(roundNumber)

        round.draw()        
        while not round.isRoundFinished():
            decisions = []
            
            #Make each agent decide to go forward or turn back
            #This list comprehension gets all of the agents still in this round
            for i in range(0, len(self.players)):
                decision = None                
                if i in round.remainingPlayers:
                    decision = self.players[i].decide(copy.deepcopy(self.gameState))                
                    if decision == None:
                        decision = TURN_BACK
                
                decisions.append(decision)
            
            #Determine number of retreaters, and determine rewards
            retreaters = [i for i in range(len(decisions)) if decisions[i] == TURN_BACK]
            round.turnBack(retreaters)
            
            round.draw()
        
        logger.info("\n" + round.roundSummary())
        logger.info("Total treasure available in round: " + str(round.maxRoundTreasureAvailable()))
        
    def run(self):
        logger.info("Running game...")
        for i in range(0, ROUNDS_IN_GAME):
            logger.info("Round " + str(i))
            self.simulateRound(i)
            self.gameState.awardTreasure(i)
            logger.info("Round " + str(i) + " over. Scores are: ")
            for i in range(0, len(self.players)):
                logger.info("Player " + str(i) + ": " + str(self.gameState.treasureValues[i]))
        
        #Determine place values for all the players for archiving
        values = {}
        self.places = []
        for i in range(0, self.playerCount):
            values[i] = self.gameState.treasureValues[i]

        while len(values.keys()) != 0:
            m = max(values.values())
            for key, value in values.iteritems():
                if m == value:
                    self.places.append(key)
                    values.pop(key)
                    break
                
    def winner(self):
        return self.places[0]
    
    def treasureCollectedInGame(self):
        return sum(self.gameState.treasureValues)
    
    def treasureAvailableInGame(self):
        treasure = 0
        for r in self.gameState.rounds:
            treasure += r.maxRoundTreasureAvailable()
        
        return treasure