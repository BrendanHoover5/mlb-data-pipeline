import psycopg2
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

conn = psycopg2.connect(
    dbname="mlb_data",
    user="brendanhoover",
    host="localhost",
    port="5432"
)

query = """
SELECT
    home_win,

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

FROM model_training_rows
WHERE home_team_games_played_before >= 10
  AND away_team_games_played_before >= 10;
"""

df = pd.read_sql(query, conn)

conn.close()

df = df.dropna()

X = df.drop(columns=["home_win"])
y = df["home_win"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = LogisticRegression(max_iter=1000)

model.fit(X_train, y_train)

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("\nModel Accuracy:")
print(round(accuracy, 4))

print("\nClassification Report:")
print(classification_report(y_test, predictions))