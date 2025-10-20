# Temperature Experiment Report

This report summarizes the effect of temperature on token usage for the experiment stored in `results_temperature_experiment_v2.csv`.

## Raw Token‑Usage Statistics by Temperature

|   temperature |   Mean (tokens) |   Std (tokens) |
|--------------:|----------------:|---------------:|
|           0   |         535.939 |        274.654 |
|           0.2 |         536.293 |        272.566 |
|           0.4 |         540.611 |        271.041 |
|           0.6 |         537.607 |        265.253 |
|           0.8 |         544.993 |        263.526 |
|           1   |         541.177 |        262.383 |
|           1.2 |         538.096 |        258.865 |
|           1.4 |         536.657 |        258.369 |
|           1.6 |         530.935 |        255.534 |
|           1.8 |         523.631 |        252.78  |
|           2   |         523.605 |        253.283 |

---

## Δ (Delta) Token‑Usage Statistics by Temperature

|   temperature |     Mean Δ |    Std Δ |
|--------------:|-----------:|---------:|
|           0   |  -1.86786  |  87.8109 |
|           0.2 |  -2.27367  | 144.31   |
|           0.4 |   2.04433  | 153.505  |
|           0.6 |  -0.96     | 162.326  |
|           0.8 |   6.42667  | 176.19   |
|           1   |   2.61033  | 187.158  |
|           1.2 |  -0.470667 | 191.741  |
|           1.4 |  -1.91     | 195.618  |
|           1.6 |  -7.63133  | 196.868  |
|           1.8 | -14.9353   | 203.902  |
|           2   | -14.9617   | 211.485  |

---

### Spearman Correlation between **temperature** and **usage tokens**: **-0.0315**

A positive value indicates that higher temperatures tend to increase token usage.

## Δ Token‑Usage Histogram (temp ≠ 0)

![Delta histogram](results/delta_histogram.png)
