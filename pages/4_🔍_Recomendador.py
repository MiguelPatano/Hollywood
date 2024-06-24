import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import seaborn as sns

# Configurar la aplicación de Streamlit
st.set_page_config(page_title="Recomendador de Películas", page_icon=":clapper:", layout="wide", initial_sidebar_state="expanded")

# Uso el cache de streamlit para el dataframe
@st.cache_data
def load_data():
    movies_df = pd.read_csv('movies_Final.csv')
    # Rellenar valores NaN en las columnas de texto
    movies_df['tagline'].fillna('', inplace=True)
    movies_df['keywords'].fillna('', inplace=True)
    movies_df['actors'].fillna('', inplace=True)
    movies_df['genres'].fillna('', inplace=True)
    movies_df['directors_name'].fillna('', inplace=True)
    return movies_df

@st.cache_data
def calculate_similarity(movies_df):
    text_features = movies_df['tagline'] + ' ' + movies_df['keywords'] + ' ' + movies_df['actors'] + ' ' + movies_df['genres'] + ' ' + movies_df['directors_name']
    tfidf = TfidfVectorizer(stop_words='english', max_df=0.7, min_df=0.01)
    tfidf_matrix = tfidf.fit_transform(text_features)
    cosine_sim_text = linear_kernel(tfidf_matrix, tfidf_matrix)
    return cosine_sim_text

# Cargar datos y calcular similitud
movies_df = load_data()
cosine_sim_text = calculate_similarity(movies_df)

# Función de búsqueda 
def buscar(titulos_peliculas, cosine_sim=cosine_sim_text):
    try:
        titles = [title.lower() for title in titulos_peliculas]
        indices = [movies_df[movies_df['title'].str.lower() == title].index[0] for title in titulos_peliculas]
        sim_scores = cosine_sim[indices].mean(axis=0)
        sim_scores = list(enumerate(sim_scores))
        sim_scores = [score for score in sim_scores if score[0] not in indices]
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[:10]
        movie_indices = [i[0] for i in sim_scores]
        recommended_movies = movies_df.iloc[movie_indices]
        recommended_movies = recommended_movies.sort_values(by='weightedRating', ascending=False)
        return recommended_movies
    except IndexError:
        return pd.DataFrame()

# Colocar estilos CSS
st.markdown("""
    <style>
    .main {
        background-color: #2F4F4F;  /* Tono más oscuro de marfil (oscuro) */
        color: white;
    }
    .stButton>button {
        color: white;
        background-color: #3B3B3B;  /* Botón con color de fondo oscuro */
    }
    h1, h2, h3 {
        color: #FFD700;  /* Dorado */
    }
    .metric-container {
        border: 2px solid #FFD700;  /* Borde amarillo */
        border-radius: 10px;  /* Bordes redondeados */
        padding: 10px;  /* Espaciado interno */
        margin: 5px 0;  /* Espaciado externo */
        text-align: center;  /* Alineación central */
        color: white;  /* Texto en blanco */
    }
    .metric-value {
        font-size: 2em;
        color: white;
    }
    .metric-label {
        color: white;
    }
    .css-1d391kg, .css-1r6slb0 {
        background-color: #2F4F4F !important;  /* Fondo oscuro para la barra lateral */
        color: white !important;
    }
    .css-1r6slb0 .css-10trblm {
        color: white !important;
    }
    .css-1r6slb0 .css-1r6slb0, .css-1d391kg .css-1d391kg {
        color: white !important;
    }
    .stMultiSelect label {
        color: white !important;
    }
    .stMultiSelect div[data-baseweb="select"], .stSelectbox div[data-baseweb="select"] {
        background-color: #FFD700 !important;  
    }
    .stMultiSelect div[role="listbox"], .stSelectbox div[role="listbox"] {
        background-color: #FFD700 !important;
    }
    .element-container img + div {
        color: white !important;
    }
    /* Ocultar barra superior de Streamlit */
    header[data-testid="stHeader"] {
        display: none;
    }
    </style>
    """, unsafe_allow_html=True)

# Dividir la configuración en dos columnas
col1, col2 = st.columns([3, 2])  

with col1:
    st.title('Recomendador de Películas')

with col2:
    st.image('https://upload.wikimedia.org/wikipedia/commons/thumb/c/cc/IMDb_Logo_Square.svg/2048px-IMDb_Logo_Square.svg.png', width=200)
    #st.image('https://st3.depositphotos.com/2927127/33886/v/450/depositphotos_338860296-stock-illustration-vector-image-cinema-hall-chairs.jpg', width=200)
    

# Crear un campo de selección múltiple
titulo_peliculas = st.multiselect('Dime una película que te guste!', movies_df['title'].tolist())

# Validar el número de selecciones
if len(titulo_peliculas) > 3:
    st.error("Has seleccionado más de tres películas. Por favor, selecciona solo tres.")
else:
    # Agregar botón de búsqueda
    if st.button('Buscar'):
        if titulo_peliculas:
            recomendaciones = buscar(titulo_peliculas)
            recomendaciones = buscar(titulo_peliculas)
            if recomendaciones.empty:
                st.write("No se encontraron recomendaciones para las películas seleccionadas.")

            st.write('Películas seleccionadas:')
            cols = st.columns(len(titulo_peliculas))
            for idx, titulo in enumerate(titulo_peliculas):
                pelicula_seleccionada = movies_df[movies_df['title'] == titulo]
                if not pelicula_seleccionada.empty:
                    poster_path = pelicula_seleccionada.iloc[0]['poster_path']
                    poster_path = "https://image.tmdb.org/t/p/w500/" + poster_path
                    with cols[idx]:
                        st.image(poster_path, width=100, caption=titulo)
            
            st.write('Películas recomendadas:')
            for i in range(0, len(recomendaciones), 5):
                cols = st.columns(5)
                for idx, (col, row) in enumerate(zip(cols, recomendaciones.iloc[i:i+5].iterrows())):
                    with col:
                        try:
                            st.image("https://image.tmdb.org/t/p/w500/" + row[1]['poster_path'], width=100)
                        except:
                            st.image("https://thumbs.dreamstime.com/b/premio-de-la-ceremonia-%C3%B3scar-113543786.jpg", width=100)
                        
                        st.write(row[1]['original_title'])
                        st.write(f"Título: {row[1]['title_es']}")
                        st.write(f"Año: {row[1]['año']}")
                        st.write(f"Director: {row[1]['directors_name']}")
                        st.write(f"Calificación: {row[1]['weightedRating']:.2f}")
                        st.write(f"[Ver en IMDb](https://www.imdb.com/title/{row[1]['imdb_id']})")



## Vamos a jugar a un juego :)

from datetime import datetime
# Voy a dejar 5 líneas de espacio
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")


st.markdown('<h1 style="color:#FFD700;">Una vida de cine</h2>', unsafe_allow_html=True)

def mostrar_caratulas(pelis):
    # Filtrar las primeras 5 películas o menos
    top_5_movies = pelis.head(5)

    # Crear una fila en Streamlit para las carátulas
    cols = st.columns(len(top_5_movies))

    for col, (_, row) in zip(cols, top_5_movies.iterrows()):
        with col:
            st.image("https://image.tmdb.org/t/p/w500/" + row['poster_path'], width=100)
            st.write(f"{row['title_es']} ({row['año']})")

current_year = datetime.now().year
years = list(range(current_year, current_year - 100, -1))
years.insert(0, '')  # Añadir una opción en blanco al principio

year_of_birth = st.selectbox("Selecciona tu año de nacimiento", years)

# Calcular la edad del usuario solo si se ha seleccionado un año
if year_of_birth:
    age = current_year - year_of_birth

    # Vamos a mirar la edad
    if age < 18:
        #st.write(f"Este año cumples {age} años!, las mejores películas lanzadas cuando naciste fueron:")
        st.markdown(f"<p style='font-size:24px; color:#FFD700;'>Este año cumples {age} años, ¡Eres un mayor eeee!, las mejores películas lanzadas cuando naciste fueron:</p>", unsafe_allow_html=True) 
        visualizar = movies_df[movies_df['año'] == year_of_birth].sort_values(by='weightedRating', ascending=False)
        
        mostrar_caratulas(visualizar)
        
        st.markdown(f"<p style='font-size:24px; color:#FFD700;'>No podemos mostrarte mucho siendo tan pequeño regresa en unos años. Te sugiero estas películas:</p>", unsafe_allow_html=True)
        visualizar = movies_df[movies_df['genres'].str.contains('Animation') & movies_df['genres'].str.contains('Family')]
        
        # Ordenar por weightedRating de mayor a menor
        visualizar = visualizar.sort_values(by='weightedRating', ascending=False)
        mostrar_caratulas(visualizar)
    else:
        st.markdown(f"<p style='font-size:24px; color:#FFD700;'>Este año cumples {age} años, las mejores películas lanzadas el año que naciste fueron:</p>", unsafe_allow_html=True) 
        visualizar = movies_df[movies_df['año'] == year_of_birth].sort_values(by='weightedRating', ascending=False)
        mostrar_caratulas(visualizar)
        st.markdown(f"<p style='font-size:24px; color:#FFD700;'>¿Te llevaron al cine a ver estas películas de pequeño?</p>", unsafe_allow_html=True)
        
        ##Ahora vamos a mostrar las peliculas de la infancia.
        start_year = year_of_birth + 3
        end_year = year_of_birth + 10
        # Voy a poner las condiciones
        filtered_df = movies_df[
            (movies_df['año'] >= start_year) & 
            (movies_df['año'] <= end_year) & 
            (movies_df['genres'].str.contains('Family', case=False, na=False))
        ]
        #st.write(len(filtered_df),start_year, end_year,age) lo dejo por si tengo que verificar otra vez
        # Ordenar por la columna 'revenue' en orden descendente
        visualizar = filtered_df.sort_values(by='revenue', ascending=False).head(10)
        mostrar_caratulas(visualizar)
        #######Seguimos la fiesta.
        #vamos a calcular cuanto ganaron los estudios desde que naciste
        st.markdown(f"<p style='font-size:24px; color:#FFD700;'>Sabias que desde que naciste, los estudios de cine han ganado:</p>", unsafe_allow_html=True)
        total_ganancias = movies_df[(movies_df['año'] >= year_of_birth) & (movies_df['año'] <= current_year)]
        total_ganancias['profit'] = total_ganancias['revenue'] - total_ganancias['budget']
        ganancias_totales = total_ganancias['profit'].sum()
        st.title(f"${ganancias_totales:,.0f}")

        
        comparaciones = {
            "PIB de Irlanda": 373_876_171_555,  
            "Presupuesto Anual de Nueva York": 100_000_000_000, 
            "Valor de Mercado de Apple": 2_400_000_000_000, 
            "Costo del Programa Artemis de la NASA": 35_000_000_000,
        }
        # Mostrar las comparaciones
        for comparacion, valor in comparaciones.items():
            
            st.markdown(f"<p style='font-size:14px; color:#FFD700;'>Esto equivale aproximadamente al {ganancias_totales / valor:.2f} veces el {comparacion}.</p>", unsafe_allow_html=True) 
        #####Mas curiosidades de cine
        
        st.markdown(f"<p style='font-size:24px; color:#FFD700;'>De adolescente fuiste capaz de ver alguna de estas películas???:</p>", unsafe_allow_html=True)
        start_year = year_of_birth + 14
        end_year = year_of_birth + 20
        # Voy a poner las condiciones
        filtered_df = movies_df[
            (movies_df['año'] >= start_year) & 
            (movies_df['año'] <= end_year) & 
            (movies_df['genres'].str.contains('Horror', case=False, na=False))
        ]
        #st.write(len(filtered_df),start_year, end_year,age) lo dejo por si tengo que verificar otra vez
        # Ordenar por la columna 'revenue' en orden descendente
        visualizar = filtered_df.sort_values(by='revenue', ascending=False).head(10)
        mostrar_caratulas(visualizar)
        ###################Mas 
        st.markdown(f"<p style='font-size:24px; color:#FFD700;'>¿Te enamoraste de alguno de estos actores?</p>", unsafe_allow_html=True)
        
        start_year = year_of_birth + 14
        end_year = year_of_birth + 22
        filtered_df = movies_df[(movies_df['año'] >= start_year) & (movies_df['año'] <= end_year)]
        sorted_df = filtered_df.sort_values(by='revenue', ascending=False)
        all_actors = ','.join(sorted_df['actors'].dropna())
        actor_counts = Counter(all_actors.split(','))
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(actor_counts)
        
        st.set_option('deprecation.showPyplotGlobalUse', False)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        st.pyplot()
        ###################
        st.markdown(f"<p style='font-size:24px; color:#FFD700;'>Cuando cumpliste 18 fuiste a ver estas peliculas al cine?</p>", unsafe_allow_html=True)
        year_of_interest = year_of_birth + 18
        filtered_movies = movies_df[movies_df['año'] == year_of_interest]
        visualizar = filtered_movies.sort_values(by='weightedRating', ascending=False)
        mostrar_caratulas(visualizar)
        filtered_movies['profit'] = filtered_movies['revenue'] - filtered_movies['budget']
        negative_profit_movies = filtered_movies[filtered_movies['profit'] < 0]
        high_budget_negative_profit_movies = negative_profit_movies.sort_values(by='budget', ascending=False)
        if len(high_budget_negative_profit_movies) >= 5:
            
            st.markdown(f"<p style='font-size:24px; color:#FFD700;'>Seguro que estas no, pobres sus productores...</p>", unsafe_allow_html=True)
            mostrar_caratulas(high_budget_negative_profit_movies)
        ####################vamos a seguiiiir

        filtered_movies = movies_df[(movies_df['año'] >= year_of_birth) & (movies_df['año'] <= current_year)]

        # Procesamiento para directores separar por comas
        directors_exploded = filtered_movies.assign(directors_name=filtered_movies['directors_name'].str.split(', ')).explode('directors_name')
        director_ratings = directors_exploded.groupby('directors_name').agg({
            'weightedRating': ['mean', 'count']
        }).reset_index()
        director_ratings.columns = ['directors_name', 'mean_weightedRating', 'count_movies']
        min_movies = 5
        top_directors = director_ratings[director_ratings['count_movies'] >= min_movies]
        # Ordenar por la media de weightedRating en orden descendente y seleccionar los 5 mejores
        top_5_directors = top_directors.sort_values(by='mean_weightedRating', ascending=False).head(5)
        top_5_director_names = top_5_directors['directors_name'].tolist()
        # Filtrar las películas de los 5 mejores directores
        top_5_movies = directors_exploded[directors_exploded['directors_name'].isin(top_5_director_names)]
        # Vamos con el gráfico
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.set_style("darkgrid", {'axes.facecolor': '#2F4F4F'})
        sns.lineplot(data=top_5_movies, x='año', y='weightedRating', hue='directors_name', marker='o', ax=ax)
        st.markdown(f"<p style='font-size:24px; color:#FFD700;'>Analicemos en tus años de vida a los directores más valorados</p>", unsafe_allow_html=True)
        ax.set_title('Trayectoria de la Calificación de las Películas de los Directores Más Aclamados', color='#FFD700', fontsize=16)
        ax.set_xlabel('Año', color='white', fontsize=14)
        ax.set_ylabel('Puntuación Weighted Rating', color='white', fontsize=14)
        ax.legend(title='Director', facecolor='#2F4F4F', edgecolor='white', title_fontsize='13', fontsize='12', labelcolor='white')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        ax.grid(False)  # Eliminar las líneas interiores de la cuadrícula
        fig.patch.set_facecolor('#2F4F4F')
        ax.set_facecolor('#2F4F4F')
        st.pyplot(fig)

        # Ahora los actores
        actors_exploded = filtered_movies.assign(actors=filtered_movies['actors'].str.split(', ')).explode('actors')
        actor_ratings = actors_exploded.groupby('actors').agg({
            'weightedRating': ['mean', 'count']
        }).reset_index()
        actor_ratings.columns = ['actors', 'mean_weightedRating', 'count_movies']
        min_movies = 10
        top_actors = actor_ratings[actor_ratings['count_movies'] >= min_movies]
        top_5_actors = top_actors.sort_values(by='mean_weightedRating', ascending=False).head(5)
        top_5_actor_names = top_5_actors['actors'].tolist()

        # Verificación de los actores seleccionados
        #st.write("Top 5 actores seleccionados:", top_5_actor_names)

        top_5_movies_actors = actors_exploded[actors_exploded['actors'].isin(top_5_actor_names)]

        # Verificación de los datos filtrados para los actores seleccionados
        #st.write("Datos filtrados para los actores seleccionados:", top_5_movies_actors)

        fig, ax = plt.subplots(figsize=(12, 6))
        sns.set_style("darkgrid", {'axes.facecolor': '#2F4F4F'})
        sns.lineplot(data=top_5_movies_actors, x='año', y='weightedRating', hue='actors', marker='o', ax=ax)
        st.markdown(f"<p style='font-size:24px; color:#FFD700;'>Ahora los actores</p>", unsafe_allow_html=True)
        ax.set_title('Trayectoria de la Calificación de las Películas de los Actores Más Aclamados', color='#FFD700', fontsize=16)
        ax.set_xlabel('Año', color='white', fontsize=14)
        ax.set_ylabel('Puntuación Weighted Rating', color='white', fontsize=14)
        ax.legend(title='Actor', facecolor='#2F4F4F', edgecolor='white', title_fontsize='13', fontsize='12', labelcolor='white')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        ax.grid(False)  # Eliminar las líneas interiores de la cuadrícula
        fig.patch.set_facecolor('#2F4F4F')
        ax.set_facecolor('#2F4F4F')
        st.pyplot(fig)

        ####################Vamos a ver las peliculas mejor valoradas del año pasado
        st.markdown(f"<p style='font-size:24px; color:#FFD700;'>Para terminar solo decirte que las peliculas mejor valoradas del año pasado fueron:</p>", unsafe_allow_html=True)
        visualizar = movies_df[movies_df['año'] == 2023].sort_values(by='weightedRating', ascending=False)
        mostrar_caratulas(visualizar)
        st.markdown(f"<p style='font-size:24px; color:#FFD700;'>Nos vemos en los cines!!! Muchas gracias por tu interes!!!</p>", unsafe_allow_html=True)
        video_url = "https://www.youtube.com/watch?v=C6_th-5HJwA"
        st.video(video_url)

                