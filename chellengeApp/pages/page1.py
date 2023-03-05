import pandas as pd
from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.express as px

df = pd.read_csv(r'C:\Users\pauli\Documents\M2\secu\challenge\Challenge_security\chellengeApp\pages\data_test.csv', sep=',')

###definition des gaphiques fig

# Créer un histogramme des requêtes par heure
requests_per_hour = df.groupby(df['datetime'].str[:2]).size().reset_index(name='count')
fig1 = px.bar(requests_per_hour, x='datetime', y='count', title='Requêtes par heure')

# Créer un graphique à barres pour les adresses IP avec le plus grand nombre de requêtes
ip_counts = df['ip'].value_counts().reset_index()
ip_counts.columns = ['ip', 'count']
top_ips = ip_counts.head(10)
fig2 = px.bar(top_ips, x='ip', y='count', title='Les 10 adresses IP les plus fréquentes')




card1 = dbc.Card(
    dbc.CardBody(
        [
            html.H4('Graph 1', className='card-title'),
            dcc.Graph(
                id='graph1',
                figure=fig1
            ),
        ]
    )
)

card2 = dbc.Card(
    dbc.CardBody(
        [
            html.H4('Graph 2', className='card-title'),
            dcc.Graph(
                id='graph2',
                figure=fig2
            ),
        ]
    )
)



def layout():
    return dbc.Container(
        [
            html.H1("Page 1"),
            html.Hr(),
            dbc.Row(
                [
                    dbc.Col(
                        dcc.DatePickerRange(
                            id='date-picker',
                            display_format='DD/MM/YYYY',
                            start_date_placeholder_text='Start Date',
                            end_date_placeholder_text='End Date',
                        ),
                        width=3,
                    ),
                    dbc.Col(
                        dcc.Dropdown(
                            id='dropdown-code',
                            options=[
                                {'label': '200', 'value': '200'},
                                {'label': '404', 'value': '404'},
                                {'label': '500', 'value': '500'}
                            ],
                            placeholder='Select a Status Code',
                        ),
                        width=3,
                    ),
                    dbc.Col(
                        dcc.Input(
                            id='ip-input',
                            type='text',
                            placeholder='Enter an IP Address',
                        ),
                        width=3,
                    ),
                ],
                className="mb-2",
            ),
            dbc.Row(
                [
                    dbc.Col(
                        card1,
                        width=3,
                    ),
                    dbc.Col(
                        card2,
                        width=3,
                    )
                ],
                className="mb-2",
            ),
        ],
        fluid=True,
    )

dcc.Dropdown(
    id='dropdown-code',
    options=[
        {'label': '200', 'value': '200'},
        {'label': '404', 'value': '404'},
        {'label': '500', 'value': '500'},
        # Ajoutez d'autres codes de retour si besoin
    ],
    value='200'
)

from datetime import date
from datetime import timedelta
dcc.DatePickerRange(
    id='date-picker-range',
    min_date_allowed=date(2022, 1, 1),
    max_date_allowed=date.today(),
    initial_visible_month=date.today(),
    start_date=date.today() - timedelta(7),
    end_date=date.today()
)

dcc.Input(
    id='input-ip',
    type='text',
    placeholder='Entrez une adresse IP'
)

import plotly.express as px

# Mise à jour du premier graphe en fonction des filtres appliqués
@callback(
    Output('graph-1', 'figure'),
    [Input('filter-code', 'value'),
     Input('filter-date', 'start_date'),
     Input('filter-date', 'end_date'),
     Input('filter-ip', 'value')])
def update_graphes_1(code, start_date, end_date, ip):
    # Filtrage des données en fonction des valeurs des filtres
    filtered_df = df[(df['code'] == code) &
                     (df['date'].dt.date >= start_date) &
                     (df['date'].dt.date <= end_date) &
                     (df['ip'].isin(ip))]
    
    # Calcul des données à afficher sur le graphe
    data = filtered_df.groupby('method')[['size']].sum().reset_index()
    
    # Création et renvoi de la figure
    fig = px.bar(data, x='method', y='size', labels={'size': 'Taille totale (en octets)'})
    fig.update_layout(title='Taille totale des requêtes par méthode HTTP',
                      xaxis_title='Méthode HTTP', yaxis_title='Taille totale (en octets)')
    return fig


# Mise à jour du deuxième graphe en fonction des filtres appliqués
@callback(
    Output('graph-2', 'figure'),
    [Input('filter-code', 'value'),
     Input('filter-date', 'start_date'),
     Input('filter-date', 'end_date'),
     Input('filter-ip', 'value')])
def update_graphes_2(code, start_date, end_date, ip):
    # Filtrage des données en fonction des valeurs des filtres
    filtered_df = df[(df['code'] == code) &
                     (df['date'].dt.date >= start_date) &
                     (df['date'].dt.date <= end_date) &
                     (df['ip'].isin(ip))]
    
    # Calcul des données à afficher sur le graphe
    data = filtered_df.groupby('ip')[['size']].sum().reset_index()
    
    # Création et renvoi de la figure
    fig = px.pie(data, values='size', names='ip')
    fig.update_layout(title='Répartition des requêtes par adresse IP',
                      xaxis_title='Adresse IP', yaxis_title='Taille totale (en octets)')
    return fig


# Mise à jour du troisième graphe en fonction des filtres appliqués
@callback(
    Output('graph-3', 'figure'),
    [Input('filter-code', 'value'),
     Input('filter-date', 'start_date'),
     Input('filter-date', 'end_date'),
     Input('filter-ip', 'value')])
def update_graphes_3(code, start_date, end_date, ip):
    # Filtrage des données en fonction des valeurs des filtres
    filtered_df = df[(df['code'] == code) &
                     (df['date'].dt.date >= start_date) &
                     (df['date'].dt.date <= end_date) &
                     (df['ip'].isin(ip))]
    
    # Calcul des données à afficher sur le graphe
    data = filtered_df.groupby(pd.Grouper(key='date', freq='1H')).size().reset_index(name='count')
    
    # Création et renvoi de la figure
    fig = px.line(data, x='date', y='count')
    fig.update_layout(title='titre',
                      xaxis_title='x', yaxis_title='y')
    return fig

