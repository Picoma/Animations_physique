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
#                       Oscillateur de Van der Pol
#                       xpp+(x**2-p)xp+(w0^2)x=0
#--------------------------------------------------------------------

#--------------------------------------------------------------------
# Description
# routine oscill_vdp.py
# function vdpt(y,t,p,w0)
#     arguments: y: solution, t:temps d'intégration, p,w0: variables du problème.
# commentaires:
# On résoud numériquement l'équa. diff. de l'oscillateur de Van der Pol pour plusieurs valeurs de p et plusieur conditions initiales (boucle sur i avec i le nombre CI testées différentes.
# La résolution numérique des équations différentielles donne un tableau où les lignes correspondent au temps, la premiere colone  à la solution pour la variable y[0]=x et la deuxième colone à la solution pour la variable y[1]=v
#--------------------------------------------------------------------

#--------------------------------------------------------------------
#       Obtention des solutions
#--------------------------------------------------------------------

# -------------------------------------------------------------------
# Definition de l'equa. diff.

# Definition des deux équa diff du premier ordre
# dxdt = v
# dvdt = -(x**2-p)*v - w0^2*x
def vdp(y, t, p, w0):
    x, v = y                            # Vecteur variable
    dvdt = -(x**2-p)*v - w0**2*x         # Equa. diff. 2
    dydt = [v,dvdt]                     # Vecteur solution
    return dydt                         

# -------------------------------------------------------------------
# Definition des constantes du problème et des CI

# Constantes du problème
w0 = 1.5
p=0.4 # Pour fixer p
pp=[0.01,4] # On calcule pour différents p
# Paramètre d'intégration: vecteur temps
start = 0                       # debut
end = 40                        # fin
numsteps = 4000                  # nombre de pas d'integration
t = linspace(start,end,numsteps)

# Conditions initiales
x0= [0.1,2]
v0= [0,0]
# Tableau des CI
CI=array([x0,v0])

# -------------------------------------------------------------------
# Initialisation du tableau des solutions
# Autant de solutions que de Q différents
X=np.zeros((numsteps, len(pp)))
V=np.zeros((numsteps, len(pp)))
X2=np.zeros((numsteps, len(x0)))
V2=np.zeros((numsteps, len(x0)))

#--------------------------------------------------------------------
# Boucle de résolution


for j in range(len(x0)):
 sol=odeint(vdp,CI[:,j],t,args=(p,w0))
 X2[:,j]=sol[:,0]
 V2[:,j]=sol[:,1]


for i in range(len(pp)): 
 sol=odeint(vdp,[0.2,0],t,args=(pp[i], w0))            
 # récupération de la solution
 X[:,i]=sol[:,0]
 V[:,i]=sol[:,1]



#--------------------------------------------------------------------
#       Tracé des solutions
#--------------------------------------------------------------------

#--------------------------------------
# Deux conditions initiales différentes
fig = plt.figure(1,figsize=(9, 9)) 
# Evolution temporelle
#subplot(1,2,1)
plot(t, X2[:, 0], '-b',label=ur"$x_0=0.1$")
plot(t, X2[:, 1], '-r',label=ur"$x_0=2$")
# Titre du graph et légendes
title('Evolution temporelle')
xlabel(ur"$t \, (s)$", fontsize=16)
ylabel(ur"$x$", fontsize=16)
legend()
grid(True)



# Portrait de phase
fig = plt.figure(2,figsize=(9, 9)) 
#subplot(1,2,2)
plot(X2[:, 0], V2[:, 0]/w0, '-b',label=ur"$x_0=0.1$")
plot(X2[:, 1], V2[:, 1]/w0, '-r',label=ur"$x_0=2$")
# Titre du graph et légendes
title('Portait de phase')
xlabel(ur"$x$", fontsize=16)
ylabel(ur"$\dot{x}/\omega_0$", fontsize=16)
legend()
grid(True)

plt.tight_layout()
plt.savefig('vdp_CI.png')



#--------------------------------------
# Deux p différents
fig2 = plt.figure(3,figsize=(9, 9)) 
# Evolution temporelle
subplot(2,2,1)
plot(t, X[:, 0], '-b',label=ur"$p=0.01$")
title('Evolution temporelle')
xlabel(ur"$t \, (s)$", fontsize=16)
ylabel(ur"$x$", fontsize=16)
grid(True)
plt.legend(loc=4)
plt.axis((start,end,-0.3,0.25))


subplot(2,2,3)
plot(t, X[:, 1], '-r',label=ur"$p=4$")
grid(True)
# Titre du graph et légendes
#title('Evolution temporelle')
xlabel(ur"$t \, (s)$", fontsize=16)
ylabel(ur"$x$", fontsize=16)
plt.legend(loc=4)
plt.axis((start,end,-5.5,4.5))

# Portrait de phase
subplot(2,2,2)
plot(X[:, 0], V[:,0]/w0, '-b',label=ur"$p=0.01$")
title('Portait de phase')
xlabel(ur"$x$", fontsize=16)
ylabel(ur"$\dot{x}/\omega_0$", fontsize=16)
grid(True)
plt.axis((-0.25,0.25,-0.25,0.25))

subplot(2,2,4)
plot(X[:, 1], V[:,1]/w0, '-r',label=ur"$p=4$")
#title('Portait de phase')
xlabel(ur"$x$", fontsize=16)
ylabel(ur"$\dot{x}/\omega_0$", fontsize=16)
grid(True)

#plt.suptitle('Differents p, CI=0.2,0')
plt.tight_layout()
plt.savefig('vdp_p.png')

plt.show()







