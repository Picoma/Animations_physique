# Objectif du programme : à partir de l'équation polaire rayon(theta), tracer le lieu en cartésiennes avec trois paramètres a, b et c...en jouter si nécessaire
# les repères sont en cartésiennes
from pylab import *
import matplotlib.pyplot as plt


a=1  #premier paramètre à utiliser si nécessaire
b=0.99 #deuxième paramètre à utiliser si nécessaire
c=0  #troisième paramètre à utiliser si nécessaire
# on peut en ajouter d'autres si nécessaire ou les renomer pour être explicite....

#gestion de la variable x
Plage = 360*pi/180 # plage d'observation choisie pour la variable x
Nb = 10000 # Nb est le nombre de points calculés
Pasdetheta = Plage/Nb # pas de calcul en x
theta = np.arange(0, Plage, Pasdetheta) # définition des valeurs de x

# définition de la fonction de theta à tracer... adapter la fonction et éventuellement le nom des paramètres s'il a été modifié
def fonction(theta):
    return a/(1+b*cos(theta+2*pi/3))

# gestion de l'affichage et création de la fonction à tracer
plt.figure(1)
x = fonction(theta)*cos(theta) # calcul de l'abscisse
y = fonction(theta)*sin(theta) # calcul de l'ordonnée
wave1 = plot(x, y)

plt.grid(b='on',which='both', axis='both', color='blue')
plt.axis()
plt.show()


