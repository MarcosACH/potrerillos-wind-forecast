# Observado vs persistencia estacional (y_{t-24}) en una ventana de test
import os

import matplotlib.dates as mdates
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

wind = df["wind_avg"].ffill().bfill()
persist = wind.shift(24)  # persistencia estacional: repite el dia anterior

win = slice("2026-03-04", "2026-03-06 23:00")
obs_w = wind.loc[win]
per_w = persist.loc[win]

fig, ax = plt.subplots(figsize=(11, 3.4))
ax.plot(obs_w.index, obs_w.values, color="C0", lw=2, label="Observado")
ax.plot(per_w.index, per_w.values, color="C1", lw=2, ls="--", label="Persistencia ($y_{t-24}$)")
ax.set_ylabel("wind_avg (kt)")
ax.set_title("Persistencia estacional: repite el día anterior (ventana de test)")
ax.xaxis.set_major_locator(mdates.DayLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter("%d-%b"))
ax.margins(x=0.01)
ax.legend(ncols=2, loc="upper left")
fig.savefig(os.path.join(FIGS, "obs_vs_persistencia.png"))
print("ok: obs_vs_persistencia.png")
