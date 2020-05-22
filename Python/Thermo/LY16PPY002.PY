# -*- coding: utf-8 -*-
"""
Created on Fri Apr  8 16:48:57 2016

@author: ENS de Lyon

Objectifs : Vérifier les lois de Stefan et de Wien en partant de la loi de Planck

Entrées :   - longueurs_d_onde : tableau des longueurs d'onde pour lesquels calculer la loi de Planck
            - temperatures : tableau des températures pour lesquelles calculer la loi de Planck
            - temperatures2 : tableau des températures pour lesquelles les lois de Stephan et de Wien seront tracées
            
Sorites :   - luminances : tableau des luminances (calculées avec la loi de Planck) pour les longueurs d'onde dans longueur_d_onde et pour les températures dans temperatures.
            - figure 1 : graphe des luminances en fonction de la longueur d'onde et pour différentes températures (cf luminances)
            - lambda_max : tableaux des longueurs d'onde pour lesquelles la luminance est maximale pour chaque température dans temperature calculées grâce à la distribution de Planck
            - lambda_max_wien : tableaux des longueurs d'onde pour lesquelles la luminance est maximale pour chaque température dans temperature2 calculées grâce à la loi de Wien
            - figure 2 : lambda_max et lambda_max_wien en fonction de la température
            - emittance : tableau des émittances pour les températures dans temperature calculées en intégrant la loi de Planck par rapport à la longueur d'onde
            - emittance_stephan : tableau des émittances pour les températures dans temperature2 calculées grâce à la loi de Stephan
            - figure 3 : graphes de emittance et emittance_stephan en fonction de la température

Toutes les grandeurs sont en unité S.I.
"""

import numpy as np# calcul numérique
import matplotlib.pyplot as plt# tracé de courbes
import scipy.constants as cte# constantes physiques

plt.close('all')

longueurs_d_onde = np.arange(1,10000,1)*1e-9# longueur d'onde en m entre 1 et 10000 nm avec un pas de 1 nm

temperatures = [300, 1000, 3000, 4000,5000.]# températures
luminances = np.zeros((len(temperatures),len(longueurs_d_onde)))# luminance en W.m^-2.sr^-1.m^-1

def planck(x,T):
    return 2 * cte.h * cte.c**2 / x**5  *  1 / ( np.exp(cte.h*cte.c/(x*cte.k*T)) - 1 )

plt.figure(1)# tracé dans la 1ere fenètre
for i in range(len(temperatures)):
    luminances[i] = [planck(l,temperatures[i]) for l in longueurs_d_onde]
    plt.plot(1e9*longueurs_d_onde, luminances[i])# la courbe est tracée pour chaque température
plt.legend(temperatures)
plt.title('Loi de Planck')
plt.xlabel('Longueur d\'onde en $nm$')
plt.ylabel('Luminance en $W.m^{-2}.sr^{-1}.m^{-1}$')

lambda_max = np.array([ longueurs_d_onde[luminances[i].argmax()] for i in range(len(temperatures)) ])# longueurs d'onde pour lesquelles la luminance est maximale
temperatures2 = 1.*np.arange(100,10000,10)# températures pour lesquelles la courbe sera tracée (en bleu, d'après l'expression de la loi de Wien)
lambda_max_wien = cte.Wien / temperatures2
plt.figure(2)
plt.plot(temperatures2,1e9 * lambda_max_wien, label='Loi de Wien théorique')
plt.plot(temperatures,1e9 * lambda_max,'o', label='Calcul numérique depuis la loi de Plank')
plt.legend()
plt.xlabel('Température en $K$')
plt.ylabel('Longueur d\'onde du maximum en $nm$')
plt.title('Illustration de la loi de Wien')

dl = longueurs_d_onde[1]-longueurs_d_onde[0]# pas pour la courbe de longueur d'onde
emittance = np.array([ luminances[i].sum()*dl for i in range(len(temperatures)) ]) * np.pi# emittance calculée numériquement à partir de la loi de Plank
emittance_stefan = cte.sigma * temperatures2**4# emittance calculée d'après la loi de Stephan
plt.figure(3)
plt.plot(temperatures2,emittance_stefan, label='Émittance théorique en $W.m^{-2}$')
plt.plot(temperatures,emittance, 'o', label='Calcul numérique depuis la loi de Plank')
plt.legend()
plt.xlabel('Température en $K$')
plt.ylabel('Émittance en $W.m^{-2}$')
plt.title('Illustration de la loi de Stefan')
