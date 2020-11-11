import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
#J'importe les 3 bibliothèques utiles à la résolution des problèmes
KM=pd.read_csv("EIVP_projet_1\EIVP_KMbis.csv") #il faut remplacer EIVP_projet_1\EIVP_KM.csv par ce qu'on a comme dossier
print(KM.head(7880)) #pour s'assurer que le fichier est bien reconnu par le système
print(KM) #pour s'assurer que le fichier est bien reconnu par le système et voir le nombre de colonne
