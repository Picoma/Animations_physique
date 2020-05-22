#Ce programme permet de tracer la courbe de position d'un oscillateur harmonique
#type ressort avec frottements solides
#On y voit x(t) ainsi que la zone d'arret si la vitesse s'annule
#
#-------------------------------------------------------------

# Packages
from math import *
import numpy as np
import matplotlib.pyplot as plt

# Parametres
pi = acos(-1);
omega_0 = 2*pi; # pulsation du probleme
N = 20; # echantillonage de l'intervalle de longueur 2pi/omega_0
dt = 2*pi/(2*N*omega_0) # pas de temps pour l'echantillonage
f = .3; # coefficient de frottement
g = 9.81 # gravite
xlim = f*g/omega_0 # x limite


# Conditions initiales
x0 = 8
dtx0 = 0.
eps = np.sign(x0) # sens frottement

# Declaration des vecteur
temps = []
temps_extr = []
x = []
dtx = []
xextr = []

# Coefficients
A = x0
B = 0

# Initialisation
x.append(x0)
dtx.append(dtx0)
temps.append(0)

# Definition des fonctions x et dx/dt
fx = lambda t: A*cos(omega_0*t)+B*sin(omega_0*t)+eps*xlim
fdtx = lambda t: -A*omega_0*sin(omega_0*t)+B*omega_0*cos(omega_0*t)

print(x0, xlim)
# Parcours du premier intervalle
for k in range(0,N) :
    temps.append(temps[-1]+dt)
    x.append(fx(temps[-1]))
    dtx.append(fdtx(temps[-1]))
eps *= -1

# Test de position extremal
xextr.append(abs(x[-1])) # initialisation
temps_extr.append(temps[-1])

# Boucle sur les intervalles de longueur 2*pi/omega_0
while abs(xextr[-1]) > xlim:
    # inversion du systeme lineaire pour trouver A et phi
    A = (x[-1]-eps*xlim)*cos(omega_0*temps[-1]) - dtx[-1]/omega_0*sin(omega_0*temps[-1])
    B = dtx[-1]/omega_0*cos(omega_0*temps[-1]) + (x[-1] - eps*xlim)*sin(omega_0*temps[-1])
    
    for k in range(0,N):
        temps.append(temps[-1]+dt)
        x.append(fx(temps[-1]))
        dtx.append(fdtx(temps[-1]))
    eps *= -1
    xextr.append(abs(x[-1]))
    temps_extr.append(temps[-1])

# Ajout de points immobiles sur une période
for k in range(0,N):
    temps.append(temps[-1]+dt)
    x.append(x[-1])
    

# Tracé du résultat en position
plt.figure(1)
plt.plot(temps,x)
plt.axhline(y=xlim , xmin = 0 , xmax=1 , color='red' )
plt.axhline(y=-xlim , xmin = 0 , xmax=1 , color='red' )
plt.title("Position en fonction du temps")
plt.xlabel("Temps $t$ ($s$)")
plt.ylabel("Position $x$ ($m$)")

## Tracé du résultat en vitesse
#plt.figure(2)
#plt.plot(temps,dtx)
#plt.title("Vitesse en fonction du temps")
#plt.xlabel("Temps $t$ ($s$)")
#plt.ylabel("Vitesse " r'$ \dot{x}$' " (" r'$m.s^{-1}$'")")
#
## Tracé du résultat en extrema supérieur
#plt.figure(3)
#plt.plot(temps_extr,xextr)
#plt.title("Position extremale $x$ en fonction du temps $t$")
#plt.xlabel(" Temps $t$ ($s$)")
#plt.ylabel(" Position extremale $x$ ")

plt.show()
