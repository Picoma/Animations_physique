#!/usr/bin/env python3

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#   (c) 2018 Hamza Dely

"""
    Ce programme affiche la distribution des impacts de photons au cours du temps. Il permet d'illustrer la nature à la fois ondulatoire et corpusculaire de la lumière ou de la matière. Les impacts sont tirés aléatoirement, suivant une distribution de probabilité imposée.
"""

import os

import numpy as np
from matplotlib import pyplot as plt, animation, path, patches

np.random.seed(sum(os.urandom(2)))
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
plt.suptitle("Répartition spatiale des impacts de photons envoyés par une source de photons uniques")

# Longueur d'onde du rayonnement incident (en mètres)
l = 365*10**(-9)

# Distance à l'écran (en mètres)
D = 1

# Espacement entre les fentes d'Young (en mètres)
e = 0.01

# Taille des fentes d'Young (en mètres)
a = 0.0005
b = 0.03

# Interfrange (en mètres)
i = l*D/e

# Taille de l'écran (en mètres)
L = l*D/(2*a)
H = l*D/(2*b)

# Pas de discrétisation de l'espace (en mètres)
dL = L/1000

# Nombre de photons
N = 10**4

# Durée entre 2 impacts (en secondes)
dt = 0.001

# Calcul de la distribution de probabilités des impacts des photons
X = np.linspace(-L/2, L/2, int(L/dL))
Y = (np.sinc(np.pi*a*X/(l*D))*np.cos(np.pi*e*X/(l*D)))**2

# Tirage des impacts de photons
X_photon = np.random.choice(X, size=(N,), p=Y/sum(Y))
Y_photon = (H/2)*(np.random.rand(N) - 0.5)

# Préparation de l'animation et de l'histogramme
ax1.set_ylim(-H/4, H/4)
ax1.set_ylabel("Position Y (m)")
line, = ax1.plot([], [], 'b.')

n, bins = np.histogram(X_photon, int(L/(2*dL)), (-L/2, L/2))

left = np.array(bins[:-1])
right = np.array(bins[1:])
bottom = np.zeros(len(left))
top = bottom + n
nrects = len(left)

nverts = nrects * (1 + 3 + 1)
verts = np.zeros((nverts, 2))
codes = np.ones(nverts, int) * path.Path.LINETO
codes[0::5] = path.Path.MOVETO
codes[4::5] = path.Path.CLOSEPOLY
verts[0::5, 0] = left
verts[0::5, 1] = bottom
verts[1::5, 0] = left
verts[1::5, 1] = top
verts[2::5, 0] = right
verts[2::5, 1] = top
verts[3::5, 0] = right
verts[3::5, 1] = bottom

def init():
    """Données initiales pour les animations"""
    line.set_data([], [])
    line2.set_data([], [])
    return [line, line2]

def animate(i):
    """Joue un pas de l'animation"""
    line.set_data(X_photon[:i], Y_photon[:i])
    n, bins = np.histogram(X_photon[:i], int(L/(2*dL)), (-L/2, L/2))
    top = bottom + n
    verts[1::5, 1] = top
    verts[2::5, 1] = top
    return [line, patch]

barpath = path.Path(verts, codes)
patch = patches.PathPatch(barpath, facecolor='red', edgecolor='black', alpha=0.5)

ax2.grid()
ax2.add_patch(patch)
ax2.set_ylim(bottom.min(), top.max())
ax2.set_xlabel("Position X (m)")
ax2.set_ylabel("Impacts")
line2, = ax2.plot(X, Y, 'r-', lw=2)

# Lancement de l'animation
anim = animation.FuncAnimation(fig, animate, init_func=init, frames=N, interval=dt, repeat=False, blit=True)

plt.show()
