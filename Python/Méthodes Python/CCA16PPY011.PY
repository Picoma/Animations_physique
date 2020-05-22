# Objectif du programme : tracer en cartésiennes du lieu défini par x(t) et y(t) avec trois paramètres a, b et c...

from pylab import *
import matplotlib.pyplot as plt


a=1  #premier paramètre à utiliser si nécessaire
b=2 #deuxième paramètre à utiliser si nécessaire
c=0.1  #troisième paramètre à utiliser si nécessaire
# on peut en ajouter d'autres si nécessaire ou les renommer pour être explicite....

#gestion de la variable t
Plage = 100 # plage d'observation choisie pour la variable t
Nb = 10000 # Nb est le nombre de points calculés
Pasdetheta = Plage/Nb # pas de calcul en t
t = np.arange(0, Plage, Pasdetheta) # définition des valeurs de t

# gestion de l'affichage et création des fonctions x(t) et y(t) à tracer
plt.figure(1)
x = a*cos(2*pi*c*t+pi/3) # calcul de l'abscisse
y = b*sin(2*pi*c*t) # calcul de l'ordonnée

# affichage de la courbe paramétrée
wave1 = plot(x, y)
plt.grid(b='on',which='both', axis='both', color='blue')
plt.axis()
plt.show()


