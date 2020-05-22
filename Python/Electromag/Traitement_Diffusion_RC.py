# -*- coding: utf-8 -*-

"""
Traitement de données : Cas particulier de la diffusion d'un signal dans une 
chaîne de blocs RC 
But : déterminer tau = L²/(pi²D) avec Dth = l²/RC
"""

## Importation des bibliotheques

import pylab as plt
import numpy as np
from scipy.optimize import curve_fit
from numpy import pi


## Remarques générales sur le montage/fichier

# blocs RC : R = 1kOhm & C = 10nF
# longueurs cellule : l = 1,5 cm & totale : L = 15cm
# générateur : carré de 0V à V0 = 10V de 10Hz & rapport cyclique 10% 
# acquisition : 600µs et échantillonnage de 2µs & 25% pré-trig
# fichier : première colonne = temps, deuxième colonne = U(générateur), autres : condensateurs


## Lectures des données à partir d'un fichier & conversions si nécessaires
W = np.loadtxt("diff_RC.csv", delimiter=';',skiprows=1)
T = W[:,0]*1e6   # extraction de la colonne "temps" et conversion en microsecondes
U = W[:,1:] # récupération des tensions aux noeuds du réseau

## Tracé de chaque tension en fonction du temps sur la figure 1

Nc = 9                  # Nombre de cellules                 
plt.figure(1)                
for i in range(0,Nc):   # plot de U(t) pour chaque cellule sur le même graphique
    plt.plot(T,U[:,i],'o')
plt.xlabel('Temps (µs)')
plt.ylabel('Tensions (V)')
plt.title('Diffusion de la tension dans une réseau échelle RC')
plt.legend()
plt.show()

## Changement d'origine temporelle à cause du pré trig

ind = 75         # repérage manuel du moment où il y a la montée du créneau
U = U[ind:,:]   # rescale des tableaux avec la "bonne origine"
T = T[ind:] 

## Décomposition en série de Fourier : on va fitter le tau = RC en théorie et le V0 du créneau

ncf = 200               # nombre de composantes dans la décomposition de Fourier
d=1                     # longueur totale de la chaine (arbitraire tant que X suit)
def F(X,t,tau,V0):      # fonction d'ajustement = série de Fourier (n) où on fit tau et V0 à différents X (cellule RC)
    S = 0               # initialisation de la série de Fourier
    for n in range(1,ncf+1):
        S = S + 1/n*np.exp(-t*n**2/tau)*np.sin(n*pi*X/d)       # somme des coefficients de Fourier
    return V0*(1-X-2/pi*S)                                     # fonction finale qui ajustera les données (pour chaque X)

plt.figure(2)               # tracer sur la figure deux les nouvelles courbes ajustées
tau_L = []              # Liste donnant tous les tau qui seront fittés
V0_L = []
for i in range(1,Nc):   # ajutement pour une tension, puis sur les autres
    Vm = U[:,i]         # pour une tension
    X = i*0.1*d         # Position de la cellule (normalisée par d)
    pop,pcov = curve_fit(lambda t,tau,V0: F(X,t,tau,V0),T,Vm) # ajustement
    tau_op,V0_op = pop      # paramètres optimisés
    tau_L.append(tau_op)    # enregistrement de chaque tau_op fitté pour chaque tension
    V0_L.append(V0_op)
    plt.plot(T,Vm,'b.')
    plt.plot(T,F(X,T,tau_op,V0_op),'r')
plt.xlabel('Temps (µs)')
plt.ylabel('Tensions (V)')
plt.title('Diffusion réseau échelle RC (ajustés)')
plt.legend()
plt.show()

## Calcul du tau moyen et de son écart type à partir des tous les tau fittés

def moyenne(tableau):                               # définition d'une fonction moyenne d'un tableau
    return np.sum(tableau) / len(tableau)

def variance(tableau):                              # définition d'une fonction variance d'un tableau
    m = moyenne(tableau)
    return moyenne([(x-m)**2 for x in tableau])

tau_m = moyenne(tau_L)
delta_tau_m = np.sqrt(variance(tau_L)/Nc)

print('tau = (%.0f +/- %.0f) µs' %(tau_m, delta_tau_m))        # affichage du tau fitté
