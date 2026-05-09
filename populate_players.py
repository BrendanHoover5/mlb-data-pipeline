import psycopg2

conn = psycopg2.connect(
    dbname="mlb_data",
    user="brendanhoover",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

cur.execute("""
    SELECT boxscore_json->'playerInfo'
    FROM game_boxscore_raw;
""")

rows = cur.fetchall()

inserted_or_updated = 0

for row in rows:
    player_info = row[0]

    if not player_info:
        continue

    for player_key, player in player_info.items():
        mlb_player_id = player.get("id")
        full_name = player.get("fullName")
        boxscore_name = player.get("boxscoreName")

        if not mlb_player_id:
            continue

        cur.execute("""
            INSERT INTO players (
                mlb_player_id,
                full_name,
                boxscore_name
            )
            VALUES (%s, %s, %s)
            ON CONFLICT (mlb_player_id) DO UPDATE SET
                full_name = EXCLUDED.full_name,
                boxscore_name = EXCLUDED.boxscore_name;
        """, (
            mlb_player_id,
            full_name,
            boxscore_name
        ))

        inserted_or_updated += 1

conn.commit()
cur.close()
conn.close()

print(f"Inserted/updated {inserted_or_updated} player records")