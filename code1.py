#J'importe les 5 bibliothèques utiles à la résolution des problèmes:
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from math import *
import sys #sys.argv pour permettre de pouvoir entrer les données sur powershell ou bien le terminal de windows



KM = pd.read_csv ('EIVP_KMbis.csv' ,sep = ';') #il faut remplacer EIVP_projet_1\EIVP_KM.csv par ce qu'on a comme dossier
#print(KMb.tail(60)['sent_at'])  #pour s'assurer que le fichier est bien reconnu par le système
KMb = KM.sort_values (by = 'id')



#Compter les limites en terme de valeurs de chaque capteurs pour pour le passage entre les capteurs pour toutes les fonctions
def count_time (KMb, id, time) :
    
    count = 0
    count_time1 = [0] #définition du 1er élément qui est forcément 0 (on pose cette liste en tant que liste des éléments inférieurs)
    count_time2 = [] #définition du 1er élément qui est forcément vide (on pose cette liste en tant que liste des éléments supérieurs)
        
    for i in range (len (KMb[time])) : #but de la boucle: permettre de lire les id limites des capteurs et de les enregistrer sur une liste
        if KMb[id][i] != KMb[id][count_time1[count]] :
            count_time1.append (i)
            count += 1
            count_time2.append (i - 1)
    count_time2.append (len (KMb[time])- 1)
    #On pose le dernier élément de la liste count_time2 qui correspond à la longueur de la liste
    return (count_time1, count_time2)



# pouvoir créer des listes de temps ou chaque temps est représenté en points
def Temps (KMb, id, time, start_at, end_at, f1) :
    
    Temp = []
    j = 0
    
    for i in range (len (KMb[time])) : #idée de base créer une boucle pour representer le temps, ici l'idée est de pouvoir exprimer le départ et l'arrivée du temps
        if start_at == KMb[time][i][:10] and KMb[time][f1 [0][j]][:19] == KMb[time][i][:19] :
            l = i
            k = 0
            #print(j)
        elif end_at == KMb[time][i][:10] and KMb[time][f1 [1][j]][:19] == KMb[time][i][:19] :
            Temp.append ([])
            while KMb[time][l][:10] != end_at :
                Temp[j].append (k)
                k += 1
                l += 1
            j += 1
            
    return Temp




def point1 ( KMb, colonne, id,time, start_at, end_at, f2, f1) : #fonction très courte permettant de mettre les éléments du dataframe KMb au sein d'une concaténation de listes
    
    y = [] 
    j = 0
    
    for i in range (len (f1)) :
        y.append ([])
        for j in f1[i] :
            y[i].append (KMb[colonne][f2[0][i] + j])
        
    return y


    
def courbe_1 (f2, f3, colonne) :
    
    for i in range (len (f2)) :
        plt.plot (f2[i], f3[i], "-+",label = 'courbe du capteur ' + str (i + 1))
        plt.title ('Courbe de ' + colonne)
        plt.legend (loc='best')
        plt.show ()





def point2 (KMb, id, time, colonne, f1) : #les données du bruit sont fournies en dBA
    
    #calcul du minimum
    min_ = []
    
    for j in range (len (f1[0])) :
        m = KMb[colonne][j]
        for k in range (f1[0][j], f1[1][j]) : #boucle permettant d'avoir 
            if KMb[colonne][k] < m :
                m = KMb[colonne][k]
        min_.append (m)
    
    #calcul du maximum
    max_ = []
    
    for j in range (len (f1[0])) :
        M = KMb[colonne][j]
        for k in range (f1[0][j],f1[1][j]) :
            if KMb[colonne][k] > M :
                M = KMb[colonne][k]
        max_.append (M)
    
    #calcul de l'écart-type, on passe par la moyenne arithmétique
    moy = []
    
    for j in range (len (f1[0])) :
        a = 0
        for k in range (f1[0][j],f1[1][j]) :
            a += KMb[colonne][k]
        a = a / (f1[1][j] - f1[0][j]) #on obtient la moyenne arithmétique
        moy.append (a)
    l = 0
    ect = []
    
    for j in range (len (f1[0])) :
        b = 0
        for k in range (f1[0][j], f1[1][j]) : 
            b += (abs (KMb[colonne][k] - moy[j])) ** 2
        ect.append( (b / (f1[1][j] - f1[0][j])) ** (1/2))
        l += 1
    
    #calcul de la variance
    V = []
    
    for i in ect :
        V.append (i ** 2)
    
    
    #calcul de la médiane
    #on va d'abord trier cette liste avec le tri par insertion par exemple
    L = []
    med = []
    
    for j in range (len (f1[0])) :
        L.append ([])
        for k in range (f1[0][j], f1[1][j]) :
            L[j].append (KMb[colonne][k])
        for i in range (1, len (L[j])) :
            x = L[j][i]
            m = i     
            while m > 0 and x < L[j][m - 1] :
                L[j][m] = L[j][m - 1]
                m = m - 1
            L[j][m] = x
        if len (L[j]) % 2 == 0 :
            med.append ( (L[j][len (L[j]) // 2] + L[j][len (L[j]) // 2 + 1]) / 2)
        else :
            med.append (L[j][len (L[j]) // 2 + 1])
        
#on différencie maintenant suivant chaque colonne
    if colonne == 'noise' :
        #on va maintenant faire la moyenne logarithmique
        d = 0
        moylog = []
        
        for j in range (len (f1[0])):
            d = 0
            for k in range (f1[0][j], f1[1][j]) : 
                d += 10 ** ( (KMb['noise'][k]) /10)
            moylog.append (10 * log10 (d / (f1[1][j] - f1[0][j])))
                
        #print ('Le bruit minimal capté est pour chacun des 6 capteurs:', min_, 'dBA.')
        #print ('Le bruit maximal capté est pour chacun des 6 capteurs:', max_, 'dBA.')
        #print ('La moyenne des valeurs est pour chacun des 6 capteurs:', moy, 'dBA')
        #print ("L'ecart-type des données récoltées est pour chacun des 6 capteurs:", ect, 'dBA.')
        #print ("La variance est pour chacun des 6 capteurs:", V, 'dBA.')
        #print ('Le bruit médian capté est pour chacun des 6 capteurs:', moylog, 'dBA.')
        
        return min_, max_, moylog, ect, V, med, ['min_', 'max_', 'moyenne logarithmique', 'ect', 'V', 'médiane']
        
        
    if colonne == 'temp' or colonne == 'lum' or colonne == 'co2' :
        #on va maintenant faire la moyenne arithmétique
        d = 0
        moyari = []
        
        for j in range (len (f1[0])) :
            d = 0
            for k in range (f1[0][j], f1[1][j]) : 
                d += KMb[colonne][k]
            moyari.append (d/(f1[1][j] - f1[0][j]))
        
        #print ('La valeur minimale captée est pour chacun des 6 capteurs:', min_)
        #print ('La valeur maximale captée est pour chacun des 6 capteurs:', max_)
        #print ('La valeur moyenne est pour chacun des 6 capteurs:', moy)
        #print ("L'ecart-type des données récoltées est pour chacun des 6 capteurs:", ect)
        #print ("La variance est de pour chacun des 6 capteurs:", V)
        #print ('La valeur médiane captée est de pour chacun des 6 capteurs:', moyari)
        
        return min_, max_, moyari , ect, V, med, ['min_', 'max_', 'moy', 'ect', 'V', 'médiane'] 
        
    if colonne == 'humidity' :
        #on calcule la moyenne géométrique
        d = 0
        moygeo = []
        
        for j in range (len (f1[0])) :
            d = 0
            for k in range (f1[0][j], f1[1][j]) : 
                d = d * (KMb['humidity'][k]) ** (1 / (f1[1][j] - f1[0][j]))
            moygeo.append (d)
            
        #print ('La valeur minimale captée est', min_)
        #print ('La valeur maximale captée est', max_)
        #print ('La valeur moyenne est', moy)
        #print ("L'ecart-type des données récoltées est", ect)
        #print ("La variance est de", V)
        #print ('La valeur médiane captée est de pour chacun des 6 capteurs:', moygeo)
        
        return min_, max_, moygeo, ect, V, med, ['min_', 'max_', 'moygeo', 'ect', 'V', 'médiane'] 



def courbe_2 (f2, f3, point2, colonne) : #A la différence de la courbe_1, ici on fait en sorte d'afficher la 1ere courbe et également les autres courbes sous la forme de 

    #f1 correspond à la liste de temps sous forme de 
    #f2 correspond à la limite sur le tableau KMb des divers capteurs
    cmap = plt.get_cmap('jet_r')
    min = []
    max = []
    plt.subplot (121)
    
    for i in range (len (f2)) :
        min.append ([])
        max.append ([])
        for j in range (len (f2[i])) :
            min[i].append (point2[0][i])
            max[i].append (point2[1][i])
        color1 = cmap (float(i) / len(f2))
        print (min[i][0], max[i][0])
        plt.plot (f2[i], min[i], c=color1)
        plt.plot (f2[i], max[i], c=color1)
        plt.plot (f2[i], f3[i], "-+", c = color1, label = 'courbe (+ min et max) du capteur ' + str(i + 1))
        plt.xlabel ('temps (en nombre de points depuis date du début)')
        plt.ylabel ('valeurs de ')
        plt.title ('Courbe de ' + colonne)
        plt.legend ()
        
    plt.subplot (122)
    m = []
    
    for l in range (len (point2[2])) :
        m.append ([])
        m[l] = [l / 10 for x in range (0,6)]
        for n in range (len (m[l])) :
            m[l][n] = m[l][n] + n            
    print (m)
    
    for i in range (1, len (point2) - 1) : #il faudra réussier à séparer les divers barres (couleurs ex)
        color2 = cmap (float(i) / len(f2))
        plt.bar (m[i], point2[i], width = 0.1, color = color2)
        plt.xlabel ("diagramme en barre pour la moyenne, l'écart type, la variance, et la " + point2[6][5] )        
    plt.show ()



def point3 (KMb, id, time, f1) :

    THx = pd.read_csv ('Humidex.csv', sep=';')
    Hr1 = KMb['humidity']
    T1 = KMb['temp']
    Hr2 = []
    T2 = []
    Hx = []
        
    for k in range (len (Hr1)) :
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
    #print (Hr2)
    #print (T2)
    #Maintenant on va lire la valeur de l'indice humidex pour chaque donnée.

    for k in range (len (T2)) : #On rappele que T2 et Hr2 sont de même longueur
        i = str (int (T2[k])) #on veut ici le nom de la colonne que l'on va chercher dans le tableau humidex / certaines valeurs sont également des flottants
        j = 0 #on va chercher l'indice de la ligne associée
        while THx.loc[j][0] != int (Hr2[k]) : #car les valeurs de cette ligne sont des flottants
            j += 1
        Hx.append (int (THx[i][j])) 
    print (Hx)
    
    
def point4 (KMb, colonne1, colonne2, id, time, f1) :
    
    moy1 = point2 (KMb, 'id', time, colonne1, f1)[2]
    moy2 = point2 (KMb, 'id', time, colonne2, f1)[2]
    #on calcule d'abord la covariance
    cov = []
    
    for j in range (len (f1[0])) :
        var = 0
        for k in range (f1[0][j], f1[1][j]) : #boucle permettant d'avoir 
            var += ((KMb[colonne1][k] - moy1) * (KMb[colonne2][k] - moy2)) / (f1[1][j] - f1[0][j])
        cov.append (var)

    #on calcule maintenant le coefficient de corrélation
    ect1 = point2 (KMb, 'id', time, colonne1, f1)[3]
    ect2 = point2 (KMb, 'id', time, colonne1, f1)[3]
    corr = []
    
    for i in range (len (cov)) :
        corr.append (cov[i] / (ect1[i] * ect2[i]))
    return (corr)


def loc1 (KMb, f1, a, b, colonne) :
    ect_loc = 0
    moy = 0
    for k in range (a, b) :
        moy += KMb[colonne][k]
    moy /= b - a + 1
    
    c = 0
    for k in range (a, b) :
        c += (KMb[colonne][k] - moy) ** 2
    ect_loc = (c / (b - a + 1)) ** (1/2)
    return (ect_loc)
   
def loc2 (KMb, f1, a, b, colonne) :
    
    L= []
    
    for k in range (a, b) :
        L.append (KMb[colonne][k])
    for i in range (1, len (L)) :
        x = L[i]
        m = i     
        while m > 0 and x < L[m - 1] :
            L[m] = L[m - 1]
            m = m - 1
        L[m] = x
    if len (L) % 2 == 0 :
        med_loc = (L[len (L) // 2] + L[len (L) // 2 + 1]) / 2
    else :
        med_loc = L[len (L) // 2 + 1]
    return (med_loc)
    


    
def anomalie (KMb, time, start_at, end_at, f1, f2, colonne) :
    ind_anomalie = []
    med_loc = 0
    ect_loc = 0
    for i in range (len (f1[1])) : #l nombre de capteurs
        y = f1[0][i]
        z = f1[1][i]
        for j in range (15 + y, z - 16) : 
            med_loc = loc2 (KMb, count_time (KMb, 'id', time), j - 15, j + 16, colonne)
            ect_loc = loc1 (KMb, count_time (KMb, 'id', time), j - 15, j + 16, colonne)
            #print (med_loc)
            #print (ect_loc)
            if KMb[colonne][j] > (med_loc + 0.5 * ect_loc) or KMb[colonne][j] < (med_loc - 0.5 * ect_loc) :
                ind_anomalie.append (j)
                
    return (ind_anomalie)
    





def erreur():
    return None


#EXECUTION du programme:
a=sys.argv
def execution(a):
    if a[1]=="display":
        if a[2]=="humidex":
            return point3()
        elif a[2]:
            return a