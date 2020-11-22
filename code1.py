#J'importe les 5 bibliothèques utiles à la résolution des problèmes:
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from math import *
import sys #sys.argv pour permettre de pouvoir entrer les données sur powershell ou bien le terminal de windows



KM = pd.read_csv ('EIVP_projet_1\EIVP_KMbis.csv' , sep=';') #il faut remplacer EIVP_projet_1\EIVP_KM.csv par ce qu'on a comme dossier
#print(KMb.tail(60)['sent_at'])  #pour s'assurer que le fichier est bien reconnu par le système
KMb=KM.sort_values(by='id')



# compter les limites pour le passage entre les capteurs pour toute les fonctions
def count_time (KMb,id,time):
    
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
    return count_time1,count_time2



# pouvoir définir les limites du temps les fonctions du temps nécéssaire
def Temps(KMb,id,time,start_at,end_at,count_time):
    
    Temp = []
    j=0
    
    for i in range(len (KMb[time])): #idée de base créer une boucle pour representer le temps, ici idée est de pouvoir exprimer le départ et l'arrivée du temps
        if start_at == KMb[time][i][:10] and KMb[time][count_time [0][j]][:19]==KMb[time][i][:19]:
            l=i
            k=0
            print(j)
            
        elif end_at == KMb[time][i][:10] and KMb[time][count_time [1][j]][:19]==KMb[time][i][:19]:
            Temp.append([])
            
            while KMb[time][l][:10] != end_at:
                Temp[j].append(k)
                k += 1
                l+=1
            j+=1
    return Temp




def point1 (KMb,colonne,id,time,start_at,end_at,f1,f2):
    
    y = []
    j=0
    
    for i in range(len(f2)):
        y.append([])
        for j in f2[i]:
            y[i].append(KMb[colonne][f1[0][i]+j])
    for i in range (len(y)):
        print (len(y[i]),len(f2[i]),f1)
    
    return y



def courbe_1 ( f1, f2, colonne, txt_additionnel ):
    
    for i in range(len(f1)):
        plt.plot (f1[i],f2[i],"-+",label='courbe du capteur '+str(i+1))
        plt.title('Courbe de '+colonne)
        plt.legend( loc='best' )
        plt.show ()
    

    

def point2 (KMb,id,time,colonne): #les données du bruit sont fournies en dBA
    
    #calcul du minimum
    min_bruit = []
    for j in range(len(count_time1)):
        m = KMb[colonne][j]
        for k in range (count_time1[j],count_time2[j]) :
            if KMb[colonne][k] < m :
                m = KMb[colonne][k]
        min_bruit.append(m)
    
    #calcul du maximum
    max_bruit = []
    for j in range(len(count_time1)):
        M = KMb[colonne][j]
        for k in range (count_time1[j],count_time2[j]) :
            if KMb[colonne][k] > M :
                M = KMb[colonne][k]
        max_bruit.append(M)
    
    #calcul de l'écart-type
    moy=[]
    for j in range(len(count_time1)):
        a = 0
        for k in range (count_time1[j],count_time2[j]) :
            a += KMb[colonne][k]
        a = a / (count_time2[j] - count_time1[j]) #on obtient la moyenne arithmétique
        moy.append(a)
    
    
    l=0
    ect=[]
    for j in range(len(count_time1)):
        b = 0
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
            d = 0
            for k in range (count_time1[j],count_time2[j]) : 
                d += 10 ** ( (KMb['noise'][k]) /10)
            moylog.append(10 * log10 (d / (count_time2[j] - count_time1[j]) ))
                
        
        print ('Le bruit minimal capté est',min_bruit,'dBA.')
        print ('Le bruit maximal capté est',max_bruit,'dBA.')
        print ('La moyenne des valeurs est',moy,'dBA')
        print ("L'ecart-type des données récoltées est",ect,'dBA.')
        print ("La variance est de", V ,'dBA.')
        print ('Le bruit médian capté est de',moylog,'dBA.')
        
        point1(KMb,colonne,id,time,'2019-08-11','2019-08-25')
        
    if colonne == 'temp' or colonne == 'lum' or colonne == 'co2' :
        #on va maintenant faire la moyenne arithmétique
        d = 0
        moyari=[]
        for j in range(len(count_time1)):
            d = 0
            for k in range (count_time1[j],count_time2[j]) : 
                d += KMb[colonne][k]
            moyari.append(d/(count_time2[j] - count_time1[j]))
        
        
        print ('La valeur minimale captée est',min_bruit)
        print ('La valeur maximale captée est',max_bruit)
        print ('La valeur moyenne est',moy)
        print ("L'ecart-type des données récoltées est",ect)
        print ("La variance est de",V)
        print ('La valeur médiane captée est de',moyari)
        plt.text('La valeur minimale captée est' + str(min_bruit) + 'La valeur maximale captée est' + str(max_bruit) + 'La valeur moyenne est' +str(moy) + "L'ecart-type des données récoltées est" + str(ect) + "La variance est de" + str(V) + 'La valeur médiane captée est de'+str(moyari))
        point1(KMb,colonne,id,time,'2019-08-11','2019-08-25')
        
    if colonne == 'humidity' :
        #on calcule la moyenne géométrique
        d = 0
        moygeo=[]
        for j in range(len(count_time1)):
            d = 0
            for k in range (count_time1[j],count_time2[j]) : 
                d = d * (KMb['humidity'][k]) ** (1/(count_time2[j] - count_time1[j]))
            moygeo.append(d)
            
        print ('La valeur minimale captée est',min_bruit)
        print ('La valeur maximale captée est',max_bruit,)
        print ('La valeur moyenne est',moy)
        print ("L'ecart-type des données récoltées est",ect)
        print ("La variance est de",V)
        print ('La valeur médiane captée est de',moygeo)
        point1(KMb,colonne,id,time,'2019-08-11','2019-08-25')



def point3 (KMb,id,time) :
    THx = pd.read_csv ('Humidex.csv' , sep=';')
    count_time()
    Hr1 = KMb['humidity']
    T1 = KMb['temp']
    Hr2 = []
    T2 = []
    
    
    for k in range (7880) :
        if (Hr1[k] * (10 ** (- 1)) % 1) < 0.5 :
            Hr2.append ((Hr1[k] * (10 ** (-1)) // 1) *10)
        else :
            Hr2.append (((Hr1[k] * (10 ** (-1)) // 1) + 1) *10)
        if T1[k] < 23 :
            T2.append (21)
        if 25 <= T1[k] < 27.5 :
            T2.append (25)
        if T1[k] > 27.5 :
            if (T1[k] * (10 ** (-1))) % 1 < 0.5 :
                T2.append ((T1[k] * (10 ** (-1)) // 1) * 10)
            else :
                T2.append (((T1[k] * (10 ** (-1)) // 1) + 1) * 10)



#EXECUTION du programme:
a=sys.argv
def execution(a):
    if a[1]=="display":
        if a[2]=="humidex" or a[2]=="Humidex":
            point3()
            