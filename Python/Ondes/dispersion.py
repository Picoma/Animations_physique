import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft,ifft
import matplotlib.animation as animation
from math import *


#Ce script calcule une animation montrant la propagation d'un paquet d'onde gaussien unidimensionnel pour differentes relations de dispersion.
#Il peut egalement etre adapte a d'autres types de paquet d'onde, mais l'utilisation de la fft rend le repliement de spectre difficilement evitable si la dispersion est trop forte

"""
Les lignes que peut changer l'utilisateur sont les suivantes :
    -la position initiale de l'onde et les valeurs de x pour lesquelles faire le tracer avec le tableau x et position_initiale
    -les valeurs de t pour lesquelles animer avec le tableau t
    -le fait de superposer ou non le tracé avec une onde harmonique avec le booleen tracer_onde_harmonique
    -la fonction frequence(sigma) pour changer la relation de dispersion
    -la condition initiale, contenue dans la variable paquet
    -la vitesse de refraichissement de l'animation en modifiant l'option interval de l'appel à FuncAnimation
"""

#Donnees----------------------------------------------------------------------
j = complex(0.,1.)

x = np.arange(-50,50,step=0.01)
sigma = x.copy() + 50
position_initiale = -30

t = np.arange(0,30,step=0.1)


tracer_onde_harmonique = False #si on veut tracer une onde progressive harmonique en arrière plan pour comparer

#Relation de dispersion-------------------------------------------------------

"""
Changer la relation de dispersion ici
La relation de dispersion est exprimée en fonction de la fréquence et du nombre d'onde
ce sont des variables plus naturelles que la pulsation et le vecteur d'onde au vu des routines de fft utilisées
"""

sigma0 = 2 #frequence spatiale centrale
c = 1 #celerite a sigma0

def frequence(sigma):
    vg = 0.3

    #return sigma*c
    #return sigma0*c + (sigma-sigma0)*vg
    return sigma0*c + (sigma-sigma0)*vg + (sigma-sigma0)**2 * 0.5

#Paquet d'onde----------------------------------------------------------------
def paquet_gaussien(x):
    largeur = 2
    return np.exp(j*2*pi*sigma0*x)*np.exp(-(x-position_initiale)**2/(2*largeur))

paquet = paquet_gaussien(x) #la condition initiale

tf_paquet = np.abs(fft(paquet))

#Propagation------------------------------------------------------------------

#NE PAS MODIFIER CETTE FONCTION, ELLE EST NECESSAIRE AUX CALCULS QUI SUIVENT
def propagation(sigma,tf_paquet,t):
    return ifft(tf_paquet*np.exp(-j*2*pi*frequence(sigma)*t)*np.exp(+j*sigma*position_initiale))

#Calculs----------------------------------------------------------------------
data1 = []
data2 = []
for time in t:
    data1.append(propagation(sigma,tf_paquet,time))
    data2.append(0.2*np.sin(2*np.pi*(sigma0*x-c*sigma0*time)))

#Affichage et animation-------------------------------------------------------

fig = plt.figure()

plt.subplot(211)
plt.plot(sigma,tf_paquet)
plt.xlim((0,10))
plt.xlabel("nombre d'onde $\sigma$")
plt.title('Transformee de fourier spatiale')

plt.subplot(212)
line, = plt.plot(x,paquet)
if tracer_onde_harmonique:
    line2 , = plt.plot(x,data2[0])
plt.xlim((-50,50))
plt.xlabel('x')
plt.title('Espace des positions')

def animate(i):
    line.set_ydata(data1[i])
    if tracer_onde_harmonique:
        line2.set_ydata(data2[i])

ani = animation.FuncAnimation(fig, animate, range(t.size), interval=80) #l'option interval represente la duree entre chaque frame, en ms

plt.show()

