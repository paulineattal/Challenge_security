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


df_tcp = df.loc[df['proto'] == 'TCP']
df_deny = df_tcp[df_tcp['action'] == 'Deny']
df_permit = df_tcp[df_tcp['action'] == 'Permit']
top_ports_deny = df_deny['dstport'].value_counts().nlargest(10).index.tolist()
df_deny = df_deny[df_deny['dstport'].isin(top_ports_deny)]
top_ports_permit = df_permit['dstport'].value_counts().nlargest(10).index.tolist()
df_permit = df_permit[df_permit['dstport'].isin(top_ports_permit)]
df_deny_gb = df_deny.groupby(['policyid', 'dstport']).size().reset_index(name='counts')
df_permit_gb = df_permit.groupby(['policyid', 'dstport']).size().reset_index(name='counts')
fig4 = px.sunburst(df_deny_gb, path=['policyid', 'dstport'], values='counts',
                   color='counts', color_continuous_scale='reds')
fig5 = px.sunburst(df_permit_gb, path=['policyid', 'dstport'], values='counts',
                   color='counts', color_continuous_scale='greens')



df_deny_permit = pd.DataFrame(df_tcp.value_counts(['action','policyid']))
df_deny_permit.reset_index(inplace=True)
df_deny_permit.columns = ['action','policyid','count']
fig6 = px.sunburst(df_deny_permit, path=['action', 'policyid'], values='count',
                    color='action', color_discrete_map={'Deny':'red', 'Permit':'green'},
                    branchvalues='total',
                    )

card4 = dbc.Card(
    dbc.CardBody(
        [
            html.H4('ID règles par rapport aux ports de destination pour action DENY', className='card-title'),
            dcc.Graph(
                id='graph4',
                figure=fig4
            ),
        ]
    )
)

card5 = dbc.Card(
    dbc.CardBody(
        [
            html.H4('ID règles par rapport aux ports de destination pour action PERMIT', className='card-title'),
            dcc.Graph(
                id='graph5',
                figure=fig5
            ),
        ]
    )
)

card6 = dbc.Card(
    dbc.CardBody(
        [
            html.H4('ID règles par rapport aux actions', className='card-title'),
            dcc.Graph(
                id='graph6',
                figure=fig6
            ),
        ]
    )
)

def layout():
    return dbc.Container(
        [
            html.H1("Desciptions action"),
            html.Hr(),
            dbc.Row([
                dbc.Col(
                        card6,
                        width=12,
                    )
            ],
            className="mb-2",
            ),
            dbc.Row(
                [
                    dbc.Col(
                        card4,
                        width=6,
                    ),
                    dbc.Col(
                        card5,
                        width=6,
                    )
                ],
                className="mb-2",
            ),
        ],
        fluid=True,
    )


