from dash import html, Input, Output, dcc
from app import app
from pages import home, page1, protocol, action, ipsrc, stat, contact, model
import dash_bootstrap_components as dbc
import gunicorn
from app import server

# Navbar layout
navbar = dbc.Navbar(
    dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        html.A(
                            dbc.Row(
                                [
                                    dbc.Col(
                                        html.Img(src="/assets/logo.png", height="30px")
                                    ),
                                    dbc.Col(dbc.NavbarBrand("Home Secu-Data", className="ml-2")),
                                ],
                                align="center",
                                className="no-gutters",
                            ),
                            href="/",
                        ),
                        width="auto",
                    ),
                    dbc.Col(
                        dbc.Nav(
                            [
                                dbc.NavItem(dbc.NavLink("FW. Protocol", href="/protocol")),
                                dbc.NavItem(dbc.NavLink("FW. Action", href="/action")),
                                dbc.NavItem(dbc.NavLink("FW. Ipsrc", href="/ipsrc")),
                                dbc.NavItem(dbc.NavLink("FW. Statistiques", href="/stat")),
                                dbc.NavItem(dbc.NavLink("FW. Modele", href="/model")),
                                dbc.NavItem(dbc.NavLink("Logs Apache", href="/page1")),
                                dbc.NavItem(dbc.NavLink("Contact", href="/contact", className="ml-auto")),
                            ],
                            navbar=True,
                        ),
                        width=True,
                        className="ml-auto",
                    ),
                ],
                align="center",
            ),
        ],
        fluid=True,
    ),
    color="dark",
    dark=True,
)

# App layout with navbar
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/':
        return home.layout
    elif pathname == '/page1':
        return page1.layout()
    elif pathname == '/protocol':
        return protocol.layout()
    elif pathname == '/action':
        return action.layout()
    elif pathname == '/ipsrc':
        return ipsrc.layout()
    elif pathname == '/stat':
        return stat.layout()
    elif pathname == '/model':
        return model.layout()
    elif pathname == '/contact':
        return contact.layout
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True)
