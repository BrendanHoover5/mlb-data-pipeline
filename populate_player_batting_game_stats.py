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
            "batters": boxscore.get("homeBatters", []),
            "team_id": home_team_id,
            "opponent_team_id": away_team_id,
            "is_home": True
        },
        {
            "batters": boxscore.get("awayBatters", []),
            "team_id": away_team_id,
            "opponent_team_id": home_team_id,
            "is_home": False
        }
    ]

    for side in sides:
        for batter in side["batters"]:
            mlb_player_id = batter.get("personId")

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
                INSERT INTO player_batting_game_stats (
                    game_id,
                    player_id,
                    mlb_player_id,
                    team_id,
                    opponent_team_id,
                    is_home,
                    batting_order,
                    position,
                    at_bats,
                    runs,
                    hits,
                    rbi,
                    walks,
                    strikeouts,
                    home_runs,
                    doubles,
                    triples,
                    stolen_bases,
                    left_on_base,
                    avg_after_game,
                    obp_after_game,
                    slg_after_game,
                    ops_after_game
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (game_id, mlb_player_id) DO UPDATE SET
                    player_id = EXCLUDED.player_id,
                    team_id = EXCLUDED.team_id,
                    opponent_team_id = EXCLUDED.opponent_team_id,
                    is_home = EXCLUDED.is_home,
                    batting_order = EXCLUDED.batting_order,
                    position = EXCLUDED.position,
                    at_bats = EXCLUDED.at_bats,
                    runs = EXCLUDED.runs,
                    hits = EXCLUDED.hits,
                    rbi = EXCLUDED.rbi,
                    walks = EXCLUDED.walks,
                    strikeouts = EXCLUDED.strikeouts,
                    home_runs = EXCLUDED.home_runs,
                    doubles = EXCLUDED.doubles,
                    triples = EXCLUDED.triples,
                    stolen_bases = EXCLUDED.stolen_bases,
                    left_on_base = EXCLUDED.left_on_base,
                    avg_after_game = EXCLUDED.avg_after_game,
                    obp_after_game = EXCLUDED.obp_after_game,
                    slg_after_game = EXCLUDED.slg_after_game,
                    ops_after_game = EXCLUDED.ops_after_game;
            """, (
                game_id,
                player_id,
                mlb_player_id,
                side["team_id"],
                side["opponent_team_id"],
                side["is_home"],
                to_int(batter.get("battingOrder")),
                batter.get("position"),
                to_int(batter.get("ab")),
                to_int(batter.get("r")),
                to_int(batter.get("h")),
                to_int(batter.get("rbi")),
                to_int(batter.get("bb")),
                to_int(batter.get("k")),
                to_int(batter.get("hr")),
                to_int(batter.get("doubles")),
                to_int(batter.get("triples")),
                to_int(batter.get("sb")),
                to_int(batter.get("lob")),
                batter.get("avg"),
                batter.get("obp"),
                batter.get("slg"),
                batter.get("ops")
            ))

            processed += 1

conn.commit()
cur.close()
conn.close()

print(f"Inserted/updated {processed} player batting stat rows") 