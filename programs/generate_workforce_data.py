

from pathlib import Path

import numpy as np
import pandas as pd


SEED = 2026
N = 600
ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"

rng = np.random.default_rng(SEED)

business_units = ["Engineering", "Data", "Product", "Consulting", "Operations", "Support"]
regions = ["India", "Europe", "North America", "Asia-Pacific"]
levels = ["Associate", "Senior Associate", "Manager", "Senior Manager"]

business_unit = rng.choice(business_units, N, p=[0.28, 0.15, 0.14, 0.16, 0.15, 0.12])
region = rng.choice(regions, N, p=[0.48, 0.20, 0.18, 0.14])
career_level = rng.choice(levels, N, p=[0.42, 0.32, 0.18, 0.08])
tenure_years = np.clip(rng.gamma(2.4, 1.8, N), 0.2, 15.0)

commitment = rng.normal(0, 1, N)
workload = np.clip(
    57 - 5.5 * commitment + rng.normal(0, 11, N), 20, 95
)
learning_hours = np.clip(
    14 + 5.0 * commitment - 0.07 * workload + rng.normal(0, 6, N), 0, 50
)
skill_match = np.clip(
    52 + 15 * commitment + 0.30 * learning_hours + rng.normal(0, 14, N), 0, 100
)
quality_score = np.clip(
    64 + 8.5 * commitment - 0.20 * (workload - 55) + rng.normal(0, 10, N), 0, 100
)
goal_attainment = np.clip(
    70 + 7.5 * commitment - 0.12 * (workload - 55) + rng.normal(0, 12, N), 20, 125
)
performance_rating = np.clip(
    2.45
    + 0.018 * goal_attainment
    + 0.010 * quality_score
    - 0.0015 * (workload - 55) ** 2
    + rng.normal(0, 0.25, N),
    1,
    5,
)
delivery_score = np.clip(
    58 + 0.30 * quality_score + 0.13 * goal_attainment
    - 0.10 * (workload - 55) + rng.normal(0, 7, N),
    0,
    100,
)
certifications = rng.poisson(np.clip(0.7 + learning_hours / 14, 0.1, None))
stretch_assignment = (
    rng.random(N)
    < 1 / (1 + np.exp(-(-1.0 + 0.045 * learning_hours + 0.45 * commitment)))
).astype(int)
collaboration_score = np.clip(
    64 + 7 * commitment - 0.08 * (workload - 55) + rng.normal(0, 10, N), 0, 100
)

wellbeing_risk = np.clip(
    18 + 0.30 * (workload - 55) - 2.4 * commitment
    + rng.normal(0, 5.5, N),
    0,
    40,
)

readiness = (
    0.25 * np.clip((performance_rating - 1) / 4 * 100, 0, 100)
    + 0.25 * skill_match
    + 0.15 * delivery_score
    + 0.15 * np.clip(learning_hours / 40 * 100, 0, 100)
    + 0.10 * np.clip(certifications / 5 * 100, 0, 100)
    + 0.10 * collaboration_score
)
readiness = np.round(np.clip(readiness, 0, 100), 1)

mobility_probability = 1 / (
    1 + np.exp(-(-4.4 + 0.075 * readiness - 0.025 * wellbeing_risk
                 + 0.35 * stretch_assignment))
)
internal_mobility = (rng.random(N) < mobility_probability).astype(int)

df = pd.DataFrame(
    {
        "employee_id": [f"E{1000 + i}" for i in range(N)],
        "business_unit": business_unit,
        "region": region,
        "career_level": career_level,
        "tenure_years": np.round(tenure_years, 1),
        "performance_rating": np.round(performance_rating, 2),
        "goal_attainment_pct": np.round(goal_attainment, 1),
        "quality_score": np.round(quality_score, 1),
        "skill_match_pct": np.round(skill_match, 1),
        "delivery_score": np.round(delivery_score, 1),
        "learning_hours": np.round(learning_hours, 1),
        "certifications": certifications,
        "stretch_assignment": stretch_assignment,
        "collaboration_score": np.round(collaboration_score, 1),
        "workload_score": np.round(workload, 1),
        "wellbeing_risk_score": np.round(wellbeing_risk, 1),
        "readiness_index": readiness,
        "internal_mobility": internal_mobility,
    }
)

DATA_DIR.mkdir(exist_ok=True)
df.to_csv(DATA_DIR / "workforce.csv", index=False)
print(f"Generated {len(df)} synthetic employee records -> {DATA_DIR / 'workforce.csv'}")
print(f"Internal mobility rate: {df.internal_mobility.mean() * 100:.1f}%")
print(f"Mean readiness: {df.readiness_index.mean():.1f}/100")
print(f"Mean wellbeing risk: {df.wellbeing_risk_score.mean():.1f}/40")
