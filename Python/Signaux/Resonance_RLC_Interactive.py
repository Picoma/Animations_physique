# -*- coding: utf-8 -*-

"""
Courbe interactive : exemple de l'influence des différents paramètres d'un 
circuit RLC série sur la bande passante.

On trace i = f(omega) en donnant une valeur initiale de R, C et L et on peut 
suivre l'évolution de la courbe en "bougeant" à l'aide d'un curseur les valeurs 
de R, C et L dans des domaines finis.

A modifier au cas par cas : Le nom et le nombre de variables ; leur domaine de 
variation et leur valeurs initiales ; la formule de la courbe à tracer
"""

## Importation des bibliotheques

import pylab as plt
import numpy as np
from matplotlib.widgets import Slider, Button


## Définition des paramètres fixes initiaux

eo = 5                      # tension maximale du générateur Volt
im = 1                      # unité de io
L0 = 16                     # inductance en milli Henry
C0 = 0.1                    # capacité en micro Farad
R0 = 100                    # résistance en Ohm
Q0 = 1/R0*np.sqrt(L0*1E-3/(C0*1E-6))
print("Q0 =",Q0)            # Affichage du facteur de qualité sur le shell


## Création de la fenêtre

fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.25)         # dimensions du graphique


## Création de la courbe initiale (avec les premières valeurs fixées)

omega = np.arange(1e3, 1e5, 1e1)                    # omega allant de 1000 à 100000 par pas de 10 (abscisse)
io = im/(np.sqrt(1+Q0**2*(omega/(1/np.sqrt(L0*1E-3*C0*1E-6))-1/np.sqrt(L0*1E-3*C0*1E-6)/omega)**2))  # formule de i (ordonnee)

l, = plt.plot(omega, io, lw=2, color='red')         # courbe à tracer i en fonction de omega
plt.axis([1000, 100000, 0, 1])                      # limite des axes (xmin,xmax,ymin,ymax)
plt.xlabel("pulsation (rad/s)")                     # titre de l'axe des abscisses
plt.ylabel("Io/Imax")                               # titre de l'axe des ordonnées
plt.title("Courbe de la résonance en intensité d un RLC série") 
plt.grid(True)                                          # quadrille le graphique


## Ajout des barres de changement de valeur des variables initiales

axcolor = 'lightgoldenrodyellow'                            # couleur des barres
axL = plt.axes([0.25, 0.07, 0.65, 0.03], axisbg=axcolor)    # localisation de la barre pour L
axC = plt.axes([0.25, 0.12, 0.65, 0.03], axisbg=axcolor)    # localisation de la barre pour C
axR = plt.axes([0.25, 0.02, 0.65, 0.03], axisbg=axcolor)    # localisation de la barre pour R

ioL = Slider(axL, 'L (mH)', 10, 100, valinit=L0)            # définition de la barre (localisation, nom, bornes, initiale)
ioC = Slider(axC, 'C (microF)', 0.01, 0.2, valinit=C0)      # prend la valeur indiquée sur la barre
ioR = Slider(axR,'R (ohm)',10,1000,valinit=R0)


## Définition de la fonction qui permet de réinitialiser les valeurs initiales par celle choisie à la barre

def update(val):
    L = ioL.val*1E-3                                        # prend la valeur de la barre pour L (et met en USI)
    C = ioC.val*1E-6
    R = ioR.val
    omegaO = 1/np.sqrt(L*C)                                 # redéfinit la valeur de omega0 et Q en conséquence
    Q = 1/R*np.sqrt(L/C)
    l.set_ydata(im/(np.sqrt(1+Q**2*(omega/omegaO-omegaO/omega)**2)))    # ressort le nousveau profil de résonance
    fig.canvas.draw_idle()                                  # redessine la courbe
    print("Q=",Q, "et omega0=",omegaO,"rad/s")              # affiche sur le côté les valeurs de Q et omega0
ioL.on_changed(update)                                      # affiche à côté de la barre la valeur de L
ioC.on_changed(update)
ioR.on_changed(update)


## Définition d'un bouton reset

resetax = plt.axes([0.03, 0.07, 0.1, 0.04])
button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')

def reset(event):
    ioL.reset()
    ioC.reset()
    ioR.reset()
button.on_clicked(reset)


## Affichage du tout

plt.show()