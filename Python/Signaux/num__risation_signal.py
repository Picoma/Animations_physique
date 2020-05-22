# Ce programme permet de visualiser les effets (allure, mesure de valeur efficace, bruit de quantification) de la numérisation d'un signal en jouant sur le nombre de bits
# de quantification, la dynamique observée. On peut par ailleurs observer les effets d'un bruit gaussien qui s'ajouterai au signal sur les effets de numérisation.

import matplotlib.pyplot as plt
from pylab import *
from scipy import signal
from scipy.stats import norm    
import numpy as np

# On fixe les paramètres de la sinusoïde à numériser... en changeant la fonction et les paramètres, on peut choisir une autre frome de signal...
Freq = 0.1 #fréquence du sinus observé
Ampli = 1*sqrt(2) # amplitude su sinus observé

# On fixe l'écart-type du bruit gaussien à valeur moyenne nulle (si on choisit d'ajouter un tel bruit)
sigma = 0.1

# On fixe les paramètres d'acquisition : durée d'acquisition, nombre de points
duree = 10 #durée du signal traité
NbPts = 1000 # nombre de points par période
pas = 1/Freq/NbPts #on calcule le pas d'échantillonnage
t = np.arange(0, duree, pas) # on prépare l'échelle de temps du signal à réaliser

# On fixe les paramètres de numérisation en amplitude : nombre de bits, dynamique (plage entres les valeurs extrèmes représentables)
NbBits = 8 # nombre de bits sur lequel on va coder la tension
DynAmpli = 40 # plage d'amplitude sur laquelle on numérise

# On réalise le signal à numériser en fonction des paramètres initialement définis 
s = Ampli*sin(2*pi*Freq*t)
# On réalise un bruit gaussien à valeur moyenne nulle d'écart-type sigma
b = sigma*norm.rvs(size=len(t)) 
# Si on veut un signal sans bruit, commenter entre s et +, si on veut un signal avec du bruit décommenter
signal = s#+b

# Nombre de pas d'histogramme pour le bruit de quantification
NbBins = 20

# on calcule la moyenne du signal et on numérisera par valeur inférieure au-dessus de la moyenne et par valeur supérieure au-dessous    
smoy = mean(signal) 

# Pour numériser :
# On considère le signal auquel on retire sa valeur moyenne
# On applique au signal un coefficient multiplicatif pour que la dymanique maximale nous ramène à un code pris entre -128 et +128
# On ne conserve que la partie entière puis on remet le signal à l'échelle

# On réalise l'opération de numérisation sur le signal (bruité ou non): on prend la partie entière du signal sans sa valeur moiyenne sur la dynamique ramenée entre -128 et 128 puis on repasse sur la bonne échelle d'amplitude.
signalnum = sign(signal-smoy)*floor(sqrt(((signal-smoy)*2**NbBits/DynAmpli)**2))*DynAmpli/2**NbBits+smoy

# On calcule le signal de bruit de quantification
bruitquantif = signal-signalnum

# On calcule la valeur RMS du signal avec et sans effet de quantification en amplitude
sRMS = sqrt(mean(signal**2))
snumRMS = sqrt(mean(signalnum**2))
sbruitquantif = sqrt(mean((signal-signalnum)**2))

# On trace les courbes du signal avant et après numérisation ainsi que le bruit de quantification sur la figure du haut et l'histogramme des valeurs du bruit de quantification sur la figure du bas.        
plt.figure(1)
plt.subplot(211)
plot (t,signal)
plot (t, signalnum)
plot (t, bruitquantif) 
plt.subplot(212)
Min = -DynAmpli/2**NbBits
Max = DynAmpli/2**NbBits
plt.axis([Min, Max, 0, 2*NbPts/NbBins])
plt.hist (bruitquantif, bins=NbBins, range=None) 

# On affiche dans la barre de commande la valeur RMS avant et après numérisation ainsi que la valeur efficace du bruit de quantification (différence entre le signal numérisé et le signal non numérisé)
print ('valeur efficace avant numérisation =', sRMS)
print ('valeur efficace après numérisation =', snumRMS)
print ('valeur efficace du bruit de quantification =', sbruitquantif)

# on affiche les courbes
plt.show()