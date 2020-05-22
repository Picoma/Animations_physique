# -*- coding: utf-8 -*-

"""
Analyse d'un signal par FFT : exemple avec signal "tension" fonction 
du temps et extrait d'un fichier csv
"""

## Importation des bibliotheques
import pylab as plt
import numpy as np
from numpy.fft import fft, fftfreq

## Lectures des données à partir d'un fichier les données sont dans les colonnes 1 et 2 
#(la colonne 0 correspond au numéro de la ligne)
T,U = np.loadtxt("nom_du_fichier.csv", delimiter=';',skiprows=1,usecols=(1,2),unpack=True)

## Tracer des courbes : expérimentales + ajustement + barres d'erreurs

fig, ax = plt.subplots(1)               # cette commande va nous permettre de rajouter du texte
plt.plot(T,U,'ro',label='experimental')      # plot du fit
plt.xlabel('Temps (s)')
plt.ylabel('Tension (V)')
plt.title('Titre à remplacer')
plt.grid(True)                              # quadrille le graphique

plt.legend(loc=2)
plt.show()

## Analyse par FFT
Ne = len(T)      		# nbre de points échantionnés (prendre toujours une puissance de 2)
fe = 1/T[1]        		# fréquence d'échantillonnage du signal
dte = T[1]-T[0]         # durée entre 2 échantillonnnages
ts = Ne*dte     		# durée d'enregistrement du signal

# # exemple d'une fonction dont on veut déterminer la TF
# t = arange(0., ts, dte)
# f = 3       			# fréquence propre du signal
# tau = 10     		# duré d'amortimenent de la sinusoïde
# A = 10
# y = A*sin(2*pi*f*t)+2*A*sin(2*pi*f*2*t)			# somme de 2 sinusoïdes

yf = abs(fft(U))[0:Ne//2]/(Ne/2)   	# spectre en fréquence normalisé
xf = fftfreq(Ne, 1./fe)[0:Ne//2]    # création d'une échelle des fréquences
df = fe/Ne

plt.figure(2)
plt.stem(xf, yf)
plt.xlabel(u"frequence (Hz)")

plt.show()
