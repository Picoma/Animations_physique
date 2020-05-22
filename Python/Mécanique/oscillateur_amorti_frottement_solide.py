#!/usr/bin/python
# # -*- coding: utf_8 -*-



#--------------------------------------------------------------------
#                       Oscillateur amorti
#                       xpp+(w0^2)x=-fg*signe(xp)
#--------------------------------------------------------------------

#Ce programme permet de tracer les trajectoires de phase de l'oscillateur 
#amorti par frottement solide pour deux (ou plus) valeurs d'élongation initale
#(la vitesse initiale est nulle), avec mise en évidence du segment attracteur.
#Il permet également de tracer l'évolution temporelle de l'élongation et
#ainsi de mettre en évidence la décroissance linéaire de l'amplitude des oscillations.


from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import os
from pylab import *
from  scipy  import *
from  scipy.integrate  import  odeint
from math import*


#paramètres du problème
w0=3 # rad/s
f=0.8
a=10*f/w0**2

# Definition des deux équa diff du premier ordre
# dxdt = v
# dvdt = -wo/Q*v - w0^2*x
def solide(y, t):
    x, v = y                            # Vecteur variable
    dvdt = -(w0**2)*x-10*f*sign(v)              # Equa. diff. 2
    dydt = [v,dvdt]                     # Vecteur solution
    return dydt 

# Paramètre d'intégration: vecteur temps
start = 0.                       # debut
end = 10.                        # fin
numsteps = 500
t = linspace(start,end,numsteps)


# Conditions initiales
x0=[5,9]
v0=[0,0]
CI=array([x0,v0])

# Initialisation du tableau des solutions
X=np.zeros((numsteps,len(x0)))
V=np.zeros((numsteps,len(x0)))


# Résolution
for i in range(len(x0)) :
    print('0')
    sol=odeint(solide,CI[:,i],t)    
    X[:,i]=sol[:,0]
    V[:,i]=sol[:,1]


#--------------------------------------------------------------------
#       Tracé 
#--------------------------------------------------------------------

plt.figure(figsize=(20, 7))
plt.suptitle('Oscillateur amorti par frottement solide',fontsize=22)
# Evolution temporelle
plt.subplot(1,2,1)
for i in range(len(x0)):
    plot(t, X[:,i], label=r'$x_0=${}'.format(round(x0[i],2)))
plt.suptitle('Oscillateur amorti: evolution temporelle',fontsize=20)
xlabel(r'$t$', fontsize=16)
ylabel(r'$x$', fontsize=16,rotation=0)
legend(fontsize=20)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.grid()
# Portrait de phase
plt.subplot(1,2,2)
for i in range(len(x0)) :
    plot(X[:,i], V[:,i]/w0, label=r'$x_0=${}'.format(round(x0[i],2)))
axes=plt.gca()
axes.add_artist(matplotlib.lines.Line2D((-a, a), (0, 0), color = 'red',linewidth=3,marker='D'))
plt.annotate('a',xy=(a,0), xytext=(a+0.5*a,0),color='red',fontsize=20)
plt.annotate('-a',xy=(-a,0), xytext=(-2.5*a,0),color='red',fontsize=20)
plt.annotate(r'$M_0$',xy=(x0[0],0), xytext=(x0[0],0.5),color='royalblue',fontsize=20)
plt.annotate(r'$M_0$',xy=(x0[1],0), xytext=(x0[1],0.5),color='orange',fontsize=20)
axes.add_artist(matplotlib.patches.Circle((x0[0], 0), 0.2, color = 'royalblue'))
axes.add_artist(matplotlib.patches.Circle((x0[1], 0), 0.2, color = 'orange'))
plt.suptitle('Oscillateur amorti par frottement solide : portait de phase',fontsize=20)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
xlabel(r'$x$', fontsize=20)
ylabel(r'$\frac{\dot{x}}{\omega_0}$', fontsize=20, rotation=0)
legend(fontsize=20)
plt.grid()
plt.axis((-12,12,-12,12))
plt.savefig('amorti_solide.png')
plt.show()
