#-----------------------------------------------------------------------
# Oscillations quantiques de la molécule de NH3
#
# Note : les ordres de grandeur en dimension/énergie sont corrects,
# mais le modèle reste grossier, à but illustratif et non prédictif
# en particulier au niveau des énergies et fréquences d'oscillations !
#-----------------------------------------------------------------------
# Renseignements/bugs : Guillaume Dewaele <agreg(at)sci-phy.org>
#-----------------------------------------------------------------------

# Paramètres modifiables

# Choix de la sortie
# 1 = Tracé des fonctions d'ondes < V0
# 2 = Tracé des fonctions d'ondes < 2V0
# 3 = Tracé des probabilités pour E < V0
# 4 = Tracé des probabilités pour E < 2V0
# 5 = Animation des probabilités pour un mélange 50/50 Sym/Anti
# 6 = Animation 3D des fonctions d'ondes pour ce même mélange

sortie = 5

# Configuration du puits quantique
#
# Note : une barrière plus haute (par exemple 0.5eV) ou plus
# épaisse rend le passage d'un côté à l'autre plus difficile, 
# donc réduit la fréquence d'inversion

a = 0.037 # distance au centre des puits (nm)
b = 0.040 # largeur des puits (nm)
V0 = 0.25 # hauteur de la barrière, eV

# Masse réduite de la particule fictive

m = 1.0e-27 # kg

# Facteur d'homothétie en temps pour les oscillations

vitesse = 5e-14

# Coefficient d'échelle pour les probabilités (oscillations)

coeff_osc = 0.015

# Coefficient d'échelle pour les amplitudes (états propres)

coeff = 0.02

# Coefficient d'échelle pour les probabilités (états propres)

coeff_prob = 0.005

#-----------------------------------------------------------------------

# Bibliothèques utilisées

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as ani
from mpl_toolkits.mplot3d import Axes3D
import scipy.integrate as itg
import scipy.optimize as opt
import itertools as itt

#-----------------------------------------------------------------------

# Détection utilisation hors Pyzo

if '__iep__' not in globals() :
    matplotlib.interactive(False)

# Constantes utiles

Colors = 'brgmcy'

hbar = 1.054e-34

# Potentiel

@np.vectorize
def V(x) :
    x = abs(x) - a
    
    if abs(x) < b/2 :
        return 0.0
    elif x < 0.0 :
        return V0
    else :
        return 1e2*V0 # +infini

# Intérieur du puits

Xext = np.linspace(-a-b/1.5, a+b/1.5, 2000)
X = np.linspace(-a-b/2.0, a+b/2.0, 200)

# Calcul de Phi(x)

def Phi(X, E) :
    def F(Y, x, E) :
        y, dy = Y

        c = 2*m / hbar**2.0 * 1.6e-19 * (1e-9)**2.0
        
        d2y = -c*(E-V(x))*y
        
        return [ dy, d2y ]

    Y = itg.odeint(F, [ 0, 0.5 ], X, args=(E,))
    Y = Y[:,0]
    
    I = itg.trapz(Y**2, X)
    return Y / (I**0.5)

# Calcul de Phi(a+b/2)

def Foo(X, E) :
    return Phi(X, E)[-1]    

# Calcul des énergies possibles

if sortie == 1 or sortie == 3 :
    Vmax = V0
else :
    Vmax = 2*V0

Energies = np.linspace(0, Vmax, 200)
XDroite = [ Foo(X, E) for E in Energies ]

PossEnerg = []
for i in range(len(XDroite)-1) :
    if XDroite[i]==0 or XDroite[i]*XDroite[i+1]<0 :
        PossEnerg.append(opt.bisect(lambda e : Foo(X, e), Energies[i], Energies[i+1]))

# Fonctions pour l'évolution de la fonction d'onde

def Evolution(LEPhi, t) :
    """Prend une liste de couples (énergie, fonction d'onde à t=0)
       et un instant t et retourne la fonction d'onde à t
       Attention, le résultat est complexe !"""
    return sum(Phi * np.exp(1j*E*1.6e-19/hbar*t) for E, Phi in LEPhi)
    
    PhiCplx = 0.0j*LEPhi[0][1]
    for E, Phi in LEPhi :
        PhiCplx += Phi * np.exp(1j*E*1.6e-19/hbar*t)
    return PhiCplx

def VersProba(PhiCplx) :
    """Prend une fonction d'onde (complexe ou réelle)
       et retourne la distribution de probabilité de présence"""
    return (PhiCplx.real)**2 + (PhiCplx.imag)**2

# Calcul des états symétriques et antisymétriques les plus bas

Es, Ys = PossEnerg[0], Phi(X, PossEnerg[0])
Ea, Ya = PossEnerg[1], Phi(X, PossEnerg[1])

#-----------------------------------------------------------------------

# Affichage

def SizeChanged(ax, old=[]) :
    current = [ ax.bbox.width, ax.bbox.height ]
    if old != current :
        old[:] = current
        return True
    return False

if sortie <= 5 :
    # Tracé du puits
    plt.axvspan(Xext[0], -a-b/2, color='r', alpha=0.4)
    plt.axvspan(a+b/2, Xext[-1], color='r', alpha=0.4)
    plt.axvspan(-a+b/2, a-b/2, color='y', alpha=0.4)
    plt.plot(Xext, V(Xext), 'k', linewidth=2)
    plt.xlim(Xext[0], Xext[-1])
    
if sortie == 1 or sortie == 2 :
    plt.ylim([-0.2*Vmax,1.2*Vmax]) 
    # Afficher toutes les fonctions d'ondes
    for i, E in enumerate(PossEnerg) :
        phi = Phi(X,E)
        plt.fill_between(X, E+0*phi, E+coeff*phi,
                         color=Colors[i%6], alpha=0.2)
        plt.plot(X, E+coeff*phi, Colors[i%6]+"-", linewidth=2)
        plt.plot([X[0],X[-1]], [E,E], Colors[i%6]+"--", linewidth=2)
    plt.title("Etats propres (amplitudes)")
    plt.ylabel("Energies et amplitudes (u.a.)")
    plt.xlabel("Position (nm)")

if sortie == 3 or sortie == 4 :
    plt.ylim([-0.2*Vmax,1.2*Vmax]) 
    # Afficher toutes les probabilités de présence
    for i, E in enumerate(PossEnerg) :
        phi = Phi(X,E)**2
        plt.fill_between(X, E+0*phi, E+coeff_prob*phi,
                         color=Colors[i%6], alpha=0.2)
        plt.plot(X, E+coeff_prob*phi, Colors[i%6]+"-", linewidth=2)
        plt.plot([X[0],X[-1]], [E,E], Colors[i%6]+"--", linewidth=2)
    plt.title("Etats propres (probabilités)")
    plt.ylabel("Energies et densités de probabilité (u.a.)")
    plt.xlabel("Position (nm)")
 
#-----------------------------------------------------------------------

# Animation des probabilités pour un mélange sym/anti

if sortie == 5 :
    Melange = [ (Ea, 0.707*Ya), (Es, 0.707*Ys) ]
    
    crv, = plt.plot(X, VersProba(Evolution(Melange, 0.0)), 'b-', linewidth=2)
    
    plt.ylim([-0.2*Vmax, 1.2*Vmax])
    plt.title("Distribution de probabilité")
    plt.ylabel("Energie (eV) / Amplitudes de prob. (u.a.)")
    plt.xlabel("Position (nm)")
    
    def Update(t) :
        phi = VersProba(Evolution(Melange, t))*coeff_osc
        crv.set_data(X, phi)
        if SizeChanged(plt.gca()) :
            plt.gcf().canvas.draw()
        return [crv]
    
    def Init() :
        crv.set_data(X, np.ma.array(X, mask=True))
        return [crv] 
    
    anim = ani.FuncAnimation(plt.gcf(), Update, frames=itt.count(0, vitesse/20), interval=50, blit=True, init_func=Init, save_count=None)

#-----------------------------------------------------------------------

# Animation 3D des fonctions d'ondes sym/anti et mélange

if sortie == 6 :
    Melange = [ (Ea, 0.707*Ya), (Es, 0.707*Ys) ]
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection="3d")
    plt.title("Evolution d'un mélange")
    plt.xlabel("Position (u.a.)")
    
    Y = Evolution([(Ea, Ya)], 0.0)
    crv1, = ax.plot(X, Y.real, Y.imag, "r", linewidth=3)
    
    Y = Evolution([(Es, Ys)], 0.0)
    crv2, = ax.plot(X, Y.real, Y.imag, "b", linewidth=3)
    
    Y = Evolution(Melange, 0.0)
    crv3, = ax.plot(X, Y.real, Y.imag, "k", linewidth=3)
    
    ax.set_xlim3d([-a-b/2, a+b/2])
    ax.set_ylim3d([-10., 10.])
    ax.set_zlim3d([-10., 10.])
    
    def Update(t) :
        Y = Evolution([(Ea, Ya)], t)
        crv1.set_data(X, Y.real)
        crv1.set_3d_properties(Y.imag)
        
        Y = Evolution([(Es, Ys)], t)
        crv2.set_data(X, Y.real)
        crv2.set_3d_properties(Y.imag)
        
        Y = Evolution(Melange, t)
        crv3.set_data(X, Y.real)
        crv3.set_3d_properties(Y.imag)
        
        if SizeChanged(plt.gca()) :
            plt.gcf().canvas.draw()
        return [crv1, crv2, crv3]
    
    anim = ani.FuncAnimation(plt.gcf(), Update, frames=itt.count(0, vitesse/20), interval=50, blit=False, save_count=None)

if '__iep__' not in globals() :
    plt.show()
