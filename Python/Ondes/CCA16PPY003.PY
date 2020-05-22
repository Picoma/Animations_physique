#Ce programme représente la superposition de deux ondes progressives se propageant en sens inverse, la seconde étant le fruit d'une réflexion avec un coefficient de réflexion réel ajustable à l'extérmité droite du système


import matplotlib.pyplot as plt
#import numpy as np
from pylab import *


r=0.5  #rapport d'amplitude entre onde incidente et onde réfléchie prendre < 1, on a choisi un coefficient réel
LgOnd =1 #longueur d'onde
Plage = LgOnd*4 # plage d'observation
PasEspace = LgOnd/100 # pas de calcul en x
x = np.arange(0, Plage, PasEspace)
Freq = 0.5 # fréquence temporelle (prendre assez lente pour pouvoir observer)
Tf = 6 # durée de l'évolution de t en secondes
dt = 0.03 # pas de l'évolution de t (prendre une valeur qui n'est pas sous multiple de Tf)
times = np.arange(0, Tf, dt)

plt.figure(1)
plt.subplot(311)
s1 = cos(-2*pi*x/LgOnd) #s1 à t = 0
wave1 = plot(x, s1)[0]
plt.grid(b='on',which='both', axis='both', color='blue')
plt.axis([0, Plage, -1, 1])
plt.ylabel('incidente')
plt.subplot(312)
s2 = r*cos(2*pi*x/LgOnd) #s2 à t = 0
wave2 = plot(x, s2)[0]
plt.grid(b='on',which='both', axis='both', color='blue')
plt.axis([0, Plage, -1, 1])
plt.ylabel('réfléchie')
plt.subplot(313)
s=s1+s2 #s à t = 0
wave = plot(x, s, color='red')[0]
plt.grid(b='on',which='major', axis='both', color='blue')
plt.axis([0, Plage, -2, 2])
plt.ylabel('incidente+réfléchie')
plt.xlabel('position en x')
plt.show()

for t in times:
    s1 = cos(2*pi*Freq*t-2*pi*x/LgOnd) #on calcule la nouvelle valeur de s1 à t
    wave1.set_ydata(s1) #on actualise le graphe de s1
    s2 = r*cos(2*pi*Freq*t+2*pi*x/LgOnd) #on calcule la nouvelle valeur de s2 à t
    wave2.set_ydata(s2) #on actualise le graphe de s2
    s = s1+s2 #on calcule la nouvelle valeur de s1+s2 à t
    wave = plot(x, s, color='red')
    #wave.set_ydata(s) #on actualise le graphe de s à utiliser si on ne veut voir qu'une courbe à la fois...
    plt.pause(dt)



