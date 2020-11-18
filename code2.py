#J'importe les 5 bibliothèques utiles à la résolution des problèmes:
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from math import *
import sys #sys.argv pour permettre de pouvoir entrer les données sur powershell ou bien le terminal de windows

KM = pd.read_csv ('EIVP_projet_1\EIVP_KMbis.csv' , sep=';') #il faut remplacer EIVP_projet_1\EIVP_KM.csv par ce qu'on a comme dossier
#print(KMb.tail(60)['sent_at'])  #pour s'assurer que le fichier est bien reconnu par le système

KMb=KM.sort_values(by='id')

def point1 (KMb,colonne,id,time,start_at,end_at): 
    y = []
    Temps = []
    k,j,count = 0,0,0
    count_time1=[0]
    count_time2=[]
        
    for i in range(len (KMb[time])):
        if KMb[id][i] != KMb[id][count_time1[count]]:
            count_time1.append(i)
            count += 1
            count_time2.append(i-1)
    count_time2.append(len(KMb[time])-1)
    #print (count_time1, count_time2)
    #return count_time
    
    for i in range(len (KMb[time])): #idée de base créer une boucle pour representer le temps, ici idée est de pouvoir exprimer le départ et l'arrivée du temps
        if start_at == KMb[time][i][:10] and KMb[time][count_time1[j]][:19]==KMb[time][i][:19]:
            l=i
            k=0
            print(j)
            
        elif end_at== KMb[time][i][:10] and KMb[time][count_time2[j]][:19]==KMb[time][i][:19]:
            Temps.append([])
            y.append([])
            Temps[j].append(k)
            y[j].append( KMb[colonne][l] )
            
            while KMb[time][l][:10] != end_at:
                k += 1
                l += 1
                y[j].append (KMb[colonne][l])
                Temps[j].append (k)
                
            j+=1
            
    for i in range(len(count_time1)):
        plt.plot (Temps[i],y[i])
        plt.show ()
    

    



def point2 (KMb,id,time,colonne): #les données du bruit sont fournies en dBA
    
    #boucle pour reconnaitre les limites des mesures de chaque capteurs
    count,k = 0,0
    count_time1=[0]
    count_time2=[]
        
    for i in range(len (KMb[time])):
        if KMb[id][i] != KMb[id][count_time1[count]]:
            count += 1
            count_time1.append(i)
            count_time2.append(i-1)
    count_time2.append(len(KMb[time])-1)
    
    #calcul du minimum
    m = 0
    min_bruit = []
    for j in range(len(count_time1)):
        for k in range (count_time1[j],count_time2[j]) :
            if KMb[colonne][k] < m :
                m = KMb[colonne][k]
        min_bruit.append(m)
    
    #calcul du maximum
    M = 0
    max_bruit = []
    for j in range(len(count_time1)):
        for k in range (count_time1[j],count_time2[j]) :
            if KMb[colonne][k] > M :
                M = KMb[colonne][k]
        max_bruit.append(M)
    
    #calcul de l'écart-type
    a = 0
    moy=[]
    for j in range(len(count_time1)):
        for k in range (count_time1[j],count_time2[j]) :
            a += KMb[colonne][k]
        a = a / (count_time2[j] - count_time1[j]) #on obtient la moyenne arithmétique
        moy.append(a)
    
    b = 0
    l=0
    ect=[]
    for j in range(len(count_time1)):
        for k in range (count_time1[j],count_time2[j]) : 
            b += (abs (KMb[colonne][k] - moy[l])) ** 2
        ect.append( (b / (count_time2[j] - count_time1[j])) ** (1/2))
        l+=1
    
    #calcul de la variance
    V=[]
    for i in ect:
        V.append( i ** 2 )
    
    
    #calcul de la médiane
    #on va d'abord trier cette liste avec le tri par insertion par exemple
    L=[]
    med=[]
    for j in range(len(count_time1)):

        L.append([])
        
        for k in range (count_time1[j],count_time2[j]) :
            L[j].append (KMb[colonne][k])
        
        for i in range (1,len(L[j])) :
            x = L[j][i]
            m = i     
            while m > 0 and x < L[j][m - 1] :
                L[j][m] = L[j][m - 1]
                m = m - 1
            L[j][m] = x
        if len (L[j]) % 2 == 0 :
            med.append( (L[j][len (L[j]) // 2] + L[j][len (L[j]) // 2 + 1]) / 2)
        else :
            med.append(L[j][len (L[j]) // 2 + 1])
        
#on différencie maintenant suivant chaque colonne
    if colonne == 'noise' :
        #on va maintenant faire la moyenne logarithmique
        d = 0
        moylog=[]
        for j in range(len(count_time1)):
            for k in range (count_time1[j],count_time2[j]) : 
                d += 10 ** ( (KMb['noise'][k]) /10)
            moylog.append(10 * log10 (d / (count_time2[j] - count_time1[j]) ))
                
        
        print ('Le bruit minimal capté est',min_bruit,'dBA.')
        print ('Le bruit maximal capté est',max_bruit,'dBA.')
        print ('La moyenne des valeurs est',moy,'dBA')
        print ("L'ecart-type des données récoltées est",ect,'dBA.')
        print ("La variance est de", V ,'dBA.')
        print ('Le bruit médian capté est de',moylog,'dBA.')
        
    if colonne == 'temp' or colonne == 'lum' or colonne == 'co2' :
        #on va maintenant faire la moyenne arithmétique
        d = 0
        moyari=[]
        for j in range(len(count_time1)):
            for k in range (count_time1[j],count_time2[j]) : 
                d += KMb[colonne][k]
        moyari.append(d/(count_time2[j] - count_time1[j]))
        
        
        print ('La valeur minimale captée est',min_bruit)
        print ('La valeur maximale captée est',max_bruit,)
        print ('La valeur des valeurs est',moy)
        print ("L'ecart-type des données récoltées est",ect)
        print ("La variance est de",V)
        print ('La valeur médiane captée est de',moyari)
        
    if colonne == 'humidity' :
        #on calcule la moyenne géométrique
        d = 0
        moygeo=[]
        for j in range(len(count_time1)):
            for k in range (count_time1[j],count_time2[j]) : 
                d = d * (KMb['humidity'][k]) ** (1/(count_time2[j] - count_time1[j]))
            moygeo.append(d)
            
        print ('La valeur minimale captée est',min_bruit)
        print ('La valeur maximale captée est',max_bruit,)
        print ('La valeur des valeurs est',moy)
        print ("L'ecart-type des données récoltées est",ect)
        print ("La variance est de",V)
        print ('La valeur médiane captée est de',moygeo)

#EXECUTION du programme:
a=sys.argv
def execution(a):
    if a[1]=="display":
        if a[2]=="humidex" or a[2]=="Humidex":
            point3()
            