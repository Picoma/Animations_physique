# -*- coding: utf-8 -*-
"""
@author: ENS de Lyon

Objectif : Illustre le théorème de Shanon et le repliement spectral en
comparant un signal réel et un signal acquis.

Entrées :   - f : fréquence du signal à acquérir en Hz
            - N : nombre de points du signal à acquérir ()
            - fe : fréquence d'échantillonnage en Hz
            - T : durée de l'acquisition en s
            
Sortie :    - figure 1 : comparaison du signal acquis et du signal à acquérir sur deux graphes différents
"""

import numpy as np
import matplotlib.pyplot as plt

f = 100# Fréquence du signal à acquérir en Hz
N = 1000# Nombre de points de signal à acquérir
fe = 99# Fréquence d'échantillonage en Hz
T = 0.2# Durée de l'acquisition en s

t = np.linspace(0,T,N)# Temps pour le signal à acquérir
Y = np.sin(2*np.pi*f*t)# Signal à acquérir

te = np.linspace(0,T,T*fe)# Temps pour le signal acquis
Ye = np.sin(2*np.pi*f*te)# Signal acquis

plt.figure(1)
plt.clf
plt.subplot(1,2,1)
plt.plot(t,Y)# Affichage du signal à acquérir
plt.xlabel("Temps (s)")
plt.ylabel("Amplitude du signal")
plt.title('Signal Réel')

plt.subplot(1,2,2)
plt.plot(te,Ye,'o')# Affichage du signal acquis
plt.xlabel("Temps (s)")
plt.ylabel("Amplitude du signal")
plt.title("Signal acquis")

plt.show()
