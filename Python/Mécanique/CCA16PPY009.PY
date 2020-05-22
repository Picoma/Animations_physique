# Objectif du programme : tracer une fonction de x avec trois paramètres a, b et c...

from pylab import *
a=1  #premier paramètre à utiliser si nécessaire
b=1  #deuxième paramètre à utiliser si nécessaire
c=0  #troisième paramètre à utiliser si nécessaire
# on peut en ajouter d'autres si nécessaire ou les renomer pour être explicite....

#gestion de la variable x
Plage = 10 # plage d'observation choisie pour la variable x
Nb = 1000 # Nb est le nombre de points calculés
Pasdex = Plage/Nb # pas de calcul en x
x = np.arange(0, Plage, Pasdex) # définition des valeurs de x

# définition de la plage de représentation en amplitude... la grandeur est représentée sur une plage comprise entre Min et Max
Max =1
Min = -1

# définition de la fonction de x à tracer...adaptez à votre problème ainsi que le nom des paramètres s'il a été modifié
def fonction(x):
    return a*cos(2*pi*x/b)+c



# gestion de l'affichage et création de la fonction à tracer
plt.figure(1)
s = fonction(x) #s1 à t = 0
wave1 = plot(x, s)
plt.grid(b='on',which='both', axis='both', color='blue')
plt.axis([0, Plage, Min, Max])
plt.ylabel('fonction') #remplacer fonction par ce que l'on veut pour que ce soit explicite
plt.xlabel('variable x') #remplacer fonction par ce que l'on veut pour que ce soit explicite
plt.show()


