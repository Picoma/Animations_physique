# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 12:12:33 2016

@author: ENS de Lyon

Objectifs :     - intègrer les équations du mouvement pour le problème de Kepler
                - afficher les trajectoires
                - vérifier la loi des aires
                
Entrées :   - m : masse du mobile
            - M : masse de l'astre
            - r0 : distance initiale entre le mobile et l'astre (périgée ou apogée)
            - Em : énergie mécanique totale (convension : l'énergie potentielle est nulle lorsque le mobile est à l'infini)
            - T1 : temps d'intégration
            - dt : pas de temps
            - N : nombre de triangles tracés pour la loi des aires
            
Sorties :   - r : vecteur position en fonction du temps
            - v : vecteur vitesse en fonction du temps
            - A : aire des différents triangles de la loi des aires
            - figure 1 : trajectoire et triangles de la loi des aires
            - erreur : déviation relative de A par rapport à la loi des aires
                
Toutes les grandeurs sont en unités SI
"""

import numpy as np
import scipy.constants as cte
import matplotlib.pyplot as plt


# GRANDEURS DU PROBLEME (UNITES SI)
m = 7.3477e22# masse Lune
M = 5.9722e24# masse Terre
#m = 1.9891e30# masse Soleil
#m = 825.5# masse Sonde Voyager
mu = M*cte.G
r0 = 3.844e8# distance Terre Lune
#r0 = 1.49597870e11# distance Terre Soleil
#v0 = 1e3# vitesse ????

# DEFINITION DE LA VITESSE A PARTIR DE L'ENERGIE
Ep = -mu*m/np.abs(r0)# énergie potentielle
#Em = -np.abs(Ep)/2# énergie mécanique (cercle)
#Em = -np.abs(Ep)/3# (ellipse)
Em = 0# (parabole)
#Em = np.abs(Ep)/2 (hyperbole)
Ec = Em-Ep# énergie cinétique
v0 = np.sqrt(2*Ec/m)# vitesse initiale

# PARAMETRES DE L'INTEGRATION
T1 = 30*24*3600# durée d'intégration
dt = 1*60# pas de temps
r = np.zeros((int(T1/dt), 2))# position aux différents temps
r[0,0] = r0# position initiale
v = np.zeros((int(T1/dt), 2))
v[0,1] = v0# vitesse initiale (orthogonale à r à t=0)

# INTEGRATION DE ÉQUATIONS DU MOUVEMENT
for i in range(len(r)-1):
    dr = dt*v[i]# définition de la vitesse
    dv = -dt*mu/(np.linalg.norm(r[i])**3)*r[i]# PFD
    r[i+1] = r[i]+dr
    v[i+1] = v[i]+dv

# TRACÉ DU RÉSULTAT
plt.plot(0,0,'o')# origine
plt.plot(r[:,0],r[:,1])# trajectoire
plt.axis('scaled')

# TRACÉ LOI DES AIRES
N = 50# nombre de trianges tracés
def aire(p1,p2,p3):# aire d'un triangle en fonction des coordonnées de ses sommets
    u = p2-p1
    v = p3-p1
    uv = np.cross(u,v)# produit vectoriel
    return np.linalg.norm(uv)/2
A = np.zeros(N)# aire des différents triangles
for i in range(N):
    k = (len(r)-1)*i/N
    A[i] = aire(np.array([0,0]),r[k,:],r[k+(len(r)-1)/N,:])
    plt.plot([0,r[k,0]],[0,r[k,1]],color='black')# tracé des triangles
plt.plot([0,r[len(r)-1,0]],[0,r[len(r)-1,1]],color='black')
erreur = (A.max()-A.min())/A.mean()# différence relative entre les aires des triangles
