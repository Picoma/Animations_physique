# -*- coding: utf-8 -*-
"""
@author : ENS de Lyon 2017-2018
Ce programme permet de résoudre les équations différentielles décrivant le mouvement de chute libre avec prise en compte de la force de Coriolis.
Les paramètres pouvant varier sont : l'altitude initiale : paramètre altitude (en mètre), et la latitude (en degré).
Les figures représentent :
        - déviation en norme lors de la chute (z = fct(déviation))
        - déviation lors de la chute en fonction du temps selon les axes EST-OUEST et SUD-NORD
        - déviation à la fin de la chute selon les axes EST-OUEST et SUD-NORD en fonction de la latitude pour une altitude donnée   
"""

import numpy as np
import matplotlib
import matplotlib.axes
import matplotlib.pyplot as plt
from scipy.integrate import odeint

#
font = {'family' : 'normal',
        'weight' : 'normal',
        'size'   : 14}

matplotlib.rc('font', **font)

#Définition des constantes
#Durée d'un jour sidéral
jour_sideral = 86164.10
#Durée d'un jour sidéral
omega_terre = 2*np.pi/jour_sideral
#accélération de la pesanteur terrestre
g=9.81
#latitude de l'expérience en degré
Latitude = 45
#conversion de la latitude en radian
lamb = Latitude * np.pi/180
#altitude de chute en mètre
altitude = 200


def dev_est(coord,t,lamb):
    '''renvoie la liste des dérivées premières de x,y,z et des dérivées de seconde pour une chute libre avec force de Coriolis'''
    x,y,z,xp,yp,zp = coord
    dcoorddt=[xp,yp,zp,2*omega_terre *np.sin(lamb)*yp , 2*omega_terre*(np.sin(lamb)*xp+np.cos(lamb)*zp) , -g+2*omega_terre*np.cos(lamb)*yp]
    return(dcoorddt)


#coordonées initiales sous la forme (x0,y0,z0,vx0,vy0,vz0)
coord0 = (0,0,altitude,0,0,0)

#calcul du temps de chute (temps avant d'arriver à z = 0 pour le cas de la chute sans Coriolis)
delta = 4*coord0[2]*g/2
time = (np.sqrt(delta))/g


#temps entre 0 et la fin de la chute
t = np.linspace(0, time, 10001)


#résolution des équations différentielles
#chute avec déviation vers l'est (Coriolis)
sol = odeint(dev_est, coord0, t, args=(lamb,))

#distance au point de chute pour la chute libre avec Coriolis
dist = np.sqrt(sol[:,1]**2+sol[:,0]**2)



#Tracé la déviation lors de la chute.
plt.title("Deviation en fonction de l'altitude lors de la chute")
plt.xlabel("Distance au point de chute sans la force de Coriolis (m)")
plt.ylabel("Altitude (m)")
plt.ticklabel_format(axis='x', style='sci', scilimits=(-2,2))
plt.ticklabel_format(axis='y', style='sci', scilimits=(-2,2))
plt.plot(dist,sol[:,2],"--",linewidth=3)
plt.grid()

#Tracé de la déviation dans le temps, selon les axes Sud-Nord et Est-Ouest
fig, ((ax1, ax2)) = plt.subplots(1, 2)

ax1.plot(t,sol[:,1],"--",linewidth=3,label="y<0 => Est, y>0 => Ouest")
ax1.set_title("Deviation selon l'axe Est-Ouest (altitude de "+str(altitude)+" metres)")
ax1.set_xlabel("Temps (s)", fontsize = 16)
ax1.set_ylabel("Deviation selon l'axe Est-Ouest (m)", fontsize = 16)
ax1.ticklabel_format(axis='y', style='sci', scilimits=(-2,2))
ax1.grid()
ax1.legend()

ax2.plot(t,sol[:,0],"r--",linewidth=3,label="y<0 => Sud, y>0 => Nord")
ax2.set_title("Deviation selon l'axe Sud-Nord (altitude de "+str(altitude)+" metres)")
ax2.set_xlabel("Temps (s)", fontsize = 16)
ax2.set_ylabel("Deviation selon l'axe Sud-Nord (m)",fontsize = 16)
ax2.ticklabel_format(axis='y', style='sci', scilimits=(-2,2))
ax2.grid()
ax2.legend()

#creation des listes de stockage des déviations est-ouest, sud-nord et des latitudes
liste_deo =[]
liste_dsn=[]
liste_latitude= []
#Calcul des déviations est-ouest, sud-nord pour les différentes latitutes (entre 0 et 90 degrés par pas de 5 degrés)
for k in range(0,95,5) :
    liste_latitude.append(k)
    lamb = k*np.pi/180 
    sol = odeint(dev_est, coord0, t, args=(lamb,))
    dsn = sol[10000,0]
    deo = sol[10000,1]    
    liste_deo.append(deo)
    liste_dsn.append(dsn)

fig, ((ax1, ax2)) = plt.subplots(1, 2)

ax1.plot(liste_latitude,liste_deo,"o",linewidth=3)
ax1.set_title("Deviation selon l'axe Est-Ouest (altitude de "+str(altitude)+" metres)")
ax1.set_xlabel("Latitude (degres)", fontsize = 16)
ax1.set_ylabel("Deviation selon l'axe Est-Ouest (m)", fontsize = 16)
ax1.ticklabel_format(axis='y', style='sci', scilimits=(-2,2))
ax1.grid()
ax1.legend()


ax2.plot(liste_latitude,liste_dsn,"o",linewidth=3)
ax2.set_title("Deviation selon l'axe Sud-Nord (altitude de "+str(altitude)+" metres)")
ax2.set_xlabel("Latitude (degres)", fontsize = 16)
ax2.set_ylabel("Deviation selon l'axe Sud-Nord (m)",fontsize = 16)
ax2.ticklabel_format(axis='y', style='sci', scilimits=(-2,2))
ax2.grid()
ax2.legend()

plt.show()
