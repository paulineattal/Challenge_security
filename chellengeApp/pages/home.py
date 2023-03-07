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
                            "ont créé une application Dash Python qui affiche des graphiquess de données de logs "
                            "d'un firewall qui a été configuré par les experts en sécurité. Les expert en sécurité "
                            "ont fournit un fichiers .csv aux data analystes pour effectuer leur travails. "
                            "Les experts en sécurité ont simulés des attaques qui arrivaient a apsser leurs règles "
                            "Le but de notre projet est de créer un modèle de machine learning qui va pouvoir "
                            "détecter si une requête est une attaque ou non, en se basant sur l'analyses de plusieurs critères."
                            "Dans un objectif d'amélioration du projet, une deuxième analyse et un deuxieme modèle "
                            "pourra etre créé en se basant sur les logs du serveur web."
                            ),
                    className="mb-5")
        ]),
        dbc.Row([
            dbc.Col(html.H2("Présentation de l'application", className="text-center")
                    , className="mb-4")
        ]),
        dbc.Row([
            dbc.Col([
                html.P("Voici les différentes pages disponibles, toutes les pages de l'application sont accessibles via le menu en haut de la page :"),
                html.Ul([
                    html.Li("La page d'accueil présente le projet et l'application."),
                    html.Li("La page 'Fw. Protocol' permet de visualiser les requêtes par protocole."),
                    html.Li("La page 'Fw. Action' permet de visualiser les paquets passés ou non en fonction de la règle et du port."),
                    html.Li("La page 'Fw. Ipsrc' permet de visualiser des caractéristiques des requêtes par IP source."),
                    html.Li("La page 'Fw. Statistiques' permet de visualiser des TOP sur les Ip sources et sur les ports."),
                    html.Li("La page 'Fw. Modèle' permet de visualiser les résultats du modèle de machine learning sur les logs firewall."),
                    html.Li("La page 'Fw. Contact' permet de contacter les développeurs de l'application.")
                ])
            ], className="mb-5")
        ]),
        dbc.Row([
            dbc.Col(html.Img(src="/assets/logo_home.jpg", height="300px"),
                    className="mb-5 mt-5 text-center")
        ])
    ])
])

