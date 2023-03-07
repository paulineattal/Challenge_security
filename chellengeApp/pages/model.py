
import pandas as pd
import os
import plotly.express as px
from scipy.cluster.hierarchy import linkage, fcluster
import dash_bootstrap_components as dbc
from dash import html, dcc
import seaborn as sns


path = os.getcwd()
df = pd.read_csv(path+'/data/FW.csv', sep=',')
df.dstport.astype("float")
df.policyid.astype("float")
# CAH

df_actif = df[["dstport","proto","action","policyid"]]
df_actif = pd.get_dummies(df_actif, columns=df_actif.select_dtypes('object').columns)

def matrice_lien(df):
    #générer la matrice des liens
    dist_ind_data =linkage(df.values,method='ward',metric='euclidean')
    return dist_ind_data

dist_ind_data = matrice_lien(df_actif)
#affichage du dendrogramme

#fig10  = sns.clustermap(dist_ind_data)


# afficher chaque groupe:
def groupe_cah(matrice,seuil,nb_groupe):
    groupes_cah = fcluster(matrice,t=seuil,criterion='distance')
    df_actif["groupe"]=groupes_cah
    groupe = df.loc[df_actif["groupe"]==nb_groupe,:]
    return groupe

groupe = groupe_cah(dist_ind_data,seuil=0.5*1000000,nb_groupe=1)


fig11 = px.histogram(groupe, x = "ipsrc")

fig12 = px.pie(groupe, values = groupe.action.value_counts(), names =groupe.action.unique())



# card10 = dbc.Card(
#     dbc.CardBody(
#         [
#             html.H4('Dendrogram CAH', className='card-title'),
#             dcc.Graph(
#                 id='graph10',
#                 figure=fig10
#             ),
#         ]
#     )
# )

card11 = dbc.Card(
    dbc.CardBody(
        [
            html.H4('Repartition des Ip source dans le groupe', className='card-title'),
            dcc.Graph(
                id='graph11',
                figure=fig11
            ),
        ]
    )
)

card12 = dbc.Card(
    dbc.CardBody(
        [
            html.H4('Repartition des actions dans le groupe', className='card-title'),
            dcc.Graph(
                id='graph12',
                figure=fig12
            ),
        ]
    )
)

def layout():
    return dbc.Container(
        [
            html.H1("Analyse de la CAH"),
            html.Hr(),
            # dbc.Row([
            #     dbc.Col(
            #             card10,
            #             width=12,
            #         )
            # ],
            # className="mb-2",
            # ),
            dbc.Row(
                [
                    dbc.Col(
                        card11,
                        width=6,
                    ),
                    dbc.Col(
                        card12,
                        width=6,
                    )
                ],
                className="mb-2",
            ),
        ],
        fluid=True,
    )


