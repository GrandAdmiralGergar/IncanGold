DROP TABLE IF EXISTS agents;
DROP TABLE IF EXISTS agent_results;
DROP TABLE IF EXISTS games;
DROP TABLE IF EXISTS game_results;
DROP TABLE IF EXISTS rounds;

CREATE TABLE agents (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  param_1 REAL,
  param_2 REAL,
  param_3 REAL,
  param_4 REAL
);  

CREATE TABLE agent_results (
  agent_id INTEGER,
  player_count INTEGER,
  games_won INTEGER,
  games_played INTEGER,
  win_rate REAL,
  deaths INTEGER,
  death_rate REAL,
  treasure_collected INTEGER,
  treasure_available INTEGER,
  treasure_rate REAL,
  first_place_rate REAL,
  second_place_rate REAL,
  third_place_rate REAL,
  fourth_place_rate REAL,
  fifth_place_rate REAL,
  sixth_place_rate REAL,
  seventh_place_rate REAL,
  PRIMARY KEY(agent_id, player_count),
  FOREIGN KEY(agent_id) REFERENCES agents(id)
);

CREATE TABLE games (
  id INTEGER PRIMARY KEY,
  total_treasure_available INTEGER NOT NULL,
  total_treasure_collected INTEGER NOT NULL,
  player_count INTEGER NOT NULL
);

CREATE TABLE game_results (
  game_id INTEGER NOT NULL,
  place INTEGER NOT NULL,
  agent_id INTEGER NOT NULL,
  total_treasure INTEGER NOT NULL,
  total_deaths INTEGER NOT NULL,
  PRIMARY KEY(game_id, place),
  FOREIGN KEY(game_id) REFERENCES games(id),
  FOREIGN KEY(agent_id) REFERENCES agents(id)
);

CREATE TABLE rounds(
  game_id INTEGER,
  round_number INTEGER,
  cards_drawn INTEGER,
  treasure_available INTEGER,
  treasure_claimed INTEGER,
  PRIMARY KEY(game_id, round_number),
  FOREIGN KEY(game_id) REFERENCES games(id)
);