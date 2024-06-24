# Hollywood
*****Descripción del Proyecto*****

Este proyecto se centra en analizar y visualizar datos de películas de Hollywood utilizando Python y Streamlit. Puedes visualizar los datos filtrando por Eras de la historia del cine en Hollywwod.
En la parte final añadimos un recomendador de peliculas y un juego donde visualizamos datos interesantes con la fecha de nacimiento de una persona.


Fué creado por Miguel Fernández y Miguel Patano para su proyecto de final de bootcamp en upgrade hub

A continuación se detalla el flujo de trabajo y los pasos necesarios para ejecutar el código correctamente.

Pasos para la Ejecución del Proyecto:

Las bases necesarias las puedes localizar en:

El usuario asaniczka creó:
https://www.kaggle.com/datasets/asaniczka/tmdb-movies-dataset-2023-930k-movies/data

La base completa de IMDB
https://developer.imdb.com/non-commercial-datasets/

*EDA y Preparación de Datos:

- Archivo: Edaimdb.ipynb
En este cuaderno realizamos el Análisis Exploratorio de Datos (EDA) sobre la base de datos de IMDB. 
Utilizamos varios archivos proporcionados por IMDB para crear un CSV consolidado con los datos necesarios para el análisis. 
El archivo resultante que exportamos es movies.csv.

*Preprocesamiento de Datos:

- Archivo: Preprocesamiento_movies_FP.ipynb
Aquí se lleva a cabo el preprocesamiento de la base de datos descargada de Kaggle. 
Nuestro objetivo es generar un CSV limpio enfocado en películas de Hollywood. 
Filtramos las películas que aún no se han estrenado para usarlas en un futuro modelo de Machine Learning. 
Además, añadimos datos faltantes como actores, directores y votaciones actualizadas desde movies.csv. 
El archivo final generado es movies_Final.csv, que utilizaremos para las visualizaciones en Streamlit y para las predicciones.


*Modelos de Machine Learning:

- Archivo: ModelosML.ipynb
En este cuaderno probamos diferentes modelos de Machine Learning para identificar cuál ofrece los resultados más precisos. 
Trabajamos extensamente con variables de texto, eliminando palabras comunes y vectorizando los textos antes de aplicar los modelos. 
El modelo que mejor resultado nos dio se exportó como top_15_movies_futuras.csv para su uso en Streamlit.

*Aplicación en Streamlit:

- Archivo: 1_🍿_Home.py
Este archivo contiene la aplicación principal de Streamlit, con las demás páginas dentro de la carpeta pages.

*Orden para Ver el Streamlit:
--1_🍿_Home.py - Detalles generales de la base de datos.
--2_💵_Información Financiera.py - Detalles financieros de las películas.
--3_❤️_Gustos.py - Detalles sobre las puntuaciones de las películas.
--4_🔍_Recomendador.py - Recomendador de películas basado en tus preferencias.
