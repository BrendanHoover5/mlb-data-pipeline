import psycopg2

def to_int(value):
    if value in (None, "", "-.--"):
        return None
    try:
        return int(value)
    except ValueError:
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
        g.home_team_id,
        g.away_team_id,
        b.boxscore_json
    FROM games g
    JOIN game_boxscore_raw b
        ON g.game_id = b.game_id;
""")

rows = cur.fetchall()
processed = 0

for game_id, home_team_id, away_team_id, boxscore in rows:
    sides = [
        {
            "pitchers": boxscore.get("homePitchers", []),
            "team_id": home_team_id,
            "opponent_team_id": away_team_id,
            "is_home": True
        },
        {
            "pitchers": boxscore.get("awayPitchers", []),
            "team_id": away_team_id,
            "opponent_team_id": home_team_id,
            "is_home": False
        }
    ]

    for side in sides:
        for pitcher in side["pitchers"]:
            mlb_player_id = pitcher.get("personId")

            if not mlb_player_id:
                continue

            cur.execute("""
                SELECT player_id
                FROM players
                WHERE mlb_player_id = %s;
            """, (mlb_player_id,))

            player_row = cur.fetchone()

            if not player_row:
                continue

            player_id = player_row[0]

            cur.execute("""
                INSERT INTO player_pitching_game_stats (
                    game_id,
                    player_id,
                    mlb_player_id,
                    team_id,
                    opponent_team_id,
                    is_home,
                    innings_pitched,
                    hits_allowed,
                    runs_allowed,
                    earned_runs,
                    walks,
                    strikeouts,
                    home_runs_allowed,
                    pitches_thrown,
                    strikes,
                    era_after_game
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (game_id, mlb_player_id) DO UPDATE SET
                    player_id = EXCLUDED.player_id,
                    team_id = EXCLUDED.team_id,
                    opponent_team_id = EXCLUDED.opponent_team_id,
                    is_home = EXCLUDED.is_home,
                    innings_pitched = EXCLUDED.innings_pitched,
                    hits_allowed = EXCLUDED.hits_allowed,
                    runs_allowed = EXCLUDED.runs_allowed,
                    earned_runs = EXCLUDED.earned_runs,
                    walks = EXCLUDED.walks,
                    strikeouts = EXCLUDED.strikeouts,
                    home_runs_allowed = EXCLUDED.home_runs_allowed,
                    pitches_thrown = EXCLUDED.pitches_thrown,
                    strikes = EXCLUDED.strikes,
                    era_after_game = EXCLUDED.era_after_game;
            """, (
                game_id,
                player_id,
                mlb_player_id,
                side["team_id"],
                side["opponent_team_id"],
                side["is_home"],
                pitcher.get("ip"),
                to_int(pitcher.get("h")),
                to_int(pitcher.get("r")),
                to_int(pitcher.get("er")),
                to_int(pitcher.get("bb")),
                to_int(pitcher.get("k")),
                to_int(pitcher.get("hr")),
                to_int(pitcher.get("p")),
                to_int(pitcher.get("s")),
                pitcher.get("era")
            ))

            processed += 1

conn.commit()
cur.close()
conn.close()

print(f"Inserted/updated {processed} player pitching stat rows") 