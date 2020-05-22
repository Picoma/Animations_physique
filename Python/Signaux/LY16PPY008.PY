# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 12:45:26 2015

@author: ENS de Lyon

Objectifs :     - Illustrer la décomposition en série de Fourier d'un signal
                - Illustrer le phénomène de Gibbs
                
Entrées :   - f : fréquence du signal
            - N : nombre de points par période pour l'échantillonnage
            - k : nombre d'harmoniques considérées pour la synthèse du signal
            - p : nombre de périodes visualisées
            - A(i) : fonction qui renvoie l'amplitude de l'harmonique k
            
Sorties :   - Y : signal synthétisé à partir de ses harmoniques
            - figure 1 : graphe de Y en fonction du temps
"""

import matplotlib.pyplot as plt
import numpy as np

def A(i):
    if i%2 == 0:
        return 0
    else:
        return 1./i# Signal créneau
#        return (-1.)**((i-1)/2) / i**2# Signal triangle

f = 100# Fréquence (Hz)
N = 10000# Nombre de points par période
k = 1000# Nombre d'harmoniques
p = 2# Nombre de périodes visualisées

t = np.linspace(0,p*1./f,N*p)# Génération de l'échelle des temps
Y = np.zeros(N*p)# Initialisation de l'amplitude

for i in range(0,k):# Calcul des différentes harmoniques
    Y += A(i)*np.sin(i*2*np.pi*f*t)

plt.plot(t,Y)# Tracé du signal
plt.xlabel("Temps (s)")
plt.ylabel("Amplitude du signal")
plt.title("Ampitude du signal en fonction du temps")
