import pandas as pd
from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.express as px

df = pd.read_csv(r'C:\Users\pauli\Documents\M2\secu\challenge\Challenge_security\chellengeApp\data\log_fw_3.csv', sep=',')

###definition des gaphiques fig

# Créer un histogramme des requêtes par heure

card1 = dbc.Card(
    dbc.CardBody(
        [
            html.H4('Graph 1', className='card-title'),
            dcc.Graph(
                id='graph1'
                #figure=fig1
            ),
        ]
    )
)

card2 = dbc.Card(
    dbc.CardBody(
        [
            html.H4('Graph 2', className='card-title'),
            dcc.Graph(
                id='graph2'
                #figure=fig2
            ),
        ]
    )
)



def layout():
    return dbc.Container(
        [
            html.H1("Desciptions Iptable"),
            html.Hr(),
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


