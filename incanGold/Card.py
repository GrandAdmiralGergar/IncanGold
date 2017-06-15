'''
Created on May 11, 2017

@author: Gregory
'''

MUMMY = 0
SNAKE = 1
ROCKS = 2
FIRE = 3
SPIDER = 4

class Card():
    '''
    classdocs
    '''
    def __init__(self, type):
        '''
        Constructor
        '''
        self.type = type
        
    def __str__(self):
        return ""
    
class Treasure(Card):
    def __init__(self, value):
        self.type = "TREASURE"
        self.value = value
    def getValue(self):
        return self.value
    def __str__(self):
        return str(self.value)
    
class Hazard(Card):
    def __init__(self, hazardType):
        self.type = "HAZARD"
        self.hazardType = hazardType
        
    def __str__(self):
        if self.hazardType == MUMMY:
            return "M"
        if self.hazardType == FIRE:
            return "F"
        if self.hazardType == ROCKS:
            return "R"
        if self.hazardType == SPIDER:
            return "S"        
        if self.hazardType == SNAKE:
            return "A"