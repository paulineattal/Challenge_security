import pandas as pd
from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.express as px

import os
import re


path = os.getcwd()
filename = str(path)+"/data/test_sise.txt"

log_regex = r'(\S+)\s+(\d+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+:\d+)\s+(\S+)\s+(\S+)\s+(\S+)\s+\[(.+)\]\s+"(.+)"\s+(\d+)\s+(\d+|-)\s+"(.+)"\s+"(.+)"'

with open(filename) as file:
    log_data = file.read()
log_list = re.findall(log_regex, log_data, re.MULTILINE)
df = pd.DataFrame(log_list, columns = ['month', 'day', 'time', 'ip', 'user', 'server', 'local_ip', 'client_id', 'user_id', 'request_datetime', 'request', 'status', 'response_size', 'referrer', 'user_agent'])

# Supprimer le fuseau horaire à la fin de request_datetime
#df['request_datetime'] = df['request_datetime'].str.replace(r'-\d{4}$', '', regex=True)

df[['hour', 'minute', 'second']] = df['time'].str.split(':', expand=True)

###definition des gaphiques fig

# Créer un histogramme des requêtes par heure
# Créer un histogramme des requêtes par minute pour une heure donnée
requests_per_minute = df.groupby('minute')['hour'].value_counts().reset_index(name='count')
fig1 = px.bar(requests_per_minute, x='minute', y='count', title='Requêtes par minute')

#requests_per_hour = df.groupby(df['minute']).size().reset_index(name='count')
#fig1 = px.bar(requests_per_hour, x='minute', y='count', title='Requêtes par heure')

# Créer un graphique à barres pour les adresses IP avec le plus grand nombre de requêtes
ip_counts = df['local_ip'].value_counts().reset_index()
ip_counts.columns = ['local_ip', 'count']
top_ips = ip_counts.head(10)
fig2 = px.bar(top_ips, x='local_ip', y='count', title='Les 10 adresses IP les plus fréquentes')

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
            html.H1("Statistques des logs Apache"),
            html.Hr(),
            dbc.Row(
            [
                dbc.Col(
                    dcc.Dropdown(
                        id='hour-dropdown',
                        options=[{'label': str(i) + ':00', 'value': i} for i in range(24)],
                        placeholder='Select an hour'
                    ),
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='status-dropdown',
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
                        width=6,
                    ),
                    dbc.Col(
                        card2,
                        width=6,
                    )
                ],
                className="mb-2",
            ),
        ],
        fluid=True,
    )


@callback(
    [Output('graph1', 'figure'),
     Output('graph2', 'figure')],
    [Input('hour-dropdown', 'value'),
     Input('status-dropdown', 'value'),
     Input('ip-input', 'value')])
def update_figures(hour, status, ip):
    filtered_df = df.copy()
    if hour :
        filtered_df = filtered_df[(filtered_df['hour'] == hour)]
    if status:
        filtered_df = filtered_df[filtered_df['status'] == int(status)]
    if ip:
        filtered_df = filtered_df[filtered_df['local_ip'] == ip]

    # Update fig1
    if not filtered_df.empty:        
        requests_per_minute = df.groupby('minute')['hour'].value_counts().reset_index(name='count')
        fig1 = px.bar(requests_per_minute, x='minute', y='count', title='Requêtes par minute')
    else:
        fig1 = px.bar(df.groupby(df['minute']).size().reset_index(name='count'), x='minute', y='count', title='Requêtes par minute')

    # Update fig2
    if not filtered_df.empty:
        ip_counts = filtered_df['local_ip'].value_counts().reset_index()
        ip_counts.columns = ['local_ip', 'count']
        top_ips = ip_counts.head(10)
        fig2 = px.bar(top_ips, x='local_ip', y='count', title='Les 10 adresses IP les plus fréquentes')
    else:
        ip_counts = df['local_ip'].value_counts().reset_index()
        ip_counts.columns = ['local_ip', 'count']
        top_ips = ip_counts.head(10)
        fig2 = px.bar(top_ips, x='local_ip', y='count', title='Les 10 adresses IP les plus fréquentes')

    return fig1, fig2
