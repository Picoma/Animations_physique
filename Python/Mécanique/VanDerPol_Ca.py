# -*- coding: Latin-1 -*-
# Programme de trac� de l'�quation de Van der Pol
# Dominique Lefebvre pour TangenteX.com
# 30 d�cembre 2015
#

# importation des librairies
from scipy.integrate import odeint 
from scipy import array, arange,pi, sin
import matplotlib.pyplot as plt


# D�finition de l'�quation diff�rentielle de Van der Pol
def VanDerPol(X,t):
    x = X[0]
    x_point = X[1]
    dx = x_point
    dx_point = epsilon*(1 - x*x)*dx - x
    return array([dx, dx_point])

# d�finition du vecteur temps de l'exp�rience
t0 = 0
tmax = 1000
pastemps = 0.0001
time = arange(t0, tmax, pastemps)

# D�finition des conditions initiales
x0 = 0.1
v0 = 0.1

# D�finition de epsilon
epsilon = 0.5
# r�solution de l'�quation diff�rentielle
x, x_point = odeint(VanDerPol,(x0,v0),time).T

# trac� de la trajectoire de l'oscillateur
#p1 = plt.figure()
#plt.grid()
#plt.xlabel('$t$', fontsize = 20)
#plt.ylabel('$x$', fontsize = 20)
#plt.plot(time, x)
#plt.show()


# trac� de la trajectoire de phase
p2 = plt.figure()
plt.grid()
plt.xlabel('$Position$', fontsize = 20)
plt.ylabel('$Vitesse$', fontsize = 20)
plt.plot(x, x_point)
plt.show()


