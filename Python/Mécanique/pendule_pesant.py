# -*- coding: utf-8 -*-
"""
@author: ENS de Lyon

DESCRIPTION

Ce code a pour objectif de traiter les donnees relatives au pendule pesant.
En particulier, il calcul l energie et realise un ajustement dans
l hypothese de frottements fluides. Les donnees sont egalement
moyennees si besoin.

Variable a modifier: fichier est un fichier .txt comprenant 2 colonnes, 
1 pour le tenps, l autre pour la tension proportionnelle a l angle.

En sortie: le graphe de l energie, et la regression exponentielle associee

Ce script nécessite un fichier externe (voir variable à modifier).
"""

"""
PACKAGES
"""

import numpy as n
import matplotlib.pyplot as plt
import scipy.stats as st


"""
DONNEES
"""

""" A MODIFIER"""
fichier = 'pendule.txt'

#etalonnage theta = a * V + b
a = 0.095
b = 0.058

data  = n.loadtxt(fichier, skiprows = 1)
temps = data[:,0]				#le temps
theta = (data[:,1]-b)/a*n.pi/180		#l angle (utiliser la loi issue de l'etalonnage du capteur angulaire)

#Parametres
N     = n.shape(theta)[0]			#la longueur des listes
dt    = 0.012					#le pas de temps, mettre theta[1]-theta[0] si inconnu
m     = 0.15098					#la masse ajoutee a la tige
T0    = 1.13192					#la periode aux petits angles

"""
TRAITEMENTS
"""

#Moyenne glissante sur theta, si necessaire (pas de 5 conseille)
pas = 5
for i in range(pas, N - pas):
     
        theta[i] = sum(theta[i - pas: i + pas])/ (2*pas)
       
#Derivee de theta
theta_point = n.zeros(N)
for i in range(pas + 1,N-1-pas):
    theta_point[i] = (theta[i+1] - theta[i-1])/(2*dt)
    
#calcul de l energie
E = m * (theta_point[pas+1:-1-pas])**2 /2 + m * (2*n.pi/T0)**2 * (1-n.cos(theta[pas+1:-1-pas]))

"""
TRACE
"""

plt.figure()

plt.ylabel('Ln(E)')
plt.xlabel('t (s)')

#Graphe de l energie, en log si voulue
plt.plot(temps[pas+1:-1-pas], n.log(E))

#Regression lineaire dans l hypothese de frottements fluides (decroissance exp)
(a, b, p, c , error_pente) = st.linregress(temps[pas+1:10000], n.log(E[:10000-1-pas]))
plt.plot(temps[pas+1:-1-pas], a*temps[pas+1:-1-pas]+b, color='r')
print("pente = %.4f +- %.4f"%(a, error_pente))

plt.show()
