from dash import html, Input, Output, dcc
from app import app
from pages import home, page1
import dash_bootstrap_components as dbc

# Navbar layout

navbar = dbc.Navbar(
    #définition du contener qui comportera des pages avec les liens
    dbc.Container(
        [
            dbc.Row([
                dbc.Col([
                    dbc.NavbarToggler(id="navbar-toggler"),
                    dbc.Nav([
                        #pourchaque page, on créer un lien
                        dbc.NavItem(dbc.NavLink("Home", href="/")),
                        dbc.NavItem(dbc.NavLink("Page 1", href="/page1")),
                    ])
                ],width=10), 
        ]),
        ],
        fluid=True,
    ),
    #couleurs de la barre de navigation
    dark=True,
    color='secondary'
)

# App layout with navbar
app.layout = html.Div([
    navbar,
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/':
        return home.layout
    elif pathname == '/page1':
        return page1.layout
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True)
