#-----------------------------------------------------------------------
# Etats propres d'un potentiel quantique
#
# Les énergies sont en eV, les distances en nm
#-----------------------------------------------------------------------
# Renseignements/bugs : Guillaume Dewaele <agreg(at)sci-phy.org>
#-----------------------------------------------------------------------

# Paramètres modifiables

# Fonction potentiel
# (décommenter la fonction choisie)

def V(x) :
    # Potentiel harmonique
    return 5.0*x**2
    
    # Potentiel carré
    # return 0.0 if abs(x)<1.0 else 40.0
    
    # Potentiel W (attention, états propres 1 et 2 proches)
    # return (1.3 - 8.0*x**2 + 12.0*x**4) if x<1.5 else 44.05

# Masse de la particule

m = 9.11e-31  # kg

# Largeur du puits (pour l'affichage)

a = 1.2       # nm

# Zone de recherche pour les énergies (et pour l'affichage)

Emin = 0.0    # eV
Emax = 5.0    # eV

# Nombre d'énergies testées
# (moins d'énergies testées = temps de calcul réduit, 
#  mais risque de manquer des états propres proches)

NbE = 200

# Affichage des probabilités de présence (True) ou de l'onde (False)

affiche_probas = False

# Echelle verticale pour les tracés des amplitudes

coeff = 0.3

#-----------------------------------------------------------------------

# Bibliothèques utilisées

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import scipy.integrate as itg
import scipy.optimize as opt

#-----------------------------------------------------------------------

# Détection utilisation hors Pyzo

if '__iep__' not in globals() :
    matplotlib.interactive(False)
    
# Paramètres pour le calcul

b = 2.0 * a    # Largeur du puis pour le calcul

hbar = 1.054e-34
c = 2*m / hbar**2.0 * 1.6e-19 * (1e-9)**2.0

X = np.linspace(-b, b, 200)

# Vectorisation de la fonction potentiel

V = np.vectorize(V)

# Calcul de Phi(x)

def PossPhi(X, E) :
    def F(Y, x, E) :
        y, dy = Y
        
        d2y = -c*(E-V(x))*y
        
        return [ dy, d2y ]

    Y = itg.odeint(F, [ 0, 1e-4 ], X, args=(E,))
    return Y[:,0]
    
# Calcul de Phi(b)

def Foo(X, E) :
    return PossPhi(X, E)[-1]    

# Fonctions pour la normalisation

def Normalize(X, Y) :
    I = itg.trapz(Y**2, X)
    return Y / (I**0.5)

def XPhi(X, E) :
    return X[40:-40], Normalize(X[40:-40], PossPhi(X, E)[40:-40])

# Calcul des énergies possibles

Energies = np.linspace(Emin, Emax, NbE)
XDroite = [ Foo(X, E) for E in Energies ]

PossEnerg = []
for i in range(len(XDroite)-1) :
    if XDroite[i]==0 or XDroite[i]*XDroite[i+1]<0 :
        PossEnerg.append(opt.bisect(lambda e : Foo(X, e), Energies[i], Energies[i+1]))

# Tracé du puits

Xaff = np.linspace(-a, a, 200)
plt.plot(Xaff, V(Xaff), 'k', linewidth=2)

diffE = Emax - Emin
plt.xlim([-a, a])
plt.ylim([Emin-diffE/5.0, Emax+diffE/5.0])
 
plt.xlabel("Position (nm)")
plt.ylabel("Énergies propres (eV)")

# Tracé des états propres

Colors = 'brgmcy'

for i, E in enumerate(PossEnerg) :
    Xr, Phir = XPhi(X, E)
    if affiche_probas :
        Phir **= 2.0
    plt.fill_between(Xr, E+0*Phir, E+coeff*Phir,
                     color=Colors[i%6], alpha=0.4)
    plt.plot(Xr, E+coeff*Phir,
             Colors[i%len(Colors)]+"-", linewidth=2)
    plt.plot([X[0],X[-1]], [E,E],
             Colors[i%len(Colors)]+"-", linewidth=2)

# Détection utilisation hors Pyzo

if '__iep__' not in globals() :
    plt.show()
