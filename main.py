import json
import statsapi
import psycopg2
from datetime import date, timedelta
from psycopg2.extras import Json

DAYS_BACK = 3

start_date = date.today() - timedelta(days=DAYS_BACK)
end_date = date.today() - timedelta(days=1)

games = statsapi.schedule(
    start_date=start_date.strftime("%m/%d/%Y"),
    end_date=end_date.strftime("%m/%d/%Y")
)

conn = psycopg2.connect(
    dbname="mlb_data",
    user="brendanhoover",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

processed = 0
boxscores_saved = 0

for game in games:
    if game.get("status") != "Final" or not game.get("winning_team"):
        continue

    game_id = game.get("game_id")
    game_datetime = game.get("game_datetime")
    game_date = game.get("game_date")
    season = int(game_date[:4]) if game_date else None

    home_team_id = game.get("home_id")
    away_team_id = game.get("away_id")
    home_team = game.get("home_name")
    away_team = game.get("away_name")

    home_score = game.get("home_score")
    away_score = game.get("away_score")
    winner = game.get("winning_team")
    status = game.get("status")

    home_probable_pitcher = game.get("home_probable_pitcher")
    away_probable_pitcher = game.get("away_probable_pitcher")

    venue_id = game.get("venue_id")
    venue_name = game.get("venue_name")

    doubleheader = game.get("doubleheader")
    game_num = game.get("game_num")

    cur.execute("""
        INSERT INTO games (
            game_id,
            game_datetime,
            game_date,
            season,
            home_team_id,
            away_team_id,
            home_team,
            away_team,
            home_score,
            away_score,
            winner,
            status,
            home_probable_pitcher,
            away_probable_pitcher,
            venue_id,
            venue_name,
            doubleheader,
            game_num
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (game_id) DO UPDATE SET
            game_datetime = EXCLUDED.game_datetime,
            game_date = EXCLUDED.game_date,
            season = EXCLUDED.season,
            home_team_id = EXCLUDED.home_team_id,
            away_team_id = EXCLUDED.away_team_id,
            home_team = EXCLUDED.home_team,
            away_team = EXCLUDED.away_team,
            home_score = EXCLUDED.home_score,
            away_score = EXCLUDED.away_score,
            winner = EXCLUDED.winner,
            status = EXCLUDED.status,
            home_probable_pitcher = EXCLUDED.home_probable_pitcher,
            away_probable_pitcher = EXCLUDED.away_probable_pitcher,
            venue_id = EXCLUDED.venue_id,
            venue_name = EXCLUDED.venue_name,
            doubleheader = EXCLUDED.doubleheader,
            game_num = EXCLUDED.game_num;
    """, (
        game_id,
        game_datetime,
        game_date,
        season,
        home_team_id,
        away_team_id,
        home_team,
        away_team,
        home_score,
        away_score,
        winner,
        status,
        home_probable_pitcher,
        away_probable_pitcher,
        venue_id,
        venue_name,
        doubleheader,
        game_num
    ))

    boxscore = statsapi.boxscore_data(game_id)

    cur.execute("""
        INSERT INTO game_boxscore_raw (
            game_id,
            boxscore_json
        )
        VALUES (%s, %s)
        ON CONFLICT (game_id) DO UPDATE SET
            boxscore_json = EXCLUDED.boxscore_json,
            collected_at = CURRENT_TIMESTAMP;
    """, (
        game_id,
        Json(boxscore)
    ))

    processed += 1
    boxscores_saved += 1

conn.commit()
cur.close()
conn.close()

print(f"Processed {processed} final games from {start_date} to {end_date}")
print(f"Saved/updated {boxscores_saved} raw boxscores")