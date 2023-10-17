#Librerías
import pypyodbc as odbc
import dash 
from dash import dcc, html  # Importamos dcc y html desde dash
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import warnings
warnings.filterwarnings("ignore")


# Crear la aplicación Dash
app = dash.Dash(__name__, external_stylesheets=['/assets/estilo.css'])

#-----------------------------------------------------------------------------
#                              AQUÍ SE CONECTA EL SQL CON PYTHON

DRIVER_NAME = 'SQL SERVER'
SERVER_NAME = 'LAPTOP-1LCPBRUM'
DATABASE_NAME = 'Movies'

connection_string = f"""
    DRIVER={{{DRIVER_NAME}}};
    SERVER={SERVER_NAME};
    DATABASE={DATABASE_NAME};
    Trusted_Connection=yes;
    uid=roberto gil garcia;
    pwd=3012;
    """

odbc_connection = odbc.connect(connection_string)

#-----------------------------------------------------------------------------
#                                 AQUÍ SE CREAN LOS GRÁFICOS

# Primera Gráfica
query = """
select r.RatingScore, count(*) Frecuencia
from Ratings r
group  by r.RatingScore
order by r.RatingScore
"""
df = pd.read_sql(query, odbc_connection)

# Crear el gráfico circular
fig1 = px.pie(df, names='ratingscore', values='frecuencia')

# Segunda Gráfica
query = """
With Relevancia(MovieID, MaxRelevance) as (
select s.MovieID, max(s.Relevance) MaxRelevance
from GenomeScores s
group by s.MovieID
)

select s.TagID, t.Tag, count(*) FrecuenciaTag
from Relevancia r join GenomeScores s 
on r.MovieID = s.MovieID and r.MaxRelevance = s.Relevance
join GenomeTags t on s.TagID = t.TagID
group by s.TagID, t.Tag
order by FrecuenciaTag desc
"""
df = pd.read_sql(query, odbc_connection)

fig2 = px.bar(df, 'tagid', 'frecuenciatag', hover_name='tag', labels={'tagid': 'Tags', 'frecuenciatag': 'Frecuencia'})

# Tercera Gráfica
query = """
SELECT m.Title, AVG(r.RatingScore) as AvgScore, count(*) CantidadReviews
FROM MoviesInfo m join Ratings r
on m.MovieID = r.MovieID
group by m.Title
order by CantidadReviews desc
"""

df = pd.read_sql(query, odbc_connection)

fig3 = px.scatter(df, 'avgscore', 'cantidadreviews', hover_name='title', labels={'avgscore': 'Rating Promedio', 'cantidadreviews': 'Cantidad de Reviews'})

# Cuarta gráfica
query = """
SELECT y.ReleaseYear, count(*) as Frecuencia
FROM MovieYear y
group by y.ReleaseYear
order by y.ReleaseYear
"""

df = pd.read_sql(query, odbc_connection)

fig4 = px.bar(df, 'releaseyear', 'frecuencia', labels={'releaseyear':'Año de Publicación', 'frecuencia':'Cantidad de Películas'})

# Quinta gráfica
query = """
select y.ReleaseYear, avg(r.RatingScore) AvgRating
from MovieYear y join Ratings r
on y.MovieID = r.MovieID
group by y.ReleaseYear
order by y.ReleaseYear
"""

df = pd.read_sql(query, odbc_connection)

fig5 = px.bar(df, 'releaseyear', 'avgrating', range_y=[1.5,4.05], labels={'releaseyear':'Año de Publicación', 'avgrating':'Rating Promedio'})


#-----------------------------------------------------------------------------
#                                 AQUÍ ESTA LO RELACIONADO AL FRONTEND

# Titulo de la pagina
app.title = 'Laboratorio de Bases de Datos'

# Diseñar la interfaz de usuario
app.layout = html.Div(
    # Este es el fondo
    style={
        'background-image': 'url("/assets/fondo.png")',
        'background-size': 'cover',
        'background-position': 'center',
        'height': '100vh'
    },
    children=[
    # Este conecta el css al python
    html.Link(rel='stylesheet', href='/assets/your_css_file.css'), 

    # Este es el elemento de la barra roja de arriba
    html.Div([html.H1('MovieLens Database Dashboard', style={'font-family': 'Times new Roman', 'text-align': 'center', 'color': '#FFFFFF', 'position': 'absolute', 'top': '50%', 'transform': 'translate(0, -50%)', 'left': '500px'}),
    ], style={'position': 'absolute', 'top': '17px', 'width': '100%', 'z-index': '2','height': '80vh'}),
    html.Div([html.H1('Roberto Gil y María Camila Gómez', style={'font-family': 'MS LineDraw', 'position': 'absolute', 'bottom': '450px', 'right': '250px', 'font-size': 'small','color': '#FFFFFF', 'text-align': 'right' }),
    ], style={'position': 'absolute', 'top': '17px', 'width': '70%', 'z-index': '2','height': '140vh', 'text-align': 'right'}),
    html.Div([
        html.Img(src='/assets/cinee.png', style={'position': 'absolute', 'bottom': '50px', 'right': '50px', 'width': '100px', 'height': '100px'}),
    ], style={'position': 'relative'}),
    html.Div(className='blue-bannerrrr'), 
    html.Div(className='blue-banner'), 

    # Gráficos    
    html.Div([
        dcc.Graph(figure=fig1, style={'display': 'inline-block', 'width': 750, 'height':450}),
        html.Div([
            html.H2('Distribución de Ratings', style={'font-family': 'Times New Roman', 'text-align': 'center', 'color': '#000000'}),
            html.P('De la gráfica se pudo concluir que la calificación de 4 estrellas fue \n la mas votada por los usuarios con un porcentaje de 26.6%. De igual manera la calificación de 0.5 estrellas fue la \n menos votada con un porcentaje de 1.57% '),
        ], style={'display': 'inline-block', 'width': '50%', 'vertical-align': 'top', 'align-items': 'center', 'text-align': 'center'}),
    ], style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center', 'height': '-700vh', 'bottom':'200px'}),

    html.Div([
        html.Div([
            html.H2('Frecuencia de Tags mas relevantes', style={'font-family': 'Times New Roman', 'text-align': 'center', 'color': '#000000'}),
            html.P('A partir de la infromación de la base de datos, concluimos que los Tags Criterion y Comedy fueron los Tags más relevantes para la mayor cantidad de películas '),
        ], style={'display': 'inline-block', 'width': '50%', 'vertical-align': 'top', 'align-items': 'center', 'text-align': 'center'}),
        dcc.Graph(figure=fig2, style={'display': 'inline-block', 'width': 750, 'height':450}),
    ], style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center', 'height': '-700vh', 'bottom':'500px'}),

     html.Div([
        dcc.Graph(figure=fig3, style={'display': 'inline-block', 'width': 750, 'height':450}),
        html.Div([
            html.H2('Promedio vs Cantidad de Ratings', style={'font-family': 'Times New Roman', 'text-align': 'center', 'color': '#000000'}),
            html.P('Según lo visto en el diagrama la película más popular fue Shawshank Redemption, con un buen rating de 4.4 estrellas, teniendo 81k Reviews'),
        ], style={'display': 'inline-block', 'width': '50%', 'vertical-align': 'top', 'align-items': 'center', 'text-align': 'center'}),
    ], style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center', 'height': '-700vh', 'bottom':'800px'}),

    html.Div([
        html.Div([
            html.H2('Frecuencia de Películas por año', style={'font-family': 'Times New Roman', 'text-align': 'center', 'color': '#000000'}),
            html.P('Según la gráfica, el año del que más películas se tiene registro es 2015 con 2513, además que la película más vieja de la que se tiene información es de 1874'),
        ], style={'display': 'inline-block', 'width': '50%', 'vertical-align': 'top', 'align-items': 'center', 'text-align': 'center'}),
        dcc.Graph(figure=fig4, style={'display': 'inline-block', 'width': 750, 'height':450}),
    ], style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center', 'height': '-700vh', 'bottom':'1100px'}),

    html.Div([
        dcc.Graph(figure=fig5, style={'display': 'inline-block', 'width': 750, 'height':450}),
        html.Div([
            html.H2('Promedio de Ratings por Año', style={'font-family': 'Times New Roman', 'text-align': 'center', 'color': '#000000'}),
            html.P('El año con mejores Ratings en promedio es 1957, con 3.99 estrellas. Ningun año llegó a una puntuación promedio de 4 o superior'),
        ], style={'display': 'inline-block', 'width': '50%', 'vertical-align': 'top', 'align-items': 'center', 'text-align': 'center'}),
    ], style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center', 'height': '-700vh', 'bottom':'800px'})
  
])



# Ejecutar la aplicación
app.run_server(debug=True)

odbc_connection.close()