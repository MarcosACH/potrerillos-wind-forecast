# Presentación final — Pronóstico de viento en Potrerillos

Estructura: 14 slides de contenido (slide 11 dividida en 11 y 11b) + portada + cierre. ~15 min. Slides solo con palabras clave + figuras (sin texto corrido).
Guion oral: lo que se dice mientras se muestra la slide.

---

## Portada (no cuenta)

**En slide:**
- Título: *Pronóstico de viento en Potrerillos*
- Análisis de Series de Tiempo y Pronósticos
- UNSaM
- Fecha de la presentación

---

## Slide 1 — Datos del grupo (obligatoria)

**En slide:**
- Grupo: **9**
- Marcos Achaval — machavalrodriguez@unsam-bue.edu.ar
- Lucas Achaval — lachavalrodriguez@estudiantes.unsam.edu.ar
- Título: Pronóstico de viento en Potrerillos
- Dataset: https://www.windguru.cz/station/15338

**Guion (30 s):** Presentación rápida de integrantes y fuente de datos.

---

## Slide 2 — Problema y objetivo

**En slide (keywords):**
- Potrerillos, Mendoza — viento térmico
- Estación **Ecowitt WS90** (club náutico)
- Endógena: `wind_avg` (nudos)
- Exógenas: `wind_max`, `temperatura`, `humedad`, `presión`, `dirección`
- Objetivo: pronóstico a **12 horas** (1 predicción por hora)

**Figura:** foto/mapa de Potrerillos o screenshot estación Windguru (opcional, da contexto visual).

**Guion (1 min):**
- Potrerillos: embalse en montaña, actividad náutica/kitesurf depende del viento térmico.
- Pregunta práctica: ¿habrá viento navegable en las próximas 12 horas?
- Endógena: velocidad media. Exógenas: las demás variables de la estación, elegidas por disponibilidad y relación física con el viento térmico (gradiente térmico → viento).

---

## Slide 3 — Datos

**En slide (keywords):**
- Rango: **ago 2025 → abr 2026** (~8.5 meses)
- Original: 1 dato/min → **resampleo 1 h** (6145 obs)
- Mediana (variables lineales) · **media circular** (dirección)
- Faltantes: 4.5 %, 12 gaps de estación → **sin imputar**

**Figura:** gráfico de la serie completa con gaps visibles (si existe en E1) o timeline de gaps.

**Guion (1 min):**
- Frecuencia original minutal, agregamos a horario: mediana por robustez a outliers; dirección con media circular (350°→10° no promedia 180°).
- Faltantes = estación offline (gaps completos, no puntos aislados). 85 % del faltante en gaps >24 h.
- Decisión: no imputar — interpolar gaps largos en el período térmico (10–19 h) inventaría justo lo que queremos predecir.

---

## Slide 4 — EDA: ciclo diurno

**En slide (keywords):**
- Ciclo térmico diario
- Calma nocturna ~1–2 kt · pico 11–16 h ~7–9 kt
- Sin tendencia de largo plazo

**Figuras:**
- E1: barras "mediana de viento por hora del día" (con franja térmica 10–19 h)
- E1: descomposición aditiva (período 24 h) — 4 paneles

**Guion (1 min):**
- El viento es casi un reloj: calma de noche, sube con el calentamiento diurno, pico al mediodía-tarde.
- Descomposición: tendencia plana (no hay deriva en 8 meses), estacionalidad diaria fuerte y estable, residuo chico.

---

## Slide 5 — ACF/PACF y estacionariedad

**En slide (keywords):**
- ACF lag 24: **+0.5** (el patrón se repite cada día)
- ACF lag 12: **negativo** (espejo día/noche)
- PACF: solo lags **1–2 y 20–24**
- ADF: p ≈ 7.58×10⁻²¹ → **estacionaria** (sin diferenciar)

**Figura:** E1: ACF + PACF (2 paneles, 48 lags).

**Guion (1.5 min):**
- ACF: fuerte memoria corta (lags 1–2), correlación negativa a 12 h (si sopló al mediodía, calma a medianoche), positiva a 24 h: ayer a esta hora explica ~25 % de la varianza de hoy.
- PACF: la información directa está solo en las últimas 1–2 horas y en el valor de hace ~24 h — el resto es correlación heredada.
- ADF rechaza raíz unitaria con mucho margen → trabajamos la serie sin diferenciar (d=0).
- Esto ya anticipa la estructura del modelo estocástico: AR corto + componente estacional de 24 h.

---

## Slide 6 — Dominio de la frecuencia

**En slide (keywords):**
- Periodograma: pico dominante **1 ciclo/día**
- Secundario débil: 2 ciclos/día
- Sin periodicidades multi-día

**Figura:** E1: periodograma + espectro suavizado (2 paneles).

**Guion (1 min):**
- El espectro confirma lo del dominio del tiempo: casi toda la potencia en 24 h.
- Pico secundario en 12 h refleja la oscilación día/noche en antifase.
- Conclusión: la dinámica es forzante térmico diario puro — un solo período estacional, S=24.

---

## Slide 7 — Metodología y benchmark

**En slide (keywords):**
- Walk-forward · horizonte **h = 1…12** · MAE / RMSE / R² por horizonte
- Split 80/20 cronológico
- Benchmark: **persistencia estacional** → ŷ(t+h) = y(t+h−24)
- RMSE **3.6 kt** · MAE 2.6 kt · R² 0.17

**Figura:** E2: métricas del benchmark por horizonte (perfil plano).

**Guion (1.5 min):**
- Misma metodología para todos los modelos: entrenamiento en el 80 % inicial, evaluación walk-forward sobre el test, métricas por cada uno de los 12 horizontes.
- Benchmark: "mañana a esta hora va a soplar lo mismo que hoy" — natural dado el ACF de 0.5 en lag 24.
- Perfil de error plano (no usa historia reciente). Es la vara: cualquier modelo debe superarlo para justificar su complejidad.

---

## Slide 8 — Modelo de ML: LassoCV

**En slide (keywords):**
- 31 features: **24 lags** + 5 exógenas + **sin/cos hora**
- L1 → selección automática de features · gap = 12 h (sin fuga)
- RMSE **2.8 kt** (−24 % vs benchmark) · R² 0.52

**Figuras:**
- E2: importancia Lasso (coeficientes en h=1, coloreados por grupo: lags / exógenas / hora) — `lasso_importancia.png`
- E2: RMSE por horizonte Lasso vs benchmark — `lasso_vs_bench.png`

**Guion (1.5 min):**
- Features: la historia (24 lags), el contexto meteorológico (exógenas) y la hora codificada circularmente (hora 23 y 0 son vecinas).
- Windowing con gap de 12 h: el test nunca ve datos que el modelo no tendría al predecir (metodología detallada en slide 7).
- El L1 apaga features irrelevantes solo — regularización elegida por CV.
- **Importancia (h=1, el horizonte más útil para navegar):** largo de barra = importancia, signo = dirección. Domina `wind_max` —proxy del viento actual, no info meteorológica nueva— seguido de la hora y algunos lags estacionales; las exógenas meteorológicas puras (temp, humedad, presión, dirección) quedan en ~0. Refuerza que la señal vive en el propio viento + ciclo diario. (Ver *Preguntas anticipadas*: signo negativo y por qué `temperature` ≈ 0 no contradice el viento térmico.)
- Resultado: −24 % de RMSE; generaliza bien (sin overfitting).

---

## Slide 9 — Modelo superador: SARIMA — selección

**En slide (keywords):**
- ACF/PACF → AR corto + estacional S=24, d=D=0
- Grid search por **AIC**: p ∈ {0,1,2} · q ∈ {0,1} · P,Q ∈ {0,1} (24 combinaciones)
- Elegido: **SARIMA(2,0,1)(1,0,1,24)** — AIC 20496

**Figura:** E2: tabla top-5 del grid AIC.

**Guion (1.5 min):**
- La elección del modelo estocástico sale directo del análisis: estacionariedad (sin diferenciar) y estructura AR + estacional de 24 h.
- Optimización de hiperparámetros = orden del modelo, vía AIC sobre una grilla (tal como sugiere la consigna).
- Ganó (2,0,1)(1,0,1,24) por margen estrecho sobre (1,0,1)(1,0,1,24) — la estructura estacional es lo no negociable.

---

## Slide 10 — SARIMA: diagnóstico y resultados

**En slide (keywords):**
- Ljung-Box ✓ → residuos sin autocorrelación
- Q-Q: **colas pesadas** (extremos de viento)
- RMSE **2.6 kt** (−28 %) · MAE 1.9 kt · R² 0.57
- h=1: RMSE 1.9 · R² 0.78

**Figuras:**
- E2: diagnóstico de residuos (Q-Q + ACF de residuos)
- E2: MAE/RMSE/R² por horizonte, SARIMA vs benchmark

**Guion (1.5 min):**
- Ljung-Box: los residuos son ruido blanco → el orden capturó toda la estructura temporal.
- Q-Q muestra colas pesadas: el supuesto gaussiano subestima extremos — limitación honesta (motiva GARCH como trabajo futuro).
- Mejor modelo: −28 % RMSE vs benchmark. A 1 hora, R² 0.78; degrada rápido hasta h=3 y luego meseta.

---

## Slide 11 — Alternativas: redes neuronales — RMSE por horizonte

**En slide (keywords):**
- Dense / LSTM · ventana **W=48** · salida directa H=12
- LSTM: RMSE **2.8 kt** — no supera a SARIMA

**Figura:** E2: RMSE por horizonte — LSTM, LSTM-exo y SARIMA (ref.) vs benchmark (`nn_vs_bench.png`).

**Guion (1 min):**
- Validamos si más capacidad ayuda: ventana de 48 h (2 ciclos), salida directa de 12 pasos, early stopping.
- Probamos 3 configuraciones (Dense, LSTM, LSTM-2capas); elegimos la LSTM simple por menor val loss y parsimonia.
- La LSTM queda apenas por detrás de SARIMA con mucha más complejidad.

---

## Slide 11b — Alternativas: redes neuronales — validación vs test

**En slide (keywords):**
- LSTM + exógenas: val loss ↓ (0.567) pero test RMSE ↑ (2.98 kt) → **overfitting**
- Las exógenas pasadas **no aportan** a resolución horaria

**Figura:** E2: val loss vs test RMSE de LSTM vs LSTM-exo (`nn_overfit.png`).

**Guion (1 min):**
- Hallazgo interesante: agregar exógenas mejora validación pero empeora test — aprenden patrones espurios. La historia del propio viento + el ciclo de 24 h ya contienen la señal.
- Esto refuerza la elección de SARIMA: la dinámica es autorregresiva + estacional, y el modelo simple la captura.

---

## Slide 12 — Comparación final

**En slide:** tabla + figura, sin texto.

| Modelo | MAE (kt) | RMSE (kt) | R² | Δ RMSE |
|---|---|---|---|---|
| **SARIMA(2,0,1)(1,0,1,24)** | **1.9** | **2.6** | **0.57** | **−28 %** |
| Lasso | 2.1 | 2.8 | 0.52 | −24 % |
| LSTM | 2.1 | 2.8 | 0.51 | −23 % |
| LSTM-exo | 2.3 | 3.0 | 0.44 | −18 % |
| Persistencia estacional | 2.6 | 3.6 | 0.17 | — |

**Figura:** E2: overlay RMSE por horizonte de los 5 modelos.

**Guion (1.5 min):**
- Todos superan al benchmark; SARIMA gana en las tres métricas.
- El orden de mérito es inverso a la complejidad: estocástico > lineal > red > red multivariada.
- Patrón común: error crece rápido h=1→3 y luego meseta — pasadas ~3 h, lo que sostiene la predicción es el ciclo diario, no la historia reciente.

---

## Slide 13 — Conclusiones y trabajo futuro

**En slide (keywords):**

Conclusiones:
- Viento térmico ≈ reloj: **ciclo 24 h domina** (tiempo + frecuencia)
- **SARIMA(2,0,1)(1,0,1,24)**: −28 % RMSE — simple y suficiente
- Exógenas pasadas: no mejoran (hasta perjudican)

Futuro:
- **SARIMAX** (exógenas dentro del mejor modelo)
- **GARCH** → intervalos honestos (colas pesadas)
- Encoding circular de dirección (sin/cos)
- Exógenas **pronosticadas** (NWP) para horizontes largos

**Guion (1 min):**
- La señal está en la propia serie: estructura AR corta + ciclo térmico de 24 h. El modelo estocástico clásico, bien diagnosticado, le gana a alternativas más complejas.
- Futuro: probar exógenas dentro de SARIMA (SARIMAX); modelar varianza condicional para intervalos realistas en extremos; y la apuesta más prometedora — usar *pronósticos* meteorológicos como exógenas, no valores pasados.

---

## Notas generales

- Métricas redondeadas a 2 cifras significativas (consigna).
- Usar siempre los números de E2 (misma metodología walk-forward para todos los modelos).
- Fuente ≥16 pt en todo, incluidas leyendas y escalas de gráficos → regenerar figuras de los notebooks con `fontsize` grande antes de exportar.
- Tiempos: 30s + 1+1+1+1.5+1+1.5+1.5+1.5+1.5+1+1+1.5+1 ≈ 15 min (slides 11 y 11b ~1 min c/u).

## Preguntas anticipadas (defensa)

Material de respaldo para Q&A, sobre todo del gráfico de importancia (slide 8) y la metodología de pronóstico multi-horizonte.

**¿Un coeficiente negativo significa "menos importante"?**
No. Sobre features estandarizadas, el **signo = dirección** de la relación y el **tamaño (`|coef|`) = importancia**. Una barra larga hacia la izquierda importa tanto como una hacia la derecha. Ej.: `cos hora` negativo *codifica* el ciclo diario — `cos = +1` a medianoche empuja el viento hacia abajo (calma nocturna), `cos = −1` al mediodía lo empuja hacia arriba (pico diurno). El signo es la física correcta, no un defecto.

**Si el viento es térmico, ¿por qué `temperature` ≈ 0?**
No se contradice. "Térmico" es el **driver físico** (ciclo de calentamiento), no el valor del termómetro en `t`. Tres razones:
- **Redundancia:** ese ciclo ya lo capturan `sin/cos hora` + los lags del propio viento → la temperatura no agrega info nueva y L1 la apaga por colinealidad (cero por redundancia, no por irrelevancia).
- **Es el gradiente, no el valor absoluto:** el viento térmico lo mueve la *diferencia* de temperatura (valle/ladera, tierra/agua) y la *tasa* de calentamiento; un único termómetro no mide ese gradiente.
- **Analogía:** las mareas las causa la Luna, pero se predicen con la tabla de mareas (el ciclo), no midiendo la Luna en vivo. El modelo **sí** usa la señal térmica — vía hora + periodicidad del viento, proxies más limpios que el grado de temperatura.

**¿Por qué Lasso ajusta 12 modelos (uno por horizonte) y SARIMA/LSTM uno solo?** Todos usan *direct/recursive multi-step*, pero distinto:
- **LSTM (1 fit):** una red con capa final `Dense(12)`. La celda LSTM comprime la ventana en una representación oculta **compartida**; las 12 salidas son 12 cabezas lineales que leen ese mismo estado. Se entrenan juntas en una pasada.
- **SARIMA (1 fit):** una ecuación generativa que se **itera** hacia adelante (recursivo). Los pesos efectivos por horizonte salen como `φʰ` — distintos en cada `h` pero **derivados** de un único coeficiente, no re-estimados.
- **Lasso (12 fits):** `ŷ = w·x` tiene salida escalar y no hay ni cuerpo compartido ni ecuación que iterar. Para 12 targets distintos hacen falta 12 vectores de pesos → 12 modelos (*direct multi-step*; se eligió sobre el recursivo para no acumular error de iteración).
- En una frase: **la LSTM ramifica, SARIMA itera, Lasso replica.**

## Pendientes

- [x] Datos del grupo y emails (slide 1) — Grupo 9, ambos integrantes
- [x] Link del dataset confirmado (windguru.cz/station/15338)
- [x] Slide 2 sin imagen: solo texto (estación Ecowitt WS90)
- [x] Figura de serie completa con gaps (`serie_completa.png`)
- [ ] Verificar fuente ≥16 pt en leyendas/escalas: `gen_figs.py` usa 14 pt en ticks y leyenda
- [ ] Confirmar que la estación es "Ecowitt WS90" (dato de slide 2, no figura en los notebooks)
- [x] Importancia de parámetros (consigna pto 8): bar de coeficientes Lasso en h=1 (slide 8)
