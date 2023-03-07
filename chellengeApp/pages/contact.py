import dash_bootstrap_components as dbc
from dash import html

devs = [
    {'name': 'ELOUETClement', 'email': 'clement.elouet@univ-lyon2.fr'},
    {'name': 'PHAM Marguerite', 'email': 'marguerite.pham@univ-lyon2.fr'},
    {'name': 'HOANG THI NGOC Tho', 'email': 'thi-ngoc-tho.hoang@univ-lyon2.fr'},
    {'name': 'ATTAL Pauline', 'email': 'pauline.attal@univ-lyon2.fr'},
    {'name': 'PAPAZIAN Louison', 'email': 'louison.papazian@univ-lyon2.fr'}
]

# Mise en forme de la page
layout = html.Div([
    dbc.Container([
        html.H1('Contactez les développeurs'),

        # Création d'une liste pour chaque développeur
        html.Ul([html.Li([
            html.H3(dev['name']),
            html.P('Email : '),
            html.A(dev['email'], href=f"mailto:{dev['email']}")
        ]) for dev in devs])
    ])
])
