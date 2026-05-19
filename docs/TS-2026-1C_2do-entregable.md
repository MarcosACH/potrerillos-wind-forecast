# Análisis de Series de Tiempo y Pronósticos

```
Primer cuatrimestre de 2026
2do Entregable
```

Entregar un notebook que responda a las siguientes preguntas respecto al conjunto
de datos que utilizarán en la presentación del Trabajo Práctico (TP) final. El notebook
se debe entregar en formato PDF, al igual que para la primera entrega.

Asimismo, buscamos que sumen texto en lenguaje natural al código fuente en
Python3 de manera que el reporte sea más claro y comprensible para el lector. Deben
enviar el archivo a través del Campus. No deben olvidar incluir todos los nombres y
direcciones de correo electrónico de cada integrante del grupo en el archivo. El trabajo
debe responder a las siguientes consignas:

1. Completar los autores y los datos de referencia del TP
   Grupo:
   Integrante: e-mail:
   Integrante: e-mail:
   Integrante: e-mail:

```
Título del entregable:
Enlace al conjunto de datos original:
```

1. Elaborar un resumen de hasta 100 palabras que plantee los objetivos del
   trabajo, repase los resultados del primer modelo de regresión con técnicas de
   ML y sintetice los logros alcanzados hasta esta entrega.
2. Proponer un modelo de referencia ( _benchmark_ ). ¿Qué desempeño tiene dicho
   modelo? El benchmark es un modelo simple, de fácil interpretación, que fija un
   desempeño mínimo (línea de base) contra el que comparar a los sucesivos
   modelos de creciente complejidad.
3. Analizar el proceso con las funciones de autocorrelación parcial y
   autocorrelación. Definir un modelo estocástico buscando el orden adecuado
   mediante el criterio de información de Akaike u otro equivalente. Analizar los
   residuos con el modelo ajustado para confirmar la selección de parámetros.
4. Evaluar al modelo estocástico y abordar las siguientes actividades:
   a. Explicar claramente cómo se evaluará el modelo luego de su
   entrenamiento. Recordar las técnicas de windowing vistas en clase.
   b. Informar el resultado de las métricas elegidas según la cantidad de
   pasos en el futuro considerados. Interpretar los resultados.
5. Definir un modelo que emplee redes neuronales para la predicción en los pasos
   de tiempo futuros requeridos. Evaluar distintas configuraciones y unidades
   (cantidad de capas, densas, LSTM, drop-off, retorno de secuencia, etc.).
   Recomendamos utilizar las técnicas de preprocesamiento que consideren
   adecuadas para su dataset, explicando el por qué de los pasos seleccionados
   (ej, normalización).
6. Evaluar el modelo de NN y abordar las siguientes actividades:
   a. Evaluar el modelo utilizando la misma metodología aplicada en el caso
   anterior.
   b. ¿Se puede interpretar los coeficientes como importancia de atributos?
7. Analizar y comparar los modelos obtenidos entre sí y con respecto al
   benchmark. ¿Qué modelo se elegiría para una posible fase operativo, y por
   qué?
8. ¿Cómo se podría continuar el trabajo?
