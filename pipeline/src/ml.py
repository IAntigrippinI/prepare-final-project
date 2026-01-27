from pathlib import Path
import joblib
import loguru
from typing import Dict, Tuple
import pandas as pd
import numpy as np

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

from sklearn.metrics import (
    roc_auc_score,
    accuracy_score,
    log_loss,
)
from sqlalchemy import create_engine, text

from config import settings


def evaluate_model(
    model,
    X_val: pd.DataFrame,
    y_val: pd.Series,
) -> Dict[str, float]:

    proba = model.predict_proba(X_val)[:, 1]
    preds = (proba >= 0.5).astype(int)

    return {
        "roc_auc": roc_auc_score(y_val, proba),
        "accuracy": accuracy_score(y_val, preds),
        "log_loss": log_loss(y_val, proba),
    }

def train_models(
    df: pd.DataFrame,
    target_col: str = "target",
    date_col: str = "game_date",
    test_size: float = 0.2,
    model_dir: str = "models",
):
    loguru.logger.info(f"Start training...")
    df = df.sort_values(date_col).reset_index(drop=True)

    X = df.drop(columns=[target_col, date_col, "game_id"])
    y = df[target_col]

    split_idx = int(len(df) * (1 - test_size))
    X_train, X_val = X.iloc[:split_idx], X.iloc[split_idx:]
    y_train, y_val = y.iloc[:split_idx], y.iloc[split_idx:]

    models = {
        "logistic_regression": Pipeline(
            [
                ("scaler", StandardScaler()),
                ("model", LogisticRegression(max_iter=1000, class_weight="balanced")),
            ]
        ),
        "random_forest": Pipeline(
            [
                ("model", RandomForestClassifier(
                    n_estimators=300,
                    max_depth=8,
                    min_samples_leaf=20,
                    random_state=42,
                ))
            ]
        ),
        "gradient_boosting": Pipeline(
            [
                ("model", GradientBoostingClassifier(
                    n_estimators=200,
                    learning_rate=0.05,
                    max_depth=3,
                    random_state=42,
                ))
            ]
        ),
    }

    best_model = None
    best_auc = -1
    metrics_by_model = {}

    for name, model in models.items():
        model.fit(X_train, y_train)

        metrics = evaluate_model(model, X_val, y_val)
        metrics_by_model[name] = metrics

        if metrics["roc_auc"] > best_auc:
            best_auc = metrics["roc_auc"]
            best_model = model
            best_model_name = name

    # ---------- сохранение ----------
    # Path(model_dir).mkdir(parents=True, exist_ok=True)
    #
    # model_path = Path(model_dir) / f"model.joblib"
    model_path = "/opt/airflow/src/models/model.joblib"
    joblib.dump(best_model, model_path)
    loguru.logger.info(f"Model saved to {model_path}")
    loguru.logger.info(f"Finish training... {metrics_by_model}")
    return best_model, metrics_by_model


class Couch:

    def __init__(self):
        pass

    def fit(self):
        engine = create_engine(settings.DB_URL)
        loguru.logger.info("Read data from db...")
        with engine.connect() as connection:
            result = connection.execute(text("select * from ml_training_dataset"))
            df = pd.DataFrame(result.fetchall(), columns=result.keys())
            # df = pd.read_sql("select * from ml_predict_dataset", connection)
        # df = pd.read_sql("select * from ml_predict_dataset", engine)
        loguru.logger.info("Read data from db successfully.")
        train_models(df)

