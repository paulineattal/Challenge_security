import plotly.graph_objects as go
import plotly.subplots as sp
from dash import html, dcc, Input, Output, callback
import pandas as pd
import dash_bootstrap_components as dbc
from plotly.subplots import make_subplots



df = pd.read_csv(r'C:\Users\pauli\Documents\M2\secu\challenge\Challenge_security\chellengeApp\data\log_fw_3.csv', sep=';', header=None)
df.drop([8,9], axis=1, inplace=True)
cnames = ['datetime','ipsrc','ipdst','proto','portsrc','portdst','policyid','action','numproto']
df.columns = cnames
df['policyid'] = df['policyid'].astype(str)
df['portsrc'] = pd.to_numeric(df['portsrc'], errors='coerce', downcast='integer')
df['portdst'] = pd.to_numeric(df['portdst'], errors='coerce', downcast='integer')
df['numproto'] = df['numproto'].astype(str)
df['datetime'] = pd.to_datetime(df['datetime'])

#count unique value of portdst for each ipsrc
test = df.groupby('ipsrc')['portdst'].nunique()
test = pd.DataFrame(test)
test.reset_index(inplace=True)
test.columns = ['ipsrc','nb_portdst']

Dipsrc = df.groupby('ipsrc')['action'].value_counts()

Dipsrc = pd.DataFrame(Dipsrc)
Dipsrc.columns = ['count']
Dipsrc.reset_index(inplace=True)
Dipsrc = Dipsrc[Dipsrc['action']=='DENY'].drop(['action'], axis=1)


distinct_ipsrc = df['ipsrc'].unique()
#merge Dipsrc and distinct_ipsrc to have all ipsrc with count=0 if they don't have any DENY
Dipsrc = Dipsrc.merge(pd.DataFrame(distinct_ipsrc, columns=['ipsrc']), on='ipsrc', how='outer')
Dipsrc['count'] = Dipsrc['count'].fillna(0)


#join test and Dipsrc on ipsrc
p = test.merge(Dipsrc, on='ipsrc')
p.columns = ['ipsrc','nb_portdst','nb_deny']
p.reset_index(drop=True, inplace=True)

# Create figure with secondary y-axis
fig = sp.make_subplots(specs=[[{"secondary_y": True}]])

# Add traces
fig.add_trace(
    go.Scatter(x=p['ipsrc'], y=p['nb_portdst'], name="nb portdst", mode='markers', marker_size=4),
    secondary_y=False,
)

fig.add_trace(
    go.Scatter(x=p['ipsrc'], y=p['nb_deny'], name="nb deny", mode='markers', marker_size=4),
    secondary_y=True,
)


# Add figure title
fig.update_layout(
    title_text="Number of portdst and number of deny for each ipsrc"
)

# Set x-axis title
fig.update_xaxes(title_text="ipsrc")

# Set y-axes titles
fig.update_yaxes(title_text="number of <b>portdst</b> and <b>deny</b>", secondary_y=False)


card7 = dbc.Card(
    dbc.CardBody(
        [
            html.H4('IP', className='card-title'),
            dcc.Graph(
                id='graph7',
                figure=fig
            ),
        ]
    )
)

# Define the layout of the app
def layout():
    return dbc.Container(
        [
            html.H1("Desciptions ipsrc"),
            html.Hr(),
            dbc.Row([
                dbc.Col(
                    dcc.Input(
                        id='min-port',
                        type='number',
                        placeholder='Enter a number of port min try',
                    ),
                    width=3,
                ),
                dbc.Col(
                    dcc.Input(
                        id='min-deny',
                        type='number',
                        placeholder='Enter a number of access denied min',
                    ),
                    width=3,
                ),
            ], className="mb-2",
            ),
            dbc.Row([
                dbc.Col(
                        card7,
                        width=12,
                    )
            ],
            className="mb-2",
            ),
        ],
        fluid=True,
    )


# Define the callback function to update the graph based on the slider values
@callback(
    Output('graph7', 'figure'),
    [Input('min-deny', 'value'),
     Input('min-port', 'value'),]
)
def update_figure(deny, port):
    global p
    p = p.copy()
    if deny is not None:
        deny = int(deny)
    else : 
        deny = 5000
    if port is not None:
        port = int(port)
    else : 
        port = 5000

    p = p[(p['nb_portdst'] >= port) & (p['nb_deny'] >= deny)]
    
    # Create figure with secondary y-axis
    fig = sp.make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig.add_trace(
        go.Scatter(x=p['ipsrc'], y=p['nb_portdst'], name="nd portdst", mode='markers', marker_size=4),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(x=p['ipsrc'], y=p['nb_deny'], name="nb deny", mode='markers', marker_size=4),
        secondary_y=True,
    )

    # Add figure title
    fig.update_layout(
        title_text="Number of portdst and number of deny for each ipsrc"
    )

    # Set x-axis title
    fig.update_xaxes(title_text="ipsrc")

    # Set y-axes titles
    fig.update_yaxes(title_text="number of <b>portdst</b> and <b>deny</b>", secondary_y=False)

    return fig
   
