# -*- coding: utf-8 -*-

"""
@author: ENS de Lyon

Ce code montre la dynamique d'une particule libre. La fonction d'onde de
l'état initial est un paquet d'onde gaussien et on visualise l'enveloppe
du paquet d'onde ainsi que sa partie réelle.

Entrées :
    - sigma0 : étalement du paquet d'onde gaussien initial
    - k : nombre d'onde
    - omega : fréquence associée à la dynamique
Sortie : Animation de la partie réelle du paquet d'onde ainsi que de son
enveloppe en fonction du temps.

Référence : Physique Quantique, Michel Le Bellac
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

sigma0 = 3 # étalement du paquet d'onde gaussien à l'instant initial
k = 1 # nombre d'onde (doit être non nul)
omega = 0.5 # fréquence associée à la dynamique


tmax = 30/omega # temps à la fin de l'animation
sigmamax = np.sqrt(sigma0**2+(2*omega*tmax/sigma0)**2)
xmin = min(tmax*omega/k-2*sigmamax/k,-2*sigma0/k) # position minimale sur le graphe
xmax = 2*sigmamax/k+tmax*omega/k # position maximale sur le graphe

# nombres d'images
nframes = 200

positions = np.linspace(xmin,xmax,500) # tableau des positions
times = np.linspace(0,tmax,nframes) # tableau des temps


# Calcul du paquet d'onde à un temps t donné
def paquetdonde(t):
    phi = 1/pow(2*np.pi*sigma0**2,1./4.)/np.sqrt(sigma0**2 + 2j*omega*t)*k  \
        * np.exp(
                1j * k * positions                                          \
                -1./(2.*sigma0**2 + 2j*omega*t)*(k*positions-omega*t)**2)
    return phi

t = 0
phi = paquetdonde(t)
ymax = np.max(np.abs(phi))
ymin = -ymax

# Initialisation de l'animation
def init():
    ax.set_ylim(ymin, ymax)
    ax.set_xlim(xmin, xmax)
    nframe = 0
    line.set_data(positions, np.real(paquetdonde(t)))
    line2.set_data(positions, np.abs(paquetdonde(t)))
    line3.set_data(positions, -np.abs(paquetdonde(t)))
    return line,line2,line3,

fig, ax = plt.subplots()
line, = ax.plot([], [], 'b', lw=2)
line2, = ax.plot([], [], 'g', lw=1)
line3, = ax.plot([], [], 'g', lw=1)
plt.legend(["Partie réelle", "Enveloppe"])

# Mise à jour de l'animation
def update(nframe):
    t = times[nframe]
    nframe = nframe + 1
    line.set_data(positions, np.real(paquetdonde(t)))
    line2.set_data(positions, np.abs(paquetdonde(t)))
    line3.set_data(positions, -np.abs(paquetdonde(t)))
    return line,line2,line3



ani = animation.FuncAnimation(fig, update, nframes,
        interval=20, blit=False, init_func=init)

plt.xlabel(r'$k \cdot x$')
plt.show()
