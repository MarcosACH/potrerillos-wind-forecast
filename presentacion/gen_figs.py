# Genera todas las figuras de la presentacion con fuentes grandes (consigna >=16pt)
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
os.makedirs(FIGS, exist_ok=True)


def save(fig, name):
    fig.savefig(os.path.join(FIGS, name))
    plt.close(fig)
    print("ok:", name)


# ---------- datos ----------
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

wind = df["wind_avg"]

# ---------- 1. serie completa con gaps ----------
fig, ax = plt.subplots(figsize=(11, 3.6))
ax.plot(wind.index, wind.values, lw=0.4, color="steelblue")
is_nan = wind.isna()
gid = (~is_nan).cumsum()
for _, g in wind[is_nan].groupby(gid[is_nan]):
    ax.axvspan(g.index[0], g.index[-1], color="red", alpha=0.25)
ax.set_ylabel("wind_avg (kt)")
ax.set_title("Serie horaria completa — en rojo: estación offline (4.5 %)")
ax.margins(x=0.01)
save(fig, "serie_completa.png")

# ---------- 2. mediana por hora ----------
hourly = wind.dropna().groupby(wind.dropna().index.hour).median()
fig, ax = plt.subplots(figsize=(10, 3.8))
ax.bar(
    hourly.index,
    hourly.values,
    color=["orange" if 10 <= h <= 19 else "steelblue" for h in hourly.index],
)
ax.set_xlabel("Hora del día")
ax.set_ylabel("Mediana wind_avg (kt)")
ax.set_title("Mediana de viento por hora — naranja: período térmico (10–19 h)")
ax.set_xticks(range(0, 24, 2))
save(fig, "mediana_hora.png")

# ---------- 3. descomposicion aditiva ----------
from statsmodels.tsa.seasonal import seasonal_decompose

wind_filled = wind.ffill().bfill()
sd = seasonal_decompose(wind_filled, model="additive", period=24, extrapolate_trend=0)
fig, axes = plt.subplots(4, 1, figsize=(11, 7), sharex=True)
for ax, comp, name in zip(
    axes,
    [sd.observed, sd.trend, sd.seasonal, sd.resid],
    ["Observada", "Tendencia", "Estacional (24 h)", "Residuo"],
):
    ax.plot(comp.index, comp.values, lw=0.4)
    ax.set_ylabel(name, fontsize=13)
    ax.margins(x=0.01)
axes[0].set_title("Descomposición aditiva de wind_avg (período = 24 h)")
save(fig, "descomposicion.png")

# ---------- 4. ACF / PACF ----------
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

fig, axes = plt.subplots(1, 2, figsize=(12, 4))
plot_acf(wind.dropna(), lags=48, bartlett_confint=False, ax=axes[0])
axes[0].set_title("ACF — wind_avg")
axes[0].set_xlabel("Lag (horas)")
plot_pacf(wind.dropna(), lags=48, ax=axes[1])
axes[1].set_title("PACF — wind_avg")
axes[1].set_xlabel("Lag (horas)")
for ax in axes:
    ax.axvline(24, color="red", ls=":", lw=1.5, alpha=0.7)
save(fig, "acf_pacf.png")

# ---------- 5. periodograma ----------
wind_centered = wind_filled - wind_filled.mean()
NT = len(wind_centered)
wind_f = np.fft.rfft(wind_centered.values)
armonics = np.arange(0, len(wind_f))
wind_f_adj = wind_f * 2 / NT
sqamp = np.real(wind_f_adj) ** 2 + np.imag(wind_f_adj) ** 2
freqs_per_day = armonics * 24 / NT
mw = 10
weights = np.ones(2 * mw + 1)
ps = 0.5 * np.convolve(NT * sqamp, weights, mode="same") / (2 * mw + 1)
ps = ps[mw :: 2 * mw + 1]
fs = armonics[mw :: 2 * mw + 1] * 24 / NT

fig, axes = plt.subplots(1, 2, figsize=(12, 3.8))
axes[0].stem(freqs_per_day, sqamp, markerfmt="C0o", basefmt="C0-", linefmt="C0-")
axes[0].set_xscale("log")
axes[0].set_xlabel("Frecuencia (ciclos/día)")
axes[0].set_title("Periodograma")
axes[0].axvline(x=1, color="r", linestyle="--", label="1/día")
axes[0].axvline(x=2, color="orange", linestyle="--", label="2/día")
axes[0].legend(loc="upper right")
axes[1].plot(fs, ps)
axes[1].set_xscale("log")
axes[1].set_xlabel("Frecuencia (ciclos/día)")
axes[1].set_title("Espectro de potencias (suavizado)")
axes[1].axvline(x=1, color="r", linestyle="--")
axes[1].axvline(x=2, color="orange", linestyle="--")
save(fig, "periodograma.png")

# ---------- tablas de metricas por horizonte (outputs de entregable_2_exo) ----------
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

# ---------- 6. benchmark por horizonte ----------
fig, axes = plt.subplots(1, 3, figsize=(13, 3.8))
for ax, col, lab in zip(axes, ["MAE", "RMSE", "R2"], ["MAE (kt)", "RMSE (kt)", "R²"]):
    ax.plot(H, bench[col], marker="o", color="steelblue")
    ax.set_xlabel("Horizonte (h)")
    ax.set_title(lab)
    ax.set_xticks(range(2, 13, 2))
fig.subplots_adjust(wspace=0.45)
fig.suptitle("Persistencia estacional — perfil plano: no usa historia reciente", y=1.04)
save(fig, "benchmark_horizonte.png")

# ---------- 7. esquema de windowing (TimeSeriesSplit con gap) ----------
fig, ax = plt.subplots(figsize=(11, 3.4))
n = 100
folds = [(0, 40, 52, 64), (0, 58, 70, 82), (0, 76, 88, 100)]
for k, (t0, t1, s0, s1) in enumerate(folds):
    y = 2 - k
    ax.barh(y, t1 - t0, left=t0, height=0.55, color="steelblue", label="Train" if k == 0 else None)
    ax.barh(y, s0 - t1, left=t1, height=0.55, color="lightgray", label="Gap = 12 h" if k == 0 else None)
    ax.barh(y, s1 - s0, left=s0, height=0.55, color="orange", label="Test" if k == 0 else None)
ax.set_yticks([2, 1, 0])
ax.set_yticklabels(["Fold 1", "Fold 2", "Fold 3"])
ax.set_xticks([])
ax.set_xlabel("Tiempo →")
ax.set_title("TimeSeriesSplit (3 folds, gap = horizonte) — sin fuga de información")
ax.legend(loc="upper left", ncols=3, bbox_to_anchor=(0, -0.18))
ax.set_xlim(0, n)
save(fig, "windowing.png")

# ---------- 8. lasso vs benchmark ----------
fig, ax = plt.subplots(figsize=(8.5, 4.2))
ax.plot(H, bench["RMSE"], marker="o", ls="--", color="gray", label="Persistencia estacional")
ax.plot(H, lasso["RMSE"], marker="s", color="C0", label="LassoCV")
ax.set_xlabel("Horizonte (h)")
ax.set_ylabel("RMSE (kt)")
ax.set_title("RMSE por horizonte — Lasso vs benchmark")
ax.set_xticks(range(2, 13, 2))
ax.legend()
save(fig, "lasso_vs_bench.png")

# ---------- 8b. importancia de atributos Lasso (h=1) ----------
from matplotlib.patches import Patch
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.linear_model import LassoCV
from sklearn.model_selection import TimeSeriesSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

N_LAGS = 24
EXOG = ["wind_max", "temperature", "rh", "mslp", "wind_direction"]
serie = df["wind_avg"].ffill().bfill()
n_train = int(0.8 * len(serie))


class LagFeatures(TransformerMixin, BaseEstimator):
    def __init__(self, lags=1):
        self.lags = lags

    def fit(self, X, y=None):
        self.X_mean = X.mean()
        return self

    def transform(self, X):
        out = pd.DataFrame(index=X.index)
        for col in X.columns:
            for lag in range(1, self.lags + 1):
                out[f"{col}_Lag_{lag}"] = X[col].shift(lag, fill_value=self.X_mean[col])
        return out


def crear_features(obj, exog, h):
    X = pd.concat([exog, LagFeatures(lags=N_LAGS).fit_transform(obj.to_frame())], axis=1)
    X["hora_sin"] = np.sin(2 * np.pi * X.index.hour / 24)
    X["hora_cos"] = np.cos(2 * np.pi * X.index.hour / 24)
    y = obj.shift(-h).rename("objetivo")
    return pd.concat([X, y], axis=1).dropna()


lasso_imp = Pipeline(
    [
        ("scaler", StandardScaler()),
        ("modelo", LassoCV(cv=TimeSeriesSplit(n_splits=3), max_iter=20000,
                           n_jobs=-1, alphas=np.logspace(-4, 1, 100))),
    ]
)
df_ml = df.ffill().bfill()
split_ts = serie.index[n_train]
gap = pd.Timedelta(hours=12)
datos = crear_features(df_ml["wind_avg"], df_ml[EXOG], 1)
train = datos[datos.index < split_ts - gap]
lasso_imp.fit(train.drop(columns="objetivo"), train["objetivo"])
coef = pd.Series(lasso_imp.named_steps["modelo"].coef_, index=train.drop(columns="objetivo").columns)
top = coef.reindex(coef.abs().sort_values().index).tail(12)


def _grupo(n):
    if n in EXOG:
        return "Exógenas"
    if n.startswith("hora"):
        return "Hora (sin/cos)"
    return "Lags wind_avg"


def _etiqueta(n):
    if n.startswith("wind_avg_Lag_"):
        return "lag " + n.split("_")[-1]
    return {"hora_sin": "sin hora", "hora_cos": "cos hora"}.get(n, n)


cmap = {"Lags wind_avg": "C0", "Exógenas": "C3", "Hora (sin/cos)": "C1"}
colors = [cmap[_grupo(n)] for n in top.index]
fig, ax = plt.subplots(figsize=(8.5, 4.2))
ax.barh(range(len(top)), top.values, color=colors)
ax.set_yticks(range(len(top)))
ax.set_yticklabels([_etiqueta(n) for n in top.index])
ax.axvline(0, color="gray", lw=0.8)
ax.set_xlabel("Coeficiente (features estandarizadas)")
ax.set_title("Importancia Lasso (h = 1)")
ax.legend(
    handles=[Patch(color=cmap[g], label=g) for g in ["Lags wind_avg", "Exógenas", "Hora (sin/cos)"]],
    loc="lower right",
)
save(fig, "lasso_importancia.png")

# ---------- 9. SARIMA vs benchmark (3 paneles) ----------
fig, axes = plt.subplots(1, 3, figsize=(13, 3.8))
for ax, col, lab in zip(axes, ["MAE", "RMSE", "R2"], ["MAE (kt)", "RMSE (kt)", "R²"]):
    ax.plot(H, bench[col], marker="o", ls="--", color="gray", label="Benchmark")
    ax.plot(H, sarima[col], marker="s", color="C2", label="SARIMA")
    ax.set_xlabel("Horizonte (h)")
    ax.set_title(lab)
    ax.set_xticks(range(2, 13, 2))
axes[0].legend()
save(fig, "sarima_vs_bench.png")

# ---------- 10. hallazgo exogenas: val loss vs test RMSE ----------
fig, axes = plt.subplots(1, 2, figsize=(10, 3.8))
labels = ["LSTM", "LSTM-exo"]
val = [0.635, 0.567]
test = [2.800, 2.980]
colors = ["C0", "C3"]
axes[0].bar(labels, val, color=colors, width=0.55)
axes[0].set_title("Val loss ↓")
axes[0].set_ylim(0.5, 0.66)
axes[1].bar(labels, test, color=colors, width=0.55)
axes[1].set_title("Test RMSE (kt) ↑")
axes[1].set_ylim(2.6, 3.05)
for ax, vals in zip(axes, [val, test]):
    for i, v in enumerate(vals):
        ax.text(i, v, f" {v:.2f}", ha="center", va="bottom", fontsize=14)
fig.suptitle("Exógenas: mejor en validación, peor en test → overfitting", y=1.06)
save(fig, "nn_overfit.png")

# ---------- 11. redes vs benchmark ----------
fig, ax = plt.subplots(figsize=(8.5, 4.2))
ax.plot(H, bench["RMSE"], marker="o", ls="--", color="gray", label="Persistencia estacional")
ax.plot(H, lstm["RMSE"], marker="^", color="C0", label="LSTM")
ax.plot(H, lstm_exo["RMSE"], marker="v", color="C3", label="LSTM-exo")
ax.plot(H, sarima["RMSE"], marker="s", color="C2", ls=":", label="SARIMA (ref.)")
ax.set_xlabel("Horizonte (h)")
ax.set_ylabel("RMSE (kt)")
ax.set_title("RMSE por horizonte — redes neuronales")
ax.set_xticks(range(2, 13, 2))
ax.legend()
save(fig, "nn_vs_bench.png")

# ---------- 12. comparacion final ----------
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
save(fig, "comparacion_final.png")

# ---------- 13. diagnostico SARIMA (refit) ----------
from statsmodels.tsa.arima.model import ARIMA

serie = wind.ffill().bfill()
n_train = int(0.8 * len(serie))
serie_train = serie.iloc[:n_train]
print("ajustando SARIMA(2,0,1)(1,0,1,24)...")
res = ARIMA(serie_train, order=(2, 0, 1), seasonal_order=(1, 0, 1, 24), trend="c").fit()
print("AIC:", round(res.aic, 2))
fig = res.plot_diagnostics(figsize=(12, 7), lags=48)
fig.tight_layout()
save(fig, "sarima_diag.png")

print("LISTO")
