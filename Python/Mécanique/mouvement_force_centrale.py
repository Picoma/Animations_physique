# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 16:45:29 2017

@author: ENS de Lyon

L'objectif de ce code est de traiter le problème d'un mouvement à force centrale sur la table à coussin d'air dans le cas d'un mobile fixe tandis que l'autre est mis en mouvement, relié par un fil ou un ressort.
Il récupère les données expérimentales et ressort le tracé de l'aire balayée en fonction du temps ainsi qu'une régression affine de la courbe. On affichera alors les paramètres de régression.

Ce script nécessite un fichier externe, 'data.txt', qui doit se trouver dans le même dossier que le code. Celui-ci contient trois colonnes : l'indice des temps, la position en x, et la position en y.
"""

"""
Importation des bibliothèques utiles.
"""


import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize

"""
Importation des données.
"""

dt=0.02 # Pas de temps (s) pour l'acquisition des positions du mobile autoporteur
xcentre=55.526 # Position (cm) selon x du mobile fixe autour duquel se meut l'objet mobile relié par un fil (cas d'une force centrale)
dxcentre=1.116 # Incertitude (cm) selon x sur la position du mobile fixe
ycentre=35.77 # Position (cm) selon y du mobile fixe autour duquel se meut l'objet mobile relié par un fil (cas d'une force centrale)
dycentre=0.582 # Incertitude (cm) selon y sur la position du mobile fixe
data=np.genfromtxt('data.txt') # Importation du tableau de données enregistré dans le document texte 'data.txt', qui doit se trouver dans le même dossier que le code (ce tableau contient la collection des indices des positions, des positions en x et en y (en cm) du mobile)
x=data[:,1]
y=data[:,2]
t=data[:,0]*dt
xprime=x-xcentre # Position réduite du mobile en x
yprime=y-ycentre # Position réduite du mobile en y 
dx=0.02*x # Incertitude de 2% du fait de la parallaxe
dy=0.02*y # Idem 
d=np.sqrt((x-xcentre)**2+(y-ycentre)**2) # Calcul de la distance entre le mobile et l'autre fixe
dd=(1/d)*np.sqrt((dx*(x-xcentre))**2+(dxcentre*(x-xcentre))**2+(dy*(y-ycentre)**2+(dycentre*(y-ycentre))**2)) # Calcul de l'incertitude de la distance entre le mobile et l'autre fixe en utilisant la formule de propagation des incertitudes

"""
Détermination de la vitesse du mobile.
"""

vx=np.gradient(x,dt) # Calcul de la vitesse selon x du mobile en utilisant la commande gradient de numpy : la dérivée se calcule en l'approximant au taux de variation (au 1er ordre sur les bords et au 2nd ordre au centre du tableau)
# Calcul de l'incertitude de la vitesse du mobile selon x en utilisant la formule de propagation des incertitudes : la formule de calcul n'est pas la même sur les bords du tableau et au milieu car la méthode de calcul n'est pas la même
dvx=[(1/dt)*np.sqrt(dx[1]**2+dx[0]**2)] 
dvx+=[1/(2*dt)*np.sqrt(dx[i+1]**2+dx[i-1]**2+4*dx[i]**2) for i in range(1,len(x)-1)]
dvx+=[(1/dt)*np.sqrt(dx[-2]**2+dx[-1]**2)]
dvx=np.array(dvx)
# Idem selon y : calcul de la vitesse et de son incertitude
vy=np.gradient(y,dt)
dvy=[(1/dt)*np.sqrt(dy[1]**2+dy[0]**2)]
dvy+=[1/(2*dt)*np.sqrt(dy[i+1]**2+dy[i-1]**2+4*dy[i]**2) for i in range(1,len(y)-1)]
dvy+=[(1/dt)*np.sqrt(dy[-2]**2+dy[-1]**2)]
dvy=np.array(dvy)
v=np.sqrt(vx**2+vy**2) # Calcul de la norme de la vitesse
dv=(1/v)*np.sqrt((dvx*vx)**2+(dvy*vy)**2) # Calcul de son incertitude, en utilisant la formule de propagation des incertitudes

"""
Calcul de l'aire
"""

A=[] # Initialisation de la liste contenant l'aire balayée par unité de temps
dA=[] # Initialisation de la liste contenant les incertitudes sur l'aire balayée par unité de temps
# Le calcul de l'aire balayée se fait par une boucle : on ajoute à l'aire balayée précédemment (sauf évidemment pour le premier point, voir else) l'aire balayée entre deux points en calculant l'aire du triangle (supposé rectangle) balayée par le mobile. L'incertitude est comme toujours calculée en utilisant la formule de propagation des incertitudes
for i in range(0,len(v)):
    if i>0:
        A+=[A[i-1]+d[i]*v[i]*dt/2]
        dA+=[dA[i-1]+dt/2*d[i]*v[i]*np.sqrt((dd[i]/d[i])**2+(dv[i]/v[i])**2)]
    else:
        A+=[d[i]*v[i]*dt/2]
        dA+=[dt/2*d[i]*v[i]*np.sqrt((dd[i]/d[i])**2+(dv[i]/v[i])**2)]
A=np.array(A) # La liste des aires est transformée en tableau
dA=np.array(dA) # Idem pour la liste des incertitudes des aires 
# On veut montrer que l'aire balayée croit linéairement avec le temps : on va donc effectuer un ajustement de A(t) par une loi linéaire.

"""
Regression linéaire de l'aire en fonction du temps
"""

def lin(x,a,b):
    return a*x+b
popt,pcov=scipy.optimize.curve_fit(lin,t,A) # Ajustement de la loi linéaire aux données expérimentales par la méthode des moindres carrées : en sortie on a deux tableaux, l'un contenant les paramètres optimisés et l'autre la matrice de covariance

"""
Tracé des données expérimentales et de la courbe de modélisation.
"""

fig,ax=plt.subplots() # Création de la figure et des axes
ax.errorbar(t,A,dA,linestyle='none',marker='o',color='crimson',label='Donnees experimentales') # Tracé des données expérimentales avec leurs barres d'erreur
ax.plot(t,popt[0]*t+popt[1],linestyle='-',color='darkgreen',linewidth=2,label='Modelisation') # Tracé de la régression linéaire
ax.set_xlabel('Temps (s)') # Légende sur l'axe des abscisses
ax.set_ylabel('Aire (cm2)') # Légende sur l'axe des ordonnées
ax.legend(loc=0) # Placement de la légende à la meilleure place sur la figure
fig.show() # On montre la figure

"""
Affichage des paramètres d'optimisation et de leurs incertitudes.
"""

