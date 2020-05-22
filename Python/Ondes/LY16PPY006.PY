# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 20:09:54 2016

@author: ENS de Lyon

Objectif :  - Tracer les surphaces sur lesquelles les ondes émises par deux sources sont en phase
            - Tracer des coupes de ces surfaces
            
Entrées :   - lam : longueur d'onde des ondes considérées
            - d : distance entre les deux sources
            - N : (2*N-1) surfaces seront tracées (afin d'alléger le calcul, toutes les surfaces ne sont pas tracées)
            - x,y : coordonnées pour lesquelles tracer les surfaces
            - y_coupe : plan dans lequel la coupe des surfaces est faite
            - x_coupe : abscisses pour lesquelles les lignes seront tracées

Sorties :   - figure 1 : surfaces 3D pour lesquelles les ondes émises par les deux sources sont en phase
            - figure 2 : coupe des ces surfaces suivant l'équation y=... (cf y_coupe)
            
"""

import numpy as np# calcul numérique
from mpl_toolkits.mplot3d import Axes3D# 3D
import matplotlib.pyplot as plt# tracé de courbes

plt.close('all')


# TRACÉ DES SURFACES 3D
# Toutes les grandeurs sont u.SI
N = 3
lam = 600e-9#  longueur d'onde
d = 10e-6# distance entre les deux sources
a = np.arange(N)*lam/2# paramètres des coniques
b = np.sqrt((d/2)**2-a**2)# //
x = y = np.linspace(-0.0001,0.0001,20)# coordonnées x,y des surfaces
X,Y = np.meshgrid(x,y)
R = np.sqrt(X**2 + Y**2)# coordonnée polaire

fig = plt.figure(1)
ax = fig.add_subplot(111, projection='3d')
plt.plot([0],[0],[-d/2],'o',color='blue')
plt.plot([0],[0],[d/2],'o',color='blue')
plt.title('Surfaces équiphase')
ax.set_xlabel('x (m)')
ax.set_ylabel('y (m)')
ax.set_zlabel('z (m)')

for i in range(len(a)):# tracé des surfaces
    z = a[i] * np.sqrt( 1 + R**2/b[i]**2 )
    Z = z.reshape(X.shape)
    col = np.random.rand(3,1)
    ax.plot_surface(X,Y,Z, rstride=1, cstride=1, color=col, alpha=0.2)
    ax.plot_surface(X,Y,-Z, rstride=1, cstride=1, color=col, alpha=0.2)
plt.show()

# TRACÉ D'UNE COUPE
N_coupe = 30
a_coupe = np.arange(N_coupe)*lam/2
b_coupe = np.sqrt((d/2)**2-a_coupe**2)
y_coupe = 0# ordonnée de la coupe
x_coupe = np.linspace(-20e-6,20e-6,500)# abscisse de la courbe
r_coupe = np.sqrt(x_coupe**2+y_coupe**2)# coordonnée polaire
plt.figure(2)
plt.plot(0,d/2,'o')
plt.plot(0,-d/2,'o')
for i in range(len(a_coupe)):# tracé des courbes
    z = a_coupe[i] * np.sqrt( 1 + r_coupe**2/b_coupe[i]**2 )
    plt.plot(x_coupe,z,color='blue')
    plt.plot(x_coupe,-z,color='blue')
plt.title('Lignes équiphase dans le plan des sources')
plt.xlabel('z')
plt.ylabel('x')
