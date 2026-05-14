import psycopg2

def innings_to_float(ip):
    if ip in (None, "", "-.--"):
        return 0

    ip = str(ip)

    if "." not in ip:
        return float(ip)

    whole, outs = ip.split(".")
    whole = int(whole)
    outs = int(outs)

    return whole + (outs / 3)

def safe_divide(num, denom):
    if denom == 0:
        return None
    return num / denom

def get_first_pitcher_id(pitchers):
    for pitcher in pitchers:
        pitcher_id = pitcher.get("personId")
        if pitcher_id:
            return pitcher_id
    return None

conn = psycopg2.connect(
    dbname="mlb_data",
    user="brendanhoover",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

cur.execute("""
    SELECT
        g.game_id,
        g.game_date,
        b.boxscore_json
    FROM games g
    JOIN game_boxscore_raw b
        ON g.game_id = b.game_id
    WHERE g.status = 'Final'
    ORDER BY g.game_date, g.game_id;
""")

games = cur.fetchall()
processed = 0

def get_pitcher_history(mlb_player_id, game_date):
    cur.execute("""
        SELECT
            ppgs.innings_pitched,
            ppgs.hits_allowed,
            ppgs.earned_runs,
            ppgs.walks,
            ppgs.strikeouts
        FROM player_pitching_game_stats ppgs
        JOIN games g
            ON ppgs.game_id = g.game_id
        WHERE ppgs.mlb_player_id = %s
          AND g.game_date < %s
        ORDER BY g.game_date DESC, g.game_id DESC;
    """, (mlb_player_id, game_date))

    return cur.fetchall()

def calculate_pitcher_features(history):
    games_before = len(history)

    total_ip = 0
    total_hits = 0
    total_er = 0
    total_bb = 0
    total_k = 0

    for row in history:
        innings_pitched, hits_allowed, earned_runs, walks, strikeouts = row

        total_ip += innings_to_float(innings_pitched)
        total_hits += hits_allowed or 0
        total_er += earned_runs or 0
        total_bb += walks or 0
        total_k += strikeouts or 0

    era = safe_divide(total_er * 9, total_ip)
    whip = safe_divide(total_hits + total_bb, total_ip)
    k_per_9 = safe_divide(total_k * 9, total_ip)
    bb_per_9 = safe_divide(total_bb * 9, total_ip)

    return {
        "games_before": games_before,
        "era": era,
        "whip": whip,
        "k_per_9": k_per_9,
        "bb_per_9": bb_per_9
    }

for game_id, game_date, boxscore in games:
    home_pitcher_id = get_first_pitcher_id(boxscore.get("homePitchers", []))
    away_pitcher_id = get_first_pitcher_id(boxscore.get("awayPitchers", []))

    home_features = calculate_pitcher_features(
        get_pitcher_history(home_pitcher_id, game_date)
    ) if home_pitcher_id else None

    away_features = calculate_pitcher_features(
        get_pitcher_history(away_pitcher_id, game_date)
    ) if away_pitcher_id else None

    cur.execute("""
        UPDATE model_training_rows
        SET
            home_starting_pitcher_id = %s,
            away_starting_pitcher_id = %s,

            home_pitcher_era_before = %s,
            away_pitcher_era_before = %s,

            home_pitcher_whip_before = %s,
            away_pitcher_whip_before = %s,

            home_pitcher_k_per_9_before = %s,
            away_pitcher_k_per_9_before = %s,

            home_pitcher_bb_per_9_before = %s,
            away_pitcher_bb_per_9_before = %s,

            home_pitcher_games_before = %s,
            away_pitcher_games_before = %s
        WHERE game_id = %s;
    """, (
        home_pitcher_id,
        away_pitcher_id,

        home_features["era"] if home_features else None,
        away_features["era"] if away_features else None,

        home_features["whip"] if home_features else None,
        away_features["whip"] if away_features else None,

        home_features["k_per_9"] if home_features else None,
        away_features["k_per_9"] if away_features else None,

        home_features["bb_per_9"] if home_features else None,
        away_features["bb_per_9"] if away_features else None,

        home_features["games_before"] if home_features else None,
        away_features["games_before"] if away_features else None,

        game_id
    ))

    processed += 1

conn.commit()
cur.close()
conn.close()

print(f"Updated pitcher features for {processed} games")