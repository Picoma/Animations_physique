#!/usr/bin/python
# # -*- coding: utf_8 -*-


#--------------------------------------------------------------------------
                       #Période de Borda
#--------------------------------------------------------------------------

#Ce programme permet de trouver la valeur exacte de la période du pendule
#grand angle pour une amplitude donnée grâce au calcul de l'intégrale.
#Il permet également de comparer cette valeur à cette obtenue par la
#formule de Borda, en traçant leur évolution en fonction de l'amplitude.


import numpy as np
import matplotlib.pyplot as plt
import os
from pylab import *
from  scipy  import *
from  scipy.integrate  import  odeint
from scipy.integrate import quad
from math import*


#période propre (pendule de 1m de long environ)
w0 = 4 #rad/s

#Définition de la fonction à intégrer
def T(theta,theta0) :
    return sqrt(2)/w0*(1/sqrt(cos(theta)-cos(theta0)))

#Exemple de calcul pour une amplitude donnéé
amp=20 #en degrés
amprad=0.01745*amp #en radians
integrale, erreur = quad(T,-amprad,amprad,args=(amprad))
print ('T=',round(integrale,2),'secondes')

#Différentes amplitudes 
CI = np.linspace(0.001,1.57,100)
periode=np.zeros(100)

#Intégration donnant la période exacte
for i in range(len(CI)) :
    theta0=CI[i]
    integrale , erreur = quad (T,-theta0,theta0,args=(theta0))
    periode[i]=integrale

#Calcul de la période approchée de Borda
borda=np.zeros(len(CI))
for i in range(len(CI)) :
    borda[i]=2*np.pi/w0*(1+CI[i]**2/16)

#Tracé des périodes en fonction de l'amplitude
plt.figure(figsize=(8,6))
plt.axis((0,90,1.3,2))
plt.plot(57.3*CI,periode,color='red',label='Periode exacte') #on convertit les angles en degrés
plt.plot(57.3*CI,borda,color='blue',label='Periode de Borda') #on convertit les angles en degrés
plt.xlabel(r'$\theta_0$ (deg)', fontsize=20)
plt.ylabel(r'$T_0$ (s)',fontsize=20)
plt.legend(fontsize=20,loc='lower right')
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.savefig('borda.png')
plt.grid()
plt.show()
