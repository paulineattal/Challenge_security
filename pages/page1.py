from dash import dcc, html
import pandas as pd
import plotly.express as px

# Dummy data
df = pd.DataFrame({
    "x": [1, 2, 3, 4, 5],
    "y": [2, 3, 1, 5, 4]
})

# Layout for page 1
layout = html.Div(
    [
        html.H2("Page 1"),
        html.Div(
            [
                dcc.Graph(
                    figure=px.scatter(df, x="x", y="y", title="Scatter Plot")
                ),
                dcc.Graph(
                    figure=px.line(df, x="x", y="y", title="Line Plot")
                ),
            ],
            className="row",
        ),
    ]
)
