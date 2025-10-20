import pandas as pd
from matplotlib import pyplot as plt

df = pd.read_csv("results/results_temperature_experiment_v2.csv")
'''
# Early versions of the code have two seeds at temperature zero,
# this is hacky code to remove them
mask = (df["temperature"] != 0.0) | (df["seed"] == 686579303)
df = df[mask].copy()
'''
zero_temp_dict = (
    df[df["temperature"] == 0.0]
      .groupby(["model", "prompt_id"])["usage_tokens"]
      .first()
      .to_dict()
)

# Compute delta to isolate change in length compared to greedy decoding
df["delta"] = df.apply(
    lambda row: row["usage_tokens"] - zero_temp_dict[(row["model"], row["prompt_id"])],
    axis=1,
)

# Calculate summary statistics according to temperature
raw_stats = (
    df.groupby("temperature")["usage_tokens"]
      .agg(["mean", "std"])
      .reset_index()
      .rename(columns={"mean": "Mean (tokens)", "std": "Std (tokens)"})
)

delta_stats = (
    df.groupby("temperature")["delta"]
      .agg(["mean", "std"])
      .reset_index()
      .rename(columns={"mean": "Mean Δ", "std": "Std Δ"})
)



spearman_corr = df["delta"].corr(df["temperature"], method="spearman")

# Remove temperatures of zero to not skew histogram
hist_df = df[df["temperature"] != 0.0]["delta"]

plt.figure(figsize=(7, 4))
n, bins, patches = plt.hist(
    hist_df,
    bins=30,
    color="#1f77b4",
    edgecolor="k",
    alpha=0.75
)
plt.title("Histogram of Δ usage tokens (temp ≠ 0)")
plt.xlabel("Δ usage tokens")
plt.ylabel("Count")


hist_path = "results/delta_histogram.png"
plt.tight_layout()
plt.savefig(hist_path, dpi=300)
plt.close()


#std_by_temp = df.groupby("temperature")["delta"].std().reset_index(name="std_usage")
spearman_rank_std_correlation = df.groupby("temperature")["delta"].std().reset_index(name="std_usage").corr(method="spearman")
spearman_rank_mean_correlation = df.groupby("temperature")["delta"].mean().reset_index(name="mean_usage").corr(method="spearman")
spearman_rank_delta_correlation = df[["temperature", "delta"]].corr(method="spearman")
print(spearman_rank_std_correlation)
print(spearman_rank_mean_correlation) 

md_lines = []

md_lines.append("# Temperature Experiment Report\n")
md_lines.append("This report summarizes the effect of temperature on token usage for the experiment stored in `results_temperature_experiment_v2.csv`.\n")

md_lines.append("## Raw Token‑Usage Statistics by Temperature\n")
md_lines.append(raw_stats.to_markdown(index=False))
md_lines.append("\n---\n")

md_lines.append("## Δ (Delta) Token‑Usage Statistics by Temperature\n")
md_lines.append(delta_stats.to_markdown(index=False))
md_lines.append("\n---\n")

md_lines.append(f"### Spearman Correlation between **temperature** and **usage tokens**: **{spearman_corr:.4f}**\n")
md_lines.append("A positive value indicates that higher temperatures tend to increase token usage.\n")

md_lines.append("## Δ Token‑Usage Histogram (temp ≠ 0)\n")
md_lines.append(f"![Delta histogram]({hist_path})\n")


# Write to file
report_file = "results/temperature_experiment_report.md"
with open(report_file, "w", encoding="utf-8") as f:
    f.write("\n".join(md_lines))