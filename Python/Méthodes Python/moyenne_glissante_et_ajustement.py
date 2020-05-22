# -*- coding: utf-8 -*-
"""
@author: ENS de Lyon

DESCRIPTION

Ce programme sert a traiter les donnees des thermocouples
de la barre de cuivre.

Variable a modifier: fichier_courbes est un fichier .txt de 12 colonnes: 
2 colonnes par capteur, 1 pour le temps, l'autre pour la tension acquise 
sous LatisPro.

En sortie:
    -le graphe des courbes moyennees (capteur_mesure.txt)
    -la liste des parametres d ajustement et leurs incertitudes (fichier_fit)

Ce script nécessite un fichier externe (voir variable à modifier).
"""

""" PACKAGES """

import numpy as n
import matplotlib.pyplot as plt


""" IMPORTATION DES DONNEES """

""" A MODIFIER """
fichier_courbes = 'test.txt'

#fichier avec parametres d ajustement
fichier_fit     = 'ajustement_mesure.txt'

#fichier donnees
data    = n.loadtxt(fichier_courbes, skiprows = 1)

temps   = data[:, 0]                  #la liste temps
N       = len(temps)                  #longueur des listes (nombre de points)
capteur = n.zeros((N, 6))             #initialisation de la liste des capteurs

for j in range(6):
    
    capteur[:, j] = data[:, 1 + 2*j]  #liste des point du capteur i


""" MOYENNAGE """

pas             = 20                  #pas de la moyenne glisssante
capteur_moyenne = capteur             #initialisation des listes moyennees                

#boucle sur les points
for i in range(pas, N - pas):
    
    #boucle sur chaque capteur
    for j in range(6):
        
        capteur_moyenne[i,j] = sum(capteur[i - pas: i + pas, j])/ (2*pas)

#troncature des points non moyennes
capteur_tronque = capteur_moyenne[pas: N - pas, :]
temps           = temps[pas: N - pas]


""" GRAPHES """

plt.figure()

plt.xlabel('t (s)')
plt.ylabel('U (V)')

#trace des graphes moyennes de chaque capteur
for j in range(6):
    plt.plot(temps, capteur_tronque[:,j])

plt.show()


""" ENREGISTREMENT """

# on enregistre dans le fichier capteur_mesure
with open('capteur_mesure.txt', 'w') as f:
    
    #premirere ligne = listes des noms des courbes
    f.write( 'temps\t' )
    for j in range(6):
        f.write( 'capteur%.i\t'%(j) )
        
    #saut de ligne
    f.write('\n')
    
    #puis on enregistre tous les points
    for i in range(N - 2*pas):
        
        #le temps d'abord
        f.write( '%.5f\t'%(temps[i]) )
        
        #puis les capteurs
        for j in range(6):
            f.write( '%.5f\t'%(capteur_tronque[i,j]) )
        
        #saut de ligne
        f.write('\n')


""" AJUSTEMENT """

from scipy.optimize import curve_fit

#fonction d'ajustement (sinus fondamental et frequence double)
def func(t, a, b, c, T, phi1, phi2):
    return a + b * n.sin(2*n.pi*t/T + phi1) + c * n.sin(4*n.pi*t/T + phi2)

#creation fichier d'enregistrement
with open(fichier_fit,'w') as f:
    f.write('capteur' + ' b u(b) phi1 u(phi1)' + '\n')
    
#boucle sur les capteurs
for j in range(6):
    
    print('capteur ' + str(j) + '\n')
    
    #ajustement
    popt, pcov = curve_fit(func,
                           temps,
                           capteur_tronque[:,j],
                           p0 = [0.3, 0.3, 0.03, 100, 5-j*0.75, 0])

    #affichage de l'amplitude et de la phase
    print('b = %.5f +- %.5f \n'%(popt[1], n.sqrt(pcov[1,1])))
    print('phi1 = %.5f +- %.5f \n'%(popt[4], n.sqrt(pcov[4,4])))
    
    #enregistrement
    with open(fichier_fit,'a') as f:
        f.write(str(j) + ' ' + 
                '%.5f %.5f  '%(popt[1], n.sqrt(pcov[1,1])) +
                '%.5f %.5f\n'%(popt[4], n.sqrt(pcov[4,4])) )
