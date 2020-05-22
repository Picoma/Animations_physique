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
#                       Oscillateur harmonique
#                         xpp+w0^2*sin(x)=0
#--------------------------------------------------------------------
#--------------------------------------------------------------------
# Description
# routine harmonique.py
# function harm(y,t)
#     arguments: y: solution, t:temps d'intégration,
# commentaires:
# On résoud numériquement l'équa. diff. de l'oscillateur harmonique pour plusieurs valeurs de vitesse initiale.
# La résolution numérique des équations différentielles donne un tableau où les lignes correspondent au temps, la premiere colone  à la solution pour la variable y[0]=x et la deuxième colone à la solution pour la variable y[1]=v
#--------------------------------------------------------------------

#--------------------------------------------------------------------
#       Obtention des solutions
#--------------------------------------------------------------------

# Paramètres du problème
w0 = 5 # pulsation propre
eps=0.001 # epsilon pour ne pas que le cas v=2 diverge

# Paramètres d'intégration
start = 0                        # debut
end = 10                         # fin
numsteps = 5000                  # nombre de pas d'integration
t = linspace(start,end,numsteps)

# Conditions initiales et résolution
x0= [0,0,0,-4,4]
v0= [1,8,(2-eps)*w0,4*w0,-4*w0]
# Tableau des CI
CI=array([x0,v0])
#print CI
#print len(CI)
#print CI[:,0]

# Tableau des solutions
X=np.zeros((numsteps, len(x0)))
V=np.zeros((numsteps, len(x0)))


# Definition des deux équa diff du premier ordre
# dxdt = v
# dvdt = -w0^2 sin(x)
def harm(y, t):
    x, v = y                    # Vecteur variable
    dvdt = -w0**2*np.sin(x)      # Equation différentielle 2
    dydt = [v,dvdt]
    return dydt                 # Solutions
                   
# Résolution numérique des équations différentielles
# Fait un tableau où les lignes correspondent au temps
# La premiere colone la solution pour la variable y[0]=x
# La deuxième colone la solution pour la variable y[1]=v
for i in range(len(x0)):
 sol=odeint(harm,CI[:,i],t)            
 # récupération de la solution
 X[:,i]=sol[:,0]
 V[:,i]=sol[:,1]


#---------------------
# Tracé des solutions
#---------------------


# Evolution temporelle
fig = plt.figure(figsize=(9, 9))
for i in range(len(x0)-2):
 plot(t, X[:, i], '-',label=r'$v_0={}$'.format(v0[i]))

# Définition des bornes des axes 
plt.axis((start,end,-10,10))
# Titre du graph et légendes
title('Evolution temporelle')
xlabel(ur"$t \, (s)$", fontsize=16)
ylabel(ur"$x$", fontsize=16)
legend(loc='lower right')
grid(True)
plt.savefig('harm_temp.png')



# Portrait de phase
fig = plt.figure(figsize=(9,9))
for i in range(len(x0)):
 plot(X[:, i], V[:, i]/w0, '-',label=r'$v_0={}$'.format(v0[i]))
# Définition des bornes des axes 
plt.axis((-5,5,-5,5))
# Titre du graph et légendes
title('Portait de phase')
xlabel(ur"$x$", fontsize=16)
ylabel(ur"$\dot{x}/\omega_0$", fontsize=16)
legend(loc='lower right')
grid(True)
plt.savefig('harm_phase.png')

plt.show()


