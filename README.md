# MLB Data Pipeline

Automated MLB data pipeline using Python, PostgreSQL, and the MLB Stats API for baseball analytics and future predictive modeling.

---

# Project Overview

This project collects MLB game and player data from the MLB Stats API, stores raw and parsed data in PostgreSQL, and prepares the data for future analytics and machine learning workflows.

The pipeline is designed to:

- ingest MLB game data automatically
- store raw API responses safely
- normalize player/team statistics
- support feature engineering
- support future predictive modeling

---

# Tech Stack

- Python
- PostgreSQL
- MLB-StatsAPI
- psycopg2
- Pandas
- VS Code

---

# Current Pipeline Flow

```text
MLB API
→ main.py
→ PostgreSQL raw storage
→ parsed analytics tables
→ future feature engineering
→ future ML modeling
```

---

# Current Database Structure

## Raw Layer

### games

Stores:
- game outcomes
- teams
- probable pitchers
- venue information
- scheduling context

### game_boxscore_raw

Stores:
- raw MLB API boxscore JSON
- full game/player/team statistics
- backup source for future parsing

---

## Reference Layer

### teams

Stores MLB teams and MLB team IDs.

### players

Stores MLB player IDs and player names.

---

## Analytics Layer

### team_game_stats

Stores:
- team batting totals
- team pitching totals
- per-game team statistics

### player_batting_game_stats

Stores:
- per-player batting statistics
- batting order
- positional information

### player_pitching_game_stats

Stores:
- per-player pitching statistics
- innings pitched
- strikeouts
- ERA
- pitch counts

---

# Current Features

- automated MLB API ingestion
- rerunnable ingestion pipeline
- ON CONFLICT upserts
- normalized relational structure
- indexed analytics tables
- foreign key relationships
- automated daily pipeline execution

---

# Current Scripts

## main.py

Pulls MLB schedule and raw boxscore data.

## populate_players.py

Extracts and stores player information.

## populate_team_game_stats.py

Parses team-level batting and pitching totals.

## populate_player_batting_game_stats.py

Parses individual batting statistics.

## populate_player_pitching_game_stats.py

Parses individual pitching statistics.

## run_daily_pipeline.py

Runs the full daily pipeline automatically.

---

# Future Goals

- feature engineering
- rolling team statistics
- rolling pitcher statistics
- model training datasets
- predictive modeling
- automation scheduling
- cloud database deployment

---

# Example Daily Run

```bash
python run_daily_pipeline.py
```

---

# Notes

This project is focused on:
- baseball analytics
- data engineering
- database design
- ETL pipelines
- future predictive modeling