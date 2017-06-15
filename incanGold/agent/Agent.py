'''
Created on May 11, 2017

@author: Gregory
'''

class Agent(object):
    '''
    classdocs
    '''

    
    def __init__(self, param1=0, param2=0, param3=0, param4=0):
        '''
        Constructor
        '''
        self.profile_id = 0
        self.player_id = 0
        self.name = ""
        self.param1 = param1
        self.param2 = param2
        self.param3 = param3
        self.param4 = param4
        
    def decide(self, gameState):
        '''
        Returns true if the agent goes forward, 
        returns false if the agent turns back
        '''
        return None
    
    def equals(self, other):
        if isinstance(other, Agent):
            if (self.name == other.name  and 
                self.param1 == other.param1 and  
                self.param2 == other.param2 and  
                self.param3 == other.param3 and
                self.param4 == other.param4):
                return True
        return False