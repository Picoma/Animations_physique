#-----------------------------------------------------------------------
# Pouvoir de résolution, critère de Rayleigh
#
# Simulation de deux tâches d'airy dont l'écartement peut être ajusté
# Critère de Rayleigh : séparables si >1.22
# Critère de Sparrow  : séparables si >1.02 
#-----------------------------------------------------------------------
# Renseignements/bugs : Guillaume Dewaele <agreg(at)sci-phy.org>
#-----------------------------------------------------------------------

# Paramètres modifiables

# Fonction pour la tâche (argument = distance au centre)

def Foo(r) :
    return (2*spc.jn(1, 3.14159*r)/(3.14159*r))**2.0

# Colormap pour l'image ("gray", "hot"...)

colormap = "gray"

#-----------------------------------------------------------------------

# Bibliothèques utilisées

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.widgets as mwg
import scipy.special as spc

#-----------------------------------------------------------------------

# Détection utilisation hors Pyzo

if '__iep__' not in globals() :
    matplotlib.interactive(False)

ecart = 0.0

T = np.zeros((150, 75), dtype=float)

axTmp = plt.axes([0.1, 0.2, 0.25, 0.7])
im = axTmp.imshow(T, cmap=colormap, extent=[-1, 1, -2, 2])

axTmp = plt.axes([0.55, 0.2, 0.35, 0.7])
X = np.linspace(-2, 2, 200)
crv1, = axTmp.plot(0*X, X, 'r--')
crv2, = axTmp.plot(0*X, X, 'b--')
crv,  = axTmp.plot(0*X, X, 'k-')
axTmp.set_xlim(0.0, 1.0)
axTmp.set_ylabel(r"x = $\theta D / \lambda$", fontsize=14)

# Slider

axTmp = plt.axes([0.15, 0.04, 0.7, 0.04])
slider = mwg.Slider(axTmp, '', valmin=0.0, valmax=2.0, valinit=1.22)

plt.gcf().text(0.5, 0.095, r"Distance entre les centres des tâches (x = $\theta D / \lambda$)", ha='center', fontsize=14)

def Update(ecart) :
    ecart /= 2
    for i in range(len(T)) :
        for j in range(len(T[0])) :
            x, y = 4*(i/len(T)-0.5), 2*(j/len(T[0])-0.5)
            T[i, j] = 0.5*(Foo(((x+ecart)**2+y**2)**0.5) + Foo(((x-ecart)**2+y**2)**0.5))
    
    im.set_data(T)
    im.autoscale()
    
    crv1.set_data(0.5*Foo((X-ecart)), X)
    crv2.set_data(0.5*Foo((X+ecart)), X)
    crv.set_data(0.5*(Foo((X-ecart))+Foo((X+ecart))), X)

slider.on_changed(Update)

slider.set_val(1.22)

# Détection utilisation hors Pyzo

if '__iep__' not in globals() :
    plt.show()