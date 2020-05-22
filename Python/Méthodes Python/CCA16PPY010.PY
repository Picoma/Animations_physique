# Objectif du programme : sur un même graphe, tracer plusieurs fonctions de x avec des paramètres a, b, c...

from pylab import *
a=1  #premier paramètre à utiliser si nécessaire
b=1  #deuxième paramètre à utiliser si nécessaire
c=0  #troisième paramètre à utiliser si nécessaire
d=0  #quatrième paramètre à utiliser si nécessaire
e=0.75  #cinquième paramètre à utiliser si nécessaire
f=0.5  #sixième paramètre à utiliser si nécessaire
g=2  #septième paramètre à utiliser si nécessaire
# on peut en ajouter d'autres si nécessaire ou les renomer pour être explicite....

#gestion de la variable x
Plage = 10 # plage d'observation choisie pour la variable x
Nb = 1000 # Nb est le nombre de points calculés
Pasdex = Plage/Nb # pas de calcul en x
x = np.arange(0, Plage, Pasdex) # définition des valeurs de x

# définition de la plage de représentation en amplitude... la grandeur est représentée sur une plage comprise entre Min et Max
Max =1
Min = -1

# définition de la fonction1 de x à tracer
def fonction1(x):
    return a*cos(2*pi*x/b)+c
    
# définition de la fonction2 de x à tracer
def fonction2(x): # à décommenter si nécessaire
    return c*cos(2*pi*x/b)+c # à décommenter si nécessaire
    
# définition de la fonction3 de x à tracer
def fonction3(x): # à décommenter si nécessaire
    return c*cos(2*pi*x/b)+e # à décommenter si nécessaire
    
# définition de la fonction4 de x à tracer
def fonction4(x): # à décommenter si nécessaire
    return c*cos(2*pi*x/b)+f # à décommenter si nécessaire

# et ajouter d'autre fonctions si nécessaire....

# gestion de l'affichage et création de la fonction à tracer
plt.figure(1)
s1 = fonction1(x) 
s2 = fonction2(x) 
s3 = fonction3(x) 
s4 = fonction4(x) 
# et ajouter d'autre fonctions si nécessaire..

wave1 = plot(x, s1) #tracé en bleu foncé
wave2 = plot(x, s2) #tracé en vert
wave3 = plot(x, s3) #tracé en rouge
wave4 = plot(x, s4) #tracé en bleu clair
# et en tracer d'autres si nécessaire..

plt.grid(b='on',which='both', axis='both', color='blue')
plt.axis()
plt.ylabel('fonctions') #remplacer fonctions par ce que l'on veut pour que ce soit explicite
plt.xlabel('variable x') #remplacer fonction par ce que l'on veut pour que ce soit explicite
plt.show()


