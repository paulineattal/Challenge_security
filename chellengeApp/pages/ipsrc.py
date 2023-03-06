import plotly.graph_objects as go
import plotly.subplots as sp
import plotly.express as px
from dash import html, dcc, Input, Output, callback

# create some data for demonstration purposes
import numpy as np
import pandas as pd



data = pd.DataFrame({'ipsrc': ipsrc, 'nb_portdst': nb_portdst, 'nb_deny': nb_deny})

# Create figure with secondary y-axis
fig = sp.make_subplots(specs=[[{"secondary_y": True}]])

# Add traces
fig.add_trace(
    go.Scatter(x=data['ipsrc'], y=data['nb_portdst'], name="yaxis data", mode='markers', marker_size=4),
    secondary_y=False,
)

fig.add_trace(
    go.Scatter(x=data['ipsrc'], y=data['nb_deny'], name="yaxis2 data", mode='markers', marker_size=4),
    secondary_y=True,
)

# Add figure title
fig.update_layout(
    title_text="Double Y Axis Example"
)

# Set x-axis title
fig.update_xaxes(title_text="xaxis title")

# Set y-axes titles
fig.update_yaxes(title_text="<b>primary</b> yaxis title", secondary_y=False)
fig.update_yaxes(title_text="<b>secondary</b> yaxis title", secondary_y=True)

# Define the layout of the app
app_layout = html.Div([
    dcc.Graph(
        id='graph',
        figure=fig
    ),
    dcc.RangeSlider(
        id='x-range-slider',
        min=data['ipsrc'].min(),
        max=data['ipsrc'].max(),
        step=1,
        value=[data['ipsrc'].min(), data['ipsrc'].max()]
    )
])

# Define the callback function to update the graph based on the slider values
@app.callback(
    Output('graph', 'figure'),
    [Input('x-range-slider', 'value')]
)
def update_figure(x_range):
    filtered_data = data[(data['ipsrc'] >= x_range[0]) & (data['ipsrc'] <= x_range[1])]
    
    # Create figure with secondary y-axis
    fig = sp.make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig.add_trace(
        go.Scatter(x=filtered_data['ipsrc'], y=filtered_data['nb_portdst'], name="yaxis data", mode='markers', marker_size=4),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(x=filtered_data['ipsrc'], y=filtered_data['nb_deny'], name="yaxis2 data", mode='markers', marker_size=4),
        secondary_y=True,
    )

    # Add figure title
    fig.update_layout(
        title_text="Double Y Axis Example"
    )

    # Set x-axis title
fig.update_xaxes(title_text="xaxis title")

# Set y-axes titles
fig.update_yaxes(title_text="<b>primary</b> yaxis title", secondary_y=False)
fig.update_yaxes(title_text="<b>secondary</b> yaxis title", secondary_y=True)
   
