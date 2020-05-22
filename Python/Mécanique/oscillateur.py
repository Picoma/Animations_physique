#!/usr/bin/python
# # -*- coding: utf_8 -*-

" A METTRE EN PREMIER "
# Pour que la division de 2 entiers donne un flottant
# (si on veut obtenit la partie entière de la division utiliser a//b)
from __future__ import division

import numpy as np

# Pour les figures
import matplotlib.pyplot as plt
import math
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
#                       Oscillateur 
#--------------------------------------------------------------------

#--------------------------------------------------------------------
# Description
# routine oscillateur.py
# commentaires:
# Petit code qui permet de tracer le portrait de phase d'un oscillateur résonant en fonction du facteur de qualité Q et de la variable réduite x=w/w0 avec w0 la pulsation propre de l'oscillateur
#--------------------------------------------------------------------

#--------------------------------------------------------------------
#  Paramètres du problème
#--------------------------------------------------------------------
Q=[0.1,0.5,10] # facteur de qualité
R=100 # résistance du circuit
eps=10E-5 # epsilon pour ne pas diviser par 0

# trace selon x, variable réduite (x=w/w0)
nstep=1000 # nombre de pas
dbt=0+eps  # début
fin=2      # fin
x=linspace(dbt,fin,nstep)
#--------------------------------------------------------------------
#  Tracé de l'admittance
#--------------------------------------------------------------------

# -------------------------------------------------------------------
# Initialisation des variables
# Module de l'admittance
Y=np.zeros((nstep, len(Q)))
# Phase de l'admittance
phi=np.zeros((nstep, len(Q)))
# Puissance
P=np.zeros((nstep, len(Q)))

# Boucle qui créé les variables pour différents facteurs de qualité
for i in range(len(Q)):
 Y[:,i]=1/(R*(1+Q[i]**2*(x-1./x)**2)**(0.5))
 phi[:,i]=arctan(Q[i]*(x-1/x))
 P[:,i]=1/(1+Q[i]**2*(x-1/x)**2)

# Racines x1 et x2 telles que Y(x1)=Y(x2)=Ymax/sqrt(2)
ym=1/R # Ymax
x1=1/(2*Q[2])*(-1+sqrt(1+4*Q[2]**2))
x2=1/(2*Q[2])*(1+sqrt(1+4*Q[2]**2))

#------------------------------------------
# Trace pour Q=1

plt.figure(1)
plt.subplot(211)
plot(x, Y[:, 2], '-', ms=6, mfc='w', mec='r',label=u"Q=10")

# --------------------------
# Plot des lignes pour visualiser x1 et x2, largeur de bande passante
plt.axvline(x1, ymin=0.0,ymax=1/sqrt(2), ls='--', color='k')
plt.axvline(x2, ymin=0.0,ymax=1/sqrt(2), ls='--',color='k')
plt.axhline(y=ym/sqrt(2), xmin=0.0, xmax=x2,ls='--', color='k')
# ---------------------------

# Définition des bornes des axes 
plt.axis((dbt,fin,0,1/R+eps))
# Titre du graph et légendes
title('Module')
xlabel(ur"$x$", fontsize=16)
ylabel(ur"$|Y|$", fontsize=16)
legend()
grid(True)
plt.subplot(212)
plot(x, phi[:, 2], '-', ms=6, mfc='w', mec='r',label=u"Q=10")
# Définition des bornes des axes 
plt.axis((dbt,fin,-1.6,1.6))
# Titre du graph et légendes
title('Phase')
xlabel(ur"$x$", fontsize=16)
ylabel(ur"$\varphi$", fontsize=16)
legend(loc=4)
grid(True)





#---------------------------------
# Tracé pour différents Q
plt.figure(2)
# Module
plt.subplot(211)
plot(x, Y[:, 0], '-', ms=6, mfc='w', mec='b',label=u"Q=0.1")
plot(x, Y[:, 1], '-', ms=6, mfc='w', mec='k',label=u"Q=0.5")
plot(x, Y[:, 2], '-', ms=6, mfc='w', mec='r',label=u"Q=10")

#plot(x, Y[:, 3], '-', ms=6, mfc='w', mec='r',label=u"Q=5")
# Définition des bornes des axes 
plt.axis((dbt,fin,0,1/R+eps))
# Titre du graph et légendes
title('Module')
xlabel(ur"$x$", fontsize=16)
ylabel(ur"$|Y|$", fontsize=16)
legend()
grid(True)
#Phase
plt.subplot(212)
plot(x, phi[:, 0], '-', ms=6, mfc='w', mec='b',label=u"Q=0.1")
plot(x, phi[:, 1], '-', ms=6, mfc='w', mec='k',label=u"Q=0.5")
plot(x, phi[:, 2], '-', ms=6, mfc='w', mec='r',label=u"Q=10")
# Définition des bornes des axes 
plt.axis((dbt,fin,-1.6,1.6))
# Titre du graph et légendes
title('Phase')
xlabel(ur"$x$", fontsize=16)
ylabel(ur"$\varphi$", fontsize=16)
legend(loc=4)
grid(True)





# -------------------------------------------------------------------
# Tracé de la puissance

plt.figure(3)
plot(x, P[:, 0], '-', ms=6, mfc='w', mec='b',label=u"Q=0.3")
plot(x, P[:, 1], '-', ms=6, mfc='w', mec='k',label=u"Q=0.5")
plot(x, P[:, 2], '-', ms=6, mfc='w', mec='r',label=u"Q=1")
# Définition des bornes des axes 
plt.axis((dbt,fin,0,1+eps))
# Titre du graph et légendes
title('Resonance en puissance')
xlabel(ur"$x$", fontsize=16)
ylabel(ur"$\frac{P}{P_{max}}$", fontsize=16)
legend()
grid(True)
#plt.savefig('amorti_temp.png')


plt.show()

