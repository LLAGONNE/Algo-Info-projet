#J'importe les 5 bibliothèques utiles à la résolution des problèmes:
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from math import *
sys.argv
import sys #sys.argv pour permettre de pouvoir entrer les données sur powershell ou bien le terminal de windows
KM = pd.read_csv ('EIVP_projet_1\EIVP_KMbis.csv' , sep=';') #il faut remplacer EIVP_projet_1\EIVP_KM.csv par ce qu'on a comme dossier
#print(KMb.tail(60)['sent_at'])  #pour s'assurer que le fichier est bien reconnu par le système


KMb=KM.sort_values(by = 'sent_at') #but travailler sur des valeurs deja triés(pas sur de pouvoir l'utiliser dans le doute):


def point1 (colonne,start_at,end_at):
     
    y = []
    Temps = []
    k=0
    
    for i in range(len(KMb['sent_at'])): #idée de base créer une boucle pour representer le temps, ici idée est de pouvoir exprimer le départ et l'arrivée du temps
        if end_at==KMb['sent_at'][i][:10]:
            j=i
            
        elif start_at==KMb['sent_at'][i][:10]:
            l=i
            
    Temps=[k]
    y=[KMb[colonne][l]]
    
    while KMb['sent_at'][l][:10]!=end_at:
        k+=1
        l+=1
        y.append(KMb[colonne][l])
        Temps.append(k)

    print (Temps)
    print(y)
    #trouver un meilleur moyen de faire les dates 
    plt.plot (Temps,y)
    plt.show ()

    

#J'avais pas vu qu'il fallait l faire sur la courbe..................

def point2 (colonne): #les données du bruit sont fournies en dBA
    #calcul du minimum
    m = KM[colonne][0]
    for k in range (1,7880) :
        if KM[colonne][k] < m :
            m = KM[colonne][k]
            
    
    #calcul du maximum
    M = KM['noise'][0]
    for k in range (1,7880) :
        if KM['noise'][k] > M :
            M = KM['noise'][k]
        
    
    #calcul de l'écart-type
    a = 0
    for k in KM[colonne] :
        a += k
    a /= 7880 #on obtient la moyenne arithmétique
    b = 0
    for k in range (7880) : 
        b += (abs (KM[colonne][k] - a)) ** 2
    et = (b / 7880) ** (1/2)
    
    
    #calcul de la variance
    V = et ** 2
    
    
    #calcul de la médiane
    L = KM[colonne]  #on va d'abord trier cette liste avec le tri par insertion par exemple
    for i in range (1,len(L)) :
        x=L[i]
        j=i     
        while j>0 and x<L[j-1] :
            L[j]=L[j-1]
            j=j-1
        L[j]=x
    if len (L) % 2 == 0 :
        med = (L[len (L) // 2] + L[len (L) // 2 + 1]) / 2
    else :
        med = L[len (L) // 2 + 1]
        
#on différencie maintenant suivant chaque colonne
    if colonne == 'noise' :
        #on va maintenant faire la moyenne logarithmique
        d = 0
        for k in range (7880) :
            d += 10 ** ( (KM['noise'][k]) /10)
        d = 10 * log10 (d / 7880)
                
        
        print ('Le bruit minimal capté est',m,'dBA.')
        print ('Le bruit maximal capté est',M,'dBA.')
        print ('La moyenne des valeurs est',d,'dBA')
        print ("L'cart-type des données récoltées est",et,'dBA.')
        print ("La variance est de",V,'dBA.')
        print ('Le bruit médian capté est de',med,'dBA.')
        
    if colonne == 'temp' or colonne == 'lum' or colonne == 'co2' :
        #on va maintenant faire la moyenne arithmétique
        d = 0
        for k in range (7880) :
            d += KM['temp'][k]
        d /= 7880
        
        
        print ('La valeur minimale captée est',m)
        print ('La valeur maximale captée est',M,)
        print ('La valeur des valeurs est',d)
        print ("L'cart-type des données récoltées est",et)
        print ("La variance est de",V)
        print ('La valeur médiane captée est de',med)
        
    if colonne == 'humidity' :
        #on calcule la moyenne géométrique
        d = 1
        for k in range (7880) :
            d = d * (KM['humidity'][k]) ** (1/7880)
            
            
        print ('La valeur minimale captée est',m)
        print ('La valeur maximale captée est',M,)
        print ('La valeur des valeurs est',d)
        print ("L'cart-type des données récoltées est",et)
        print ("La variance est de",V)
        print ('La valeur médiane captée est de',med)

#EXECUTION du programme:

