#-----------------------------------------------------------------------
# Effet Doppler non relativiste
#-----------------------------------------------------------------------
# Renseignements/bugs : Guillaume Dewaele <agreg(at)sci-phy.org>
#-----------------------------------------------------------------------

# Paramètres modifiables

# Position initiale de l'émetteur

X0 = 0
Y0 = 15

# Vitesse de l'émetteur

V = 7.5

# Pulsation de l'émetteur

omeg = 3.5

# Vitesse des ondes sonores

W = 15

# Position du récepteur

XC = 75
YC = 35

# Tracé du signal reçu
# 1.0 : amplitude normalisée
# 0.0 : amplitude réelle
# 0.5 : approximation grossière mais raisonnable
#       du "niveau" sonore perçu

coeff = 0.5

# Affichage (point rouge) de l'origine instantanée
# du signal sonore (origine des sons parvenant à
# l'instant t au récepteur, illustre le fait
# que l'on a l'impression que le son "suit" la source)

ghost = True

# Images par seconde (à réduire si l'ordinateur n'est pas assez rapide)

fps = 20

#-----------------------------------------------------------------------

# Bibliothèques utilisées

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as ani
from matplotlib.colors import LinearSegmentedColormap

#-----------------------------------------------------------------------

# Détection utilisation hors Pyzo

if '__iep__' not in globals() :
    matplotlib.interactive(False)

# Grille de calcul

X, Y = np.meshgrid(np.linspace(0, 150, 151), np.linspace(0, 40, 41))

# Calcul du signal en tout point à t

def Get(T, X, Y, full=False) :
    A = W**2-V**2
    Bs2 = (V*(X-X0)-W**2*T)
    mC = (X-X0)**2 + (Y-Y0)**2 - W**2*T**2
    Delta = np.abs(Bs2**2+A*mC)
    TE = (-Delta**0.5-Bs2)/A
    if full :
        return np.sin(omeg*TE), (YC-Y0)**2/(W**2*(T-TE)**2), TE
    return np.sin(omeg*TE)

# Carte de couleurs

basic_cols=['#6577F5', '#000000', '#ffd700']
my_cmap=LinearSegmentedColormap.from_list('mycmap', basic_cols)

# Instants considérés

duration = (X[0][-1] - 2*X0)/V
TT = np.linspace(0.0, duration, duration*fps)

# Premier tracé

fig = plt.figure()
ax2 = fig.add_subplot(2, 1, 2)
ax2.grid()
ax2.set_ylim(-1.2, 1.2)
sig, = ax2.plot(TT, [0.0] * len(TT), linewidth=2.0)
ax1 = fig.add_subplot(2, 1, 1)
ax1.plot([XC], [YC], "wd", markersize=20)
em, = ax1.plot([XC], [YC], "wo", markersize=16)
if ghost :
    gh, = ax1.plot([-20.0], [YC], "ro", markersize=16)
tbl = plt.imshow(Get(10.0, X, Y), cmap=my_cmap)

# Fonction de mise à jour

def Update(t) :
    tbl.set_array(Get(t, X, Y))
    em.set_data([X0+V*t], [Y0])
    TI = [ ti for ti in TT if ti<=t ]
    SA = [ Get(ti, XC, YC, True) for ti in TI ]
    S = [ s*a**coeff for s, a, _ in SA ]
    sig.set_data(TI, S)
    if ghost :
        gh.set_data([X0+V*SA[-1][2]], [Y0])
        return [tbl, em, gh, sig]
    return [tbl, em, sig]

# Animation

anim = ani.FuncAnimation(fig, Update, frames=TT,
                         interval=1000//fps, blit=False)

# Détection utilisation hors Pyzo

if '__iep__' not in globals() :
    plt.show()
