CREATE TABLE IF NOT EXISTS games (
    game_id BIGINT PRIMARY KEY,
    game_datetime TIMESTAMP,
    game_date DATE,
    season INTEGER,

    home_team_id INTEGER,
    away_team_id INTEGER,

    home_team TEXT,
    away_team TEXT,

    home_score INTEGER,
    away_score INTEGER,

    winner TEXT,
    status TEXT,

    home_probable_pitcher TEXT,
    away_probable_pitcher TEXT,

    venue_id INTEGER,
    venue_name TEXT,

    doubleheader TEXT,
    game_num INTEGER,

    home_pitcher_id INTEGER,
    away_pitcher_id INTEGER
);

CREATE TABLE IF NOT EXISTS teams (
    team_id SERIAL PRIMARY KEY,
    team_name TEXT UNIQUE,
    team_abbr TEXT UNIQUE,
    mlb_team_id INTEGER UNIQUE
);

CREATE TABLE IF NOT EXISTS players (
    player_id SERIAL PRIMARY KEY,
    mlb_player_id INTEGER UNIQUE NOT NULL,
    full_name TEXT,
    boxscore_name TEXT
);

CREATE TABLE IF NOT EXISTS game_boxscore_raw (
    game_id BIGINT PRIMARY KEY,
    boxscore_json JSONB,
    collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (game_id)
    REFERENCES games(game_id)
);

CREATE TABLE IF NOT EXISTS team_game_stats (
    game_id BIGINT NOT NULL,
    team_id INTEGER NOT NULL,
    opponent_team_id INTEGER NOT NULL,
    is_home BOOLEAN NOT NULL,

    runs INTEGER,
    hits INTEGER,
    at_bats INTEGER,
    walks INTEGER,
    strikeouts INTEGER,
    home_runs INTEGER,
    doubles INTEGER,
    triples INTEGER,
    rbi INTEGER,
    left_on_base INTEGER,

    pitching_innings TEXT,
    pitching_hits_allowed INTEGER,
    pitching_runs_allowed INTEGER,
    pitching_earned_runs INTEGER,
    pitching_walks INTEGER,
    pitching_strikeouts INTEGER,
    pitching_home_runs_allowed INTEGER,
    pitches_thrown INTEGER,
    strikes INTEGER,

    PRIMARY KEY (game_id, team_id),

    FOREIGN KEY (game_id)
    REFERENCES games(game_id),

    FOREIGN KEY (team_id)
    REFERENCES teams(mlb_team_id),

    FOREIGN KEY (opponent_team_id)
    REFERENCES teams(mlb_team_id)
);

CREATE TABLE IF NOT EXISTS player_batting_game_stats (
    game_id BIGINT NOT NULL,
    player_id INTEGER NOT NULL,
    mlb_player_id INTEGER NOT NULL,
    team_id INTEGER NOT NULL,
    opponent_team_id INTEGER NOT NULL,
    is_home BOOLEAN NOT NULL,

    batting_order INTEGER,
    position TEXT,

    at_bats INTEGER,
    runs INTEGER,
    hits INTEGER,
    rbi INTEGER,
    walks INTEGER,
    strikeouts INTEGER,
    home_runs INTEGER,
    doubles INTEGER,
    triples INTEGER,
    stolen_bases INTEGER,
    left_on_base INTEGER,

    avg_after_game TEXT,
    obp_after_game TEXT,
    slg_after_game TEXT,
    ops_after_game TEXT,

    PRIMARY KEY (game_id, mlb_player_id),

    FOREIGN KEY (game_id)
    REFERENCES games(game_id),

    FOREIGN KEY (player_id)
    REFERENCES players(player_id)
);

CREATE TABLE IF NOT EXISTS player_pitching_game_stats (
    game_id BIGINT NOT NULL,
    player_id INTEGER NOT NULL,
    mlb_player_id INTEGER NOT NULL,
    team_id INTEGER NOT NULL,
    opponent_team_id INTEGER NOT NULL,
    is_home BOOLEAN NOT NULL,

    innings_pitched TEXT,
    hits_allowed INTEGER,
    runs_allowed INTEGER,
    earned_runs INTEGER,
    walks INTEGER,
    strikeouts INTEGER,
    home_runs_allowed INTEGER,
    pitches_thrown INTEGER,
    strikes INTEGER,
    era_after_game TEXT,

    PRIMARY KEY (game_id, mlb_player_id),

    FOREIGN KEY (game_id)
    REFERENCES games(game_id),

    FOREIGN KEY (player_id)
    REFERENCES players(player_id)
);