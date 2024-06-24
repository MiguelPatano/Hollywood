import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
#import st_pages

# Cargar datos
data = pd.read_csv("movies_Final.csv")
#st_pages.main()
st.set_page_config(page_title="Películas IMDB", page_icon=":popcorn:", layout="wide", initial_sidebar_state="expanded")

#vamos a cambiar el color de la barra lateral
st.markdown("""<style>.css-1d391kg, .css-1r6slb0 {background-color: #2F4F4F !important; color: white !important;}</style>""", unsafe_allow_html=True)
#.css-nzvw1x {background-color: #2F4F4F; color: white;}
             
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
    filtered_data = data[data['era'] == selected_era]
else:
    filtered_data = data

# Creo el resumen superior en 4 columnas
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">Cantidad Películas</div>
            <div class="metric-value">{filtered_data.shape[0]:,}</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">Cantidad Actores</div>
            <div class="metric-value">{filtered_data['actors'].str.split(',').explode().nunique():,}</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">Cantidad Directores</div>
            <div class="metric-value">{filtered_data['directors_name'].str.split(',').explode().nunique():,}</div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">Duración Media</div>
            <div class="metric-value">{filtered_data['runtime'].mean().round(2):,}</div>
        </div>
    """, unsafe_allow_html=True)

# Dividimos la sección central en dos columnas: 80% y 20%
col1, col2 = st.columns([8, 2])

# Gráfico de barras de cantidad de películas por productora
top_producers_bar = filtered_data['production_companies'].value_counts().nlargest(10).reset_index()
top_producers_bar.columns = ['production_companies', 'count']

with col1:
    fig_bar, ax_bar = plt.subplots(figsize=(12, 6))  # Cambio el tamaño
    sns.barplot(y='production_companies', x='count', data=top_producers_bar, ax=ax_bar, palette='dark:#5A9')
    ax_bar.set_title('Top 10 Productoras por Cantidad de Películas', color='#FFD700', fontsize=16)  # Color Dorado y tamaño de fuente
    ax_bar.set_xlabel('Cantidad de Películas', color='white', fontsize=14)
    ax_bar.set_ylabel('Productoras', color='white', fontsize=14)
    ax_bar.tick_params(axis='x', colors='white')
    ax_bar.tick_params(axis='y', colors='white')
    fig_bar.patch.set_facecolor('#2F4F4F')
    ax_bar.set_facecolor('#2F4F4F')
    st.pyplot(fig_bar)

with col2:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/cc/IMDb_Logo_Square.svg/2048px-IMDb_Logo_Square.svg.png", use_column_width=True)

# Creamos los 3 gráficos inferiores
#st.write("## Análisis de Películas")

# Tamaño estándar de las figuras
fig_size = (10, 10)

col1, col2, col3 = st.columns(3)

# Aumentar el tamaño del texto
plt.rcParams.update({'font.size': 16})

#Vamos a separar los generos y crear el gráfico con ellos.
all_genres = filtered_data['genres'].str.split(',').explode().str.strip()
top_genres = all_genres.value_counts().nlargest(10)

# Crear el gráfico de pastel actualizado
fig1, ax1 = plt.subplots(figsize=(10, 7))
ax1.pie(top_genres, labels=top_genres.index, autopct='%1.1f%%', colors=sns.color_palette("dark:#5A9", len(top_genres)))
ax1.set_title('Top 10 Géneros', color='#FFD700', fontsize=16)  # Dorado y tamaño de fuente
for text in ax1.texts:
    text.set_color("white")
fig1.patch.set_facecolor('#2F4F4F')  # Fondo con color #2F4F4F
ax1.set_facecolor('#2F4F4F')
col1.pyplot(fig1)

# Top 10 Directores por cantidad de películas
director_counts = filtered_data['directors_name'].str.split(',').explode().value_counts().nlargest(10)
fig2, ax2 = plt.subplots(figsize=fig_size)
ax2.pie(director_counts, labels=director_counts.index, autopct=lambda p: f'{int(p * sum(director_counts) / 100):,}', colors=sns.color_palette("dark:#5A9", len(director_counts)))
ax2.set_title('Top 10 Directores', color='#FFD700', fontsize=16)  # Dorado y tamaño de fuente
for text in ax2.texts:
    text.set_color("white")
fig2.patch.set_facecolor('#2F4F4F')  # Fondo con color #2F4F4F
ax2.set_facecolor('#2F4F4F')
col2.pyplot(fig2)

# Top 10 Actores por cantidad de películas
actor_counts = filtered_data['actors'].str.split(',').explode().value_counts().nlargest(10)
fig3, ax3 = plt.subplots(figsize=fig_size)
ax3.pie(actor_counts, labels=actor_counts.index, autopct=lambda p: f'{int(p * sum(actor_counts) / 100):,}', colors=sns.color_palette("dark:#5A9", len(actor_counts)))
ax3.set_title('Top 10 Actores', color='#FFD700', fontsize=16)  # Dorado y tamaño de fuente
for text in ax3.texts:
    text.set_color("white")
fig3.patch.set_facecolor('#2F4F4F')  # Fondo con color #2F4F4F
ax3.set_facecolor('#2F4F4F')
col3.pyplot(fig3)
