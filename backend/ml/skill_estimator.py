from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import joblib
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor

from backend.app.core.config import get_settings
from backend.ml.features import FEATURE_NAMES, make_feature_vector


@dataclass
class MasteryEstimate:
    mastery: dict[str, float]
    confidence: dict[str, float]
    feature_importance: dict[str, float]
    model_source: str


class SkillEstimator:
    """Predict per-topic mastery using a small, explainable regressor.

    Limitations: the bundled model is trained on synthetic data, so scores are
    directional and should be updated as real learning outcomes accumulate.
    """

    def __init__(self, model_path: Path | None = None) -> None:
        self.model_path = model_path or get_settings().model_path
        self.model: Any = None
        self.source = "cold-start heuristic"
        self._load()

    def _load(self) -> None:
        if self.model_path.exists():
            try:
                self.model = joblib.load(self.model_path)
                self.source = "synthetic GradientBoostingRegressor"
            except (OSError, ValueError, EOFError):
                self.model = None

    def predict_topic(self, rating: float, history: list[dict], time: float, attempts: float, hints: float) -> float:
        vector = make_feature_vector(rating, history, time, attempts, hints)
        if self.model is None:
            result = 0.45 * (rating / 5) + 0.30 * float(vector[0, 1]) + 0.25 * float(vector[0, 5])
            return float(np.clip(result, 0, 1))
        return float(np.clip(self.model.predict(vector)[0], 0, 1))

    def estimate(
        self,
        self_ratings: dict[str, float],
        solve_history: list[dict],
        time_per_problem: float,
        attempts: float,
        hints_used: float,
    ) -> MasteryEstimate:
        topics = set(self_ratings) | {str(row.get("topic")) for row in solve_history if row.get("topic")}
        if not topics:
            topics = {"arrays"}
        mastery = {}
        for topic in sorted(topics):
            topic_history = [row for row in solve_history if row.get("topic") in {topic, None}]
            mastery[topic] = round(self.predict_topic(self_ratings.get(topic, 2.5), topic_history, time_per_problem, attempts, hints_used), 3)
        importance = getattr(self.model, "feature_importances_", np.asarray([0.22, 0.28, 0.12, 0.10, 0.06, 0.22]))
        normalized = np.asarray(importance) / max(1e-9, np.asarray(importance).sum())
        feature_importance = {name: round(float(value), 3) for name, value in zip(FEATURE_NAMES, normalized, strict=True)}
        confidence_score = 0.55 if self.model is None else min(0.92, 0.65 + len(solve_history) / 100)
        confidence = {topic: round(confidence_score, 3) for topic in mastery}
        return MasteryEstimate(mastery, confidence, feature_importance, self.source)


def estimate_mastery(
    self_ratings: dict[str, float], solve_history: list[dict], time_per_problem: float, attempts: float, hints_used: float
) -> MasteryEstimate:
    return SkillEstimator().estimate(self_ratings, solve_history, time_per_problem, attempts, hints_used)
