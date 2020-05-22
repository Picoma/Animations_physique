#!/usr/bin/python
# # -*- coding: utf_8 -*-


#--------------------------------------------------------------------
#                       Oscillateur de Van der Pol
#                       xpp+(x**2-p)xp+(w0^2)x=0
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


# Constantes du problème
w0 = 1.5
p=0.4 # Pour fixer p
pp=[0.01,4] # On calcule pour différents p
# Paramètre d'intégration: vecteur temps
start = 0                       # debut
end = 40                        # fin
numsteps = 4000                  # nombre de pas d'integration
t = linspace(start,end,numsteps)


# Definition de l'equa. diff.
def vdp(y, t, p, w0):
    x, v = y                            # Vecteur variable
    dvdt = -(x**2-p)*v - w0**2*x         # Equa. diff. 2
    dydt = [v,dvdt]                     # Vecteur solution
    return dydt                         


# Conditions initiales
x0= [0.1,2]
v0= [0,0]
# Tableau des CI
CI=array([x0,v0])

# Initialisation du tableau des solutions
# Autant de solutions que de Q différents
X=np.zeros((numsteps, len(pp)))
V=np.zeros((numsteps, len(pp)))
X2=np.zeros((numsteps, len(x0)))
V2=np.zeros((numsteps, len(x0)))

# Résolution
for j in range(len(x0)):
 sol=odeint(vdp,CI[:,j],t,args=(p,w0))
 X2[:,j]=sol[:,0]
 V2[:,j]=sol[:,1]
for i in range(len(pp)): 
 sol=odeint(vdp,[0.2,0],t,args=(pp[i], w0))            
 X[:,i]=sol[:,0]
 V[:,i]=sol[:,1]


#--------------------------------------------------------------------
#       Tracé des solutions
#--------------------------------------------------------------------


# Deux conditions initiales différentes
plt.figure(figsize=(9, 15)) 
plt.suptitle('Oscillateur de Van der Pol : influence des conditions initiales',fontsize=20)
# Evolution temporelle
plt.subplot(2,1,1)
plot(t, X2[:, 0], '-b',label=r'$x_0=${}'.format(round(x0[0],2)))
plot(t, X2[:, 1], '-r',label=r'$x_0=${}'.format(round(x0[1],2)))
plt.title('Evolution temporelle',fontsize=20)
xlabel(r'$t$', fontsize=20)
ylabel(r'$x$', fontsize=20, rotation=0)
legend(loc='upper right',fontsize=20)
grid(True)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
# Portrait de phase
subplot(2,1,2)
plot(X2[:, 0], V2[:, 0]/w0, '-b',label=r'$x_0=${}'.format(round(x0[0],2)))
plot(X2[:, 1], V2[:, 1]/w0, '-r',label=r'$x_0=${}'.format(round(x0[1],2)))
# Titre du graph et légendes
title('Portait de phase',fontsize=20)
xlabel(r'$x$', fontsize=20)
ylabel(r'$\dot{x}$', rotation=0, fontsize=20)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
legend(fontsize=20,loc='upper right')
plt.grid()
plt.savefig('vdp_CI.png')



#--------------------------------------
# Deux p différents

plt.figure(figsize=(12, 9)) 
plt.suptitle(r'Oscillateur de Van der Pol : influence du parametre $p$')
# Evolution temporelle p=0.01
subplot(2,2,1)
plot(t, X[:, 0], '-b',label=r'$p=${}'.format(round(pp[0],2)))
title('Evolution temporelle')
xlabel('$t$', fontsize=16)
ylabel('$x$', fontsize=16,rotation=0)
grid(True)
plt.legend()
plt.axis((start,end,-0.3,0.25))

# Evolution temporelle p=4
subplot(2,2,3)
plot(t, X[:, 1], '-r',label=r'$p=${}'.format(round(pp[1],2)))
grid(True)
xlabel('$t$', fontsize=16)
ylabel('$x$', fontsize=16,rotation=0)
plt.legend()
plt.axis((start,end,-5.5,4.5))

# Portrait de phase p=0.01
subplot(2,2,2)
plot(X[:, 0], V[:,0]/w0, '-b',label=r'$p=${}'.format(round(pp[0],2)))
title('Portait de phase')
xlabel('$x$', fontsize=16)
ylabel(r'$\dot{x}$', rotation=0,fontsize=16)
grid(True)
plt.axis((-0.25,0.25,-0.25,0.25))

#Portrait de phase p=4
subplot(2,2,4)
plot(X[:, 1], V[:,1]/w0, '-r',label=r'$p=${}'.format(round(pp[1],2)))
xlabel(r'$x$', fontsize=16)
ylabel(r'$\dot{x}$', fontsize=16,rotation=0)
grid(True)

#plt.tight_layout()
plt.savefig('vdp_p.png')
plt.show()







