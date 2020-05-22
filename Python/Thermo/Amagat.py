# -*- coding: utf-8 -*-
"""
@author: ENS de Lyon

DESCRIPTION

Ce programme trace les courbes d Amagat pour differents gaz reels,
a partir d ajustements experimentaux (voir BFR de thermo).

En sortie: les graphes dans le diagramme (p,pV) dans le fichier Amagat.pdf
"""

""" PACKAGES """

import matplotlib.pyplot as plt
import numpy as n

""" DATA """

gaz = [r'$H_2$', r'$He$', r'$O_2$', r'$N_2$']        # noms des gaz

#coefficients
a   = n.array([0.2453, 0.0346, 1.382, 1.370])        # en bar L^2/mol
b   = n.array([0.02651, 0.0238, 0.03186, 0.0387])    # en L/mol
N   = len(gaz)

""" CONSTANTES """

R = 8.314    #constante des gaz parfaits
T = 298.15   #temperature de 25 degres

#pV = A + B p + C p^2
A  = R * T * n.ones(N) / 10**5 * 10**3
B  = b - a / A
C  = (B + b) * a / A**2

""" TRACE """

c = ['red', 'blue', 'green', 'black']
p = n.linspace(0, 500, 100)
plt.figure()
plt.xlabel(r'$p \, (bar)$', fontsize = 18)
plt.ylabel(r'$pV \, (bar\cdot L)$', fontsize = 18)

def f(i, x):
    return A[i] + B[i]*x + C[i]*x**2
    
for i in range(N):
    plt.plot(p, f(i, p), color = c[i], label = gaz[i])

plt.legend(loc = 'upper left', fontsize = 16)

plt.savefig('Amagat.pdf')
