# -*- coding: utf-8 -*-

"""
Filtre RLC et détection synchrone
"""

## Importation des bibliotheques

import pylab as plt
import numpy as np
import scipy
import pandas as pd
from scipy.optimize import curve_fit


## Definition des parametres fixes initiaux (caractéristiques du passe bande RLC)

L = 0.030                   # inductance en Henry
C = 10.5*1E-9                 # capacite en Farad
R = 6*1E3                # resistance en Ohm
Q = 1/R*np.sqrt(L/C)
omega0 = 1/np.sqrt(L*C)
f0 = omega0/(2*np.pi)
print("Q =",Q, 'f0 =', f0)            # Affichage du facteur de qualitÃ© sur le shell


## Creation courbes Gain et Phase théoriques

f = np.arange(1e2, 1e6, 10)  # omega allant de 1000 a  100000 par pas de 10 (abscisse)
omega = f*(2*np.pi)
# G = 1/np.sqrt((1-(omega/omega0)**2)**2+(omega/(Q*omega0))**2)
G = 1/np.sqrt(1+Q**2*(omega/omega0-omega0/omega)**2)

## Caractérisation directe du filtre
# f_mes = np.array([100,1000,2000,3000,4000,5000,10000,100000])
f_mes = np.array([100,1000,2000,3000,4000,5000,6000,7000,8000,9000,10000,11000,15000,20000,25000,30000,40000,50000,100000])
omega_mes = f_mes*(2*np.pi)

# # G_mes = 1/np.sqrt(1+Q**2*(omega_mes/omega0-omega0/omega_mes)**2)
Vcc1 = 2.0
Vcc2 = np.array([0.110,0.780,1.30,1.62,1.82,1.90,2.02,2.04,2.06,2.08,2.06,2.06,2.00,1.9,1.76,1.64,1.38,1.16,0.540])
G_mes = Vcc2/Vcc1

# # Phase_mes = -np.arctan(Q*(omega_mes/omega0-omega0/omega_mes))
Phase_1_2 = np.array([-85,-72,-52,-38,-28,-21,-15,-8,-4,0,3,5,15,25,36,41,54,62,85])
Phase_mes = Phase_1_2/360*(2*np.pi)

def func(x,Q_fit,omega0_fit):
    return 1/np.sqrt(1+Q_fit**2*(x/omega0_fit-omega0_fit/x)**2)
    
p, covm = curve_fit(func, omega_mes, G_mes,[10,10000])
Q_fit,omega0_fit = p
f0_fit = omega0_fit/(2*np.pi)
print("Q fit =",Q_fit, 'f0 fit =', f0_fit)  
G_fit = func(omega, Q_fit,omega0_fit)

## Mesures par détection synchrone
#coefficient multiplieur
K = 0.1
f_mes_sync = np.array([1000,2000,3000,4000,5000,6000,7000,8000,9000,10000,11000,12000,15000,20000,25000,30000,40000,50000])
omega_mes_sync = f_mes_sync*(2*np.pi)

# tension continue par détection synchrone avec signal en phase
V1 = np.array([0.9,7.5,15.9,24.2,31.1,36.4,39.7,41.8,42.2,42.1,41.1,40.1,34.5,25.1,18.0,12.3,5.7,2.0])*10**(-3)
G_cosPhi = (V1*2/K)/(Vcc1/2)
# tension continue par détection synchrone avec signal en dephasage pi/2
V2 = np.array([-5.7,-13.2,-17.2,-17,-15.3,-10.2,-6.8,0.0,1.7,6.1,8.5,16.4,23.4,25.9,27.9,25.4,22.7,19.0])*10**(-3)
G_sinPhi = (V1*2/K)/(Vcc1/2)

Phase_mes_sync = np.arctan(V2/V1)
G_mes_sync = (V1*2/K)/(np.cos(Phase_mes_sync)*(Vcc1/2))


## Mesures en séance

f_mes_seance = np.array([10000,30000])
omega_mes_seance = f_mes_sync*(2*np.pi)
# tension continue par détection synchrone avec signal en phase
V1_seance = np.array([42.10,12.4])*10**(-3)
G_cosPhi_seance = (V1_seance*2/K)/(Vcc1/2)
# tension continue par détection synchrone avec signal en dephasage pi/2
V2_seance = np.array([0.9,20.5])*10**(-3)
G_sinPhi_seance = (V2_seance*2/K)/(Vcc1/2)

Phase_mes_seance = np.arctan(V2_seance/V1_seance)
G_mes_seance = (V1_seance*2/K)/(np.cos(Phase_mes_seance)*(Vcc1/2))

    
p2, covm2 = curve_fit(func, omega_mes_sync, G_mes_sync,[10,10000])
Q_fit_sync,omega0_fit_sync = p2
f0_fit_sync = omega0_fit_sync/(2*np.pi)
print("Q fit_sync =",Q_fit_sync, 'f0 fit_sync =', f0_fit_sync)  
G_fit_sync = func(omega, Q_fit_sync,omega0_fit_sync)




fig, ax = plt.subplots(1)

# #caracteristique filtre theorique
ax.plot(f,20*np.log10(G),label="theo")
# 
#mesure filtre sans bruit
ax.plot(f_mes,20*np.log10(G_mes),'x',label="mesures")
ax.plot(f,20*np.log10(G_fit),label="fit sans bruit")

#mesure sync prepa
ax.plot(f_mes_sync,20*np.log10(G_mes_sync),'x',color='c',label="mesures")
# ax.plot(f,20*np.log10(G_fit_sync),label="fit")
ax.plot(f_mes_seance,20*np.log10(G_mes_seance),'o',color='r',label="mesures")

plt.xscale('log')
plt.xlabel("fréquence")
plt.ylabel("Gain (dB)")




# Phase = -np.arctan((omega/(Q*omega0))/(1-(omega/omega0)**2))

Phase = -np.arctan(Q*(omega/omega0-omega0/omega))
fig2, ax2 = plt.subplots(1)
# ax2.plot(f,Phase,label="theo")
plt.xscale('log')
plt.xlabel("fréquence")
plt.ylabel("déphasage")
ax2.plot(f_mes,Phase_mes,'x',label="mesures")
ax2.plot(f_mes_sync,Phase_mes_sync,'x',label="mesures")
ax2.plot(f_mes_seance,Phase_mes_seance,'o',color='r',label="mesures")



## Affichage du tout

plt.show()