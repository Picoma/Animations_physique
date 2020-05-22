# -*- coding: Latin-1 -*-
# Programme de tracé de l'équation de Van der Pol
# Dominique Lefebvre pour TangenteX.com
# 30 décembre 2015
#

# importation des librairies
from scipy.integrate import odeint 
from scipy import array, arange,pi, sin
import matplotlib.pyplot as plt


# Définition de l'équation différentielle de Van der Pol
def VanDerPol(X,t):
    x = X[0]
    x_point = X[1]
    dx = x_point
    dx_point = epsilon*(1 - x*x)*dx - x
    return array([dx, dx_point])

# définition du vecteur temps de l'expérience
t0 = 0
tmax = 1000
pastemps = 0.0001
time = arange(t0, tmax, pastemps)

# Définition des conditions initiales
x0 = 0.1
v0 = 0.1

# Définition de epsilon
epsilon = 0.5
# résolution de l'équation différentielle
x, x_point = odeint(VanDerPol,(x0,v0),time).T

# tracé de la trajectoire de l'oscillateur
#p1 = plt.figure()
#plt.grid()
#plt.xlabel('$t$', fontsize = 20)
#plt.ylabel('$x$', fontsize = 20)
#plt.plot(time, x)
#plt.show()


# tracé de la trajectoire de phase
p2 = plt.figure()
plt.grid()
plt.xlabel('$Position$', fontsize = 20)
plt.ylabel('$Vitesse$', fontsize = 20)
plt.plot(x, x_point)
plt.show()


