# Diagnostico compacto SARIMA: Q-Q + ACF de residuos (2 paneles)
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

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


def circular_mean(angles):
    a = angles.dropna()
    return round(stats.circmean(a, high=360, low=0)) if a.size > 0 else np.nan


df = pd.read_csv(os.path.join(os.path.dirname(__file__), "..", "data", "station_15338.csv"))
df.set_index(pd.to_datetime(df["datetime"]), inplace=True)
df.drop(columns=["datetime", "unixtime"], inplace=True)
median_cols = ["wind_avg", "wind_max", "temperature", "rh", "mslp"]
df = (
    df.resample("1h")
    .agg({**{c: "median" for c in median_cols}, "wind_direction": circular_mean})
    .asfreq("1h")
)

from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.arima.model import ARIMA

serie = df["wind_avg"].ffill().bfill()
n_train = int(0.8 * len(serie))
res = ARIMA(
    serie.iloc[:n_train], order=(2, 0, 1), seasonal_order=(1, 0, 1, 24), trend="c"
).fit()
resid = res.resid.iloc[24:]  # descartar arranque

fig, axes = plt.subplots(1, 2, figsize=(12, 3.8))
import statsmodels.api as sm

sm.qqplot(resid, line="s", ax=axes[0], markersize=3)
axes[0].set_title("Q--Q residuos: colas pesadas")
plot_acf(resid, lags=48, bartlett_confint=False, ax=axes[1])
axes[1].set_title("ACF residuos: ruido blanco")
axes[1].set_xlabel("Lag (horas)")
fig.tight_layout()
fig.savefig(os.path.join(FIGS, "sarima_diag2.png"))
print("ok: sarima_diag2.png")
