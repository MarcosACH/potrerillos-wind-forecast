## **Análisis de Series de Tiempo y Pronósticos** 

## Primer cuatrimestre de 2026 

1er Entregable 

Entregar un notebook que responda a las siguientes preguntas respecto al conjunto de datos que utilizarán para el Trabajo Práctico (TP) final. El notebook se debe entregar en formato PDF el cual se puede generar desde Colab. Para ello, se selecciona “Print”, desde las opciones en “File”, y se debe elegir guardar en PDF en lugar de enviarlo a una impresora. (Existen otras opciones para generar el PDF que pueden explorar. Encontrarán algunas sugerencias en la sección de _Complementos_ en el Campus Virtual). 

Buscamos que sumen texto en lenguaje natural al código fuente en Python3 de manera que el reporte sea más claro y comprensible para el lector. Deben enviar el archivo  a  través  del  Campus.  No  deben  olvidar  incluir  todos  los  nombres  y direcciones de correo electrónico de cada integrante del grupo en el archivo. El trabajo debe responder a las siguientes consignas: 

1. Completar los autores y los datos de referencia del TP Grupo: Integrante: e-mail: Integrante: e-mail: Integrante: e-mail: 

Título del entregable: Enlace al conjunto de datos original: 

2. Describir brevemente el conjunto de datos, incluyendo su origen. Tengan en cuenta que esto  no solamente refiere al  repositorio  donde  obtuvieron el conjunto de datos sino que, tal vez, tengan que investigar cómo se obtuvo o dónde se generó. 

3. Exponer el problema o pregunta a resolver. Tiene que quedar claro cuál es el la predicción deseada, y con qué métrica ó métricas esperan evaluar el modelo. Asimismo, informar cuál es el horizonte de pronóstico, y cómo y cuántos pasos en el futuro se predecirán. 

## 4. Explorar el conjunto de datos: 

- a. ¿Por qué considera que el conjunto de datos debe ser abordado como una serie de tiempo? 

- b. ¿Cómo se relaciona un paso con el avance de tiempo real? ¿Cuáles son los valores mínimos y máximos para el índice de tiempo? 

   - c. ¿Hay valores faltantes? ¿Cómo se puede completar la información faltante y cómo afectaría en el análisis posterior? 

   - d. Analizar  los  tipos  de  datos  presentes.  ¿Cuáles  son  variables endógenas y cuáles exógenas? 

   - e. Analizar la presencia de tendencias, efectos estacionales, y/o ciclos. 

   - f. Informar si se trata de un problema estacionario. Eventualmente, ¿se puede extraer una serie estacionaria de residuos? 

   - g. Estudiar la autocorrelación para la variable de interés. h. ¿Cuál  es  el  período  entre  registros?  ¿Cómo  es  el  espectro  de potencias? 

5. Dada la serie propuesta, proponer un modelo de regresión (lineal, LASSO, K- NN, árboles, etc.) para predecir el valor de la variable dentro del horizonte de pronóstico previsto. Explicar la elección del modelo de regresión y evaluar su desempeño. Comparar el desempeño con un modelo trivial como linea de base. 

