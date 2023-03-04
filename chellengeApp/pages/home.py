import dash_bootstrap_components as dbc
from dash import html

layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Bienvenue sur notre projet de sécurité", className="text-center")
                    , className="mb-5 mt-5")
        ]),
        dbc.Row([
            dbc.Col(html.H2("Présentation du projet", className="text-center")
                    , className="mb-4")
        ]),
        dbc.Row([
            dbc.Col(html.P("Notre projet est une collaboration entre des étudiants en sécurité "
                            "et des étudiants en analyse de données. Les analystes de données "
                            "ont créé une application Dash Python qui affiche des graphes de données de logs "
                            "d'un serveur Apache qui a été configuré par les experts en sécurité. Les experts en sécurité "
                            "ont configuré ce serveur qui récupère des logs d'un pare-feu ou n'importe quel autre serveur "
                            ": ils ont configuré les règles firewall pour laisser passer ou non des paquets. "
                            "Le but pour les analystes de données est de créer un modèle spécifique pour détecter "
                            "si une requête/paquet qui est passé sur le serveur est une attaque ou non. "
                            "Ce modèle est appelé dans l'application pour afficher des graphes spécifiques."),
                    className="mb-5")
        ]),
        dbc.Row([
            dbc.Col(html.H2("Présentation de l'application", className="text-center")
                    , className="mb-4")
        ]),
        dbc.Row([
            dbc.Col(html.P("page 1 : blablabla"),
                    className="mb-5")
        ]),
        dbc.Row([
            dbc.Col(html.Img(src="/assets/logo_home.jpg", height="300px"),
                    className="mb-5 mt-5 text-center")
        ])
    ])
])

