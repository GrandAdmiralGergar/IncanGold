'''
Created on May 21, 2017

@author: Gregory
'''
from incanGold.agent.Agent import Agent
from random import shuffle, choice
from copy import copy

class AgentPool(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.agents = []
    def addAgentProfile(self, agent):
        for a in self.agents:
            if agent.equals(a):
                return            
        agent.profile_id = len(self.agents)
        self.agents.append(agent)
    
    def getNAgents(self, n):
        pool = copy(self.agents)
        shuffle(pool)
        while n > len(pool):
            pool.append(choice(pool))
        return pool[:n]