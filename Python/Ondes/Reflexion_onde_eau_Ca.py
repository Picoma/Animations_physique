#-----------------------------------------------------------------------
# Réflexion d'un paquet d'onde sur une interface vide-eau
#-----------------------------------------------------------------------
# Renseignements/bugs : Guillaume Dewaele <agreg(at)sci-phy.org>
#-----------------------------------------------------------------------

# Paramètres modifiables

# Paramètres du paquet d'onde
# w0 contrôle la pulsation centrale, dw l'étalement, 
# et N le nombre de pulsations différentes dans le paquet

w0 = 1.0
dw = 0.05
N = 21

# Vitesse de l'animation

speed = 0.1

# Calculs des relations entre k_g (à gauche) et k_d (à droite)
# et la pulsation w

def Kg(w) :
    return 1.0*w                # vide

def Kd(w) :
    return 1.33*w               # eau

# Coulueur du milieu de droite

col = 'b'

# Titre

titre = "Réflexion sur une interface vide-eau"

#-----------------------------------------------------------------------

# Bibliothèques utilisées

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as ani
from itertools import count

#-----------------------------------------------------------------------

# Création du paquet d'onde

W = np.linspace(w0-2*dw, w0+2*dw, N)
A = np.exp( - ((W-w0)/dw)**2 ) 

# Calcul des K correspondants

K1 = Kg(W)
K2 = Kd(W)

# Position de l'interface, choix des abscisses

d = 30
X1 = np.linspace(0, d, 1000)
X2 = np.linspace(d, 2*d, 1000)
X = np.concatenate([X1, X2])

# Calcul des coefficients de réflexion/transmission

R = (K1-K2)/(K1+K2)*np.exp(4j*np.pi*K1*d)
T = np.exp(2j*np.pi*(K1-K2)*d) + R*np.exp(-2j*np.pi*(K1+K2)*d)

# Calcul des amplitudes des ondes réfléchies/transmises

Ar = R*A
At = T*A

#-----------------------------------------------------------------------

# Calcul de l'onde à l'instant t

def Onde(t) :
    Y1 = np.real( np.sum(A[i] * np.exp( 2j*np.pi*( K1[i]*X1-W[i]*t ))
                for i in range(len(W))))
    Y1 += np.real( np.sum(Ar[i] * np.exp( 2j*np.pi*(-K1[i]*X1-W[i]*t ))
                for i in range(len(W))))
    Y2 = np.real( np.sum(At[i] * np.exp( 2j*np.pi*( K2[i]*X2-W[i]*t ))
                for i in range(len(W))))
    return np.concatenate([Y1, Y2])

#-----------------------------------------------------------------------

# Détection utilisation hors Pyzo

if '__iep__' not in globals() :
    matplotlib.interactive(False)

# Création d'une figure

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
crv, = ax.plot(X, Onde(0.1))

# Décoration

plt.title(titre)

ax.set_ylim(-15.0, 15.0)
ax.axvspan(d, 2*d, facecolor=col, alpha=0.5)

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

anim = ani.FuncAnimation(fig, Update, count(0.0, speed), interval=10, blit=True, init_func=Init)

# Détection utilisation hors Pyzo

if '__iep__' not in globals() :
    plt.show()
    

