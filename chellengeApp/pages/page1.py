import pandas as pd
from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc

filename = "C:/Users/pauli/Documents/M2/secu/challenge/Challenge_security/chellengeApp/pages/test_sise.txt"

# Définir la liste des noms de colonnes pour le dataframe
column_names = ['date', 'ip_address', 'server_name', 'client_identity', 'user_identity', 'timestamp', 'request', 'status_code', 'response_size', 'referer', 'user_agent']

# Ouvrir le fichier texte et lire les lignes en tant que liste
with open(filename, 'r') as f:
    lines = f.readlines()

# Créer une liste vide pour stocker chaque ligne de données en tant que dictionnaire
data_list = []

# Boucle à travers chaque ligne et extraire les données en tant que dictionnaire
for line in lines:
    # Diviser la ligne en utilisant l'espace comme séparateur
    fields = line.split()
    # Extraire chaque champ de données et l'ajouter au dictionnaire
    data_dict = {
        'date': fields[0] + ' ' + fields[1] + ' ' + fields[2],
        'ip_address': fields[3],
        'server_name': fields[4].split(':')[0],
        'client_identity': fields[4].split(':')[1] if len(fields[4].split(':')) > 1 else '-',
        'user_identity': fields[5] if fields[5] != '-' else '-',
        'timestamp': fields[6].lstrip('['),
        'request': fields[7] + ' ' + fields[8] + ' ' + fields[9],
        'status_code': fields[10],
        'response_size': fields[11],
        'referer': fields[12][1:-1] if fields[12] != '-' else '-',
        'user_agent': ' '.join(fields[13:])[1:-2] if fields[12] != '-' else '-'
    }
    # Ajouter le dictionnaire à la liste de données
    data_list.append(data_dict)

# Convertir la liste de dictionnaires en un dataframe Pandas
df = pd.DataFrame(data_list, columns=column_names)


card1 = dbc.Card(
    dbc.CardBody(
        [
            html.H4('Graph 1', className='card-title'),
            dcc.Graph(
                id='graph1',
                figure={
                    'data': [
                        {'x': df['date'], 'y': df['timestamp'], 'type': 'line', 'name': 'Response Time'},
                    ],
                    'layout': {
                        'title': 'Response Time by Date',
                        'xaxis': {'title': 'Date'},
                        'yaxis': {'title': 'Response Time (ms)'},
                    }
                }
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
                figure={
                    'data': [
                        {'x': df['date'], 'y': df['response_size'], 'type': 'bar', 'name': 'Bytes Sent'},
                    ],
                    'layout': {
                        'title': 'Bytes Sent by Date',
                        'xaxis': {'title': 'Date'},
                        'yaxis': {'title': 'Bytes Sent'},
                    }
                }
            ),
        ]
    )
)

card3 = dbc.Card(
    dbc.CardBody(
        [
            html.H4('Graph 3', className='card-title'),
            dcc.Graph(
                id='graph3',
                figure={
                    'data': [
                        {'x': df['date'], 'y': df['request'], 'type': 'scatter', 'mode': 'lines', 'name': 'Requests'},
                    ],
                    'layout': {
                        'title': 'Requests by Date',
                        'xaxis': {'title': 'Date'},
                        'yaxis': {'title': 'Requests'},
                    }
                }
            ),
        ]
    )
)

card4 = dbc.Card(
    dbc.CardBody(
        [
            html.H4('Graph 4', className='card-title'),
            dcc.Graph(
                id='graph4',
                figure={
                    'data': [
                        {'x': df['date'], 'y': df['status_code'], 'type': 'scatter', 'mode': 'markers', 'name': 'Status Code'},
                    ],
                    'layout': {
                        'title': 'Status Code by Date',
                        'xaxis': {'title': 'Date'},
                        'yaxis': {'title': 'Status Code'},
                    }
                }
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
                className="mb-4",
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
                    ),
                    dbc.Col(
                        card3,
                        width=3,
                    ),
                    dbc.Col(
                        card4,
                        width=3,
                    ),
                ],
                className="mb-4",
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

