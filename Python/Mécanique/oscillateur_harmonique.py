#!/usr/bin/python
# # -*- coding: utf_8 -*-


#--------------------------------------------------------------------
#                       Oscillateur harmonique
#                         xpp+w0^2*sin(x)=0
#--------------------------------------------------------------------

#Ce programme permet de tracer les trajectoires de phase de l'oscillateur
#harmonique pour plusieurs valeurs de vitesse initiale (l'angle initial est nul)
#et de visualiser l'enrichissment spectral causé par les non-linéarités en
#traçant l'évolution temporelle d'une part et la TF des oscillations à 
#grande amplitude d'aure part.

#--------------------------------------------------------------------

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
eps=0.000001 # epsilon pour ne pas que le cas v=2*w0 diverge

# Paramètres d'intégration
start = 0                        # debut
end = 100                         # fin
numsteps = 5000                  # nombre de pas d'integration
t = np.linspace(start,end,numsteps)

# Conditions initiales
Ninit=20 # nbr de conditions initiales
x0=0*np.ones(Ninit) # angle initial fixé à 0
v0=np.linspace(-15,15,Ninit) #vitesse initiale en rad/s
CI=array([x0,v0])

# Tableau des solutions
X=np.zeros((numsteps, Ninit))
V=np.zeros((numsteps, Ninit))

# Definition des deux équa diff du premier ordre
def harm(y, t):
    x, v = y                    # Vecteur variable
    dvdt = -w0**2*np.sin(x)     # Equation différentielle
    dydt = [v,dvdt]
    return dydt                 # Solutions
                   
# Résolution numérique des équations différentielles
# Fait un tableau où les lignes correspondent au temps
# La premiere colone contient la solution pour la variable y[0]=x
# La deuxième colone contient la solution pour la variable y[1]=v
for i in range(Ninit):
    sol=odeint(harm,CI[:,i],t)            
    X[:,i]=sol[:,0]
    V[:,i]=sol[:,1]


#Résolution pour la condition initiale critique v0=2*w0
X_crit=np.zeros(numsteps)
V_crit=np.zeros(numsteps)
sol_crit=odeint(harm,[0,(2-eps)*w0],t)
X_crit=sol_crit[:,0]
V_crit=sol_crit[:,1]


# Portrait de phase
fig = plt.figure(figsize=(10,10))
for i in np.arange(Ninit):
    plot(X[:, i], V[:, i], '-', color='blue') #label='v_0={}'.format(v0[i])
    plot(-X[:, i], V[:, i], '-',color='blue') #la fonction vitesse(theta) est paire
plt.axis((-5,5,-20,20))
title('Oscillateur harmonique : Portait de phase', fontsize=20)
xlabel(r'$\theta$', fontsize=20)
ylabel(r'$\dot{\theta}$', fontsize=20,rotation=0)
grid(True)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
# Séparatrice tracé séparément en rouge
plt.plot(X_crit,V_crit,color='red', label=r'$\dot{\theta}_0=2\omega_0$')
plt.legend(fontsize=20)
plt.savefig('harm_phase.png')
plt.show()


#Enrichissement spectral
fig = plt.figure(figsize=(16,6))
plt.suptitle('Oscillateur harmonique : $v_0=7,1$ m/s',fontsize=22)
# Evolution temporelle
plt.subplot(1,2,1)
plt.plot(t, X[:,14]) #on choisit une solution de grande amplitude pour accentuer l'effet, mais pas trop pour ne pas avoir un mouvement de type fronde
title('Evolution temporelle',fontsize=20)
xlabel(r'$t$ (s)', fontsize=20)
ylabel(r'$\theta$', fontsize=20, rotation=0)
grid(True)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
#Spectre
plt.subplot(1,2,2)
freq=np.fft.fftfreq(numsteps,(end-start)/numsteps) #construction du vecteur des fréquences, contient autant de points que de pas de temps
plt.plot(freq,abs(np.fft.fft(X[:,14],numsteps))) #tracé de la partie réelle de la FFT
plt.axis((0,4,0,5000))
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.grid()
xlabel('frequence (Hz)', fontsize=20)
plt.ylabel('amplitude',fontsize=20)
plt.title('Spectre de Fourier',fontsize=20)
plt.legend(fontsize=10)
plt.savefig('harm_temp.png')
plt.show()
