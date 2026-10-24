from collections.abc import Iterable

import numpy as np


FEATURE_NAMES = [
    "self_rating",
    "solved_ratio",
    "avg_time_minutes",
    "attempts",
    "hints_used",
    "recent_success",
]


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, float(value)))


def aggregate_history(history: Iterable[dict]) -> dict[str, float]:
    rows = list(history)
    if not rows:
        return {"solved_ratio": 0.0, "avg_time_minutes": 35.0, "attempts": 1.0, "hints_used": 0.0, "recent_success": 0.5}
    solved = [row for row in rows if row.get("solved", row.get("status") == "solved")]
    times = [float(row.get("time_minutes", row.get("total_time_seconds", 2100) / 60)) for row in rows]
    attempts = [float(row.get("attempts", 1)) for row in rows]
    hints = [float(row.get("hints_used", 0)) for row in rows]
    recent = rows[-5:]
    return {
        "solved_ratio": len(solved) / len(rows),
        "avg_time_minutes": sum(times) / len(times),
        "attempts": sum(attempts) / len(attempts),
        "hints_used": sum(hints) / len(hints),
        "recent_success": sum(bool(row.get("solved", row.get("status") == "solved")) for row in recent) / len(recent),
    }


def make_feature_vector(
    self_rating: float,
    solve_history: Iterable[dict],
    time_per_problem: float | None = None,
    attempts: float | None = None,
    hints_used: float | None = None,
) -> np.ndarray:
    history = aggregate_history(solve_history)
    values = [
        clamp(self_rating / 5, 0, 1),
        clamp(history["solved_ratio"], 0, 1),
        clamp((time_per_problem if time_per_problem is not None else history["avg_time_minutes"]) / 120, 0, 1),
        clamp((attempts if attempts is not None else history["attempts"]) / 8, 0, 1),
        clamp((hints_used if hints_used is not None else history["hints_used"]) / 5, 0, 1),
        clamp(history["recent_success"], 0, 1),
    ]
    return np.asarray(values, dtype=float).reshape(1, -1)
