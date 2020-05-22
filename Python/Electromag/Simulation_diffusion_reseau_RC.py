# -*- coding: utf-8 -*-

"""
Simulation d'une diffusion par un réseau RC :
Réponse temporelle à différents points d'un réseau échelle RC à un échelon de 
tension en entrée d'amplitude V0.
La solution théorique est donnée par la série de Fourier : 
(version LaTeX)
$$
V\left(x,t\right)=V_{0}\left(1-\frac{x}{L}\right)
-\frac{2V_{0}}{\pi}\sum_{n\geq1}\frac{1}{n}e^{-n^{2}t/\tau_{1}}\sin\left(\frac{n\pi x}{L}\right)
$$
(ou en version un peu plus lisible)
V(x,t) = V0*(1−x/L)−(2*V0/π)∑(n≥1)1/n*e(−n^2*t/τ1)*sin(nπx/L)
avec τ1=RC
"""

## Importation des bibliotheques
import pylab as plt
import numpy as np
from numpy import pi


t = np.linspace(0.1,100,10000) # création de la variable temps

Nc = 9                  # Nombre de cellules       
V0 = 10                 # tension imposée à l'instant t = 0
ncf = 20                # nombre de composantes dans la décomposition de Fourier
d = 1                     # longueur totale de la chaine (arbitraire tant que X suit)
tau = 30                  # temps donné par le coefficient de diffusion

          
plt.figure(1) 
for i in range(1,Nc): # boucle sur plusieurs x (position des condensateurs)
    x = 0.1*i
    S = 0             # initialisation de la somme pour la série de Fourier
    for n in range(1,ncf+1):
        S = S + 1/n*np.exp(-t*n**2/tau)*np.sin(n*pi*x) # série de Fourier
    U = V0*(1-x-2*S/pi)
    plt.plot(t,U)         # tracer de la courbe pour chaque condensateur

# légende du graphique
plt.xlabel('Temps')
plt.ylabel('Tensions')
plt.title('Diffusion de la tension à plusieurs endroits')
plt.legend()
plt.show()