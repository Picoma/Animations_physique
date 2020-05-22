# -*- coding: utf-8 -*-
"""
@author: ENS de Lyon

DESCRIPTION

Ce code calcule un decrement logarithmique, apres moyennage, detection des
maxima et regression.

Variable a modifier: fichier est un fichier .txt de 2 colonnes, 1 pour le temps, l'autre pour la
tension.

En sortie: le graphe et la valeur du decrement.

Ce script nécessite un fichier externe (voir variable à modifier).
"""


""" PACKAGES """

import numpy as n
import matplotlib.pyplot as plt
import scipy.stats as st

""" IMPORTATION """

""" A MODIFIER"""
fichier = 'decrement.txt'

data = n.loadtxt(fichier, skiprows = 1)
t    = data[:,0]
U    = data[:,1]
N    = n.shape(t)[0]

#initialisation detection maxi
V    = []
maxi = []
tmax = []

""" TRAITEMENT """

#moyenne gjissante
pas = 10
for i in range(pas, N-pas):
    V.append(sum(U[i-pas: i+pas]))

#detection des maxima
a    = 1
Umax = 0

#ATTENTION: la detection suppose que la fonction est monotone entre les maxima
#voulus, d ou l utilite du moyennage.
for i in range(N-2*pas):
    if a*V[i] > a*Umax:
        Umax = V[i]
    else:
        a = -a
        if a == -1:
            maxi.append(V[i-1])
            tmax.append(t[i-1])
            Umax = V[i]

""" TRACE """

plt.figure()

T = 6.189/10**3
x = n.array(tmax)/T
y = n.log(n.abs(maxi/maxi[0]))
plt.plot(x, y)

#regression lineaire du log sur les premiers points
M = 7
(a, b, c, d, e) = st.linregress(x[:M], y[:M])
plt.plot(x, a*n.array(x) + b, color = 'r')

plt.xlim([0,x[-1]/3])
plt.ylim([min(y),0])

plt.xlabel('t (s)')
plt.ylabel('Ln(Vmax/Vmax0)')


print('pente = {} +- {}'.format(a, e))

plt.show()
