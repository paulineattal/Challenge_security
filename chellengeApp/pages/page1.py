import pandas as pd
from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go

df = pd.read_csv(r'C:\Users\pauli\Documents\M2\secu\challenge\Challenge_security\chellengeApp\data\data_test.csv', sep=',')

###definition des gaphiques fig

# Créer un histogramme des requêtes par heure
requests_per_hour = df.groupby(df['minute']).size().reset_index(name='count')
fig1 = px.bar(requests_per_hour, x='minute', y='count', title='Requêtes par heure')

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
    [Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date'),
     Input('status-dropdown', 'value'),
     Input('ip-input', 'value')])
def update_figures(start_date, end_date, status, ip):
    filtered_df = df.copy()
    if start_date and end_date:
        filtered_df = filtered_df[(filtered_df['time'] >= start_date) & (filtered_df['time'] <= end_date)]
    if status:
        filtered_df = filtered_df[filtered_df['status'] == int(status)]
    if ip:
        filtered_df = filtered_df[filtered_df['local_ip'] == ip]

    # Update fig1
    if not filtered_df.empty:
        requests_per_minute = filtered_df.groupby(filtered_df['minute']).size().reset_index(name='count')
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
