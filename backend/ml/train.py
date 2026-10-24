from __future__ import annotations

import json
from pathlib import Path

import joblib
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from backend.app.core.config import get_settings
from backend.ml.features import FEATURE_NAMES
from backend.ml.synthetic_data import generate_dataset


def train(output_path: Path | None = None) -> dict:
    features, target = generate_dataset()
    x_train, _, y_train, _ = train_test_split(features.to_numpy(), target, test_size=0.2, random_state=42)
    model = Pipeline(
        [
            ("scale", StandardScaler()),
            ("regressor", GradientBoostingRegressor(random_state=42, n_estimators=120, max_depth=2, learning_rate=0.05)),
        ]
    )
    model.fit(x_train, y_train)
    scores = cross_val_score(model, features.to_numpy(), target, cv=5, scoring="neg_mean_absolute_error")
    destination = output_path or get_settings().model_path
    destination.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, destination)
    metrics = {"mae_mean": round(float(-scores.mean()), 4), "mae_std": round(float(scores.std()), 4), "features": FEATURE_NAMES}
    destination.with_suffix(".json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    return metrics


if __name__ == "__main__":
    print(train())
