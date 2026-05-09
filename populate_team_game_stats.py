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
    teams_to_process = [
        {
            "team_id": home_team_id,
            "opponent_team_id": away_team_id,
            "is_home": True,
            "batting": boxscore.get("homeBattingTotals", {}),
            "pitching": boxscore.get("homePitchingTotals", {})
        },
        {
            "team_id": away_team_id,
            "opponent_team_id": home_team_id,
            "is_home": False,
            "batting": boxscore.get("awayBattingTotals", {}),
            "pitching": boxscore.get("awayPitchingTotals", {})
        }
    ]

    for team in teams_to_process:
        batting = team["batting"]
        pitching = team["pitching"]

        cur.execute("""
            INSERT INTO team_game_stats (
                game_id,
                team_id,
                opponent_team_id,
                is_home,
                runs,
                hits,
                at_bats,
                walks,
                strikeouts,
                home_runs,
                doubles,
                triples,
                rbi,
                left_on_base,
                pitching_innings,
                pitching_hits_allowed,
                pitching_runs_allowed,
                pitching_earned_runs,
                pitching_walks,
                pitching_strikeouts,
                pitching_home_runs_allowed,
                pitches_thrown,
                strikes
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (game_id, team_id) DO UPDATE SET
                opponent_team_id = EXCLUDED.opponent_team_id,
                is_home = EXCLUDED.is_home,
                runs = EXCLUDED.runs,
                hits = EXCLUDED.hits,
                at_bats = EXCLUDED.at_bats,
                walks = EXCLUDED.walks,
                strikeouts = EXCLUDED.strikeouts,
                home_runs = EXCLUDED.home_runs,
                doubles = EXCLUDED.doubles,
                triples = EXCLUDED.triples,
                rbi = EXCLUDED.rbi,
                left_on_base = EXCLUDED.left_on_base,
                pitching_innings = EXCLUDED.pitching_innings,
                pitching_hits_allowed = EXCLUDED.pitching_hits_allowed,
                pitching_runs_allowed = EXCLUDED.pitching_runs_allowed,
                pitching_earned_runs = EXCLUDED.pitching_earned_runs,
                pitching_walks = EXCLUDED.pitching_walks,
                pitching_strikeouts = EXCLUDED.pitching_strikeouts,
                pitching_home_runs_allowed = EXCLUDED.pitching_home_runs_allowed,
                pitches_thrown = EXCLUDED.pitches_thrown,
                strikes = EXCLUDED.strikes;
        """, (
            game_id,
            team["team_id"],
            team["opponent_team_id"],
            team["is_home"],

            to_int(batting.get("r")),
            to_int(batting.get("h")),
            to_int(batting.get("ab")),
            to_int(batting.get("bb")),
            to_int(batting.get("k")),
            to_int(batting.get("hr")),
            to_int(batting.get("doubles")),
            to_int(batting.get("triples")),
            to_int(batting.get("rbi")),
            to_int(batting.get("lob")),

            pitching.get("ip"),
            to_int(pitching.get("h")),
            to_int(pitching.get("r")),
            to_int(pitching.get("er")),
            to_int(pitching.get("bb")),
            to_int(pitching.get("k")),
            to_int(pitching.get("hr")),
            to_int(pitching.get("p")),
            to_int(pitching.get("s"))
        ))

        processed += 1

conn.commit()
cur.close()
conn.close()

print(f"Inserted/updated {processed} team game stat rows") 