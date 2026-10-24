"""Synthetic training data generator.

The generator models a noisy but interpretable relationship: self-rating and
recent success increase mastery, while long solve times, repeated attempts,
and hint dependence reduce it. It is intentionally not presented as real user
data and must be replaced or recalibrated before production decisions.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def generate_dataset(samples: int = 2400, seed: int = 42) -> tuple[pd.DataFrame, pd.Series]:
    rng = np.random.default_rng(seed)
    frame = pd.DataFrame(
        {
            "self_rating": rng.uniform(0, 1, samples),
            "solved_ratio": rng.beta(3, 2, samples),
            "avg_time_minutes": rng.uniform(10, 120, samples) / 120,
            "attempts": np.clip(rng.gamma(2.2, 1.2, samples) / 8, 0, 1),
            "hints_used": np.clip(rng.gamma(1.4, 0.9, samples) / 5, 0, 1),
            "recent_success": rng.beta(4, 2, samples),
        }
    )
    signal = (
        0.22 * frame["self_rating"]
        + 0.28 * frame["solved_ratio"]
        + 0.22 * frame["recent_success"]
        + 0.12 * (1 - frame["avg_time_minutes"])
        + 0.10 * (1 - frame["attempts"])
        + 0.06 * (1 - frame["hints_used"])
    )
    noise = rng.normal(0, 0.06, samples)
    target = np.clip(signal + noise, 0, 1)
    return frame, pd.Series(target, name="mastery")
