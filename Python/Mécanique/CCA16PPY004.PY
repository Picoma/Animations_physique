# -*- coding: utf-8 -*-

"""
Résolution numérique de l'équation du pendule amorti : d^2x/dt^2+omega0/Q*dx/dt+omega0^2*sin(x)=0
en décomposant en un système de deux équations du premier ordre
dx/dt = v
dv/dt = -omega0/Q*v+omega0^2*sin(x)

***
Le but est de tracer des portraits de phase pour un pendule simple amorti (ou non si le facteur de qualité est important), notamment en régime fortement non linéaire.
Le programme fournit aussi l'évolution temporelle.
On peut modifier l'équation physique (du second ordre nécessairement) dans "système différentel", la durée de résolution dans "paramètres d'intégration", les conditions initiales dans "conditions initiales" et les paramètres d'affichage de l'évolution temporelle et du portrait de phase dans les sections "évolution temporelle" et "portrait de phase"
***

***
Paramètres à ajuster : Q, omega0, conditions initiales. Suivant ces dernières, les limites des axes des graphes peuvent ne pas convenir.
***

"""

from __future__ import division
from scipy import *
from pylab import *
from scipy.integrate import odeint      # Module de résolution des équations différentielles

omega0 = 2*pi				# Paramètres de l'équation différentielle à résoudre : d^2x/dt^2+omega0/Q*dx/dt+omega0^2*sin(x)=0
Q = 100

# Système différentiel
def deriv(syst, t):
    x = syst[0]                         # Variable1 x
    v = syst[1]                         # Variable2 v
    dxdt = v                            # Equation différentielle 1		*** adapter ces deux lignes à l'équation ***
    dvdt = -omega0/Q*v-omega0**2*sin(x) # Equation différentielle 2		***     du système physique considéré    ***
    return [dxdt,dvdt]                  # Dérivées des variables

# Paramètres d'intégration (Plage de temps sur laquelle s'effectue la résolution)
start = 0
end = 20
numsteps = 1000
t = linspace(start,end,numsteps)

# Conditions initiales et résolution
x0=1					# Modifier les CI ici pour les différents régimes (fronde, lâcher sans vitesse initiale,...)
v0=11.2
syst_CI=array([x0,v0])                  # Tableau des CI
Sols=odeint(deriv,syst_CI,t)            # Résolution numérique des équations différentielles

# Récupération des solutions
x = Sols[:, 0]
v = Sols[:, 1]


# Graphiques des solutions
# Evolution temporelle (attention aux limites des axes)
figure1 = figure()
plot(t, x, 'o', ms=2, mfc='w', mec='b',label=u"Sol.Num.")       # Solution numérique
xlim(0, 10)                                                     # Limites de l'axe des abscisses
xlabel("$t \, (s)$", fontsize=16)                             # Label de l'axe des abscisses
ylim(-1, v0+x0)                                                     # Limites de l'axe des ordonnées
ylabel("$x/x_0$", fontsize=16)               # Label de l'axe des ordonnées
legend()

# Portrait de phase (attention aux limites des axes)
figure2 = figure()
plot(x, v/omega0, 'o', ms=2, mfc='w', mec='b',label=u"Sol.num.")          # Solution numérique
xlim(-x0, x0)                                       # Limites de l'axe des abscisses
xlabel("$x/x_0$", fontsize=16)       # Label de l'axe des abscisses
ylim(-v0, v0)                                             # Limites de l'axe des ordonnées
ylabel("$v/\omega_0$", fontsize=16)  # Label de l'axe des ordonnées
axis('equal')
legend()
show()