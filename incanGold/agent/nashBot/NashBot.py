'''
Created on May 14, 2017

@author: Gregory
'''
from incanGold.agent.Agent import Agent
from incanGold.Deck import CARDS_PER_HAZARD
from incanGold.GameState import GO_FORWARD, TURN_BACK
import random
from scipy.optimize.zeros import newton

def pascalsTriangle(n):
    if n <= 1:
        return [1]
    line = pascalsTriangle(n-1)
    ret = [1]
    for i in range(0, len(line)-1):
        ret.append(line[i]+line[i+1])
    ret.append(1)
    return ret

def approximation(x, forwardValues, backwardValues):
    '''
    This function takes advantage of the fact that in a 1 to 1 treasure <-> 
    utility valuation, the payout matrices are symmetric across all n 
    dimensions (n = number of players). Thus if we know the values assigned
    for a certain number of players going forward vs staying back, we can
    condense them into n values for this agent going forward and n values
    for this agent going back, multiplied by the binomial expansion for n
    
    This function is passed into a newton approximation function and tries to
    solve for value x such that approximation(x) = 0. This is the crossover point
    where all agents are indifferent to each other's action, and represents the
    value 0 < p < 1 where agents choose to go forward. This p is symmetric for
    all agents as well
    '''
    if len(forwardValues) != len(backwardValues):
        raise ValueError("Nashbot forward and backward values must be same length!!!")
    
    n = len(forwardValues)
    binomials = pascalsTriangle(n)
    
    #Just to match notation
    p = x
    q = (1-x)
    
    ret = 0.0
    for i in range(0, n):
        forward = binomials[i] * forwardValues[i] * pow(p, n-i-1) * pow(q, i)
        backward =  binomials[i] * backwardValues[i] * pow(p, n-i-1) * pow(q, i)
        ret += forward - backward
    
    return ret

class NashBot(Agent, object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        super(NashBot, self).__init__(param1=0)
        self.name = "NashBot"
    
    def expectedValueOfDeck(self, gameState):
        hazards = gameState.hazardsRevealed
        currentDeck = gameState.deck
        
        probabilityOfDeathPerFutureRound = [0] * currentDeck.cardsLeft()
        for h in hazards.keys():
            if hazards[h] == 0:
                round = len(gameState.cardsDrawn)
                probability = 1.0
                for i in range(0, currentDeck.cardsLeft()):
                    #Log the odds for this future round by multiplying by chance of second hazard being drawn
                    #against the odds of a single hazard being drawn
                    probabilityOfDeathPerFutureRound[i] += (2.0/(currentDeck.cardsLeft()-i)) * (1.0 - probability)
                    
                    #Odds that one card (of specific hazard) will not be drawn up to this point
                    probability *= (1.0 - (float(CARDS_PER_HAZARD)/(currentDeck.cardsLeft()-i)))
                    
                    
            if hazards[h] == 1:
                round = len(gameState.cardsDrawn)
                probability = 1.0
                for i in range(0, currentDeck.cardsLeft()):
                    #Odds that second card will be drawn up to this point
                    probability *= (1.0 - (float(CARDS_PER_HAZARD-1)/(currentDeck.cardsLeft()-i)))
                    
                    #Log the odds for this event in the array
                    probabilityOfDeathPerFutureRound[i] += (1.0 - probability)
                
        valuePerCard = currentDeck.expectedValueOfNextDraw()
        valueFraction = map(lambda y: (1.0 - y) if (1.0-y) > 0 else 0.0, probabilityOfDeathPerFutureRound)
        for j in range(1, len(valueFraction)):
            valueFraction[j] = valueFraction[j] * valueFraction[j-1]
        valuations = map(lambda y: valuePerCard * y, valueFraction)
        #valuations.insert(0, valuePerCard * (1.0 - probabilityOfDeathPerFutureRound[0]))
        return sum(valuations)
                
    
    def expectedValuesOfGoingForward(self, gameState, value, numberAdvancing, numberRetreating):
        if numberAdvancing == 0:
            return 0
        roundTreasure = gameState.roundTreasureValues[self.player_id]
        leftoverTreasure = gameState.leftoverTreasure #assumed to be negligible for now
        pNextCardFail = gameState.probabilityOfNextCardEndingRound()
        pNextCardSuccess = 1.0 - pNextCardFail
                
        failureValue = pNextCardFail * (0)
        successValue = pNextCardSuccess * (roundTreasure) + (value / numberAdvancing)
        
        ret = failureValue + successValue
        return ret
    
    def expectedValuesOfGoingBack(self, gameState, numberAdvancing, numberRetreating):
        if numberRetreating == 0:
            return 0
        
        roundTreasure = gameState.roundTreasureValues[self.player_id]
        leftoverTreasure = gameState.leftoverTreasure
        
        ret = roundTreasure + (leftoverTreasure / numberRetreating)
        return ret
    
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
            p = newton(approximation, 0.5, fprime=None, args=(forwardValues, backwardValues), tol=1.0e-04, maxiter=1500)
        except:
            # In the rare case we cannot actually converge on a value, we simply
            # use an heuristic to guess which option is better
            if sum(forwardValues) > sum(backwardValues):
                return GO_FORWARD
            else:
                return TURN_BACK
        
        if random.random() <= p:
            return GO_FORWARD
        else:
            return TURN_BACK
        
#         return GO_FORWARD
    

    
        
        