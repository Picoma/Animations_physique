# -*- coding: utf-8 -*-

#Auteur : ENS de Lyon promotion 2017-2018
#
#Illustration de l'effet Oberth
#Ce programme illustre l'effet Oberth
#Il trace le delta_v obtenu en fonction de l'impulsion fournie au vaisseau (vimp) et ce pour pluiseurs orbite différentes :
#    -Une orbite autour de la terre à 100 km d'altitude
#    -Une orbite autour de la terre à 1000 km d'altitude
#    -Une orbite autour de la terre à l'altitude des satellites géostationnaires
#    -Une orbite autour de la terre à l'altitude de la Lune
#    -Une orbite autour du soleil avec les mêmes paramètres de que l'orbite de la terre
#
    
import numpy as np
import matplotlib.pyplot as plt

vimp_max=5


#Rayon de l'orbite pour une altitude de 100km
rmin = 6470
#Rayon de l'orbite pour une altitude de 1000km
rmin2 = 7370
#Rayon de l'orbite pour une altitude de "géostationnaire"
rmin3 = 42200
#Rayon de l'orbite pour une altitude de la lune
rmin4 = 386000


#Demi grand-axe de l'obite de Mars
a_mars = 227936637
#Demi grand-axe de l'obite de Saturne
a_saturne = 1429394069
#Demi grand-axe de l'obite la Terre
a_terre = 149597887.5

#Masse du Soleil, de la Terre et constante de gravitation.
msoleil=1.9891*10**30
mterre =5.972 * 10**24
G = 6.674 * 10**(-20)

#Calcul des delta_v pour aller de la Terre à Saturne/Mars avec l'équation de force vive
delta_v_ts = np.sqrt(G*msoleil*(2/a_terre-1/a_saturne)) -  np.sqrt(G*msoleil*(1/a_terre))
delta_v_tm = np.sqrt(G*msoleil*(2/a_terre-1/a_mars)) -  np.sqrt(G*msoleil*(1/a_terre))

#Constante des aires pour les différentes altitudes d'orbite
C = rmin * np.sqrt(2*mterre*G/rmin)
C2 = rmin2 * np.sqrt(2*mterre*G/rmin2)
C3 = rmin3 * np.sqrt(2*mterre*G/rmin3)
C4 = rmin4 * np.sqrt(2*mterre*G/rmin4)

#Masse du satellite
msat = 1
k = msat*mterre*G

#Création de la rampe d'impulsion pour les fits
vimp = np.linspace(0,vimp_max,num=2001)

#Energie autour de la Terre en fonction de l'altitude et de la vitesse.
E = 1./2.*msat*(C/rmin+vimp)**2 - k/rmin
E2 = 1./2.*msat*(C2/rmin2+vimp)**2 - k/rmin2
E3 = 1./2.*msat*(C3/rmin3+vimp)**2 - k/rmin3
E4 = 1./2.*msat*(C4/rmin4+vimp)**2 - k/rmin4

#Vitesse d'éjection de l'orbite autour de la Terre
veject = np.sqrt(2*E/msat)
veject2 = np.sqrt(2*E2/msat)
veject3 = np.sqrt(2*E3/msat)
veject4 = np.sqrt(2*E4/msat)


plt.plot(vimp,veject,lw=2,label="100km")
plt.plot(vimp,veject2,lw=2,label="1000km")
plt.plot(vimp,veject3,lw=2,label="Geostat")
plt.plot(vimp,veject4,lw=2,label="Lune")
plt.plot(vimp,np.linspace(delta_v_tm,delta_v_tm,len(vimp)),"--",lw=2,color="red",label="$\Delta v$ Necessaire pour aller sur Mars")
plt.plot(vimp,np.linspace(delta_v_ts,delta_v_ts,len(vimp)),"--",lw=2,color="green",label="$\Delta v$ Necessaire pour aller sur Saturne")
plt.xlabel("Impulsion appliquee aux vaisseau (km/s)",fontsize=20)
plt.ylabel("$\Delta v$ obtenue par le vaisseau (km/s)",fontsize=20)
plt.plot(vimp,vimp,lw=2,label="Orbite autour du soleil a la meme altitude que la Terre")
plt.legend(loc='upper left')
plt.title("Illustration de l'effet Oberth",fontsize=20)

'''
#Ouvre la figure en plein écran 
figManager = plt.get_current_fig_manager()
figManager.window.showMaximized()
'''

plt.show()
