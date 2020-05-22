# Ce programme permet d'illustrer la création d'un champ tournant à partir de trois bobinages différents alimentés par des courants triphasés 
# Il permet de tracer quatres courbes en fonction du temps : le champ créé par chaque bobinage à répartition spatiale sinusoïdale alors qu'ils sont décalés de 120° et 
# alimentés par un système de courants sinusoïdaux triphasés, ainsi que la résultante de ces trois champs

import matplotlib.pyplot as plt

from pylab import *

#on choisit le nombre de paires de pôles
p=2  

# on va étudier sur tour du rotor soit 360 degrés avec un pas de calcul de 0,1 degré
plage=360
pas=0.1
x = np.arange(0, plage, pas)

# On fixe la fréquence des courants
Freq = 2 # fréquence assez faible pour que le phénomène soit visible à l'oeil quand t évolue
# On fixe les paramètres de l'évolution temporelle
Tf = 20 # durée de l'évolution de t en secondes
dt = 0.01 # pas de l'évolution de t
times = np.arange(0, Tf, dt) #on va faire évoluer le temps entre 0 et Tf par pas de dt

# On créé une figure à quatre sous-figures.
# Les trois premières sous-figures sont les champs stationnaires supposés radiaux créés par les trois bobinages statoriques, déphasés spatialement de 120 degrés
plt.figure(1)
plt.subplot(411)
s1 = cos(2*p*pi*x/360) #s1 à t = 0
wave1 = plot(x, s1)[0]
plt.grid(b='on',which='both', axis='both', color='blue')
plt.axis([0, plage, -1, 1])
plt.ylabel('H1 (A/m)')
plt.subplot(412)
s2 = cos(-2*pi/3)*cos(2*p*pi*x/360-2*pi/3) #s2 à t = 0
wave2 = plot(x, s2)[0]
plt.grid(b='on',which='both', axis='both', color='blue')
plt.axis([0, plage, -1, 1])
plt.ylabel('H2 (A/m)')
plt.subplot(413)
s3 = cos(-4*pi/3)*np.cos(2*p*pi*x/360-4*pi/3) #s3 à t = 0
wave3 = plot(x, s3)[0]
plt.grid(b='on',which='both', axis='both', color='blue')
plt.axis([0, plage, -1, 1])
plt.ylabel('H3 (A/m)')
plt.subplot(414)
s=s1+s2+s3 #s à t = 0
# la dernière sous-figure représente la somme des trois champs précédents : cette somme n'est plus stationnaire et "glisse" dans l'entrefer
wave = plot(x, s, color='red')[0]
plt.grid(b='on',which='major', axis='both', color='blue')
plt.axis([0, plage, -2, 2])
plt.ylabel('H1+H2+H3')
plt.xlabel('position angulaire (degrés)')
plt.show()


for t in times:
    s1 = cos(2*pi*Freq*t)*cos(2*p*pi*x/360) #on calcule la nouvelle valeur de s1 à t
    wave1.set_ydata(s1) #on actualise le graphe de s1
    s2 = cos(2*pi*Freq*t-2*pi/3)*np.cos(2*p*pi*x/360-2*pi/3) #on calcule la nouvelle valeur de s2 à t
    wave2.set_ydata(s2) #on actualise le graphe de s2
    s3 = cos(2*pi*Freq*t-4*pi/3)*np.cos(2*p*pi*x/360-4*pi/3) #on calcule la nouvelle valeur de s3 à t  
    wave3.set_ydata(s3) #on actualise le graphe de s3
    s = s1+s2+s3
    wave.set_ydata(s) #on actualise le graphe de s
    plt.pause(dt)



