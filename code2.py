#J'importe les 5 bibliothèques utiles à la résolution des problèmes:
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from math import *
import sys #sys.argv pour permettre de pouvoir entrer les données sur powershell ou bien le terminal de windows

KM = pd.read_csv ('EIVP_projet_1\EIVP_KMbis.csv' , sep=';') #il faut remplacer EIVP_projet_1\EIVP_KM.csv par ce qu'on a comme dossier
#print(KMb.tail(60)['sent_at'])  #pour s'assurer que le fichier est bien reconnu par le système

KMb=KM.sort_values(by='id')

def point1 (colonne,start_at,end_at): 
    y = []
    Temps = []
    k,j,count = 0,0,0
    count_time1=[0]
    count_time2=[]
        
    for i in range(len (KMb['sent_at'])):
        if KMb['id'][i] != KMb['id'][count_time1[count]]:
            count+=1
            count_time1.append(i)
            count_time2.append(i-1)
    count_time2.append(len(KMb['sent_at'])-1)
    print (count_time1, count_time2)
    #return count_time
    
    for i in range(len (KMb['sent_at'])): #idée de base créer une boucle pour representer le temps, ici idée est de pouvoir exprimer le départ et l'arrivée du temps
        if start_at == KMb['sent_at'][i][:10] and KMb['sent_at'][count_time1[j]][:19]==KMb['sent_at'][i][:19]:
            l=i
            k=0
            print(j)
            
        elif end_at== KMb['sent_at'][i][:10] and KMb['sent_at'][count_time2[j]][:19]==KMb['sent_at'][i][:19]:
            Temps.append([])
            y.append([])
            Temps[j].append(k)
            y[j].append( KMb[colonne][l] )
            
            while KMb['sent_at'][l][:10] != end_at:
                k += 1
                l += 1
                y[j].append (KMb[colonne][l])
                Temps[j].append (k)
            j+=1
    for i in range(len(count_time1)):
        plt.plot (Temps[i],y[i])
        plt.show ()
    

    



def point2 (colonne): #les données du bruit sont fournies en dBA
    #calcul du minimum
    m = KMb[colonne][0]
    for k in range (1,7880) :
        if KM[colonne][k] < m :
            m = KMb[colonne][k]
            
    
    #calcul du maximum
    M = KMb['noise'][0]
    for k in range (1,7880) :
        if KMb['noise'][k] > M :
            M = KMb['noise'][k]
        
    
    #calcul de l'écart-type
    a = 0
    for k in KMb[colonne] :
        a += k
    a /= 7880 #on obtient la moyenne arithmétique
    b = 0
    for k in range (7880) : 
        b += (abs (KMb[colonne][k] - a)) ** 2
    et = (b / 7880) ** (1/2)
    
    
    #calcul de la variance
    V = et ** 2
    
    
    #calcul de la médiane
    #on va d'abord trier cette liste avec le tri par insertion par exemple
    L=[]
    for k in range (7880) :
        L.append (KMb[colonne][k])
        
    for i in range (1,len(L)) :
        x = L[i]
        j = i     
        while j > 0 and x < L[j - 1] :
            L[j] = L[j - 1]
            j = j - 1
        L[j] = x
    if len (L) % 2 == 0 :
        med = (L[len (L) // 2] + L[len (L) // 2 + 1]) / 2
    else :
        med = L[len (L) // 2 + 1]
        
#on différencie maintenant suivant chaque colonne
    if colonne == 'noise' :
        #on va maintenant faire la moyenne logarithmique
        d = 0
        for k in range (7880) :
            d += 10 ** ( (KMb['noise'][k]) /10)
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
            d += KMb['temp'][k]
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
            d = d * (KMb['humidity'][k]) ** (1/7880)
            
            
        print ('La valeur minimale captée est',m)
        print ('La valeur maximale captée est',M,)
        print ('La valeur des valeurs est',d)
        print ("L'cart-type des données récoltées est",et)
        print ("La variance est de",V)
        print ('La valeur médiane captée est de',med)

#EXECUTION du programme:
a=sys.argv
def execution(a):
    if a[1]=="display":
        if a[2]=="humidex" or a[2]=="Humidex":
            point3()
        else:
            