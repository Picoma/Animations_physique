#-----------------------------------------------------------------------
# Séparation des états pairs et impairs dans un double puits
#
# Note : l'affichage de la courbe nécessite un temps de calcul
# important, dû à la détermination des différentes énergies
#-----------------------------------------------------------------------
# Renseignements/bugs : Guillaume Dewaele <agreg(at)sci-phy.org>
#-----------------------------------------------------------------------

# Paramètres modifiables

# Configuration du puits quantique

amin = 0.022 # distance minimale au centre des puits (nm)
amax = 0.056 # distance maximale au centre des puits (nm)
nb = 8 # nombre de distances considérées
b = 0.040 # largeur des puits (nm)
V0 = 0.25 # hauteur de la barrière, eV

# Masse réduite de la particule fictive

m = 1.0e-27 # kg

#-----------------------------------------------------------------------

# Bibliothèques utilisées

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import scipy.integrate as itg
import scipy.optimize as opt
import itertools as itt

#-----------------------------------------------------------------------

# Détection utilisation hors Pyzo

if '__iep__' not in globals() :
    matplotlib.interactive(False)

# Constantes utiles

hbar = 1.054e-34

# Potentiel

@np.vectorize
def V(x, a) :
    x = abs(x) - a
    
    if abs(x) < b/2 :
        return 0.0
    elif x < 0.0 :
        return V0
    else :
        return 1e2*V0 # +infini

# Intérieur du puits

Xext = np.linspace(0.0, amax+b/1.5, 2000)
X = np.linspace(0.0, amax+b/2.0, 200)

# Calcul de Phi(x>0)

def Phi(X, E, pair, a) :
    def F(Y, x, E, a) :
        y, dy = Y

        c = 2*m / hbar**2.0 * 1.6e-19 * (1e-9)**2.0
        
        d2y = -c*(E-V(x, a))*y
        
        return [ dy, d2y ]
    
    if pair :
        cond_ini = [ 1.0, 0.0 ]
    else :
        cond_ini = [ 0.0, 1.0 ]
        
    Y = itg.odeint(F, cond_ini, X, args=(E, a))
    Y = Y[:,0]
    
    I = itg.trapz(Y**2, X)
    return Y / (I**0.5)

# Calcul de Phi(a+b/2)

def Foo(X, E, pair, a) :
    return Phi(X, E, pair, a)[-1]    

# Calcul des énergies possibles

Vmax = 3*V0

Energies = np.linspace(0, Vmax, 15)

A = np.linspace(amin, amax, nb)

EPaires = []
EImpaires = []

for i, a in enumerate(A) :
    print("simulation ", i+1, "/", nb, sep="") 
    # Fonctions paires     
    XDroite = [ Foo(X, E, True, a) for E in Energies ]
    
    PossEnerg = []
    for i in range(len(XDroite)-1) :
        if XDroite[i]==0 or XDroite[i]*XDroite[i+1]<0 :
            PossEnerg.append(opt.bisect(lambda e : Foo(X, e, True, a), Energies[i], Energies[i+1], xtol=V0/100))
    
    EPaires.append(PossEnerg)

    # Fonctions impaires     
    XDroite = [ Foo(X, E, False, a) for E in Energies ]
    
    PossEnerg = []
    for i in range(len(XDroite)-1) :
        if XDroite[i]==0 or XDroite[i]*XDroite[i+1]<0 :
            PossEnerg.append(opt.bisect(lambda e : Foo(X, e, False, a), Energies[i], Energies[i+1]))
    
    EImpaires.append(PossEnerg)

for Energies, lignes in zip([ EPaires, EImpaires ], [ "b", "r" ]) :
    n = max(len(lst) for lst in Energies)
    for j in range(n) :
        X = []
        Y = []
        for i, a in enumerate(A) :
            if len(Energies[i]) > j :
                X.append(a/b)
                Y.append(Energies[i][j])
            plt.plot(X, Y, lignes, linewidth=2)

plt.title("Energies des états pairs (bleu) et impairs (rouge) selon a/b")
plt.grid()
plt.xlim(amin/b, amax/b)
plt.ylim(0, 2.5*V0)
plt.axhspan(0, V0, facecolor="g", alpha=0.3)
plt.xlabel("a/b")
plt.ylabel("Energies (eV)")

#-----------------------------------------------------------------------

# Détection utilisation hors Pyzo

if '__iep__' not in globals() :
    plt.show()
