import pandas as pd
from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.express as px

df = pd.read_csv(r'C:\Users\pauli\Documents\M2\secu\challenge\Challenge_security\chellengeApp\data\log_fw_3.csv', sep=';', header=None)
df.drop([8,9], axis=1, inplace=True)
cnames = ['datetime','ipsrc','ipdst','proto','portsrc','portdst','policyid','action','numproto']
df.columns = cnames
df['policyid'] = df['policyid'].astype(str)
df['portsrc'] = pd.to_numeric(df['portsrc'], errors='coerce', downcast='integer')
df['portdst'] = pd.to_numeric(df['portdst'], errors='coerce', downcast='integer')
df['numproto'] = df['numproto'].astype(str)
df['datetime'] = pd.to_datetime(df['datetime'])



df_tcp = df.loc[df['proto'] == 'TCP']
df_deny = df_tcp[df_tcp['action'] == 'DENY']
df_permit = df_tcp[df_tcp['action'] == 'PERMIT']
top_ports_deny = df_deny['portdst'].value_counts().nlargest(10).index.tolist()
df_deny = df_deny[df_deny['portdst'].isin(top_ports_deny)]
top_ports_permit = df_permit['portdst'].value_counts().nlargest(10).index.tolist()
df_permit = df_permit[df_permit['portdst'].isin(top_ports_permit)]
df_deny_gb = df_deny.groupby(['policyid', 'portdst']).size().reset_index(name='counts')
df_permit_gb = df_permit.groupby(['policyid', 'portdst']).size().reset_index(name='counts')
fig4 = px.sunburst(df_deny_gb, path=['policyid', 'portdst'], values='counts')
fig5 = px.sunburst(df_permit_gb, path=['policyid', 'portdst'], values='counts')


df_deny_permit = pd.DataFrame(df_tcp.value_counts(['action','policyid']))
df_deny_permit.reset_index(inplace=True)
df_deny_permit.columns = ['action','policyid','count']
fig6 = px.sunburst(df_deny_permit, path=['action', 'policyid'], values='count')

card4 = dbc.Card(
    dbc.CardBody(
        [
            html.H4('Classement des règles les plus utilisées', className='card-title'),
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
            html.H4('Classement des règles les plus utilisées', className='card-title'),
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
            html.H4('Classement des règles les plus utilisées', className='card-title'),
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
                        card4,
                        width=12,
                    )
            ],
            className="mb-2",
            ),
            dbc.Row(
                [
                    dbc.Col(
                        card5,
                        width=6,
                    ),
                    dbc.Col(
                        card6,
                        width=6,
                    )
                ],
                className="mb-2",
            ),
        ],
        fluid=True,
    )


