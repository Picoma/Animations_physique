# -*- coding: utf-8 -*-
"""
@author: ENS de Lyon

Triangle_Fourier.py

Ce programme calcule et affiche la fonction "triangle" à partir de sa série de Fourier, pour différents ordres maximaux de la série.

Les sorties sont des graphes :
	- Valeur des a_n fonction de n
	- Differentes reconstitution du signal a partir des coefficients de Fourier.
"""


"""
Bibliothèques
"""
import numpy as np
import matplotlib.pyplot as plt

"""
Fonctions de définition des coefficients et du signal théorique
"""
def A(n):   # Amplitude du n-ième terme de la série
    return 1.0/n**2  * 4/np.pi**2 * (np.cos(n*np.pi)-1)

def B(n):   # Amplitude du n-ième terme de la série
    return 0

def triangle(x):     # Triangle théorique (masqué par défaut)
    pi = np.pi
    a = x % (2*pi)
    if a < pi:
        return a/(pi/2)-1
    else:
        return 3-a/(pi/2)


"""
Calcul de la série de Fourier pour les différents ordres
"""
x = np.arange(-4, 8, 0.001);

y1 = 0
for n in range(1,2):
    y1 = y1 + A(n)*np.cos(n*x) + B(n)*np.sin(n*x)    # On somme une à une les composantes jusqu'à N = 1

y3 = 0
for n in range(1,4):
    y3 = y3 + A(n)*np.cos(n*x) + B(n)*np.sin(n*x)    # On somme une à une les composantes jusqu'à N = 3

y6 = 0
for n in range(1,7):
    y6 = y6 + A(n)*np.cos(n*x) + B(n)*np.sin(n*x)    # On somme une à une les composantes jusqu'à N = 6

y10 = 0
for n in range(1,11):
    y10 = y10 + A(n)*np.cos(n*x) + B(n)*np.sin(n*x)    # On somme une à une les composantes jusqu'à N = 10

# Affichage des coefficients de Fourier, puis des fonctions reconstituees
y_triangle = [ triangle(p) for p in x ]

plt.figure()
plt.plot(np.arange(1,11,1),-A(np.arange(1,11,1)),'o')
plt.xlabel(r'$n$', fontsize=18)
plt.ylabel(r'$a_{n}$', fontsize=18)
plt.show()

plt.figure()
ax1 = plt.subplot(221)
plt.plot(x, y_triangle, "r-")
plt.axis([-4.0,8.0,-1.5,1.5])
plt.plot(x, y1, "b")
plt.title(r'$N=1$', fontsize=18)

ax2 = plt.subplot(222)
plt.plot(x, y_triangle, "r-")
plt.axis([-4.0,8.0,-1.5,1.5])
plt.plot(x, y3, "b")
plt.title(r'$N=3$', fontsize=18)

ax3 = plt.subplot(223)
plt.plot(x, y_triangle, "r-")
plt.axis([-4.0,8.0,-1.5,1.5])
plt.plot(x, y6, "b")
plt.title(r'$N=6$', fontsize=18)

ax4 = plt.subplot(224)
plt.plot(x, y_triangle, "r-")
plt.axis([-4.0,8.0,-1.5,1.5])
plt.plot(x, y10, "b")
plt.title(r'$N=10$', fontsize=18)

plt.show()
