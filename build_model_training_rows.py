import psycopg2

conn = psycopg2.connect(
    dbname="mlb_data",
    user="brendanhoover",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

cur.execute("""
    SELECT
        game_id,
        game_date,
        home_team_id,
        away_team_id,
        home_score,
        away_score
    FROM games
    WHERE status = 'Final'
    ORDER BY game_date, game_id;
""")

games = cur.fetchall()
processed = 0

def get_team_history(team_id, game_date):
    cur.execute("""
        SELECT
            g.game_id,
            g.game_date,
            tgs.team_id,
            tgs.opponent_team_id,
            tgs.is_home,
            tgs.runs,
            tgs.pitching_runs_allowed,
            CASE
                WHEN tgs.runs > tgs.pitching_runs_allowed THEN 1
                ELSE 0
            END AS win
        FROM team_game_stats tgs
        JOIN games g
            ON tgs.game_id = g.game_id
        WHERE tgs.team_id = %s
          AND g.game_date < %s
        ORDER BY g.game_date DESC, g.game_id DESC;
    """, (team_id, game_date))

    return cur.fetchall()

def safe_avg(values):
    values = [v for v in values if v is not None]
    if not values:
        return None
    return sum(values) / len(values)

def win_pct(wins, games_played):
    if games_played == 0:
        return None
    return wins / games_played

for game in games:
    game_id, game_date, home_team_id, away_team_id, home_score, away_score = game

    if home_score is None or away_score is None:
        continue

    home_win = 1 if home_score > away_score else 0

    home_history = get_team_history(home_team_id, game_date)
    away_history = get_team_history(away_team_id, game_date)

    home_games_before = len(home_history)
    away_games_before = len(away_history)

    home_wins_before = sum(row[7] for row in home_history)
    away_wins_before = sum(row[7] for row in away_history)

    home_last_10 = home_history[:10]
    away_last_10 = away_history[:10]

    home_last_10_wins = sum(row[7] for row in home_last_10)
    away_last_10_wins = sum(row[7] for row in away_last_10)

    home_runs = [row[5] for row in home_history]
    away_runs = [row[5] for row in away_history]

    home_runs_allowed = [row[6] for row in home_history]
    away_runs_allowed = [row[6] for row in away_history]

    home_home_games = [row for row in home_history if row[4] is True]
    away_away_games = [row for row in away_history if row[4] is False]

    home_home_wins = sum(row[7] for row in home_home_games)
    away_away_wins = sum(row[7] for row in away_away_games)

    cur.execute("""
        INSERT INTO model_training_rows (
            game_id,
            game_date,
            home_team_id,
            away_team_id,
            home_win,
            home_team_games_played_before,
            away_team_games_played_before,
            home_team_win_pct_before,
            away_team_win_pct_before,
            home_team_last_10_wins,
            away_team_last_10_wins,
            home_team_runs_per_game_before,
            away_team_runs_per_game_before,
            home_team_runs_allowed_per_game_before,
            away_team_runs_allowed_per_game_before,
            home_team_home_win_pct_before,
            away_team_away_win_pct_before
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (game_id) DO UPDATE SET
            game_date = EXCLUDED.game_date,
            home_team_id = EXCLUDED.home_team_id,
            away_team_id = EXCLUDED.away_team_id,
            home_win = EXCLUDED.home_win,
            home_team_games_played_before = EXCLUDED.home_team_games_played_before,
            away_team_games_played_before = EXCLUDED.away_team_games_played_before,
            home_team_win_pct_before = EXCLUDED.home_team_win_pct_before,
            away_team_win_pct_before = EXCLUDED.away_team_win_pct_before,
            home_team_last_10_wins = EXCLUDED.home_team_last_10_wins,
            away_team_last_10_wins = EXCLUDED.away_team_last_10_wins,
            home_team_runs_per_game_before = EXCLUDED.home_team_runs_per_game_before,
            away_team_runs_per_game_before = EXCLUDED.away_team_runs_per_game_before,
            home_team_runs_allowed_per_game_before = EXCLUDED.home_team_runs_allowed_per_game_before,
            away_team_runs_allowed_per_game_before = EXCLUDED.away_team_runs_allowed_per_game_before,
            home_team_home_win_pct_before = EXCLUDED.home_team_home_win_pct_before,
            away_team_away_win_pct_before = EXCLUDED.away_team_away_win_pct_before;
    """, (
        game_id,
        game_date,
        home_team_id,
        away_team_id,
        home_win,
        home_games_before,
        away_games_before,
        win_pct(home_wins_before, home_games_before),
        win_pct(away_wins_before, away_games_before),
        home_last_10_wins,
        away_last_10_wins,
        safe_avg(home_runs),
        safe_avg(away_runs),
        safe_avg(home_runs_allowed),
        safe_avg(away_runs_allowed),
        win_pct(home_home_wins, len(home_home_games)),
        win_pct(away_away_wins, len(away_away_games))
    ))

    processed += 1

conn.commit()
cur.close()
conn.close()

print(f"Inserted/updated {processed} model training rows")