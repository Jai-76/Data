"""Analyze synthetic MNC workforce data and create five dashboard images."""

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "workforce.csv"
IMAGE_DIR = ROOT / "img"
IMAGE_DIR.mkdir(exist_ok=True)
df = pd.read_csv(DATA_PATH)

mpl.rcParams.update(
    {
        "figure.dpi": 120,
        "savefig.dpi": 180,
        "savefig.bbox": "tight",
        "font.size": 10,
        "axes.titlesize": 12,
        "axes.titleweight": "bold",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.color": (0.90, 0.91, 0.92),
        "axes.axisbelow": True,
    }
)

BLUE, TEAL, ORANGE = (0.15, 0.39, 0.92), (0.06, 0.46, 0.42), (0.98, 0.45, 0.09)
PURPLE, RED, INK = (0.49, 0.23, 0.72), (0.86, 0.15, 0.15), (0.12, 0.18, 0.27)

df["wellbeing_band"] = pd.cut(
    df.wellbeing_risk_score,
    bins=[-1, 10, 20, 30, 41],
    labels=["Stable", "Watch", "Priority", "Critical aggregate signal"],
)

PERF_CUT, READY_CUT = 3.5, 60
df["performance_group"] = np.where(
    df.performance_rating >= PERF_CUT, "High performance", "Developing performance"
)
df["readiness_group"] = np.where(
    df.readiness_index >= READY_CUT, "Role ready", "Not yet ready"
)
df["segment"] = df["performance_group"] + " / " + df["readiness_group"]

print("=" * 72)
print("MNC WORKFORCE READINESS AND WELLBEING ANALYSIS")
print("=" * 72)
print(f"Employees: {len(df)}")
print(f"Mean performance rating: {df.performance_rating.mean():.2f}/5")
print(f"Mean readiness: {df.readiness_index.mean():.1f}/100")
print(f"Mean wellbeing risk: {df.wellbeing_risk_score.mean():.1f}/40")
print(f"Internal mobility: {df.internal_mobility.mean() * 100:.1f}%")
print("\nSegment summary:")
summary = df.groupby("segment", observed=True).agg(
    employees=("employee_id", "size"),
    performance=("performance_rating", "mean"),
    readiness=("readiness_index", "mean"),
    wellbeing_risk=("wellbeing_risk_score", "mean"),
    mobility=("internal_mobility", "mean"),
)
summary["mobility"] *= 100
print(summary.round(1).to_string())

fig, axes = plt.subplots(1, 3, figsize=(12, 3.8))
axes[0].hist(df.performance_rating, bins=np.arange(1, 5.2, 0.2), color=BLUE, edgecolor="white")
axes[0].axvline(df.performance_rating.mean(), color=INK, linestyle="--")
axes[0].set(title="Performance distribution", xlabel="Rating (1–5)", ylabel="Employees")
axes[1].hist(df.readiness_index, bins=20, color=TEAL, edgecolor="white")
axes[1].axvline(READY_CUT, color=ORANGE, linestyle="--", label=f"Cut-off {READY_CUT}")
axes[1].set(title="Role Readiness Index", xlabel="Index (0–100)")
axes[1].legend(frameon=False, fontsize=8)
band_counts = df["wellbeing_band"].value_counts().reindex(
    ["Stable", "Watch", "Priority", "Critical aggregate signal"]
)
axes[2].bar(
    band_counts.index,
    band_counts.values,
    color=[(0.13, 0.77, 0.36), (0.98, 0.79, 0.09), ORANGE, RED],
)
axes[2].set(title="Aggregate wellbeing risk", ylabel="Employees")
axes[2].tick_params(axis="x", rotation=28, labelsize=8)
fig.suptitle("Figure 1 — Global workforce profile", x=0.02, ha="left", fontweight="bold")
fig.tight_layout()
fig.savefig(IMAGE_DIR / "f1_workforce_profile.png")
plt.close(fig)

cols = [
    "performance_rating", "skill_match_pct", "delivery_score", "learning_hours",
    "workload_score", "wellbeing_risk_score", "readiness_index",
]
labels = ["Performance", "Skill match", "Delivery", "Learning h", "Workload", "Wellbeing risk", "Readiness"]
corr = df[cols].corr().to_numpy()
fig, ax = plt.subplots(figsize=(7.4, 5.8))
im = ax.imshow(corr, cmap="RdBu_r", vmin=-1, vmax=1)
ax.set_xticks(range(len(labels)), labels, rotation=38, ha="right")
ax.set_yticks(range(len(labels)), labels)
for i in range(len(labels)):
    for j in range(len(labels)):
        ax.text(j, i, f"{corr[i, j]:.2f}", ha="center", va="center",
                color="white" if abs(corr[i, j]) > 0.55 else INK, fontsize=8)
ax.set_title("Figure 2 — Capability and wellbeing associations", loc="left")
fig.colorbar(im, ax=ax, fraction=0.04, pad=0.03, label="Correlation (association only)")
fig.tight_layout()
fig.savefig(IMAGE_DIR / "f2_correlation_matrix.png")
plt.close(fig)

fig, ax = plt.subplots(figsize=(9, 5.4))
scatter = ax.scatter(
    df.performance_rating,
    df.readiness_index,
    c=df.wellbeing_risk_score,
    cmap="YlOrRd",
    vmin=0,
    vmax=40,
    s=32,
    alpha=0.78,
    edgecolor="white",
    linewidth=0.35,
)
ax.axvline(PERF_CUT, color=INK)
ax.axhline(READY_CUT, color=INK)
ax.set(xlim=(0.8, 5.2), ylim=(0, 100), xlabel="Performance rating", ylabel="Role Readiness Index")
positions = [(3.58, 96, "High performance / Role ready"),
             (3.58, 56, "High performance / Not yet ready"),
             (1.05, 96, "Developing performance / Role ready"),
             (1.05, 56, "Developing performance / Not yet ready")]
for x, y, label in positions:
    ax.text(x, y, label, fontsize=8.5, color=INK, fontweight="bold",
            bbox=dict(facecolor="white", alpha=0.75, edgecolor="none", pad=2))
ax.set_title("Figure 3 — Performance/readiness segments", loc="left")
fig.colorbar(scatter, ax=ax, label="Wellbeing risk score (aggregate use only)")
fig.tight_layout()
fig.savefig(IMAGE_DIR / "f3_performance_readiness_segments.png")
plt.close(fig)

band_order = ["Stable", "Watch", "Priority", "Critical aggregate signal"]
band = df.groupby("wellbeing_band", observed=True).agg(
    performance=("performance_rating", "mean"),
    mobility=("internal_mobility", "mean"),
).reindex(band_order)
band["mobility"] *= 100
fig, axes = plt.subplots(1, 2, figsize=(10, 3.9))
axes[0].bar(
    band.index,
    band.performance,
    color=[(0.13, 0.77, 0.36), (0.98, 0.79, 0.09), ORANGE, RED],
)
axes[0].set(title="Mean performance by risk band", ylabel="Rating (1–5)")
axes[0].tick_params(axis="x", rotation=28, labelsize=8)
axes[1].plot(band.index, band.mobility, "o-", color=PURPLE, linewidth=2.3)
axes[1].set(title="Internal mobility by risk band", ylabel="Mobility rate (%)")
axes[1].tick_params(axis="x", rotation=28, labelsize=8)
fig.suptitle("Figure 4 — Wellbeing bands and workforce outcomes", x=0.02, ha="left", fontweight="bold")
fig.tight_layout()
fig.savefig(IMAGE_DIR / "f4_wellbeing_outcomes.png")
plt.close(fig)

df["learning_quartile"] = pd.qcut(
    df.learning_hours, 4, labels=["Q1 lowest", "Q2", "Q3", "Q4 highest"]
)
lever = df.groupby("learning_quartile", observed=True).agg(
    readiness=("readiness_index", "mean"),
    mobility=("internal_mobility", "mean"),
)
lever["mobility"] *= 100
fig, axes = plt.subplots(1, 2, figsize=(10, 3.9))
axes[0].bar(lever.index, lever.readiness, color=TEAL)
axes[0].set(title="Readiness rises with applied learning", ylabel="Mean readiness (0–100)")
axes[0].tick_params(axis="x", rotation=20)
axes[1].plot(lever.readiness, lever.mobility, "o-", color=BLUE, linewidth=2.3)
axes[1].set(title="Mobility by learning quartile", xlabel="Mean readiness", ylabel="Mobility rate (%)")
for x, y in zip(lever.readiness, lever.mobility):
    axes[1].annotate(f"{y:.0f}%", (x, y), xytext=(0, 8), textcoords="offset points", ha="center")
fig.suptitle("Figure 5 — Development levers", x=0.02, ha="left", fontweight="bold")
fig.tight_layout()
fig.savefig(IMAGE_DIR / "f5_development_levers.png")
plt.close(fig)

print(f"\nSaved five graph images to {IMAGE_DIR}")
