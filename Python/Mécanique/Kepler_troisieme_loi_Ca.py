#-----------------------------------------------------------------------
# Illustration de la troisième loi de Kepler
#
# Les quatre objets ayant le même demi grand-axe a,
# ils ont la même période T
#-----------------------------------------------------------------------
# Renseignements/bugs : Guillaume Dewaele <agreg(at)sci-phy.org>
#-----------------------------------------------------------------------

# Paramètres modifiables

# Durée de la simulation en jours

NbJours = 730

# Vitesse

vitesse = 1.0

#-----------------------------------------------------------------------

# Bibliothèques utilisées

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as ani
from scipy.integrate import odeint

#-----------------------------------------------------------------------
    
# Quelques constantes

au = 149597870700.0 # km

G = 6.6742e-11 # SI

# Paramètres des corps

M = [ 1.0,
      1.0,
      1.0,
      1.0 ]

MS = 1.989e30      # kg, Soleil

P1 = [ au, 0, 0 ]
P2 = [ 1.25*au, 0, 0 ]
P3 = [ 1.5*au, 0, 0 ]
P4 = [ 1.75*au, 0, 0 ]

def Foo(e) :
    return (1+e)/(1-e**2)**0.5
    
V1 = [ 0, 6.283*au/(365.25*86400), 0 ]
V2 = [ 0, 6.283*au/(365.25*86400)/Foo(0.25), 0 ]
V3 = [ 0, 6.283*au/(365.25*86400)/Foo(0.5), 0 ]
V4 = [ 0, 6.283*au/(365.25*86400)/Foo(0.75), 0 ]

C0 = np.concatenate([P1,P2,P3,P4,V1,V2,V3,V4])

# Calcul des dérivées

def Der(Y, t) :
    P = Y.reshape((2*len(M),3))

    res = np.zeros((2*len(M),3))
    res[:len(M)] = P[len(M):]

    for i in range(len(M)) :
        # Calcul de l'accÃ©lÃ©ration
        acc = np.zeros((3,))

        # Attraction solaire
        acc += -G * MS * P[i] / (np.sum(P[i]*P[i])**1.5)

        # Attraction du corps j sur le corps i
        for j in range(len(M)) :
            if i != j :
                acc += -G * M[j] * (P[i]-P[j]) / (sum((P[i]-P[j])**2))**(3/2)

        res[len(M)+i] = acc

    return res.reshape((6*len(M),))

# Simulation

T = np.linspace(0.0, 86400*NbJours, int(NbJours/vitesse))

res = odeint(Der, C0, T)

#-----------------------------------------------------------------------

# Détection utilisation hors Pyzo

if '__iep__' not in globals() :
    matplotlib.interactive(False)

# Animation des résultats

cT, = plt.plot(res[:,0], res[:,1], "b", label="Terre")
cL, = plt.plot(res[:,3], res[:,4], "k", label="Lune")
cM, = plt.plot(res[:,6], res[:,7], "r", label="Mars")
cV, = plt.plot(res[:,9], res[:,10], "g", label="Venus")
pT, = plt.plot(res[-1:,0], res[-1:,1], "bo")
pL, = plt.plot(res[-1:,3], res[-1:,4], "ko")
pM, = plt.plot(res[-1:,6], res[-1:,7], "ro")
pV, = plt.plot(res[-1:,9], res[-1:,10], "go")
plt.plot([0,0], [0,0], "yo", markersize = 20)
plt.xlim(-2e11, 3e11)
plt.axis('equal')
plt.title("Troisième loi de Kepler : même a => même période T")

def SizeChanged(ax, old=[]) :
    current = [ ax.bbox.width, ax.bbox.height ]
    if old != current :
        old[:] = current
        return True
    return False

def Update(i) :
    cT.set_data(np.ma.array(res[:,0], mask=False),
                 np.ma.array(res[:,1], mask=False))
    cL.set_data(np.ma.array(res[:,3], mask=False),
                 np.ma.array(res[:,4], mask=False))
    cM.set_data(np.ma.array(res[:,6], mask=False),
                 np.ma.array(res[:,7], mask=False))
    cV.set_data(np.ma.array(res[:,9], mask=False),
                 np.ma.array(res[:,10], mask=False))
    pT.set_data(res[i:i+1,0], res[i:i+1,1])
    pL.set_data(res[i:i+1,3], res[i:i+1,4])
    pM.set_data(res[i:i+1,6], res[i:i+1,7])
    pV.set_data(res[i:i+1,9], res[i:i+1,10])
    
    for k in 0, 1 :
        cT.get_data()[k][i:] = np.ma.masked
        cL.get_data()[k][i:] = np.ma.masked
        cM.get_data()[k][i:] = np.ma.masked
        cV.get_data()[k][i:] = np.ma.masked
    
    if SizeChanged(plt.gca()) :
        plt.gcf().canvas.draw()
    return [cT,cL,cM,cV,pT,pL,pM,pV]
    
def Init() :
    cT.set_data(np.ma.array(res[:,0], mask=True),
                 np.ma.array(res[:,1], mask=True))
    cL.set_data(np.ma.array(res[:,0], mask=True),
                 np.ma.array(res[:,1], mask=True))
    cM.set_data(np.ma.array(res[:,0], mask=True),
                 np.ma.array(res[:,1], mask=True))
    cV.set_data(np.ma.array(res[:,0], mask=True),
                 np.ma.array(res[:,1], mask=True))
    pT.set_data(np.ma.array(res[-1:,0], mask=True), np.ma.array(res[-1:,1], mask=True))
    pL.set_data(np.ma.array(res[-1:,3], mask=True), np.ma.array(res[-1:,4], mask=True))
    pM.set_data(np.ma.array(res[-1:,6], mask=True), np.ma.array(res[-1:,7], mask=True))
    pV.set_data(np.ma.array(res[-1:,9], mask=True), np.ma.array(res[-1:,10], mask=True))
    
    return [cT,cL,cM,cV,pT,pL,pM,pV]

anim = ani.FuncAnimation(plt.gcf(), Update, frames=len(res),
                         interval=50, blit=True,
                         init_func=Init)

# Détection utilisation hors Pyzo

if '__iep__' not in globals() :
    plt.show()
