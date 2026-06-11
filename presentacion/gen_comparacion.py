# Regenera solo comparacion_final.png (mas ancha, sin distorsion)
import os

import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams.update(
    {
        "font.size": 15,
        "axes.titlesize": 17,
        "axes.labelsize": 16,
        "xtick.labelsize": 14,
        "ytick.labelsize": 14,
        "legend.fontsize": 14,
        "figure.dpi": 150,
        "savefig.bbox": "tight",
    }
)

FIGS = os.path.join(os.path.dirname(__file__), "figs")
H = list(range(1, 13))

bench = pd.DataFrame(
    {
        "MAE": [2.557, 2.555, 2.556, 2.555, 2.555, 2.557, 2.555, 2.558, 2.555, 2.554, 2.554, 2.552],
        "RMSE": [3.641, 3.639, 3.639, 3.639, 3.639, 3.639, 3.638, 3.640, 3.637, 3.637, 3.637, 3.636],
        "R2": [0.166, 0.169, 0.170, 0.169, 0.168, 0.168, 0.167, 0.166, 0.167, 0.167, 0.167, 0.168],
    },
    index=H,
)
sarima = pd.DataFrame(
    {
        "MAE": [1.297, 1.727, 1.894, 1.977, 2.014, 2.029, 2.044, 2.050, 2.046, 2.044, 2.045, 2.046],
        "RMSE": [1.878, 2.398, 2.586, 2.658, 2.691, 2.703, 2.720, 2.728, 2.726, 2.726, 2.728, 2.729],
        "R2": [0.778, 0.639, 0.581, 0.557, 0.545, 0.541, 0.535, 0.531, 0.532, 0.532, 0.531, 0.531],
    },
    index=H,
)
lstm = pd.DataFrame(
    {
        "MAE": [1.558, 1.889, 2.028, 2.100, 2.141, 2.171, 2.185, 2.192, 2.199, 2.211, 2.207, 2.225],
        "RMSE": [2.147, 2.589, 2.759, 2.841, 2.882, 2.907, 2.911, 2.901, 2.907, 2.915, 2.914, 2.923],
        "R2": [0.710, 0.580, 0.524, 0.494, 0.479, 0.470, 0.468, 0.472, 0.470, 0.468, 0.468, 0.464],
    },
    index=H,
)
lstm_exo = pd.DataFrame(
    {
        "MAE": [1.724, 2.098, 2.134, 2.284, 2.364, 2.331, 2.332, 2.388, 2.327, 2.331, 2.336, 2.371],
        "RMSE": [2.305, 2.764, 2.866, 3.089, 3.189, 3.122, 3.101, 3.131, 3.020, 3.035, 3.045, 3.087],
        "R2": [0.667, 0.522, 0.486, 0.402, 0.363, 0.389, 0.397, 0.385, 0.428, 0.423, 0.419, 0.403],
    },
    index=H,
)
lasso = pd.DataFrame(
    {
        "MAE": [1.436, 1.933, 2.119, 2.194, 2.205, 2.207, 2.214, 2.206, 2.191, 2.183, 2.182, 2.181],
        "RMSE": [2.026, 2.594, 2.788, 2.868, 2.880, 2.880, 2.876, 2.865, 2.847, 2.834, 2.834, 2.835],
        "R2": [0.742, 0.577, 0.511, 0.482, 0.478, 0.478, 0.479, 0.483, 0.490, 0.494, 0.494, 0.494],
    },
    index=H,
)

fig, axes = plt.subplots(1, 3, figsize=(16.5, 4))
curvas = [
    ("Benchmark", bench, "o", "gray", "--"),
    ("SARIMA", sarima, "s", "C2", "-"),
    ("Lasso", lasso, "D", "C1", "-"),
    ("LSTM", lstm, "^", "C0", "-"),
    ("LSTM-exo", lstm_exo, "v", "C3", "-"),
]
for ax, col, lab in zip(axes, ["MAE", "RMSE", "R2"], ["MAE (kt)", "RMSE (kt)", "R²"]):
    for nombre, tabla, mk, color, ls in curvas:
        ax.plot(H, tabla[col], marker=mk, ms=5, color=color, ls=ls, label=nombre)
    ax.set_xlabel("Horizonte (h)")
    ax.set_title(lab)
    ax.set_xticks(range(2, 13, 2))
axes[0].legend(fontsize=12)
fig.savefig(os.path.join(FIGS, "comparacion_final.png"))
print("ok: comparacion_final.png")
