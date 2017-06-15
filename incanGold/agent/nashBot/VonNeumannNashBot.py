'''
Created on May 14, 2017

@author: Gregory
'''
from incanGold.agent.nashBot.NashBot import NashBot
from incanGold.GameState import GO_FORWARD, TURN_BACK
from scipy.optimize.zeros import newton
from incanGold.agent.nashBot.NashBot import approximation, pascalsTriangle

class VonNeumannNashBot(NashBot, object):
    '''
    classdocs
    '''


    def __init__(self, adjustment=1.0):
        '''
        Constructor
        '''
        super(VonNeumannNashBot, self).__init__()
        self.param1 = adjustment
        self.name = "VonNeumannNashBot"
        self.adjustment = adjustment
        
    def utility(self, x):
        return pow(x, self.adjustment)
    
    
    def decide(self, gameState):
        forwardValues = []
        backwardValues = []
        
        # This is effectively building the symmetric payout matrix between all 
        # of the players. It assumes all agents behave rationally with the goal 
        # of maximizing their total treasure (not necessarily minimizing their
        # own place amongst all the agents)
        value = self.expectedValueOfDeck(gameState.round())
        for i in range(0, len(gameState.round().remainingPlayers)):
            forwardValues.append(self.expectedValuesOfGoingForward(gameState.round(), value, len(gameState.round().remainingPlayers)-i, i))
            backwardValues.append(self.expectedValuesOfGoingBack(gameState.round(), len(gameState.round().remainingPlayers)-i-1, i+1))
        
        try:
            p = newton(approximation, 0.5, fprime=None, args=(forwardValues, backwardValues), tol=1.0e-05, maxiter=2000)
            q = 1.0-p
            
            #Shortcuts for dominant strategies
            if p > 1.0:
                return GO_FORWARD
            if p < 0:
                return TURN_BACK
            
            #For this bot we have a slightly different valuation on the utility of the outcomes
            adjustedForwardValues = map(self.utility, forwardValues)
            adjustedBackwardValues = map(self.utility, backwardValues)
            
            adjustedExpectedForwardValue = 0.0
            adjustedExpectedBackwardValue = 0.0
            players = len(gameState.round().remainingPlayers)
            binomials = pascalsTriangle(players)
            for j in range(0, players):
                adjustedExpectedForwardValue  += binomials[j] * adjustedForwardValues[j] * pow(p, players-j-1) * pow(q, j)
                adjustedExpectedBackwardValue += binomials[j] * adjustedBackwardValues[j] * pow(p, players-j-1) * pow(q, j)
            
        except:
            adjustedExpectedForwardValue = sum(forwardValues)
            adjustedExpectedBackwardValue = sum(backwardValues)
        
        # Now we simply see which option is better
        if adjustedExpectedForwardValue > adjustedExpectedBackwardValue:
            return GO_FORWARD
        else:
            return TURN_BACK