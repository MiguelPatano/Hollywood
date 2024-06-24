# Exploring Hollywood Cinema
*****Descripción del Proyecto*****

Este proyecto se centra en analizar y visualizar datos de películas de Hollywood utilizando Python y Streamlit. Puedes visualizar los datos filtrando por Eras de la historia del cine en Hollywwod.
En la parte final añadimos un recomendador de peliculas y un juego donde visualizamos datos interesantes con la fecha de nacimiento de una persona.


Fué creado por:
Miguel Fernández:https://github.com/MIGUEL98FDEZ
Miguel Patano: https://github.com/MiguelPatano/

para su proyecto de final de bootcamp en upgrade hub

Para la división por eras en el cine de Hollywood usamos:

1. Era del Cine Mudo (1890s-1920s)
Características: Las primeras películas eran mudas y en blanco y negro. La narrativa visual y la actuación eran muy expresivas debido a la ausencia de sonido.
Eventos Clave:
1895: Primera proyección de los hermanos Lumière.
1903: "El gran robo del tren", una de las primeras películas de acción narrativa.
1927: Estreno de "El cantante de jazz", la primera película sonora parcial que marcó el fin de esta era.
2. Era del Cine Clásico de Hollywood (1930s-1940s)
Características: Desarrollo del cine sonoro, auge de los grandes estudios de Hollywood y el sistema de estrellas.
Eventos Clave:
1939: Estrenos de "Lo que el viento se llevó" y "El mago de Oz".
1941: Estreno de "Ciudadano Kane", a menudo considerada una de las mejores películas de todos los tiempos.
3. Era de la Postguerra y la Edad de Oro del Cine (1950s-1960s)
Características: Expansión del cine a nivel mundial, surgimiento del cine de autor, y la aparición del cine en color como estándar.
Eventos Clave:
1954: Estreno de "La ventana indiscreta" de Hitchcock.
1957: "El séptimo sello" de Ingmar Bergman.
1960: "Psicosis" de Alfred Hitchcock.
4. Era del Nuevo Hollywood y el Cine Moderno (1970s-1980s)
Características: Revolución en las técnicas de narración, auge de los directores-autor, y el nacimiento de los blockbusters.
Eventos Clave:
1972: Estreno de "El padrino".
1977: Estreno de "Star Wars".
1982: Estreno de "E.T., el extraterrestre".
5. Era del Cine Contemporáneo y la Globalización (1990s-presente)
Características: Avances tecnológicos significativos (CGI, efectos especiales), globalización de la industria, y el surgimiento del cine digital.
Eventos Clave:
1993: Estreno de "Jurassic Park", que revolucionó los efectos especiales.
1997: Estreno de "Titanic", que se convirtió en la película más taquillera hasta ese momento.
2009: Estreno de "Avatar", otra revolución en los efectos especiales y 3D.
2010s en adelante: Crecimiento de las plataformas de streaming y cambios en la forma de distribución y consumo de cine.

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
