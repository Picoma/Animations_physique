# -*- coding: utf-8 -*-

"""

Created on Wed May 17 13:36:34 2017



@author: ENS de Lyon

objectif : tracer le diagramme de Nyquist, de Bode et de H en fonction de f pour le résonateur de Wien. 
Pour cela on fait l'acquisition sur Latis pro de la réponse indicielle et on l'exporte sous forme de txt
avec des ; comme séprateur et des points comme caractère de décimale

Entrée : -le fichier txt 'nyquist.txt' contenant en première colonne le temps et en deuxième le signal. La première ligne 
            contient le nom des colonnes.
         - le temps d'échantillonage de notre acquisition Te en seconde

Ce script nécessite un fichier externe (voir entrée).
"""

import numpy as np
import matplotlib.pyplot as plt


data = np.loadtxt('nyquist.txt',delimiter = ';',skiprows = 1)# on importe les données
Te = 0.0002# on donne le temps d'échantillonage en seconde


temps = data[:,0]# on récupère le temps
signal=data[:,1]# on récupère le signal

TF = 1/np.sqrt(len(signal))*np.fft.fft(signal)# on fait la FFT normalisé

fr =np.fft.fftshift(np.fft.fftfreq(len(temps),Te))# on calcule les fréquence et on les met dans le bon ordre
TF = np.fft.fftshift(TF)#on met les points de la FFT dans le bon odre (ordre croissant des fréquences)
H = [complex(0,1)*2*np.pi*TF[i]*fr[i] for i in range(len(TF))] # on calcule H en multipliant la TF par 2*i*Pi*f


plt.figure()
plt.clf()
plt.plot(fr[len(H)/2:],np.abs(H)[len(H)/2:],'ro-') # on trace le module de H en fonction de f pour les fréquences positives
plt.xlabel('fréquence en Hz')
plt.ylabel('module de H')
plt.title('Fonction de transfert')
plt.show()


ReH = np.real(H)[len(H)/2:]#calcule de la partie réel de H pour les fréquences positives
ImH = np.imag(H)[len(H)/2:]#calcule de la partie imaginaire de H pour les fréquences positives

plt.figure()
#tracé du digramme de nyquist
plt.plot(ReH,ImH,'ro-')
plt.grid()
plt.xlabel('Re(H)')
plt.ylabel('Im(H)')
plt.title('Diagramme de Nyquist')
plt.show()


plt.figure()
#tracé du diagramme de Bode en amplitude pour les fréquences positives
plt.plot(np.log(fr)[len(H)/2:],20*np.log(np.abs(H))[len(H)/2:],'ro-')
plt.xlabel('log(f)')
plt.ylabel('G')
plt.title('Diagramme de Bode')
plt.show()
