'''
Created on May 11, 2017

@author: Gregory
'''
from incanGold.Card import Treasure, Hazard, MUMMY, FIRE, ROCKS, SPIDER, SNAKE
import random
import logging

logger = logging.getLogger(__name__)

CARDS_PER_HAZARD = 3
HAZARD_COUNT = 5
STARTING_DECK_SIZE = 30

class Deck():
    '''
    Represents a deck of Incan Gold cards, and initializes to the full set of 
    30 cards used for a single round of the game. As cards are drawn from the 
    deck, they are removed from the internal storage, so the entire deck needs
    to be reconstructed every round
    '''


    def __init__(self, cards = []):
        '''
        Constructor
        '''
        if len(cards) == 0:
            self.reset()
        else:
            self.cards = cards
        
    def reset(self):
        self.cards = []
        self.cards.append(Treasure(1))
        self.cards.append(Treasure(2))
        self.cards.append(Treasure(3))
        self.cards.append(Treasure(4))
        self.cards.append(Treasure(5))
        self.cards.append(Treasure(5))
        self.cards.append(Treasure(7))
        self.cards.append(Treasure(7))
        self.cards.append(Treasure(9))
        self.cards.append(Treasure(11))
        self.cards.append(Treasure(11))
        self.cards.append(Treasure(13))
        self.cards.append(Treasure(14))
        self.cards.append(Treasure(15))
        self.cards.append(Treasure(17))
        self.cards.append(Hazard(MUMMY))
        self.cards.append(Hazard(MUMMY))
        self.cards.append(Hazard(MUMMY))
        self.cards.append(Hazard(SNAKE))
        self.cards.append(Hazard(SNAKE))
        self.cards.append(Hazard(SNAKE))
        self.cards.append(Hazard(ROCKS))
        self.cards.append(Hazard(ROCKS))
        self.cards.append(Hazard(ROCKS))
        self.cards.append(Hazard(FIRE))
        self.cards.append(Hazard(FIRE))
        self.cards.append(Hazard(FIRE))
        self.cards.append(Hazard(SPIDER))
        self.cards.append(Hazard(SPIDER))
        self.cards.append(Hazard(SPIDER))
        random.shuffle(self.cards)
    
    def drawCard(self):
        random.shuffle(self.cards)
        if len(self.cards) > 0:
            return self.cards.pop()
        else:
            return None
    
    def cardsLeft(self):
        return len(self.cards)
    
    def treasureLeft(self):
        sum = 0
        for card in self.cards:
            if isinstance(card, Treasure):
                sum += card.getValue()
        return sum
    
    def treasureCardsLeft(self):
        cards = 0
        for card in self.cards:
            if isinstance(card, Treasure):
                cards += 1
        return cards
    
    def hazardCardsLeft(self):
        return self.cardsLeft() - self.treasureCardsLeft()
    
    def specificHazardCardsLeft(self, hazardType):
        total = 0
        for card in self.cards:
            if isinstance(card, Hazard):
                if card.hazardName.equal(hazardType):
                    total += 1 
        return total
    
    def expectedValueOfNextDraw(self):
        value = 0.0
        for card in self.cards:
            if isinstance(card, Treasure):
                value += card.getValue()
        
        value /= self.cardsLeft()
        return value