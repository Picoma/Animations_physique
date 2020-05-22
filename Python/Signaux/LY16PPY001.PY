# -*- coding: utf-8 -*-
"""
carre.py

@author: ENS de Lyon
q
Ce programme calcule et affiche la fonction "créneaux" à partir de sa série de Fourier.

Les valeurs à modifier sont :
- ligne 25 : l'ordre minimal de la série de Fourier
- ligne 26 : l'ordre maximal de la série de Fourier
- lignes 62 et 65 : enlever les commentaires pour afficher la fonction théorique
"""


"""
Bibliothèques
"""
import numpy as np
import matplotlib.pyplot as plt


"""
Variables
"""
D = 1     # Ordre min de la série de Fourier, MINIMUM = 1 ET NON PAS 0
N = 50    # Ordre max de la série de Fourier


"""
Fonctions de définition des coefficients et du signal théorique
"""
def A(n):   # Amplitude du n-ième terme de la série
    return 0

def B(n):   # Amplitude du n-ième terme de la série
    if n % 2 == 0:      # Si le nombre est pair:
        return 0
    else:                # Si le nombre est impair :
        return 1.0/n*4/np.pi

def carre(x):     # créneau théorique (masqué par défaut)
    pi = np.pi
    deuxpi = 2*np.pi
    a = x % deuxpi # Le modulo est assez embêtant
    if a < pi:
        return 1
    else:
        return -1


"""
Calcul et affichage de la série de Fourier
"""
x = np.arange(-4, 8, 0.001);

y = 0
for n in range(D,N+1):
    y = y + A(n)*np.cos(n*x) + B(n)*np.sin(n*x)    # On somme une à une les composantes

# À décommenter pour afficher le signal théorique
"""
y_creneau = [ carre(p) for p in x ]
plt.plot(x, y_creneau, "r-")
"""

plt.axis([-4.0,8.0,-1.5,1.5])

plt.plot(x, y, "b-")

#plt.savefig("image.png")
