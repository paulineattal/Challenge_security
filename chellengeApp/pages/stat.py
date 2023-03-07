import pandas as pd
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px

import os
path = os.getcwd()
df = pd.read_csv(path+'/data/FW.csv', sep=',')

df['policyid'] = df['policyid'].astype(str)
df['dstport'] = pd.to_numeric(df['dstport'], errors='coerce', downcast='integer')
df['datetime'] = pd.to_datetime(df['datetime'])


top5_ipsrc = df['ipsrc'].value_counts().nlargest(5)
# Visualisation du TOP 5 des IP sources les plus émettrices
fig8 = px.bar(x=top5_ipsrc.index, y=top5_ipsrc.values, labels={'x':'IP source', 'y':'Nombre de paquets'}, title='TOP 5 des IP sources les plus émettrices')

# TOP 10 des ports inférieurs à 1024 avec un accès autorisé
top10_ports = df.loc[(df['dstport'] < 1024) & (df['action'] == 'Permit'), 'dstport'].value_counts().nlargest(10)


# Définition du dictionnaire port_labels
port_labels = {
    20: 'FTP data',
    21: 'FTP control',
    22: 'SSH',
    23: 'Telnet',
    25: 'SMTP',
    53: 'DNS',
    80: 'HTTP',
    110: 'POP3',
    119: 'NNTP',
    143: 'IMAP',
    443: 'HTTPS'
}

# Création d'une série contenant les modalités des ports
modalites_ports = top10_ports.index.map(port_labels)

# Visualisation du TOP 10 des ports inférieurs à 1024 avec un accès autorisé en modalités
fig9 = px.bar(x=modalites_ports, y=top10_ports.values, labels={'x':'Port destination', 'y':'Nombre de paquets'}, title='TOP 10 des ports inférieurs à 1024 avec un accès autorisé')

card8 = dbc.Card(
    dbc.CardBody(
        [
            html.H4('TOP 5 des IP sources les plus émettrices', className='card-title'),
            dcc.Graph(
                id='graph8',
                figure=fig8
            ),
        ]
    )
)

card9 = dbc.Card(
    dbc.CardBody(
        [
            html.H4('TOP 10 des ports inférieurs à 1024 avec un accès autorisé', className='card-title'),
            dcc.Graph(
                id='graph9',
                figure=fig9
            ),
        ]
    )
)

def layout():
    return dbc.Container(
        [
            html.H1("Statistiques"),
            html.Hr(),
            dbc.Row(
                [
                    dbc.Col(
                        card8,
                        width=6,
                    ),
                    dbc.Col(
                        card9,
                        width=6,
                    )
                ],
                className="mb-2",
            ),
        ],
        fluid=True,
    )


