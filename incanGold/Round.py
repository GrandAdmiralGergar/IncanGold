'''
Created on May 20, 2017

@author: Gregory
'''

from incanGold.Deck import Deck
from incanGold.Card import MUMMY, FIRE, ROCKS, SPIDER, SNAKE, Card, Treasure, Hazard

import logging
logger = logging.getLogger(__name__)

class Round(object):
    '''
    classdocs
    '''


    def __init__(self, roundNumber, playerCount):
        '''
        Constructor
        '''
        self.playerCount = playerCount
        self.initRound(roundNumber)
        
    def initRound(self, roundNumber):
        self.round = roundNumber
        
        self.deck = Deck()
        
        self.remainingPlayers = range(0, self.playerCount)
        self.roundTreasureValues = [0] * self.playerCount
        self.leftoverTreasure = 0
        
        self.hazardsRevealed = {}
        self.hazardsRevealed[MUMMY] = 0
        self.hazardsRevealed[SNAKE] = 0
        self.hazardsRevealed[ROCKS] = 0
        self.hazardsRevealed[FIRE] = 0
        self.hazardsRevealed[SPIDER] = 0
        
        self.cardsDrawn = []
        self.playerEndTime = [0] * self.playerCount
    
    
    def turnBack(self, retreaters):
        if len(retreaters) <= 0:
            return
        
        treasureSplit = self.leftoverTreasure / len(retreaters)
        self.leftoverTreasure = self.leftoverTreasure % len(retreaters)
        for r in retreaters:
            self.remainingPlayers.remove(r)
            self.playerEndTime[r] = len(self.cardsDrawn)
            self.roundTreasureValues[r] += treasureSplit
    
    def draw(self):
        '''
        Draws a card from the deck and updates the state based on whether it is
        a treasure or a hazard
        '''
        card = self.deck.drawCard()
        
        if isinstance(card, Treasure) and len(self.remainingPlayers) > 0:
            #Award treasure to players
            self.leftoverTreasure += card.value % len(self.remainingPlayers)
            for p in self.remainingPlayers:
                self.roundTreasureValues[p] += card.value / len(self.remainingPlayers)
        elif isinstance(card, Hazard):
            #Update the hazard count
            self.hazardsRevealed[card.hazardType] += 1
        
        self.cardsDrawn.append(card)
    
    def probabilityOfNextCardEndingRound(self):
        '''
        Quick check for odds of the next card killing the round
        '''
        p = 0.0
        for k in self.hazardsRevealed.keys():
            if self.hazardsRevealed[k] == 1:
                p += 2.0 / self.deck.cardsLeft()
        return p
    
    def twoHazardsReached(self):
        '''
        Shortcut function for determining if enough hazards have happened to 
        warrant an end to the round
        '''
        for h in self.hazardsRevealed.keys():
            if self.hazardsRevealed[h] >= 2:
                for p in self.remainingPlayers:
                    self.playerEndTime[p] = len(self.cardsDrawn)
                    self.roundTreasureValues[p] = 0
                return True
        return False
    
    def isRoundFinished(self):
        '''
        Determines whether the round should be over or not
        '''
        return self.twoHazardsReached()
            
    def maxRoundTreasureAvailable(self):
        if self.twoHazardsReached():
            drawn = Deck(self.cardsDrawn)
            return drawn.treasureLeft()
        
        logger.error("Called max round treasure available before round end!")
        return None
    
    def roundTreasureCollected(self):
        return sum(self.roundTreasureValues)
    
    def roundSummary(self):
        retString = "Cards \t"
        for card in self.cardsDrawn:
            retString += str(card) + "\t"
        retString += "\n"
        for i in range(0, self.playerCount):
            retString += "P" + str(i) + "\t"
            for j in range(0, len(self.cardsDrawn)):
                if self.playerEndTime[i]-1 == j:
                    retString += str(self.roundTreasureValues[i])
                retString += "\t"
            retString += "\n"
        return retString
