'''
Created on May 13, 2017

@author: Gregory
'''

import os
import json
import logging.config
import Game
import sqlite3
import datetime
from incanGold.sqlFunctions import executeScriptsFromFile
from incanGold.agent.AgentPool import AgentPool
from incanGold.agent.RandomAgent import RandomAgent
from incanGold.agent.CollectNAgent import CollectNAgent
from incanGold.agent.nashBot.NashBot import NashBot
from incanGold.agent.nashBot.VonNeumannNashBot import VonNeumannNashBot
from incanGold.Game import MAX_PLAYERS, MIN_PLAYERS
from incanGold.agent.ChancesOfDyingAgent import ChancesOfDyingAgent
from incanGold.agent.InverseRiskAgent import InverseRiskAgent
from incanGold.agent.NthTreasureAgent import NthTreasureAgent
from incanGold.GameState import ROUNDS_IN_GAME


logger = logging.getLogger(__name__)
t = datetime.datetime.now()
sqlDatabaseFilename = str(datetime.date.today())+"_{:%H}_{:%M}".format(t,t) + ".db"
sqlConn = sqlite3.connect(sqlDatabaseFilename)
executeScriptsFromFile(sqlConn.cursor(), "database_definitions.sql")

agentPool = AgentPool()
agentPool.addAgentProfile(NashBot())
agentPool.addAgentProfile(VonNeumannNashBot(1.1))
agentPool.addAgentProfile(VonNeumannNashBot(1.2))
agentPool.addAgentProfile(VonNeumannNashBot(0.9))
agentPool.addAgentProfile(VonNeumannNashBot(0.8))
agentPool.addAgentProfile(RandomAgent(weight=0.7))
agentPool.addAgentProfile(RandomAgent(weight=0.75))
agentPool.addAgentProfile(RandomAgent(weight=0.8))
agentPool.addAgentProfile(RandomAgent(weight=0.85))
agentPool.addAgentProfile(RandomAgent(weight=0.9))
agentPool.addAgentProfile(CollectNAgent(4))
agentPool.addAgentProfile(CollectNAgent(5))
agentPool.addAgentProfile(CollectNAgent(6))
agentPool.addAgentProfile(ChancesOfDyingAgent(0.10))
agentPool.addAgentProfile(ChancesOfDyingAgent(0.15))
agentPool.addAgentProfile(ChancesOfDyingAgent(0.175))
agentPool.addAgentProfile(ChancesOfDyingAgent(0.20))
agentPool.addAgentProfile(NthTreasureAgent(2))
agentPool.addAgentProfile(NthTreasureAgent(3))
agentPool.addAgentProfile(NthTreasureAgent(4))

def setupLogging(
    default_path='logging.json',
    default_level=logging.INFO,
    env_key='LOG_CFG'):
    
    """Setup logging configuration"""
    
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)

def writeAgentPoolToDatabase(agentPool):
    cursor = sqlConn.cursor()
    #Make sure all agents are added into the db if they aren't already
    for p in agentPool.agents:
        cursor.execute("INSERT INTO agents VALUES(?,?,?,?,?,?)", (p.profile_id, p.name, p.param1, p.param2, p.param3, p.param4,))
        for i in range(MIN_PLAYERS, MAX_PLAYERS+1):
            cursor.execute("INSERT INTO agent_results VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (p.profile_id, i, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,))
    sqlConn.commit()
    
def writeGameToDatabase(game):
    cursor = sqlConn.cursor()
    
    agentDeaths = [0] * game.playerCount
    for i in range(0, game.playerCount):
        for j in range(0, ROUNDS_IN_GAME):
            if game.gameState.rounds[j].roundTreasureValues[i] == 0:
                agentDeaths[i] += 1

    #Add entry for game
    cursor.execute("INSERT INTO games VALUES(?,?,?,?)", (game.id, game.treasureAvailableInGame(), game.treasureCollectedInGame(), len(game.players),))
    
    #Add entries for game_results (1 for each player involved)
    for i in range(0, game.playerCount):
        cursor.execute("INSERT INTO game_results VALUES(?,?,?,?,?)", (game.id, game.places[i], game.players[game.places[i]].profile_id, game.gameState.treasureValues[game.places[i]], agentDeaths[i],))
    
    #Add entries for each round of play
    for r in game.gameState.rounds:
        cursor.execute("INSERT INTO rounds VALUES(?,?,?,?,?)", (game.id, r.round, len(r.cardsDrawn), r.maxRoundTreasureAvailable(), r.roundTreasureCollected(),))
    
    #Update agent entries
    for i in range(0, game.playerCount):
        cursor.execute("""SELECT games_won, games_played, treasure_collected, treasure_available, deaths,
                        first_place_rate, second_place_rate, third_place_rate, fourth_place_rate, 
                        fifth_place_rate, sixth_place_rate, seventh_place_rate 
                        FROM agent_results WHERE agent_id = ? AND player_count = ?""", 
                        (game.players[i].profile_id, game.playerCount,))
        [won, played, collected, available, deaths, first, second, third, fourth, fifth, sixth, seventh] = cursor.fetchone()
        places = [first, second, third, fourth, fifth, sixth, seventh]
        if game.winner() == i:
            won += 1
        played += 1
        win_rate = won/(1.0*played)
        collected += game.gameState.treasureValues[i]
        available += game.treasureAvailableInGame()
        treasure_rate = 0
        if available != 0:
            treasure_rate = collected / (1.0 * available)
        deaths += agentDeaths[i]
        death_rate = deaths/(1.0*played)
        
        for j in range(0, game.playerCount):
            totalInPlace = places[j] * (played-1)
            if game.places[j] == i:
                totalInPlace += 1.0
            
            places[j] = totalInPlace / played
        
        cursor.execute("""UPDATE agent_results SET games_won = ?, games_played = ?, 
                        win_rate = ?, deaths = ?, death_rate = ?, treasure_collected = ?, treasure_available = ?, 
                        treasure_rate = ?, first_place_rate = ?, second_place_rate = ?, 
                        third_place_rate = ?, fourth_place_rate = ?, fifth_place_rate = ?, 
                        sixth_place_rate = ?, seventh_place_rate = ?
                        WHERE agent_id = ? AND player_count = ?""",
                        (won, played, win_rate, deaths, death_rate, collected, available,treasure_rate,
                         places[0],places[1],places[2],places[3],places[4],places[5],places[6],
                         game.players[i].profile_id, game.playerCount,))
    
    sqlConn.commit()
    
    return
if __name__ == '__main__':
    setupLogging()
    writeAgentPoolToDatabase(agentPool)
    gameCount = 10000
    for i in range(0, gameCount):
        print "Running game " + str(i) + " of " + str(gameCount)
        game = Game.Game(i, agentPool)
        game.run()
        writeGameToDatabase(game)
    
    
    