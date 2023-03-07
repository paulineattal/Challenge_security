import dash
import dash_bootstrap_components as dbc
import gunicorn

app = dash.Dash(__name__, suppress_callback_exceptions=True, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server


