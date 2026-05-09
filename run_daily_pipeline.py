import subprocess
import sys

scripts = [
    "main.py",
    "populate_players.py",
    "populate_team_game_stats.py",
    "populate_player_batting_game_stats.py",
    "populate_player_pitching_game_stats.py"
]

for script in scripts:
    print(f"\nRunning {script}...")

    result = subprocess.run([sys.executable, script])

    if result.returncode != 0:
        print(f"\nPipeline stopped. {script} failed.")
        sys.exit(result.returncode)

print("\nDaily MLB pipeline completed successfully.")