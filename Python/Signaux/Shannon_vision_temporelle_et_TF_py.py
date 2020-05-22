# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 08:56:19 2015

@author: ENS de Lyon (titre original : Snanon vision temporelle)

2018 : modifié par S.Dorizon prépa agreg Rennes
ajout d'une figure avec le spectre des deux signaux

Objectif : Illustre le théorème de Shanon et le repliement spectral en
comparant un signal réel et un signal acquis.

Entrées :   - f : fréquence du signal à acquérir
            - N : nombre de points du signal à acquérir ()
            - fe : fréquence d'échantillonnage
            - T : durée de l'acquisition
            
Sortie :    - figure 1 : comparaison du signal acquis et du signal à acquérir
            - figure 2 : spectre du signal à acquérir (symétrique par rapport à 0)
            -figure 3 : spectre du signal échantillonné
"""

import numpy as np
import matplotlib.pyplot as plt

f = 100# Fréquence du signal à acquérir
fe = 247# Fréquence d'échantillonage
"""
attention ne pas prendre un rapport entier entre f et fe
choisir par exemple 100 et 133 ou 100 et 247
"""
T = 0.2# Durée de l'acquisition
N=150
N1=fe*T
print(N)

t = np.linspace(0,T,N)# Temps pour le signal à acquérir

Y = np.sin(2*np.pi*f*t)# Signal à acquérir
YTF = np.fft.fftshift(np.fft.fft(Y))
fr= np.fft.fftshift(np.fft.fftfreq(N,T/N))
#YTF=np.fft.fft(Y);

te = np.linspace(0,T,T*fe)# Temps pour le signal acquis
Ye = np.sin(2*np.pi*f*te)# Signal acquis
YeTF= np.fft.fftshift(np.fft.fft(Ye));
frr= np.fft.fftshift(np.fft.fftfreq(int(fe*T),1/(fe)))

plt.subplot(311)
plt.plot(t,Y,label="Signal réel")# Affichage du signal à acquérir
plt.plot(te,Ye,'o-',label="Signal acquis")# Affichage du signal acquis
#plt.plot(te,Ye,label="Signal acquis")# Affichage du signal acquis
plt.legend()
plt.xlabel("Temps (s)")
plt.ylabel("Amplitude du signal")
plt.title("Comparaison du signal réel et du signal acquis")


plt.subplot(312)
plt.plot(fr,abs(YTF)/N,color="blue",label="Signal réel")

#plt.subplot(313)
plt.plot(frr,abs(YeTF)/N1,color="red",label="Signal acquis")
plt.legend()
plt.xlabel("freq (Hz)")
plt.ylabel("Amplitude")
plt.show()