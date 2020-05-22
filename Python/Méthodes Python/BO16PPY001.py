# -*- coding: utf-8 -*-

"""
Fichier de Régression linéaire et d'estimation des incertitudes
A modifier pour s'en servir :
- le nom et chemin d'accès au fichier contenant les données
- éventuellement le délimiteur pour la lecture du fichier csv
- Le titre et les légendes des axes (en fin de fichier)
Référence : BUP 928, Incertitudes expérimentales, FX Bally et JM Berroir, p.995
"""

#Importation des bibliotèques
import numpy as np
import pylab as plt
import pandas as pd
from scipy.optimize import curve_fit

# Importations des données de dat.csv (dans le dossier où se trouve le script)
data = pd.read_csv("C:/Users/Utilisateur/SkyDrive/Python/Agreg/dat.csv", delimiter=';')
print(data)
sigma_exp = data['err_Y']

# Définition de la fonction d'ajustement linéaire
def flin(x,a,b):
    return a*x+b

# Ajustement linéaire
nDOF = len(data['X'])
p, covm = curve_fit(flin, data['X'], data['Y'])
a,b = p
yth = flin(data['X'], a, b)
print(a,b)
print(covm[0,0],covm[1,1])
print(np.diag(covm))

# Calcul des tests du chi2
chi2 = sum(((yth - data['Y'])/sigma_exp)**2) # compute the chi-squared
chi2_red = chi2/(nDOF - 2) # divide by no.of DOF
erra, errb = np.sqrt(np.diag(covm)/chi2_red) # correct the error bars
print(erra,errb)

# Résultat de l'ajustement
print("pente = %10.1f +/- %7.1f"  %(a, erra))
print("ordonnée origine = %10.0f +/- %7.0f \n" %(b, errb))
print ("chi2 / NDF = %7.1e" % chi2_red)

# Tracé de la courbe
fig, ax = plt.subplots(1)
# ax.plot(data['X'],data['Y'],'o',label="data")
ax.errorbar(data['X'],data['Y'],yerr=sigma_exp,xerr=data['err_X'],fmt='o',label="data")
ax.plot(data['X'],yth,label="fit")
textstr = "y = a*x + b\n\
a = %.2f +/- %.2f \n\
b = %.2f +/- %.2f \n\
chi2_red = %.1f"  %(a,erra,b,errb,chi2_red)
ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=12, verticalalignment='top')
ax.legend(loc=4)
plt.title(u'Titre du graphique')
plt.xlabel(u'Titre x')
plt.ylabel(u'Titre y')
