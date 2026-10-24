from __future__ import annotations

from pathlib import Path

import joblib
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

from backend.app.core.config import get_settings
from backend.ml.synthetic_data import generate_dataset


def evaluate(model_path: Path | None = None) -> dict[str, float]:
    features, target = generate_dataset(seed=7)
    x_train, x_test, y_train, y_test = train_test_split(features.to_numpy(), target, test_size=0.2, random_state=7)
    path = model_path or get_settings().model_path
    model = joblib.load(path)
    model.fit(x_train, y_train)
    prediction = model.predict(x_test)
    return {"mae": round(float(mean_absolute_error(y_test, prediction)), 4), "r2": round(float(r2_score(y_test, prediction)), 4)}


if __name__ == "__main__":
    print(evaluate())
