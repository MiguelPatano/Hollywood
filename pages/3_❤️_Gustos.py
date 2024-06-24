import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

# Cargar datos
data = pd.read_csv("movies_Final.csv")

st.set_page_config(page_title="Películas IMDB", page_icon=":popcorn:", layout="wide", initial_sidebar_state="expanded")

# Color de fondo de la barra lateral
sidebar_style = """
<style>
.css-1d391kg {
  background-color: #2F4F4F !important;
  color: white !important;
}
</style>
"""

# Colocamos los estilos CSS
st.markdown(
    f"""
    <style>
    .main {{
        background-color: #2F4F4F;  /* Tono más oscuro de marfil (oscuro) */
        color: white;
    }}
    .stButton>button {{
        color: white;
        background-color: #3B3B3B;  /* Botón con color de fondo oscuro */
    }}
    h1, h2, h3 {{
        color: #FFD700;  /* Dorado */
    }}
    .metric-container {{
        border: 2px solid #FFD700;  /* Borde amarillo */
        border-radius: 10px;  /* Bordes redondeados */
        padding: 10px;  /* Espaciado interno */
        margin: 5px 0;  /* Espaciado externo */
        text-align: center;  /* Alineación central */
        color: white;  /* Texto en blanco */
    }}
    .metric-value {{
        font-size: 2em;
        color: white;
    }}
    .metric-label {{
        color: white;
    }}
    .css-1d391kg, .css-1r6slb0 {{
        background-color: #2F4F4F !important;  /* Fondo oscuro para la barra lateral */
        color: white !important;
    }}
    .css-1r6slb0 .css-10trblm {{
        color: white !important;
    }}
    .css-1r6slb0 .css-1r6slb0, .css-1d391kg .css-1d391kg {{
        color: white !important;
    }}
    /* Ocultar barra superior de Streamlit */
    header[data-testid="stHeader"] {{
        display: none;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Filtro en la barra lateral para seleccionar la era del cine
st.sidebar.title('Eras del Cine en Hollywood')
era_options = ["Todo"] + list(data['era'].unique())
selected_era = st.sidebar.selectbox('Seleccione la Era del Cine', era_options)

# Filtrar los datos según la selección de era
if selected_era != "Todo":
    data = data[data['era'] == selected_era]
else:
    data = data 
st.title("Gustos")
st.write("Esta es la Página sobre Gustos.")
# Creo el resumen superior en 2 columnas
col1, col2 = st.columns(2)

with col1:# Muestra el número acumulado de vote_count
    
    st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">Número de Votos</div>
            <div class="metric-value">{data['vote_count'].sum():,}</div>
        </div>
    """, unsafe_allow_html=True)
            

with col2:
    st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">Nota Media</div>
            <div class="metric-value">{data['weightedRating'].mean():.2f}</div>
        </div>
    """, unsafe_allow_html=True)


# Dividimos la sección central en dos columnas: 80% y 20%
col1, col2 = st.columns([8, 2])

data['genres'] = data['genres'].apply(lambda x: x.split(', ') if isinstance(x, str) else [x])

# Paso 2: Explotar las listas de géneros en filas individuales y resetear el índice
df_exploded = data.explode('genres').reset_index(drop=True)

# Paso 3: Calcular el weightedRating promedio para cada género
average_ratings = df_exploded.groupby('genres')['weightedRating'].mean().nlargest(10)

# Filtrar los datos para incluir solo los top 10 géneros
df_top_genres = df_exploded[df_exploded['genres'].isin(average_ratings.index)]

# Configurar Streamlit para mostrar el gráfico
st.title('Valoraciones del Top 10 Géneros')

# Crear el boxplot usando Seaborn y Matplotlib
fig_box, ax_box = plt.subplots(figsize=(10, 6))  # Tamaño del gráfico

# Usar sns.boxplot para el boxplot
sns.boxplot(x='genres', y='weightedRating', data=df_top_genres, ax=ax_box, palette='Set2')

# Configurar el estilo del gráfico
ax_box.set_title('Distribución de Valoraciones por Top 10 Géneros',color='#FFD700', fontsize=16)
ax_box.set_xlabel('Género', color='white', fontsize=14)
ax_box.set_ylabel('Valoración', color='white', fontsize=14)
ax_box.tick_params(axis='x', colors ='white', labelrotation=45)  # Rotar etiquetas x para mejor legibilidad
ax_box.tick_params(axis='y', color='white')  # Color de las marcas del eje y
ax_box.set_facecolor('#2F4F4F')  # Color de fondo del gráfico de barras
fig_box.patch.set_facecolor('#2F4F4F') 
# Mostrar el gráfico en Streamlit
st.pyplot(fig_box)


with col2:
    st.image("https://www.rockandrollarmy.com/magazine/wp-content/uploads/2019/08/likes.png", use_column_width=True)

# Creamos los 3 gráficos inferiores
#st.write("## Análisis de Películas")

# Tamaño estándar de las figuras
fig_size = (10, 10)

col1, col2, col3 = st.columns(3)

# Aumentar el tamaño del texto
plt.rcParams.update({'font.size': 16})

# Top 10 Géneros
data_genres = data.dropna(subset=['genres'])

# Asegúrate de que los actores estén en una lista
data_genres['genres'] = data_genres['genres'].apply(lambda x: x.split(', ') if isinstance(x, str) else x)

# Descomponer las listas de actores en filas individuales
genres_data = data_genres.explode('genres')
genres_counts = genres_data['genres'].value_counts()
genres_over_10 = genres_counts[genres_counts > 10].index.tolist()
genres_data_filtered = genres_data[genres_data['genres'].isin(genres_over_10)]

# Paso 2: Calcular el promedio de weightedRating para cada actor actors_vote_average = df_exploded.groupby('actors')['popularity'].mean().nlargest(10)
average_ratings = genres_data_filtered.groupby('genres')['weightedRating'].mean().sort_values(ascending=False)

# Obtener los top 5 actores con el weightedRating promedio más alto
top_genres = average_ratings.head(5)

# Crear el gráfico de barras usando Seaborn y Matplotlib
fig_bar, ax_bar = plt.subplots(figsize=(8, 5))  # Tamaño del gráfico de barras
palette = sns.color_palette("dark:#5A9", n_colors=5)  # Paleta de colores

# Usar sns.barplot para el gráfico de barras
sns.barplot(x=top_genres.index, y=top_genres.values, palette=palette, ax=ax_bar)

# Mostrar la puntuación media obtenida en cada barra del gráfico
for idx, value in enumerate(top_genres):
    ax_bar.text(idx, value, f'{value:.2f}', ha='center', va='bottom', color='white', fontsize=14)

# Configurar el estilo del gráfico de barras
ax_bar.set_title('Top 5 géneros con mejores valoraciones', color='#FFD700', fontsize=16)  # Título con color dorado y tamaño de fuente
ax_bar.set_xlabel('Género', color='white', fontsize=10)  # Etiqueta del eje x con color blanco y tamaño de fuente
ax_bar.set_ylabel('Promedio de Valoraciones', color='white', fontsize=14)  # Etiqueta del eje y con color blanco y tamaño de fuente
ax_bar.tick_params(axis='x', colors='white')  # Color de las marcas del eje x
ax_bar.tick_params(axis='y', colors='white')  # Color de las marcas del eje y
fig_bar.patch.set_facecolor('#2F4F4F')  # Color de fondo de la figura
ax_bar.set_facecolor('#2F4F4F')  # Color de fondo del gráfico de barras

# Rotar las etiquetas del eje x diagonalmente
plt.xticks(rotation=45, ha='right')

# Mostrar el gráfico de barras en Streamlit
# Mostrar el gráfico en Streamlit

col1.pyplot(fig_bar)

# Top 10 Directores por cantidad de películas
data_directors_name = data.dropna(subset=['directors_name'])

# Asegúrate de que los actores estén en una lista
data_directors_name['directors_name'] = data_directors_name['directors_name'].apply(lambda x: x.split(', ') if isinstance(x, str) else x)

# Descomponer las listas de actores en filas individuales
directors_data = data_directors_name.explode('directors_name')
directors_counts = directors_data['directors_name'].value_counts()
directors_over_10 = directors_counts[directors_counts > 1].index.tolist()
directors_data_filtered = directors_data[directors_data['directors_name'].isin(directors_over_10)]

# Paso 2: Calcular el promedio de weightedRating para cada actor actors_vote_average = df_exploded.groupby('actors')['popularity'].mean().nlargest(10)
average_ratings = directors_data_filtered.groupby('directors_name')['weightedRating'].mean().sort_values(ascending=False)

# Obtener los top 5 actores con el weightedRating promedio más alto
top_directors = average_ratings.head(5)

fig_bar, ax_bar = plt.subplots(figsize=(8, 5))  # Tamaño del gráfico de barras
palette = sns.color_palette("dark:#5A9", n_colors=5)  # Paleta de colores

# Usar sns.barplot para el gráfico de barras
sns.barplot(x=top_directors.index, y=top_directors.values, palette=palette, ax=ax_bar)

# Mostrar la puntuación media obtenida en cada barra del gráfico
for idx, value in enumerate(top_directors):
    ax_bar.text(idx, value, f'{value:.2f}', ha='center', va='bottom', color='white', fontsize=14)

# Configurar el estilo del gráfico de barras
ax_bar.set_title('Top 5 directores con mejores valoraciones', color='#FFD700', fontsize=16)  # Título con color dorado y tamaño de fuente
ax_bar.set_xlabel('Director', color='white', fontsize=10)  # Etiqueta del eje x con color blanco y tamaño de fuente
ax_bar.set_ylabel('Promedio de Valoraciones', color='white', fontsize=14)  # Etiqueta del eje y con color blanco y tamaño de fuente
ax_bar.tick_params(axis='x', colors='white')  # Color de las marcas del eje x
ax_bar.tick_params(axis='y', colors='white')  # Color de las marcas del eje y
fig_bar.patch.set_facecolor('#2F4F4F')  # Color de fondo de la figura
ax_bar.set_facecolor('#2F4F4F')  # Color de fondo del gráfico de barras

# Rotar las etiquetas del eje x diagonalmente
plt.xticks(rotation=45, ha='right')

# Mostrar el gráfico de barras en Streamlit
# Mostrar el gráfico en Streamlit
col2.pyplot(fig_bar)

# Top 10 Actores por mejores puntuaciones
data_actors = data.dropna(subset=['actors'])

# Asegúrate de que los actores estén en una lista
data_actors['actors'] = data_actors['actors'].apply(lambda x: x.split(', ') if isinstance(x, str) else x)

# Descomponer las listas de actores en filas individuales
actors_data = data_actors.explode('actors')
actors_counts = actors_data['actors'].value_counts()
actors_over_10 = actors_counts[actors_counts > 3].index.tolist()
actors_data_filtered = actors_data[actors_data['actors'].isin(actors_over_10)]

# Paso 2: Calcular el promedio de weightedRating para cada actor actors_vote_average = df_exploded.groupby('actors')['popularity'].mean().nlargest(10)
average_ratings = actors_data_filtered.groupby('actors')['weightedRating'].mean().sort_values(ascending=False)

# Obtener los top 5 actores con el weightedRating promedio más alto
top_actors = average_ratings.head(5)

# Crear el gráfico de barras usando Seaborn y Matplotlib
fig_bar, ax_bar = plt.subplots(figsize=(8, 5))  # Tamaño del gráfico de barras
palette = sns.color_palette("dark:#5A9", n_colors=5)  # Paleta de colores

# Usar sns.barplot para el gráfico de barras
sns.barplot(x=top_actors.index, y=top_actors.values, palette=palette, ax=ax_bar)

# Mostrar la puntuación media obtenida en cada barra del gráfico
for idx, value in enumerate(top_actors):
    ax_bar.text(idx, value, f'{value:.2f}', ha='center', va='bottom', color='white', fontsize=14)

# Configurar el estilo del gráfico de barras
ax_bar.set_title('Top 5 Actores con mejores valoraciones', color='#FFD700', fontsize=16)  # Título con color dorado y tamaño de fuente
ax_bar.set_xlabel('Actor', color='white', fontsize=10)  # Etiqueta del eje x con color blanco y tamaño de fuente
ax_bar.set_ylabel('Promedio de Valoraciones', color='white', fontsize=14)  # Etiqueta del eje y con color blanco y tamaño de fuente
ax_bar.tick_params(axis='x', colors='white')  # Color de las marcas del eje x
ax_bar.tick_params(axis='y', colors='white')  # Color de las marcas del eje y
fig_bar.patch.set_facecolor('#2F4F4F')  # Color de fondo de la figura
ax_bar.set_facecolor('#2F4F4F')  # Color de fondo del gráfico de barras

plt.xticks(rotation=45, ha='right')
# Mostrar el gráfico de barras en Streamlit
# Mostrar el gráfico en Streamlit

col3.pyplot(fig_bar)

decade_data = data.groupby('decade').agg({
    'weightedRating': 'mean',
    'vote_count': 'mean'
}).reset_index()

# Configurar Streamlit para mostrar el gráfico
st.title('Evolución de Weighted Rating y Vote Count por Década')

# Crear el gráfico de líneas usando Seaborn y Matplotlib
fig_decade, ax_weighted = plt.subplots(figsize=(12, 6))

# Usar sns.lineplot para el gráfico de líneas de weightedRating
sns.lineplot(x='decade', y='weightedRating', data=decade_data, estimator='mean', ci=None, marker='o', label='Weighted Rating Promedio', ax=ax_weighted)

# Configurar el segundo eje y para vote_count
ax_votes = ax_weighted.twinx()
sns.lineplot(x='decade', y='vote_count', data=decade_data, estimator='mean', ci=None, marker='s', label='Vote Count Promedio', ax=ax_votes, color='orange')

# Configurar el estilo del gráfico - eje y izquierdo (weightedRating)
ax_weighted.set_title('Evolución de las Valoraciones y Número de Votos de usuarios por Década', color='#FFD700', fontsize=16)
ax_weighted.set_xlabel('Década', color='white', fontsize=14)
ax_weighted.set_ylabel('Valoraciones', color='white', fontsize=14)
ax_weighted.tick_params(axis='x', colors='white')
ax_weighted.tick_params(axis='y', colors='white')
ax_weighted.legend(loc='upper left', fontsize=10)

# Configurar el estilo del gráfico - eje y derecho (vote_count)
ax_votes.set_ylabel('Nº de votos promedio', color='white', fontsize=14)
ax_votes.tick_params(axis='y', colors='orange')
ax_votes.legend(loc='upper right', fontsize=10)

fig_decade.patch.set_facecolor('#2F4F4F')
ax_weighted.set_facecolor('#2F4F4F')

# Mostrar el gráfico en Streamlit
st.pyplot(fig_decade)


# Función para mostrar el top 10 de películas con mejor puntuación de usuario
def mostrar_top_10_peliculas_mejor_puntuacion(data):
    # Ordenar por puntuación y tomar el top 10
    top_10 = data.nlargest(10, 'weightedRating')

    # Crear una lista de diccionarios con los detalles de las películas
    peliculas = []
    for _, row in top_10.iterrows():
        pelicula = {
            'title': row['title_es'],
            'rating': row['weightedRating'],
            'budget': row['budget'],
            'poster_url': "https://image.tmdb.org/t/p/w500/" + row['poster_path'],
            'imdb_url': "https://www.imdb.com/title/" + row['imdb_id']
        }
        peliculas.append(pelicula)

    # Mostrar el listado en Streamlit
    st.write("### Top 10 Películas con Mejor Puntuación de Usuario")
    for pelicula in peliculas:
        col1, col2 = st.columns([1, 4])
        with col1:
            st.image(pelicula['poster_url'], width=100)
        with col2:
            st.markdown(f"**[{pelicula['title']}]({pelicula['imdb_url']})**")
            st.write(f"**Puntuación:** {pelicula['rating']:.2f}")
            st.write(f"**Presupuesto:** {pelicula['budget']} millones de euros")

# Función para mostrar el top 10 de películas con mayor presupuesto y peor puntuación
def mostrar_top_10_peliculas_peor_puntuacion(data):
    # Filtrar las películas con los presupuestos más altos y peor puntuación
    high_budget_data = data.nlargest(100, 'budget')
    top_10_fracasos = high_budget_data.nsmallest(10, 'weightedRating')

    # Crear una lista de diccionarios con los detalles de las películas
    peliculas = []
    for _, row in top_10_fracasos.iterrows():
        pelicula = {
            'title': row['title_es'],
            'rating': row['weightedRating'],
            'budget': row['budget'],
            'poster_url': "https://image.tmdb.org/t/p/w500/" + row['poster_path'],
            'imdb_url': "https://www.imdb.com/title/" + row['imdb_id']
        }
        peliculas.append(pelicula)

    # Mostrar el listado en Streamlit
    st.write("### Top 10 Películas con Mayor Presupuesto y Peor Puntuación")
    for pelicula in peliculas:
        col1, col2 = st.columns([1, 4])
        with col1:
            st.image(pelicula['poster_url'], width=100)
        with col2:
            st.markdown(f"**[{pelicula['title']}]({pelicula['imdb_url']})**")
            st.write(f"**Puntuación:** {pelicula['rating']:.2f}")
            st.write(f"**Presupuesto:** {pelicula['budget']} millones de euros")

# Dividir en dos columnas: una para mejor puntuación y otra para peor puntuación
col_mejor_puntuacion, col_peor_puntuacion = st.columns(2)

with col_mejor_puntuacion:
    mostrar_top_10_peliculas_mejor_puntuacion(data)

with col_peor_puntuacion:
    mostrar_top_10_peliculas_peor_puntuacion(data)

def show_page4():
    st.title("Sistema de Recomendación")
    st.write("Elige hasta 3 películas que te gusten y te recomendaremos otras películas similares.")
    st.write("Resultados")
