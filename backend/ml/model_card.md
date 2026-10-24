# AlgoForge Skill Estimator Model Card

## Intended use

The estimator produces a directional 0–1 mastery signal for each topic during
onboarding and after progress events. The recommender uses that signal to place
problems near a zone of proximal development, roughly targeting a 60–75%
predicted success probability.

## Training data

The checked-in training script generates synthetic records from realistic
feature ranges: self-rating, solved ratio, average solve time, attempts, hints,
and recent success. Gaussian noise is included to avoid a perfectly deterministic
relationship. No real learner data is bundled.

## Model

`GradientBoostingRegressor` is trained with five-fold cross-validation. A small
feature vector and feature importances are returned by the API for inspection.

## Limitations and risks

- Synthetic data cannot represent every learner, language, disability, or
  educational context.
- Self-ratings can be miscalibrated and recent history can be sparse.
- The output is not a hiring prediction, exam score, or guarantee of success.
- Production use should use consented, anonymized outcomes and monitor drift.
