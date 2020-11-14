import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
#J'importe les 3 bibliothèques utiles à la résolution des problèmes
KM=pd.read_csv("EIVP_KMbis.csv",sep=';') #il faut remplacer EIVP_projet_1\EIVP_KM.csv par ce qu'on a comme dossier
#print(KM.head(50)) #pour s'assurer que le fichier est bien reconnu par le système
#print(KM['noise']) #pour s'assurer que le fichier est bien reconnu par le système et voir le nombre de colonne


noise = []
for element in KM['noise']:
    noise.append(element)
#print (noise)


Temps = []
k = 0
for element in KM['sent_at']:
    Temps.append(k)
    k += 1
#print (Temps)
#trouver un meilleur moyen de faire les dates 

plt.plot(Temps,noise)
plt.show()
