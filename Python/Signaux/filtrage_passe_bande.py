#Auteur : ENS de Lyon promotion 2017-2018
#Modification du programme  "Effet d'un filtrage linéaire passe-bande" pour rajouter des jauge pour modifier le facteur de qualité et la fréquence centrale du filtre.

# On fabrique un signal sinusoïdal d'amplitude A et de fréquence f0 sommé à un bruit gaussien d'écart-type sigma
# Ce signal bruité est passé dans un filtre passe-bande de fréquence centrale fc, de facteur de qualite Q et de gain maximum Go


import matplotlib.pyplot as plt
from pylab import *
# from matplotlib.widgets import Slider, Button, RadioButtons
import numpy as np
import scipy
import scipy.fftpack
from scipy.stats import norm
import matplotlib.widgets as wd

# import math as mt
# import random

fig, ax = plt.subplots()
plt.subplots_adjust(left=0.15, bottom=0.25,hspace=0.4)

# On fixe les paramètres caractéristiques du signal, f0, A et sigma... pour supprimer le bruit, prendre sigma = 0...
A = 1
f0 = 1.
sigma = 1
# On fixe les paramètres utiles du filtre passe bande : la fréquence centrale fc, le facteur de qualité Q, le gain maximum G0
fc = 1
Q = 2
G0 = 1

# On fixe des paramètres utiles au programme
ii = complex(0,1)
prec = 100

# on prépare l'échelle de temps du signal à réaliser
Nper = 20 # nombre de périodes du sinus sur lequel on calcule et que l'on représente
duree = Nper/f0 #durée du signal traité de Nper périodes du signal sinusoïdal
NbPts = 1000 # nombre de points par période
pas = 1./f0/NbPts #on calcule le pas d'échantillonnage
t = np.arange(0, duree, pas) 


# Creation du signal bruité.
s = A*sin(2*pi*f0*t)+sigma*norm.rvs(size=len(t))

# Calcul des paramètres caractéristiques de notre FFT compte tenu des paramètres temporels choisis avant
PasFreq = 1/duree # pas de calcul en fréquence, inverse de la durée temporelle traitée
PlageFreq = 1/(duree/(Nper*NbPts)) # plage fréquentielle sur laquelle on calcule le spectre = moitié de fa fréquence d'échantilonnage
NptsFFT = Nper*NbPts/2+1 # nombre de points sur lequel on calcule la FFT = nombre de points du signal temporel divisé par 2 plus 1.


# Définition de la fonction de transfert du filtre
# On calcule la fonction de transfert entre 0 et PasFreq avec un pas en fréquence de PasFreq
f = np.arange(0, PlageFreq, PasFreq)
# Calcule du module pour l'affichage
Gain = 20*log10(G0*f/sqrt(f*f+(Q*(f*f/fc-fc))**2)+0.000000000001)
# On calcule le gain complexe pour faire ensuite le produit avec la FFT
H = G0*f/(f+ii*Q*((f*f/fc)-(fc)))


# Réalisation du filtrage.
# 1/ On calcule la FFT du signal bruité
FFT = scipy.fft(s)
# 2/ On multiplie cette FFT par la fonction de transfert du filtre
Res = H*FFT
# 3/ On effectue la FFT inverse du produit calculé en 2/
invres = scipy.ifft(Res)
invres = 2*invres.real


# Tracé du graphe du signal bruité en fonction du temps avant filtrage
plt.subplot(311)
wave1, = plt.plot(t,s)
plt.axis([0, duree, -4*A, 4*A])
plt.ylabel("avant filtrage",fontsize=17)
plt.xlabel("Temps (s)",fontsize=17)

# Tracé du module du diagramme de bode du filtre passe bande
# Définition des bornes d'amplitude
GdBMax = 20*log10(G0)+10
GdBMin = 20*log10(G0)-40
# Tracé
plt.subplot(312)
wave2, = plt.semilogx(f, Gain, color='red')
plt.grid(b='on',which='both', axis='both', color='red')
plt.axis([0, PlageFreq, GdBMin, GdBMax])
plt.ylabel('Gain(dB)',fontsize=17)
plt.xlabel('frequence (Hz)',fontsize=17)
plt.grid(b='on',which='both', axis='both', color='blue')

# Tracé du graphe du signal bruité en fonction du temps après filtrage
plt.subplot(313)
wave3, = plt.plot(t, invres)
plt.axis([0, duree, -1.5*A, 1.5*A])
plt.ylabel("apres filtrage",fontsize=17)
plt.xlabel("Temps (s)",fontsize=17)


#Définition du slider et fonction de mise-à-jour du plot
slider_fc = plt.axes([0.2, 0.12, 0.6, 0.03])
f_c = wd.Slider(slider_fc, 'Frequence coupure', 0.000000000001, 20, valinit=fc)

slider_Q = plt.axes([0.2, 0.09, 0.6, 0.03])
Qs = wd.Slider(slider_Q, 'Facteur de qualite', 0.01, 20, valinit=Q)

def update(val):
    log_fc = np.log(f_c.val)
    f_c.valtext.set_text(round(10**(log_fc),2))
    Gain_aju = 20*log10(G0*f/sqrt(f*f+(Qs.val*(f*f/10**(log_fc)-10**(log_fc)))**2)+0.000000000001)
    
    H_aju = G0*f/(f+ii*Qs.val*((f*f/10**(log_fc))-(10**(log_fc))))
    FFT_aju = scipy.fft(s)
    Res_aju = H_aju*FFT_aju
    invres_aju = scipy.ifft(Res_aju)
    invres1_aju = 2*invres_aju.real

    fig.canvas.draw_idle()
    wave2.set_ydata(Gain_aju)
    wave3.set_ydata(invres1_aju)
    
f_c.on_changed(update)
Qs.on_changed(update)

resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
button = wd.Button(resetax, 'Reset', hovercolor='0.975')


def reset(event):
    f_c.reset()
    Qs.reset()
button.on_clicked(reset)

plt.show()

