#!/usr/bin/python
# # -*- coding: utf_8 -*-


#--------------------------------------------------------------------
#                       Pendule de torsion lesté
#                         xpp+a*x+b*xp+w0^2*sin(x)=0
#--------------------------------------------------------------------

#Ce programme modélise le cas d'un pendule de torsion type
#disque traversé par un fil au niveau de son axe de révolution, 
#déséquilibré par une masse m collée sur la surface du disque à une 
#distance l de l'axe, au dessus de celui-ci par rapport au sol. 
#Ainsi à partir d'une massse critique, le pendule admet deux positions
#d'équilibre symétriques au lieu d'une seule en theta=0. L'équation du mouvement
#se déduit de l'expression de l'énergie du système à laquelle s'ajoute le 
#terme -mgl(1-cos x).

#Le programme permet de tracer l'allure du potentiel les oscillations pour
#différentes masses afin de voir apparaître un double-puits, ainsi que 
#l'évolution temporelle de l'angle et les trajectoires de phase associées.

#---------------------------------------------------------------------

from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import os
from mpl_toolkits.mplot3d import Axes3D # pour la 3D
from pylab import *
from  scipy  import *
from  scipy.integrate  import  odeint
from math import*


# Paramètres du problème
w0 = 4 # pulsation propre en rad/s
Q = 10 #amortissement fluide
C = 0.8 #couple de torsion en N.m
l = 1 #distance masse-axe en m
m=np.linspace(0.01,0.15,5) #différentes valeurs de masses en kg


# Paramètres d'intégration
start = 0                        # debut
end = 15                         # fin
numsteps = 5000                  # nombre de pas d'integration
t = np.linspace(start,end,numsteps)

# Conditions initiales
x0=0  #angle initial égal à 0
v0=15 #vitesse initiale en m/s
CI=np.array([x0,v0])

# Tableau des solutions
X=np.zeros((numsteps, len(m)))
V=np.zeros((numsteps, len(m)))

# Definition des deux équa diff du premier ordre
def tors(y, t,u):
    x, v = y                    # Vecteur variable
    dvdt = w0**2*np.sin(x)-C/u/l**2*x-w0/Q*v    # Equation différentielle 
    dydt = [v,dvdt]
    return dydt                 # Solutions
                   
# Résolution numérique des équations différentielles
# Fait un tableau où les lignes correspondent au temps
# La premiere colone la solution pour la variable y[0]=x
# La deuxième colone la solution pour la variable y[1]=v
for i in range(len(m)):
    sol=odeint(tors,CI,t,args=(m[i],))            
    X[:,i]=sol[:,0]
    V[:,i]=sol[:,1]


#---------------------
# Tracés
#---------------------

#Double puits de potentiel
plt.figure()
theta=np.linspace(-np.pi,np.pi,100)
Ep=np.zeros((len(theta),len(m)))
for i in range(len(m)):
    Ep[:,i]=0.5*C*theta**2-10*m[i]*l*(1-np.cos(theta))
    plot(theta,Ep[:,i],label='m={}'.format(round(m[i],2)))
plt.legend()
plt.savefig('double_puits.png')


# Evolution temporelle
plt.figure(figsize=(10,16))
plt.suptitle('Pendule de torsion double-puits',fontsize=22)
plt.subplot(2,1,1)
plot(t,57.3*X[:,0], '-',label='m={}'.format(round(m[0],2)))
plot(t,57.3*X[:, len(m)-1], '-',label='m={}'.format(round(m[len(m)-1],2)))
title('Evolution temporelle',fontsize=20)
xlabel(r'$t$ (s)', fontsize=20)
ylabel(r'$\theta$ (degres)', fontsize=20, rotation=0)
grid(True)
plt.legend(fontsize=20)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
# Portrait de phase
plt.subplot(2,1,2)
plot(57.3*X[:,0], V[:,0], '-',label='m={}'.format(round(m[0],2)))
plot(57.3*X[:, len(m)-1], V[:, len(m)-1], '-',label='m={}'.format(round(m[len(m)-1],2)))
#plt.axis((-5,5,-20,20))
title('Portait de phase', fontsize=20)
xlabel(r'$\theta$ (degres)', fontsize=20)
ylabel(r'$\dot{\theta}$', rotation=0, fontsize=20)
grid(True)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.legend(fontsize=20, loc='upper right')
plt.savefig('double_puits.png')
plt.show()

