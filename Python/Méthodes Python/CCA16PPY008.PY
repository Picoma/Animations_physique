# Objectif du programme : à partir de l'équation polaire rayon(theta), tracer une fonction de l'angle avec trois paramètres a, b et c...en jouter si nécessaire
# la représentation est polaire
from pylab import *
import matplotlib.pyplot as plt


a=1  #premier paramètre à utiliser si nécessaire
b=0.99 #deuxième paramètre à utiliser si nécessaire
c=0  #troisième paramètre à utiliser si nécessaire
# on peut en ajouter d'autres si nécessaire ou les renomer pour être explicite....

#gestion de la variable x
Plage = 360*pi/180 # plage d'observation choisie pour la variable theta
Nb = 10000 # Nb est le nombre de points calculés
Pasdetheta = Plage/Nb # pas de calcul en theta
theta = np.arange(0, Plage, Pasdetheta) # définition des valeurs de theta

# définition de la fonction de theta à tracer... adaptez à votre problème ainsi que le nom des paramètres s'il a été changé
def fonction(theta):
 return a/(1+b*cos(theta+2*pi/3))

# gestion de l'affichage et création de la fonction à tracer
fig = plt.figure(1)
ax = fig.add_subplot(111, projection='polar')
wave1 = plot(theta, fonction(theta))


plt.show()


