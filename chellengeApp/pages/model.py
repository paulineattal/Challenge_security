
import pandas as pd
import numpy as np
import os
import plotly.express as px

path = os.getcwd()
df = pd.read_csv(path+'/data/FW.csv', sep=',')

# CAH
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster

df_actif = df[["dstport","proto","action","policyid"]]
df_actif = pd.get_dummies(df_actif, columns=df_actif.select_dtypes('object').columns)

def matrice_lien(df):
    #générer la matrice des liens
    dist_ind_data =linkage(df.values,method='ward',metric='euclidean')
    return dist_ind_data

dist_ind_data = matrice_lien(df_actif)
print(dist_ind_data.shape)
#affichage du dendrogramme
plt.title("CAH") 
dendrogram(dist_ind_data,orientation='right',color_threshold=0) 
plt.show()

# afficher chaque groupe:
def groupe_cah(matrice,seuil,nb_groupe):
    groupes_cah = fcluster(matrice,t=seuil,criterion='distance')
    df_actif["groupe"]=groupes_cah
    groupe = df.loc[df_actif["groupe"]==nb_groupe,:]
    return groupe

groupe = groupe_cah(dist_ind_data,seuil=0.5*1000000,nb_groupe=1)

#print(groupe)

fig_ipsrc = px.histogram(groupe, x = "ipsrc")
fig_ipsrc.show()

fig_action = px.pie(groupe, values = groupe.action.value_counts(), names =groupe.action.unique())
fig_action.show()