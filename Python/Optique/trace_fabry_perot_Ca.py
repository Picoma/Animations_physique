# Objectif du programme : tracer une fonction de x avec trois paramètres a, b et c...
#ici trace la réponse d'une cavité farby perot en fonction du coefficient de reflexion R choisi

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pylab import *

a=1
b=1


#gestion de la variable x
Plage = 5 # plage d'observation choisie pour la variable x
Nb = 1000 # Nb est le nombre de points calculés
Pasdex = Plage/Nb # pas de calcul en x
x = np.arange(0, Plage, Pasdex) # définition des valeurs de x

# définition de la plage de représentation en amplitude... la grandeur est représentée sur une plage comprise entre Min et Max
Max =1
Min = 0

# définition de la fonction de x à tracer...adaptez à votre problème ainsi que le nom des paramètres s'il a été modifié
def fonction(x,R):
  
 return 1/(1+(2*sqrt(R)/(1-R))**2*sin(pi*x)**2)




# gestion de l'affichage et création de la fonction à tracer
plt.figure(1)
s = fonction(x,0.7) #s1 à t = 0
s2=fonction(x,0.2)
s3=fonction(x,0.99)
wave1 =plt.plot(x, s, color="r")
wave2=plt.plot(x,s2,color="b")
wave3=plt.plot(x,s3,color="g")


#plt.grid(b='on',which='both', axis='both', color='blue')
plt.axis([0, Plage, Min, Max])
plt.title("It/Ii")

plt.ylabel('It/Ii') #remplacer fonction par ce que l'on veut pour que ce soit explicite
plt.xlabel('f/fISL x') #remplacer fonction par ce que l'on veut pour que ce soit explicite

wave1_patch=mpatches.Patch(color="r", label="R=0.7") #legend
wave2_patch=mpatches.Patch(color='b', label='R=0.2')
wave3_patch=mpatches.Patch(color='g', label='R=0.99')
plt.legend([wave1_patch,wave2_patch,wave3_patch],["R=0.7","R=0.2","R=0.99"],loc="upper right")
plt.show()


