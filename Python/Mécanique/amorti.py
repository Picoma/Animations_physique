#!/usr/bin/python
# # -*- coding: utf_8 -*-

" A METTRE EN PREMIER "
# Pour que la division de 2 entiers donne un flottant
# (si on veut obtenit la partie entière de la division utiliser a//b)
from __future__ import division

import numpy as np

# Pour les figures
import matplotlib.pyplot as plt

# Pour lire des images
import os
#import skimage
#from skimage import io
#from scipy import misc

from mpl_toolkits.mplot3d import Axes3D # pour la 3D
from pylab import *

# Pour les équa diff
from  scipy  import *
from  scipy.integrate  import  odeint

# Pour les animations
#import matplotlib.animation as anim

# Pour toutes les fonctions mathématiques
from math import*


#--------------------------------------------------------------------
#                       Oscillateur amorti
#                       xpp+(w0/Q)xp+(w0^2)x=0
#--------------------------------------------------------------------

#--------------------------------------------------------------------
# Description
# routine amorti.py
# function amort(y,t,Q,w0)
#     arguments: y: solution, t:temps d'intégration, Q,w0: variables du problème.
# commentaires:
# On résoud numériquement l'équa. diff. de l'oscillateur amorti pour plusieurs valeurs du facteur de qualité (boucle sur i avec i le nombre de Q testés différents.
# La résolution numérique des équations différentielles donne un tableau où les lignes correspondent au temps, la premiere colone  à la solution pour la variable y[0]=x et la deuxième colone à la solution pour la variable y[1]=v
#--------------------------------------------------------------------

#--------------------------------------------------------------------
#       Obtention des solutions
#--------------------------------------------------------------------

# -------------------------------------------------------------------
# Definition de l'equa. diff.

# Definition des deux équa diff du premier ordre
# dxdt = v
# dvdt = -wo/Q*v - w0^2*x
def amort(y, t, Q, w0):
    x, v = y                            # Vecteur variable
    dvdt = -w0/Q*v-w0**2*x              # Equa. diff. 2
    dydt = [v,dvdt]                     # Vecteur solution
    return dydt                         

# -------------------------------------------------------------------
# Definition des constantes du problème et des CI

# Constantes du problème
w0 = 2*pi
Q=[0.3,0.5,5] # On calcule pour différents facteurs de qualité



# Paramètre d'intégration: vecteur temps
start = 0                       # debut
end = 10                        # fin
numsteps = 500                  # nombre de pas d'integration
t = linspace(start,end,numsteps)

# Conditions initiales
x0=0
v0=5
# Tableau des CI
CI=array([x0,v0])

# -------------------------------------------------------------------
# Initialisation du tableau des solutions
# Autant de solutions que de Q différents
X=np.zeros((numsteps, len(Q)))
V=np.zeros((numsteps, len(Q)))


#--------------------------------------------------------------------
# Boucle de résolution

for i in range(len(Q)): 
 sol=odeint(amort,CI,t,args=(Q[i], w0))            
 # récupération de la solution
 X[:,i]=sol[:,0]
 V[:,i]=sol[:,1]


#--------------------------------------------------------------------
#       Tracé des solutions
#--------------------------------------------------------------------


# Evolution temporelle
fig2 = plt.figure(figsize=(9
, 9))
plot(t, X[:, 0], '-', ms=6, mfc='w', mec='b',label=u"Q=0.3")
plot(t, X[:, 1], '-', ms=6, mfc='w', mec='k',label=u"Q=0.5")
plot(t, X[:, 2], '-', ms=6, mfc='w', mec='r',label=u"Q=5")
# Définition des bornes des axes 
#plt.axis((-0.25,0.25,-0.25,0.25))
# Titre du graph et légendes
title('Oscillateur amorti: Evolution temporelle')
xlabel(ur"$t \, (s)$", fontsize=16)
ylabel(ur"$x$", fontsize=16)
legend()
grid(True)
plt.savefig('amorti_temp.png')


# Portrait de phase
fig2 = plt.figure()
plot(X[:, 0], V[:, 0]/w0, '-', ms=6, mfc='w', mec='b',label=u"Q=0.3")
plot(X[:, 1], V[:, 1]/w0, '-', ms=6, mfc='w', mec='b',label=u"Q=0.5")
plot(X[:, 2], V[:, 2]/w0, '-', ms=6, mfc='w', mec='b',label=u"Q=5")
# Définition des bornes des axes 
plt.axis((-1,1,-1,1))
# Titre du graph et légendes
title('Oscillateur amorti: Portait de phase')
xlabel(ur"$x$", fontsize=16)
ylabel(ur"$\dot{x}/\omega_0$", fontsize=16)
axis('equal')
legend()
grid(True)
plt.savefig('amorti_phase.png')



plt.show()
