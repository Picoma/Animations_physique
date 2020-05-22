#-----------------------------------------------------------------------
# Animation de l'étalement d'un paquet d'onde gaussien
#-----------------------------------------------------------------------
# Renseignements/bugs : Guillaume Dewaele <agreg(at)sci-phy.org>
#-----------------------------------------------------------------------

# Paramètres modifiables

# Vitesse de groupe

Vg = 0.5

# Modèle :
# 1 : w = a.k     (non dispersif)
# 2 : w = a.k^2   (type electron libre) 
# 3 : w = a.k^0.5 (type vagues, défilement dans l'autre sens)
# 4 : w = a.k^3   (non physique, mais plus visible)

type = 4

# Tracé de l'enveloppe ou de l'onde

enveloppe = False

# Contrôle des paramètres

assert(0.2 <= Vg <= 2.0)
assert(type in (1, 2, 3, 4))
 
#-----------------------------------------------------------------------

# Bibliothèques utilisées

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as ani
from numpy.fft import fft, fftfreq

#-----------------------------------------------------------------------

# Foncton définissant la vitesse de phase en fonction du
# nombre d'onde sigma

@np.vectorize
def Vp(sig) :
    # Pas d'étalement :
    if type == 1 :
        return Vg
        
    # a.k^2
    if type == 2 :
        return Vg*sig/2.0
    
    # a.k^0.5
    if type == 3 :
        if sig==0.0 :
            return 0.0
        return Vg*2.0/(np.abs(sig))**0.5
    
    # a.k^3
    if type == 4 :
        return Vg*sig**2.0/3.0
    
# Détection utilisation hors Pyzo

if '__iep__' not in globals() :
    matplotlib.interactive(False)

# Abscisses

X = np.linspace(0, 160, 4096)

# Nombres d'ondes correspondants

Sig = fftfreq(len(X), 160/4096)

# Calcul de la forme de l'onde à un instant t

def Onde(t) :
    Yp = np.exp(-((Sig-1)/0.07)**2 + 6.283j*Sig*Vp(Sig)*t)
    
    if enveloppe :
        return np.abs(fft(Yp))
    else :
        return np.real(fft(Yp))

# Premier tracé pour préparer l'animation

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
crv, = plt.plot(X, Onde(0))

# Décoration

if type == 1 :
    ax.set_title(r"Évolution du paquet d'onde (non dispersif, $\omega = \alpha k$)")
elif type == 2 :
    ax.set_title(r"Évolution du paquet d'onde (type électron, $\omega = \alpha k^2$)")
elif type == 3 :
    ax.set_title(r"Évolution du paquet d'onde (type vagues, $\omega = \alpha \sqrt{k}$)")
elif type == 4 :
    ax.set_title(r"Évolution d'un paquet d'onde dans un milieu dispersif")

# Animation

def SizeChanged(ax, old=[]) :
    current = [ ax.bbox.width, ax.bbox.height ]
    if old != current :
        old[:] = current
        return True
    return False

def Update(t) :
    crv.set_data(X, Onde(t))
    if SizeChanged(plt.gca()) :
        plt.gcf().canvas.draw()
    return [crv]

def Init() :
    crv.set_data(X, np.ma.array(X, mask=True))
    return [crv]

anim = ani.FuncAnimation(fig, Update,
                         frames=np.linspace(int(10/Vg), int(130/Vg), int(241/Vg)),
                         interval = 50,
                         blit=True, init_func=Init)

# Détection utilisation hors Pyzo

if '__iep__' not in globals() :
    plt.show()
