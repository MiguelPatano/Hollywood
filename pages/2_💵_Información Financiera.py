import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter

# Cargar datos
data = pd.read_csv("movies_Final.csv")

# Calcular los beneficios y el ROI por si lo puedo usar.
data['benefits'] = data['revenue'] - data['budget']
data['roi'] = (data['revenue'] - data['budget']) / data['budget']

# Filtrar las películas con presupuesto mayor que 0 para evitar división por cero
filtered_data = data[data['budget'] > 0].copy()

st.set_page_config(page_title="Películas IMDB", page_icon="💵", layout="wide", initial_sidebar_state="expanded")

# Color de fondo de la barra lateral no fuciona
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
# Quiero poner la barra lateral de color oscuro no funciona
st.markdown(sidebar_style, unsafe_allow_html=True)

# Filtro en la barra lateral para seleccionar la era del cine
st.sidebar.title('Eras del Cine en Hollywood')
era_options = ["Todo"] + list(filtered_data['era'].unique())
selected_era = st.sidebar.selectbox('Seleccione la Era del Cine', era_options)

# Filtrar los datos según la selección de era
if selected_era != "Todo":
    filtered_data = filtered_data[filtered_data['era'] == selected_era]

# Crear el resumen superior en 4 columnas
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">Presupuesto Medio</div>
            <div class="metric-value">${filtered_data['budget'].mean().round(2):,}</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">Beneficios Medios</div>
            <div class="metric-value">${filtered_data['benefits'].mean().round(2):,}</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">Ingresos Totales</div>
            <div class="metric-value">${filtered_data['revenue'].sum().round(2):,}</div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">Ingresos Medios</div>
            <div class="metric-value">${filtered_data['revenue'].mean().round(2):,}</div>
        </div>  
    """, unsafe_allow_html=True)

######################
st.markdown("\n")
# Dividimos la sección central en dos columnas
col1, col2 = st.columns(2)

# Separar las productoras
production_data = filtered_data.copy()
production_data['production_companies'] = production_data['production_companies'].str.split(',')
production_data = production_data.explode('production_companies')

# Limpiar los nombres de las productoras
production_data['production_companies'] = production_data['production_companies'].str.strip().str.lower()

# Calcular la suma de presupuestos y beneficios por productora
aggregated_data = production_data.groupby('production_companies').agg({
    'budget': 'sum',
    'benefits': 'sum'
}).reset_index()

# Gráfico de barras de top 10 productoras por suma de presupuestos
top_producers_budget_sum = aggregated_data.nlargest(10, 'budget')
top_producers_budget_sum['budget'] = top_producers_budget_sum['budget'] / 1_000_000  # Lo uso para convertir a millones

with col1:
    fig_budget, ax_budget = plt.subplots(figsize=(12, 6))  # Cambio el tamaño
    sns.barplot(y='production_companies', x='budget', data=top_producers_budget_sum, ax=ax_budget, palette='dark:#5A9')
    ax_budget.set_title('Top 10 Productoras por Suma de Presupuestos', color='#FFD700', fontsize=16)
    ax_budget.set_xlabel('Suma de Presupuestos (Millones)', color='white', fontsize=14)
    ax_budget.set_ylabel('Productoras', color='white', fontsize=14)
    ax_budget.tick_params(axis='x', colors='white')
    ax_budget.tick_params(axis='y', colors='white')
    fig_budget.patch.set_facecolor('#2F4F4F')
    ax_budget.set_facecolor('#2F4F4F')
    st.pyplot(fig_budget)

# Gráfico de barras de top 10 productoras por suma de beneficios
top_producers_benefits_sum = aggregated_data.nlargest(10, 'benefits')
top_producers_benefits_sum['benefits'] = top_producers_benefits_sum['benefits'] / 1_000_000

with col2:
    fig_benefits, ax_benefits = plt.subplots(figsize=(12, 6)) # Cambio el tamaño
    sns.barplot(y='production_companies', x='benefits', data=top_producers_benefits_sum, ax=ax_benefits, palette='dark:#5A9')
    ax_benefits.set_title('Top 10 Productoras por Suma de Beneficios', color='#FFD700', fontsize=16)
    ax_benefits.set_xlabel('Suma de Beneficios (Millones)', color='white', fontsize=14)
    ax_benefits.set_ylabel('Productoras', color='white', fontsize=14)
    ax_benefits.tick_params(axis='x', colors='white')
    ax_benefits.tick_params(axis='y', colors='white')
    fig_benefits.patch.set_facecolor('#2F4F4F')
    ax_benefits.set_facecolor('#2F4F4F')
    st.pyplot(fig_benefits)
# Separar los directores
directors_data = filtered_data.copy()
directors_data['directors_name'] = directors_data['directors_name'].str.split(',')
directors_data = directors_data.explode('directors_name')

# Limpiar los nombres de los directores
directors_data['directors_name'] = directors_data['directors_name'].str.strip().str.lower()

# Calcular la suma de presupuestos y beneficios por director
aggregated_directors_data = directors_data.groupby('directors_name').agg({
    'budget': 'sum',
    'benefits': 'sum'
}).reset_index()

# Dividir la sección de directores en dos columnas
col3, col4 = st.columns(2)

# Gráfico de línea de top 10 directores por suma de presupuestos
top_directors_budget_sum = aggregated_directors_data.nlargest(10, 'budget')
top_directors_budget_sum['budget'] = top_directors_budget_sum['budget'] / 1_000_000 

with col3:
    fig_directors_budget, ax_directors_budget = plt.subplots(figsize=(12, 6))
    ax_directors_budget.plot(top_directors_budget_sum['directors_name'], top_directors_budget_sum['budget'], marker='o', linestyle='-', color='#5A9')
    ax_directors_budget.set_title('Top 10 Directores por Suma de Presupuestos', color='#FFD700', fontsize=16)
    ax_directors_budget.set_xlabel('Directores', color='white', fontsize=14)
    ax_directors_budget.set_ylabel('Suma de Presupuestos (Millones)', color='white', fontsize=14)
    ax_directors_budget.tick_params(axis='x', colors='white', rotation=45)
    ax_directors_budget.tick_params(axis='y', colors='white')
    fig_directors_budget.patch.set_facecolor('#2F4F4F')
    ax_directors_budget.set_facecolor('#2F4F4F')
    st.pyplot(fig_directors_budget)

# Gráfico de línea de top 10 directores por suma de beneficios
top_directors_benefits_sum = aggregated_directors_data.nlargest(10, 'benefits')
top_directors_benefits_sum['benefits'] = top_directors_benefits_sum['benefits'] / 1_000_000

with col4:
    fig_directors_benefits, ax_directors_benefits = plt.subplots(figsize=(12, 6))
    ax_directors_benefits.plot(top_directors_benefits_sum['directors_name'], top_directors_benefits_sum['benefits'], marker='o', linestyle='-', color='#5A9')
    ax_directors_benefits.set_title('Top 10 Directores por Suma de Beneficios', color='#FFD700', fontsize=16) 
    ax_directors_benefits.set_xlabel('Directores', color='white', fontsize=14)
    ax_directors_benefits.set_ylabel('Suma de Beneficios (Millones)', color='white', fontsize=14)
    ax_directors_benefits.tick_params(axis='x', colors='white', rotation=45)
    ax_directors_benefits.tick_params(axis='y', colors='white')
    fig_directors_benefits.patch.set_facecolor('#2F4F4F')
    ax_directors_benefits.set_facecolor('#2F4F4F')
    st.pyplot(fig_directors_benefits)

# Separar los actores
actors_data = filtered_data.copy()
actors_data['actors'] = actors_data['actors'].str.split(',')
actors_data = actors_data.explode('actors')

# Limpiar los nombres de los actores
actors_data['actors'] = actors_data['actors'].str.strip().str.lower()

# Calcular la suma de presupuestos y beneficios por actor
aggregated_actors_data = actors_data.groupby('actors').agg({
    'budget': 'sum',
    'benefits': 'sum'
}).reset_index()

# Dividir la sección de actores en dos columnas
col5, col6 = st.columns(2)

# Gráfico de área de top 10 actores por suma de presupuestos
top_actors_budget_sum = aggregated_actors_data.nlargest(10, 'budget')
top_actors_budget_sum['budget'] = top_actors_budget_sum['budget'] / 1_000_000 

with col5:
    fig_actors_budget, ax_actors_budget = plt.subplots(figsize=(12, 6))
    ax_actors_budget.fill_between(top_actors_budget_sum['actors'], top_actors_budget_sum['budget'], color='#5A9', alpha=0.6)
    ax_actors_budget.set_title('Top 10 Actores por Suma de Presupuestos', color='#FFD700', fontsize=16)
    ax_actors_budget.set_xlabel('Actores', color='white', fontsize=14)
    ax_actors_budget.set_ylabel('Suma de Presupuestos (Millones)', color='white', fontsize=14)
    ax_actors_budget.tick_params(axis='x', colors='white', rotation=45)
    ax_actors_budget.tick_params(axis='y', colors='white')
    fig_actors_budget.patch.set_facecolor('#2F4F4F')
    ax_actors_budget.set_facecolor('#2F4F4F')
    st.pyplot(fig_actors_budget)

# Gráfico de área de top 10 actores por suma de beneficios
top_actors_benefits_sum = aggregated_actors_data.nlargest(10, 'benefits')
top_actors_benefits_sum['benefits'] = top_actors_benefits_sum['benefits'] / 1_000_000

with col6:
    fig_actors_benefits, ax_actors_benefits = plt.subplots(figsize=(12, 6))
    ax_actors_benefits.fill_between(top_actors_benefits_sum['actors'], top_actors_benefits_sum['benefits'], color='#5A9', alpha=0.6)
    ax_actors_benefits.set_title('Top 10 Actores por Suma de Beneficios', color='#FFD700', fontsize=16)
    ax_actors_benefits.set_xlabel('Actores', color='white', fontsize=14)
    ax_actors_benefits.set_ylabel('Suma de Beneficios (Millones)', color='white', fontsize=14)
    ax_actors_benefits.tick_params(axis='x', colors='white', rotation=45)
    ax_actors_benefits.tick_params(axis='y', colors='white')
    fig_actors_benefits.patch.set_facecolor('#2F4F4F')
    ax_actors_benefits.set_facecolor('#2F4F4F')
    st.pyplot(fig_actors_benefits)

# Gráfico de líneas de evolución de presupuestos y beneficios por década
# Dividir la sección en dos columnas: 70% y 30%
col7, col8 = st.columns([7, 3])

# Gráfico de líneas de evolución de presupuestos y beneficios por década
decade_data = filtered_data.groupby('decade').agg({
    'budget': 'sum',
    'benefits': 'sum'
}).reset_index()

decade_data['decade'] = decade_data['decade'].astype(int)
decade_data['budget'] = decade_data['budget'] / 1_000_000
decade_data['benefits'] = decade_data['benefits'] / 1_000_000

with col7:
    fig_decade, ax_decade = plt.subplots(figsize=(12, 6))
    sns.lineplot(x='decade', y='budget', data=decade_data, marker='o', label='Presupuestos (Millones de Dolares)', ax=ax_decade)
    sns.lineplot(x='decade', y='benefits', data=decade_data, marker='o', label='Beneficios (Millones de Dolares)', ax=ax_decade)

    ax_decade.axhline(y=decade_data['benefits'].mean(), color='red', linestyle='--', label='Beneficios Medios')

    ax_decade.set_title('Evolución de Presupuestos y Beneficios por Década', color='#FFD700', fontsize=16)
    ax_decade.set_xlabel('Década', color='white', fontsize=14)
    ax_decade.set_ylabel('Millones de Dolares', color='white', fontsize=14)
    ax_decade.tick_params(axis='x', colors='white')
    ax_decade.tick_params(axis='y', colors='white')
    ax_decade.legend(loc='upper left', fontsize=12)

    fig_decade.patch.set_facecolor('#2F4F4F')
    ax_decade.set_facecolor('#2F4F4F')
    st.pyplot(fig_decade)
with col8:
    st.markdown("\n")  
    st.markdown("\n")
    st.markdown("\n")    
    st.markdown("\n") 
    st.image("https://www.elsoldemexico.com.mx/incoming/raso3g-premios-oscar.jpg/ALTERNATES/LANDSCAPE_768/Premios%20Oscar.jpg", use_column_width=True)

def mostrar_top_10_peliculas_exitos(filtered_data):
    # Ordenar por beneficios y tomar el top 10
    top_10 = filtered_data.nlargest(10, 'benefits')

    # Crear una lista de diccionarios con los detalles de las películas
    peliculas = []
    for _, row in top_10.iterrows():
        pelicula = {
            'title': row['title_es'],
            'benefits': row['benefits'],
            'rating': row['weightedRating'],
            'poster_url': "https://image.tmdb.org/t/p/w500/" + row['poster_path'],
            'imdb_url': "https://www.imdb.com/title/" + row['imdb_id'],
            'director': row['directors_name']
        }
        peliculas.append(pelicula)

    # Mostrar el listado en Streamlit
    st.write("### Top 10 Películas con Más Beneficios")
    for pelicula in peliculas:
        col1, col2 = st.columns([1, 4])
        with col1:
            st.image(pelicula['poster_url'], width=100)
        with col2:
            st.markdown(f"**[{pelicula['title']}]({pelicula['imdb_url']})**")
            st.write(f"**Director:** {pelicula['director']}")
            st.write(f"**Beneficios:** ${pelicula['benefits']:,.2f}")
            st.write(f"**Calificación:** {pelicula['rating']:.2f}")

# Función para mostrar el top 10 de fracasos
def mostrar_top_10_peliculas_fracasos(filtered_data):
    # Filtrar las películas con los presupuestos más altos y beneficios más negativos
    high_budget_data = filtered_data.nlargest(100, 'budget')
    top_10_fracasos = high_budget_data.nsmallest(10, 'benefits')

    # Crear una lista con los detalles de las películas
    peliculas = []
    for _, row in top_10_fracasos.iterrows():
        pelicula = {
            'title': row['title_es'],
            'benefits': row['benefits'],
            'rating': row['weightedRating'],
            'poster_url': "https://image.tmdb.org/t/p/w500/" + row['poster_path'],
            'imdb_url': "https://www.imdb.com/title/" + row['imdb_id'],
            'director': row['directors_name']  
        }
        peliculas.append(pelicula)

    # Mostrar el listado en Streamlit
    st.write("### Top 10 Fracasos")
    for pelicula in peliculas:
        col1, col2 = st.columns([1, 4])
        with col1:
            st.image(pelicula['poster_url'], width=100)
        with col2:
            st.markdown(f"**[{pelicula['title']}]({pelicula['imdb_url']})**")
            st.write(f"**Director:** {pelicula['director']}")
            st.write(f"**Beneficios:** ${pelicula['benefits']:,.2f}")
            st.write(f"**Calificación:** {pelicula['rating']:.2f}")

# Dividir en dos columnas: una para éxitos y otra para fracasos
col_exitos, col_fracasos = st.columns(2)

with col_exitos:
    mostrar_top_10_peliculas_exitos(filtered_data)

with col_fracasos:
    mostrar_top_10_peliculas_fracasos(filtered_data)


#Ahora vamos a mostrar las peliculas que más recaudaran los próximos años
#Primero vamos a cargar un csv
exitos = pd.read_csv("top_15_movies_futuras.csv")
st.write('¿Quienes serán los grandes exitos de los próximos años?????:')
for i in range(0, 10, 5):
    cols = st.columns(5)
    for idx, (col, row) in enumerate(zip(cols, exitos.iloc[i:i+5].iterrows())):
        with col:
            st.image("https://image.tmdb.org/t/p/w500/" + row[1]['poster_path'], width=100)
            st.write(row[1]['original_title'])
            st.write(f"Título: {row[1]['title_es']}")
            st.write(f"Posible recaudación: ${row[1]['predicted_revenue']:,.2f}")
            st.write(f"Año: {row[1]['año']}")
            st.write(f"Director: {row[1]['directors_name']}")
            st.write(f"Género: {row[1]['genres']}")
            st.write(f"[Ver en IMDb](https://www.imdb.com/title/{row[1]['imdb_id']})")


#Que pasó en 2020?? 
#icono de ojo

st.markdown(f"<p style='font-size:24px; color:#FFD700;'>👁️¿Que pasó en 2020?👁️</p>", unsafe_allow_html=True)

filtered_data_2020 = data[(data['año'] >= 2014) & (data['año'] <= 2023)]
annual_data = filtered_data_2020.groupby('año').agg({
    'budget': 'sum',
    'revenue': 'sum'
}).reset_index()

# Convertir las cantidades a millones de dólares
annual_data['budget'] /= 1_000_000
annual_data['revenue'] /= 1_000_000

# Crear el gráfico
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x='año', y='budget', data=annual_data, marker='o', label='Presupuestos (Millones de Dólares)', ax=ax)
sns.lineplot(x='año', y='revenue', data=annual_data, marker='o', label='Recaudación (Millones de Dólares)', ax=ax)

# Añadir línea de beneficios medios
ax.axhline(y=annual_data['revenue'].mean(), color='red', linestyle='--', label='Recaudación Media')

# Personalizar el gráfico
ax.set_title('Evolución de Presupuestos y Recaudación por Año (2014-2024)', color='#FFD700', fontsize=16)
ax.set_xlabel('Año', color='white', fontsize=14)
ax.set_ylabel('Millones de Dólares', color='white', fontsize=14)
ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')
ax.legend(loc='upper right', fontsize=12)

fig.patch.set_facecolor('#2F4F4F')
ax.set_facecolor('#2F4F4F')

# Mostrar el gráfico en Streamlit
st.pyplot(fig)