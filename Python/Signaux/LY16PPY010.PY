# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 08:56:19 2015

@author: ENS de Lyon

Objectif : Illustre le théorème de Shanon et le repliement spectral en
comparant un signal réel et un signal acquis.

Entrées :   - f : fréquence du signal à acquérir
            - N : nombre de points du signal à acquérir ()
            - fe : fréquence d'échantillonnage
            - T : durée de l'acquisition
            
Sortie :    - figure 1 : comparaison du signal acquis et du signal à acquérir
"""

import numpy as np
import matplotlib.pyplot as plt

f = 100# Fréquence du signal à acquérir
N = 1000# Nombre de points de signal à acquérir
fe = 99# Fréquence d'échantillonage
T = 0.2# Durée de l'acquisition

t = np.linspace(0,T,1000)# Temps pour le signal à acquérir
Y = np.sin(2*np.pi*f*t)# Signal à acquérir

te = np.linspace(0,T,T*fe)# Temps pour le signal acquis
Ye = np.sin(2*np.pi*f*te)# Signal acquis

plt.plot(t,Y,label="Signal réel")# Affichage du signal à acquérir
plt.plot(te,Ye,'o',label="Signal acquis")# Affichage du signal acquis
plt.legend()
plt.xlabel("Temps (s)")
plt.ylabel("Amplitude du signal")
plt.title("Comparaison du signal réel et du signal acquis")
