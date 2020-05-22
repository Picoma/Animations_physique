# -*- coding: utf-8 -*-
"""
Created on Sun Apr 10 10:04:07 2016

@author: ENS de Lyon

ATTENTION : ce programme est très long à l'exécution, c'est normal car son but est de comparer 2 algorithmes dans leur vitesse de calcul

Dans la suite : FFT = Fast Fourier Transform (algorithme de transformée de Fourier rapide), TF = transformée de Fourier, TFD = transformée de Fourier discrète

Objectif :  - Vérifier que l'algorithme de FFT calcule effectivelent la TFD (PARTIE 1)
            - Comparer le temps de calcul de la TF en utilisant 2 algorithmes : la TFD naïve et la FFT (PARTIE 2)
            - Vérifier que la complexité de la FFT et linéaire et que celle de la TFD naïve est quadratique (PARTIE 3)

Entrées :   - N : Nombre de points pour du tableau de données qui sert de test à l'algorithme de FFT
            - t : Abscisse de la courbe servant de test à la FFT (temps)
            - s : Courbe servant de test à la FFT
            - N2 : Nombes de points sur lesquels comparer les temps de calcul de FFT et TFD naïve
            
Sorties :   - f : Abscisse de la TFD (fréquence)
            - figure 1 : représentation temporelle du signal s(t)
            - figure 2 : graphe de la TFD du signal s en fonction de f calculée par les deux algorithmes
            - console (".... OK :") : le résultat du calcul fait par l'algorithme est-il le même que celui fait par la bibliothèque interne de Python
            - t_FFT : tableau des temps mis par la FFT pour calculer la TFD pour des signaux de taille dans N2
            - t_TFD : tableau des temps mis par TFD naïve pour calculer la TFD pour des signaux de taille dans N2
            - figure 3 : t_FFT et t_TFD en fonction de N2 en échelle log-log
            - console ("... t proportionnel à N^...") : complexité calculée de l'algorithme

Ce programme compare le temps de calcul pour deux algorithmes de calcul de transformée de Fourier discrète (TFD) : la FFT et la TFD naïve.
"""

import numpy as np# calcul numérique
import matplotlib.pyplot as plt# tracé
import time# mesure de temps

plt.close('all')

# PARTIE 1 : TEST DE L'ALGORITHME FFT
N = 1024# nombre de points
t = np.arange(0,N,1)# temps
f = np.fft.fftfreq(N,1)# fréquences
s = np.sin(2*np.pi*0.1*t)# signal dont on veut calculer la TF

plt.figure(1)
plt.plot(t,s,'+-')

def TFD(x):# Algorithme de TFD naïf
    return np.array([ (x*np.exp(-2.*np.pi*1.j*np.arange(len(x))*k/len(x))).sum() for k in range(len(x)) ])
        
def FFT(x):# Algorithme FFT
    if len(x) == 1: 
        return x
    else:
        P = FFT(x[::2])
        I = FFT(x[1::2])
        E = np.exp(-2.*np.pi*1.j*np.arange(len(x))/len(x))
        return np.concatenate([ P + E[:len(x)/2]*I,
                                P + E[len(x)/2:]*I ])

plt.figure(2)
plt.plot(f,np.abs(TFD(s)),label="TFD du signal",color='blue')
plt.plot(f,np.abs(FFT(s)),label="FFT du signal",color='red')
plt.legend()


# PARTIE 2 : COMPARAISON DES TEMPS DE CALCUL
N2 = [2**i for i in [5,6,7,8]]# nombres de points pour lesquels mesurer le temps de calcul
t_TFD = np.zeros(len(N2))# initialisation de tableux des temps de calcul
t_FFT = np.zeros(len(N2))
for i in range(len(N2)):
    s = np.random.random(N2[i])# signal aléatoire pour lequel calculer la TF
    
    t1 = time.time()# chronomètrage de TFD naïf
    y_TFD = TFD(s)
    t2 = time.time()
    t_TFD[i] = t2-t1
    print('TFD %i OK : %s'%(N2[i], str(np.allclose(y_TFD,np.fft.fft(s))) ))# vérification du résultat
    
    t1 = time.time()# chronomètrage de FFT
    y_FFT = FFT(s)
    t2 = time.time()
    t_FFT[i] = t2-t1
    print('FFT %i OK : %s'%(N2[i], str(np.allclose(y_FFT,np.fft.fft(s))) ))# vérification du résultat

# TRACÉ DES TEMPS DE CALCUL EN FONCTION DE LN(N) (ON S'ATTENDS À CE QUE t=a*N^...)
plt.figure(3)
X = np.log10(N2)# log(N)
Y_TFD = np.log10(t_TFD)# log(temps de calcul TFD)
Y_FFT = np.log10(t_FFT)# log(temps de calcul FFT)
plt.plot(X,Y_TFD,'o',color='blue', label='Transformée de Fourier naïve')
plt.plot(X,Y_FFT,'o',color='red', label='Transformée de Fourier rapide')
plt.legend(loc='upper left')


# PARTIE 3 : CALCUL DE LA COMPLEXITE
a_TFD = np.polyfit(X,Y_TFD,1)[0]# régression linéaire
b_TFD = np.polyfit(X,Y_TFD,1)[1]
plt.plot(X,a_TFD*X+b_TFD,color='blue')
a_FFT = np.polyfit(X,Y_FFT,1)[0]
b_FFT = np.polyfit(X,Y_FFT,1)[1]
plt.plot(X,a_FFT*X+b_FFT,color='red')

print('TFD : t proportionnel à N^%f'%a_TFD)
print('FFT : t proportionnel à N^%f'%a_FFT)
