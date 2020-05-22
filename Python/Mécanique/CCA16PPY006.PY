# Objectif du programme : tracer une fonction de l'espace (ou d'autre chose) qui évolue en fonction du temps avec trois paramètres a, b et c...

from pylab import *
a=1  #premier paramètre à utiliser si nécessaire
b=1  #deuxième paramètre à utiliser si nécessaire
c=1  #troisième paramètre à utiliser si nécessaire
# on peut en ajouter d'autres si nécessaire ou les renomer pour être explicite....

#gestion des paramètres spaciaux
LgOnd =1 #longueur d'onde
Plage = LgOnd*6 # plage d'observation choisie en fonction de la longueur d'onde
PasEspace = LgOnd/100 # pas de calcul en x avec 100 points par longueur d'onde... à modifier si nécessaire
position = np.arange(0, Plage, PasEspace) # définition des valeurs d'espace traitées

#gestion des paramètres temporels
Freq = 0.5 # fréquence temporelle (prendre assez lente pour pouvoir observer)
Tf = 6 # durée de l'évolution de t en secondes
dt = 0.03 # pas de l'évolution de t (prendre une valeur qui n'est pas sous multiple de Tf)
t = np.arange(0, Tf, dt) # définition des valeurs temporelles traitées

# définition de la fonction de l'espace et du temps à traiter : à adapter à ce que l'on veut tracer
def fonction(x,t):
    return a*cos(2*pi*Freq*t-2*pi*x/LgOnd)

# définition de la plage en amplitude... la grandeur est représentée sur une plage comprise entre Min et Max... à adapter à ce que l'on trace
Max =1
Min = -1


# gestion de l'affichage et création de la fonction à propager
plt.figure(1)
s1 = fonction(position, 0) #s1 à t = 0
wave1 = plot(position, s1)[0]
plt.grid(b='on',which='both', axis='both', color='blue')
plt.axis([0, Plage, Min, Max])
plt.ylabel('fonction')#remplacer fonction par ce que l'on veut pour que ce soit explicite
plt.xlabel('position en x')#remplacer par ce que l'on veut en fonction de problème
plt.show()

for temps in t:
    s1 = fonction(position,temps) #on calcule la nouvelle valeur de s1 à t
    wave1.set_ydata(s1) #on actualise le graphe de s1
    plt.pause(dt)



