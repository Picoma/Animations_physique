# -*- coding: utf-8 -*-
"""
Created on Sat May 20 15:05:52 2017

@author: ENS de Lyon

Objectif : Montrer l'intensité obtenue en fonction de sin(theta)-sin(theta incident) après un réseau optique
 et son évolution avec le nombre de traits éclairés, le nombre de traits par mm et la longueur d'onde

le programme donne trois couples de deux figures. Dans chaque couple il y a une figure de référence et
une figure où on a changé un seul paramètre

Entrées :   - a1 et a2 : pas du réseau, a1 est le pas de référence, en mètre
            - N1 et N2 : nombre de traits éclairés, N1 est le nombre de traits de référence
            - londe1 et londe2 : longueur d'onde, londe1 est la longueur d'onde de référence, en mètre
            
Sortie :    - figure 1 : ensemble des 6 figures réparties sur trois ligne. Première ligne écolution avec
le nombre de traits éclairés, deuxième ligne avec le pas du réseau et troisième ligne avec la longueur d'onde.
L'intensité tracé est l'intensité normalisé par l'intensité d'un trait, elle est dans normalisée et sans dimension.
"""

import numpy as np
import matplotlib.pyplot as plt

a1=0.001/600 # pas du réseau de référence en mètre
a2 = 0.001/100 # pas du réseau pour comparaison en mètre

N1 = 5*600 # nombre de traits éclairées de référence
N2 = 0.01*600 # nombre de traits éclairée pour comparaison

londe1  = 600E-9 #longueur d'onde de référence en mètre
londe2  = 400E-9 #longueur d'onde comparaison en mètre

d = 0.001/6000  # taille de la fente que constitue chaque trait en mètre


epsilon = np.linspace(-2,2,2*1000000)# epsilon est la différence entre le sin de l'angle de sortie moins le sinus de l'angle d'entré de l'onde
                                     #on crée une liste pour epsilon allant de -2 à 2 contenant 2000000 point

plt.figure(num='Intensité lumineuse normalisée',figsize = [100,100])# on crée la figure, son nom est intensité lumineuse et sa taille et de 100pouces par 100pouces soit tous l'écran
plt.clf()
plt.subplot(3,2,1)#on subdivise l'écran un 3lignes et trois colonnes
I =np.square(np.sinc(np.pi*d*epsilon/londe1)*np.sin(np.pi*epsilon*a1*N1/londe1)/np.sin(np.pi*epsilon*a1/londe1))
#on calcule l'intensité lumineuse pour les paramètres de références, en la normalise par l'intensité Io d'une fente. Elle est donc sans dimension
plt.ylabel('Intensité lumineuse normalisée')
plt.plot(epsilon,I)#on trace
plt.title('N = {}'.format(N1))#on indique le nombre de traits éclairés

plt.subplot(3,2,2)
I =np.square(np.sinc(np.pi*d*epsilon/londe1)*np.sin(np.pi*epsilon*a1*N2/londe1)/np.sin(np.pi*epsilon*a1/londe1))
#on calcule l'intensité lumineuse en faisant varier le nombre de trait
plt.ylabel('Intensité lumineuse normalisée')
plt.plot(epsilon,I)#on trace
plt.title('N = {}'.format(N2))#on indique le nombre de traits éclairés

plt.subplot(3,2,3)
I =np.square(np.sinc(np.pi*d*epsilon/londe1)*np.sin(np.pi*epsilon*a1*N1/londe1)/np.sin(np.pi*epsilon*a1/londe1))
#on calcule l'intensité lumineuse pour les paramètres de références
plt.ylabel('Intensité lumineuse normalisée')
plt.plot(epsilon,I)#on trace
plt.title('{:3.0f} traits/mm'.format(1/a1*0.001))#on indique le nombre de traits pas mm du réseau


plt.subplot(3,2,4)
I =np.square(np.sinc(np.pi*d*epsilon/londe1)*np.sin(np.pi*epsilon*a2*N1/londe1)/np.sin(np.pi*epsilon*a2/londe1))
#on calcule l'intensité lumineuse en faisant varier le pas du réseau
plt.ylabel('Intensité lumineuse normalisée')
plt.plot(epsilon,I)#on trace
plt.title('{:3.0f} traits/mm'.format(1/a2*0.001))#on indique le nombre de traits pas mm du réseau


plt.subplot(3,2,5)
I =np.square(np.sinc(np.pi*d*epsilon/londe1)*np.sin(np.pi*epsilon*a1*N1/londe1)/np.sin(np.pi*epsilon*a1/londe1))
#on calcule l'intensité lumineuse pour les paramètres de références
plt.xlabel('sin(theta) - sin(theta incident)')
plt.ylabel('Intensité lumineuse normalisée')
plt.plot(epsilon,I)#on trace
plt.title('lambda = {:3} nm'.format(londe1*1E9))#on indique la longueur d'onde

plt.subplot(3,2,6)
I =np.square(np.sinc(np.pi*d*epsilon/londe2)*np.sin(np.pi*epsilon*a1*N1/londe2)/np.sin(np.pi*epsilon*a1/londe2))
#on calcule l'intensité lumineuse en faisant varier la longueur d'onde
plt.xlabel('sin(theta) - sin(theta incident)')
plt.ylabel('Intensité lumineuse normalisée')
plt.plot(epsilon,I)#on trace
plt.title('lambda = {:3} nm'.format(londe2*1E9))#on indique la longueur d'onde


plt.show()# on affiche la figure
