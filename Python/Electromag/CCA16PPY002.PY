# On considère une antenne consituée de deux conducteurs de longueur lamba/4 coaxiaux
# theta = 0 correspond à l'axe défini par les deux conducteurs coaxiaux et r = 0 correspond au centre de symétrie de l'antenne
# puis on place un nombre N d'antennes élémentaires parralèles entre elles et gardant les mêmes repère qu'initialement pour r et theta
# Dans tous les cas, on trace la densité surfacique de puissance rayonnée en fonction de la position angulaire
# les repères sont en polaire
# la courbe bleue représente l'antenne simple.
# la courbe verte représente le réseau d'antennes

from pylab import *
import matplotlib.pyplot as plt

a= 1 # coefficient arbitraire, en W
r= 1 # distance à l'antenne >> longueur d'onde
n = 9 # nombre d'antennes élémentaires
Lambda = 0.001 # longueur d'onde de l'onde émise
d=0.0005 # distance entre deux antennes parralèles

#gestion de la variable x
Plage = 360*pi/180 # plage d'observation choisie pour la variable theta
Nb = 10000 # Nb est le nombre de points calculés
Pasdetheta = Plage/(Nb+1) # pas de calcul en theta (on ajoute 1 pour éviter de tomber sur des angles particuliers qui posent problème... phase, quadrature, etc...
theta = np.arange(Pasdetheta, Plage, Pasdetheta) # définition des valeurs de theta

# densité surfacique de puissance rayonnée pour une seule antenne demi onde : 2L=Lambda/2
# pas de simplification pour cos(pi/2.cos(theta)) 
def fonction(theta):
 return a*1/r**2*(cos(pi/2*cos(theta)))**2/(sin(theta))**2
 
# densité surfacique de puissance rayonnée pour plusieurs antennes parallèles
def fonction2(theta):
 return a*1/r**2*(cos(pi/2*cos(theta)))**2/(sin(theta))**2*abs(sin(n*2*pi*d*sin(theta)/Lambda/2)/sin(2*pi*d*sin(theta)/Lambda/2))

# gestion de l'affichage et création de la fonction à tracer
fig = plt.figure(1)
ax = fig.add_subplot(111, projection='polar')
wave1 = plot(theta, fonction(theta)) # en bleu l'antenne simple
wave2 = plot(theta, fonction2(theta)) # en vert le réseau d'antennes


plt.show()

# Bibliographie : Christian Garing, Ondes électromagnétiques dans le vide et les milieux conducteurs, éditions ellipses


