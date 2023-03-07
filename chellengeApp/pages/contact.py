import dash_bootstrap_components as dbc
from dash import html

devs = [    {'name': 'ELOUETClement', 'email': 'clement.elouet@univ-lyon2.fr'},    {'name': 'PHAM Marguerite', 'email': 'marguerite.pham@univ-lyon2.fr'},    {'name': 'HOANG THI NGOC Tho', 'email': 'thi-ngoc-tho.hoang@univ-lyon2.fr'},    {'name': 'ATTAL Pauline', 'email': 'pauline.attal@univ-lyon2.fr'},    {'name': 'PAPAZIAN Louison', 'email': 'louison.papazian@univ-lyon2.fr'}]

# Mise en forme de la page
layout = html.Div([
    dbc.Container([
        html.H1('Contactez les développeurs', className='display-4 mt-5 mb-3 text-center'),

        # Création d'une liste pour chaque développeur
        dbc.Row([dbc.Col(html.Div([
            html.H3(dev['name'], className='h5 font-weight-bold'),
            html.P('Email : '),
            html.A(dev['email'], href=f"mailto:{dev['email']}", className='text-muted font-weight-bold')
        ], className='bg-light rounded p-3 mb-3 shadow-sm'), width=12) for dev in devs])
    ], className='py-5')
])
