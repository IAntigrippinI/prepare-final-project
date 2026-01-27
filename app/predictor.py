from datetime import datetime, time

import pandas as pd
from sqlalchemy import create_engine, text

from schemas import NHLGame
from connector import ParsingConnector

import joblib


class Predictor:

    def __init__(self, ml_path: str = "models/model.joblib"):
        self._ml_path = ml_path
        self._model = joblib.load("models/model.joblib")

    def build_features_for_games(
            self,
            games: list[NHLGame],
            df_team_current: pd.DataFrame,
            df_team_form: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Преобразует список NHLGame в feature-matrix для модели
        """

        # --- привести дату в team_form ---
        df_team_form = df_team_form.copy()
        df_team_form["game_date"] = pd.to_datetime(df_team_form["game_date"])

        rows = []

        for game in games:
            home = game.home_name
            away = game.away_name
            game_date = datetime.combine(game.game_date, time.min)

            # --------- team current ---------
            hc_df = df_team_current[df_team_current["team_abbrev"] == home]
            ac_df = df_team_current[df_team_current["team_abbrev"] == away]

            if hc_df.empty or ac_df.empty:
                continue

            hc = hc_df.iloc[0]
            ac = ac_df.iloc[0]

            home_avg_points_per_game = hc["points"] / hc["games_played"]
            away_avg_points_per_game = ac["points"] / ac["games_played"]

            home_goal_diff_per_game = hc["goal_differential"] / hc["games_played"]
            away_goal_diff_per_game = ac["goal_differential"] / ac["games_played"]

            # --------- team form (последняя ДО игры) ---------
            h_form_df = (
                df_team_form[
                    (df_team_form["team"] == home)
                    & (df_team_form["game_date"] < game_date)
                    ]
                .sort_values("game_date")
            )

            a_form_df = (
                df_team_form[
                    (df_team_form["team"] == away)
                    & (df_team_form["game_date"] < game_date)
                    ]
                .sort_values("game_date")
            )

            if h_form_df.empty or a_form_df.empty:
                continue

            h = h_form_df.iloc[-1]
            a = a_form_df.iloc[-1]

            rows.append(
                {
                    "game_id": game.game_id,
                    "game_date": game_date,

                    # абсолютные
                    "home_avg_points_per_game": home_avg_points_per_game,
                    "away_avg_points_per_game": away_avg_points_per_game,
                    "home_goal_diff_per_game": home_goal_diff_per_game,
                    "away_goal_diff_per_game": away_goal_diff_per_game,

                    "home_avg_goals_for_5": h["avg_goals_for_last_5"],
                    "home_avg_goals_against_5": h["avg_goals_against_last_5"],
                    "away_avg_goals_for_5": a["avg_goals_for_last_5"],
                    "away_avg_goals_against_5": a["avg_goals_against_last_5"],

                    "home_win_rate_5": h["win_rate_last_5"],

                    # относительные
                    "diff_avg_points_per_game":
                        home_avg_points_per_game - away_avg_points_per_game,

                    "diff_win_rate_5":
                        h["win_rate_last_5"] - a["win_rate_last_5"],

                    # контекст
                    "is_home": 1,
                }
            )

        return pd.DataFrame(rows)

    def predict(self, date: str):
        engine = create_engine("postgresql+psycopg2://admin:admin@db-pipeline:5432/pipeline")
        games = ParsingConnector("https://api-web.nhle.com/v1").fetch_games_by_date(date).games

        with engine.connect() as connection:
            result = connection.execute(text("select * from dim_team_current"))
            df_team_current = pd.DataFrame(result.fetchall(), columns=result.keys())

            result = connection.execute(text("select * from fct_team_form"))
            df_team_form = pd.DataFrame(result.fetchall(), columns=result.keys())

        X_pred = self.build_features_for_games(
            games,
            df_team_current,
            df_team_form,
        )

        features = list(self._model.feature_names_in_)

        proba = self._model.predict_proba(
            X_pred[features]
        )[:, 1]

        X_pred["home_win_proba"] = proba
        # return X_pred["home_win_proba"]
        return [
            {
                "home": game.home_name,
                "away": game.away_name,
                "prob_win_home": f"{proba[i]:.2f}"
            } for i ,game in enumerate(games)
        ]