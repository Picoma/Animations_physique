#-----------------------------------------------------------------------
# Système mécanique à 1 d.d.l.
#
# Tracé de l'évolution, du portrait de phase, 
# de la surface énergétique en 3D
#-----------------------------------------------------------------------
# Renseignements/bugs : Guillaume Dewaele <agreg(at)sci-phy.org>
#-----------------------------------------------------------------------

# Paramètres modifiables

# Type d'affichage :
# 1 : tracé de l'énergie potentielle
# 2 : tracé de x(t), v(t), Ep(t), Ec(t) et Em(t)
# 3 : portrait de phase
# 4 : tracé de l'énergie mécanique en 3D

type = 3

# Tracé de la trajectoire ? (requis pour type=2)

trajectoire = True

# Problème étudié (décommenter le problème choisi)
# Note : dans tous les cas, la variable est notée <x>, même s'il s'agit
# d'un angle, mais on peut changer l'inscription sur l'axe des abscisses

# Problème 1 : Masse sur une tige inclinée d'un angle alpha avec ressort
# Problème 2 : Pendule simple

probleme = 1

# Pour changer les paramètres des problèmes ou choisir un autre problème,
# il suffit de modifier les éléments dans la section suivante

#-----------------------------------------------------------------------

if probleme == 1 :
    g = 9.81 # m/s^2
    m = 1.000 # kg
    k = 100.0 # N/m
    l0 = 0.250 # m
    h = 0.1000 # m
    alpha = 0.200 # rad
    xlabel = "position (m)"
    ylabel = "vitesse (m/s)"
    
    # limites en x et en vitesse
    xmin, xmax = -0.5, 0.5
    vmin, vmax = -2.0, 2.0
    
    # pour la trajectoire 
    X0 = 0.450 # m
    V0 = 0.000 # m/s
    eta = 1.450 # frottements fluides
    tmax = 6.0 # s
    N = 500 # nombre de points sur le tracé
    
    def Ep(x) : # Energie potentielle
        dx = x*np.cos(alpha)
        dy = h-x*np.sin(alpha)
        d = (dx**2 + dy**2)**0.5
        return m*g*x*np.sin(alpha) + 0.5*k*(d-l0)**2
    
    def Ec(vx) : # Energie cinétique
        return 0.5*m*vx**2
        
    def Ff(x, vx) : # Force de frottements
        return -eta*vx

# Problème 2 : Pendule simple
# Note : x désigne ici l'angle avec la verticale

if probleme == 2 :
    R = 1.000 # m
    m = 1.000 # kg
    g = 9.81 # m/s^2
    xlabel = "angle (rad)"
    ylabel = "vitesse angulaire (rad/s)"
    
    # limites en x et en vitesse
    xmin, xmax = -2*np.pi, 4*np.pi
    vmin, vmax = -12.0, 12.0
    
    # pour la trajectoire 
    X0 = -1.450 # m
    V0 = 8.000 # m/s
    eta = 0.350 # frottements fluides
    tmax = 20.0 # s
    N = 500 # nombre de points sur le tracé
    
    def Ep(x) :
        return -m*g*np.cos(x)
    
    def Ec(vx) :
        return 0.5*m*(R*vx)**2.0
    
    def Ff(x, vx) : # Force de frottements
        return -eta*vx

#-----------------------------------------------------------------------

# Bibliothèques utilisées

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import scipy.misc as msc
import scipy.integrate as itg

#-----------------------------------------------------------------------

# Détection utilisation hors Pyzo

if '__iep__' not in globals() :
    matplotlib.interactive(False)
    
# Calcul de la trajectoire

def Fx(x, vx) :
    return -msc.derivative(Ep, x, dx=(xmax-xmin)/10000) + Ff(x, vx)

def Em(x, vx) :
    return Ep(x) + Ec(vx)

if trajectoire :
    def Der(Etat, t) :
        x, v = Etat
        return v, Fx(x, v)/m

    T = np.linspace(0.0, tmax, N)
    res = itg.odeint( Der, [ X0, V0 ], T )
    
# Tracé des résultats

if type == 1 :
    X = np.linspace(xmin, xmax, 100)
    if trajectoire :
        plt.plot(res[:,0], Em(res[:,0], res[:,1]), 'r', linewidth = 2)
    plt.plot(X, Ep(X), 'b', linewidth = 2)
    plt.xlim(xmin, xmax)
    plt.grid()
    plt.title("Énergie potentielle du système")
    plt.xlabel(xlabel)
    plt.ylabel("Ep(x) (J)") 

elif type == 2 and trajectoire == True :
    plt.subplot(3, 1, 1)
    plt.plot(T, res[:,0], 'b')
    plt.ylabel(xlabel)
    plt.grid()
    plt.subplot(3, 1, 2)
    plt.plot(T, res[:,1], 'r')
    plt.ylabel(ylabel)
    plt.grid()
    plt.subplot(3, 1, 3)
    plt.plot(T, Ep(res[:,0]), 'b', label="Ep")
    plt.plot(T, Ec(res[:,1]), 'r', label="Ec")
    plt.plot(T, Em(res[:,0], res[:,1]), 'k', label="Em")
    plt.xlabel("temps (s)")
    plt.ylabel("Energies (J)")
    plt.grid()
    plt.legend()
    
elif type == 3 :
    X, V = np.meshgrid( np.linspace(xmin, xmax, 100),
                        np.linspace(vmin, vmax, 100) )
    Z = Em(X, V)
    plt.contourf(X, V, Z, levels = np.linspace(np.min(Z), np.max(Z), 12), alpha=0.3)
    plt.contour(X, V, Z, levels = np.linspace(np.min(Z), np.max(Z), 12))
    if trajectoire :
        plt.plot(res[:,0], res[:,1], "k-", linewidth=4)
    plt.title("Portrait de phase")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    
elif type == 4 :
    X, V = np.meshgrid( np.linspace(xmin, xmax, 100),
                        np.linspace(vmin, vmax, 100) )
    Z = Em(X, V)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection="3d")
    ax.plot_surface(X, V, Z, cmap="summer")
    if trajectoire :
        ax.plot(res[:,0], res[:,1], Em(res[:,0], res[:,1]), "k-", linewidth=4)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

# Détection utilisation hors Pyzo
    
if '__iep__' not in globals() :
    plt.show()