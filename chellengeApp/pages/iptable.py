import pandas as pd
from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.express as px

df = pd.read_csv(r'C:\Users\pauli\Documents\M2\secu\challenge\Challenge_security\chellengeApp\data\log_fw_3.csv', sep=';', header=None)

###definition des gaphiques fig
df.drop([8,9], axis=1, inplace=True)
cnames = ['datetime','ipsrc','ipdst','proto','portsrc','portdst','policyid','action','numproto']
df.columns = cnames
df['policyid'] = df['policyid'].values.astype('int')
df['policyid'] = df['policyid'].values.astype('str')


rules = pd.DataFrame(df['policyid'].value_counts(normalize=True))
#rules = pd.DataFrame(df['policyid'][df['proto'] == "TCP"].value_counts(normalize=True))
rules.reset_index(inplace=True)
rules.columns = ['policyid','percentage']
rules5 = rules.head(5)
#threshold = 0.2
#rules5 = rules5[rules5['percentage'] > threshold]
rules5['percentage'] = rules5['percentage']*100
fig3 = px.bar(rules5, x='policyid', y='percentage', title='Most used rules')


# Créer un histogramme des requêtes par heure

card3 = dbc.Card(
    dbc.CardBody(
        [
            html.H4('Classement des règles les plus utilisées', className='card-title'),
            dcc.Graph(
                id='graph3',
                figure=fig3
            ),
        ]
    )
)

def layout():
    return dbc.Container(
        [
            html.H1("Desciptions Iptable"),
            html.Hr(),
            dbc.Row([
                dbc.Col(
                    dcc.Dropdown(
                        id='protocol-dropdown',
                        options=[
                            {'label': 'UDP', 'value': 'UDP'},
                            {'label': 'TCP', 'value': 'TCP'}
                        ],
                        placeholder='Select a Status protocol',
                    ),
                    width=3,
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='TOP-dropdown',
                        options=[
                            {'label': '5', 'value': 5},
                            {'label': '10', 'value': 10}
                        ],
                        placeholder='Select a TOP',
                    ),
                    width=3,
                )
            ],
            className="mb-2",
            ),
            dbc.Row(
                [
                    dbc.Col(
                        card3,
                        width=12,
                    )
                ],
                className="mb-2",
            ),
        ],
        fluid=True,
    )

@callback(
    [Output('graph3', 'figure')],
    [Input('protocol-dropdown', 'value'),
     Input('TOP-dropdown', 'value')]
)
def update_figures(protocol, top):
    global df
    df = df.copy()

    # Filtrer par protocol
    if protocol is not None:
        protocol = protocol
    else : 
        protocol = "TCP"

    # Filtrer par top
    if top is not None: 
        top = top
    else :
        top = 5
          
    
    rules = pd.DataFrame(df['policyid'][df['proto'] == protocol].value_counts(normalize=True))
    rules.reset_index(inplace=True)
    rules.columns = ['policyid','percentage']
    rules5 = rules.head(top)
    #threshold = 0.2
    #rules5 = rules5[rules5['percentage'] > threshold]
    rules5['percentage'] = rules5['percentage']*100
    fig3 = px.bar(rules5, x='policyid', y='percentage', title='Most used rules')

    return [fig3]
