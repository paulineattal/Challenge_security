
import pandas as pd
import numpy as np
import os
import plotly.express as px
os.chdir("/Users/dangnguyenviet/Desktop/projet-securite")

# histogramme événement par heure:
def histo_evenement_heure(df):
    df['hour_of_event'] = pd.to_datetime(df['datetime']).dt.hour

    eventdata = pd.DataFrame({'hour_of_event': df['hour_of_event']})
    eventdata['Horaire'] = eventdata['hour_of_event'].apply(lambda x: 'Horaires ouvrés' if 7 <= x <= 18 else 'Horaires non ouvrés')

    fig = px.histogram(eventdata, x='hour_of_event', color='Horaire', nbins=24,
                   labels={'hour_of_event': 'Heure', 'count': 'Somme'},
                   category_orders={'Horaire': ['Horaires ouvrés', 'Horaires non ouvrés']},
                   color_discrete_sequence=px.colors.qualitative.Pastel)
    fig.update_layout(title='Evenements par heure', yaxis_title='Somme', xaxis_title='',
                  xaxis=dict(dtick=1, tick0=0, range=[0, 24]), bargap=0.1)
    fig.update_traces(hovertemplate='Horaire: %{legendgroup}<br>Heure: %{x}<br>Count: %{y}')
    fig.show()
    
histo_evenement_heure(df)

# échantillonnage
f = open("log_fw_3.csv","r")
lst = f.readlines()
print(len(lst)-1)
#fermeture
f.close()

def extraction(source,sortie,n,N):
    #fichier source
    fin = open(source,"r")
    #fichier de sortie
    fout = open(sortie,"w")
    #en-tête
    s = fin.readline()
    fout.write(s)
    #compteur de vérification - pas absolument nécessaire
    cpt = 0
    #boucler
    while (n > 0):
        #lire la ligne
        s = fin.readline()
        #inclure dans la sortie ?
        if (N * np.random.rand() <= n):
            #oui
            fout.write(s)
            #un de moins à insérer
            n = n - 1
            #incrémentation compteur
            cpt = cpt + 1
        #une entrée a été traitée
        N = N - 1
    #fin du tant que
    fin.close()
    fout.close()
    #return
    return cpt

N = len(lst)-1

source = "log_fw_3.csv"
sortie = "log_fw_3_extract.csv"
n = 5000
extraction(source, sortie,n,N)

df = pd.read_table("log_fw_3_extract.csv",sep=";",header=None)
df.drop([8,9],axis=1,inplace=True)

df.columns = ["datetime","ipsrc","ipdst","proto","portsrc","portdst","policyid","action","numproto"]

df_actif = df.iloc[:,3:]
df_actif = pd.get_dummies(df_actif, columns=df_actif.select_dtypes('object').columns)

# CAH
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
#générer la matrice des liens
dist_ind_data=linkage(df_actif.values,method='ward',metric='euclidean')

#affichage du dendrogramme
plt.title("CAH") 
dendrogram(dist_ind_data,orientation='right',color_threshold=0) 
plt.show()

# afficher chaque groupe:
groupes_cah = fcluster(dist_ind_data,t=0.5*1000000,criterion='distance')
df_actif["groupe"]=groupes_cah
groupe1 = df.loc[df_actif["groupe"]==1,:]
groupe1
