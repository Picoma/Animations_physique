###        DIFFRACTION PAR N FENTES       ###
###    DANS L'APPROXIMATION DE FRAUNHOFER ###



# pour les calculs de tableaux :
import numpy as np
# pour le nombre pi :
from math import pi
# pour les graphiques :
import matplotlib.pyplot as plt
# pour l'interactivite du graphique :
from matplotlib.widgets import Slider, Button, RadioButtons


#  cree une figure et une tableau d'abscisses
fig = plt.figure()
ax = fig.add_subplot(111)
plt.subplots_adjust(bottom=0.25)   #  laisse un espace pour les barres interactives
t = np.arange(-1., 1.0, 0.0001)    #  ABSCISSE sur l'ecran (en m)

#parametres initiaux
a0 = 30e-6     #largeur d'une fente [m]
b0 = 50e-6     #espacement entre deux fentes [m]
lambda0=1e-6  #longueur d'one [m]
z0=1.         #distance de l'ecran [m]
N=1           #nombre de fentes

#intensite diffractee :
s = (np.sin(pi*a0*t/(lambda0*z0)) / (pi*t*a0/(lambda0*z0)) *
     np.sin(pi*t*N*b0/(z0*lambda0)) / np.sin(pi*t*b0/(z0*lambda0)) )**2
l, = plt.plot(t,s, lw=2, color='red')

# cree les glissieres pour ajuster a et b
axcolor = 'lightgoldenrodyellow'
axA  = plt.axes([0.25, 0.15, 0.65, 0.03], axisbg=axcolor)
axB = plt.axes([0.25, 0.1, 0.65, 0.03], axisbg=axcolor)

sA = Slider(axA, 'A', 1, 100.0, valinit=a0*1e6)
sB = Slider(axB, 'B', 1, 100.0, valinit=b0*1e6)

# procedure pour actualiser le graphique apr�s modification de a , b ou N :
def update(val):
    global N, z0,lambda0
    a1 = sA.val *1e-6
    b1 = sB.val *1e-6
    l.set_ydata((np.sin(pi*a1*t/(lambda0*z0)) / (np.pi*a1*t/(lambda0*z0)) *
     np.sin(pi*t*N*b1/(z0*lambda0)) / np.sin(pi*t*b1/(z0*lambda0)) )**2        )
    #fig.canvas.draw_idle()
    ax.set_ylim([0, N**2])
    plt.draw()

# rendre les glissieres actives :
sA.on_changed(update)
sB.on_changed(update)

#  creer un bouton reset , pour les glissieres :
resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')
def reset(event):
    sA.reset()
    sB.reset()
button.on_clicked(reset)

# creer deux boutons pour modifier le nombre de fentes :
# on rajoute une fente :
k1ax = plt.axes([0.1, 0.025, 0.1, 0.04])
k1button = Button(k1ax, '+1', color=axcolor, hovercolor='0.975')
def fp1(event):
    global N
    N+=1
    print (N)
    update(sA)
k1button.on_clicked(fp1)

# on enleve une fente :
k2ax = plt.axes([0.2, 0.025, 0.1, 0.04])
k2button = Button(k2ax, '-1', color=axcolor, hovercolor='0.975')
def fm1(event):
    global N
    N-=1
    print (N)
    update(sA)
k2button.on_clicked(fm1)

# afficher le graphe :
plt.show()
