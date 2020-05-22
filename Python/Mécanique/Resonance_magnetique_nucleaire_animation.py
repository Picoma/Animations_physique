# -*- coding: utf-8 -*-

"""
Animation du 3D où on trace un vecteur en 3D et on affiche à chaque image sa 
position au cours du temps

Cas de la Résonance Magnétique : orientation au cours du temps du spin de la 
particule et des champs magnétiques

Ce que l'on peut changer :
- la fonction donnant l'évolution temporelle des coordonnées des points liés 
par le vecteur (ici Sx, Sy, Sz, etc...)
- Les coordonnées des points fixes du vecteur (dans la fonction Arrow3D en 
fin de programme)
"""

## Importation des bibliothèques

import pylab as plt
import numpy as np
#from mpl_toolkits.mplot3d import *
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d


## Définition des grandeurs autres que le temps

om0=20                          # pulsation de Larmor associée à B0
om1=10                          # pulsation associée à B1
om=20                           # pulsation associée à la rotation de B1

d=om0-om                        # désaccord en fréquence
Om=np.sqrt(om1**2+(om-om0)**2)  # fréquence de la probabilité de transition


## Définition de la fonction flèche (elle n'est pas à changer)
class Arrow3D(FancyArrowPatch):                                         # définition de la fonction flèche en 3D
    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0,0), (0,0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))                 # définition des coordonnées des deux points du vecteur
        FancyArrowPatch.draw(self, renderer)


## Tracer de plusieurs images à des instants t différents

fig = plt.figure()
for t in range(100):   
    plt.clf()                                       # permet d'effacer l'image t pour reboucler à t+1                             # temps qui va défiler (1 pour chaque image)
    ax = fig.gca(projection='3d')                   # On fait une figure 3D
    t = t/100
    Sz=1-2*(om1**2/(Om**2))*(np.sin(Om*t/2))**2        # coordonnées de l'extrémité du vecteur spin suivant z du vecteur à afficher
    Sx=(om1/Om)*((d/2)*np.sin(Om*t/2)*np.sin(Om*t)*np.cos(om*t)+np.sin(om*t)*np.cos(Om*t/2)*np.sin(Om*t/2))
    Sy=(om1/Om)*((d/2)*np.sin(Om*t/2)*np.sin(Om*t)*np.sin(om*t)-np.cos(om*t)*np.cos(Om*t/2)*np.sin(Om*t/2))
    B1x=(1/np.sqrt(2))*np.cos(om*t)                       # coordonnées de l'extrémité du vecteur B1 suivant x
    B1y=(1/np.sqrt(2))*np.sin(om*t)
    S = Arrow3D([0,Sx],[0,Sy],[0,Sz], mutation_scale=10, lw=1, arrowstyle="-|>", color="r",label='spin') 
    ax.add_artist(S)                                # affichage de la flèche à l'instant t allant du point (0,0,0) au point donné par (Sx,Sy,Sz)
    B0 = Arrow3D([0,0],[0,0],[0,1], mutation_scale=10, lw=1, arrowstyle="-|>", color="b",label='Champ B0')
    ax.add_artist(B0)
    B1 = Arrow3D([0,B1x],[0,B1y],[0,0], mutation_scale=10, lw=1, arrowstyle="-|>", color="g",label='Champ B1')
    ax.add_artist(B1)
    plt.xlabel("Axe x (unités arbitraires)")
    plt.ylabel("Axe y (unités arbitraires)")
    # zlabel(" ")
    plt.xlim(-2,2)
    plt.ylim(-2,2)
    plt.title('Précession de Larmor')
    plt.legend()
    plt.show()
    plt.pause(0.001)
    