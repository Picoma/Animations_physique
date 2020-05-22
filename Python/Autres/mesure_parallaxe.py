#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: ENS de Lyon

Ce code a pour but de calculer la distance h d'un object par la méthode de parallaxe. On 
place deux goniomètres à une distance L (connue) l'un de l'autre. On mesure les angles alpha 
et beta desquels il faut tourner les goniomètres initialement en regard pour pointer l'objet. 
On calcule également les incertitudes (l'incertitude associée à une grandeur voit son nom
précédé par delta).
"""
 
from math import * # On importe les fonctions necessaires

L = 2.02 # en metre, a modifier
deltaL = 0.02 # en metre, a modifier

alpha =  67.3 #en degres, a modifier
deltaalpha = 4/60 #en degres, a modifier

beta = 80.9 #en degres, a modifier
deltabeta = 4/60 #en degres, a modifier

#On exprime les angles en radians

alpha = alpha * pi / 180 
beta = beta * pi / 180


deltaalpha = deltaalpha * pi / 180 
delatabeta = deltabeta * pi / 180

#Calcul de h

h = L/(1/tan(alpha) + 1/tan(beta))

#Calcul de deltah

deltah = sqrt((deltaL / L) ** 2 \
            + ((deltaalpha / sin(alpha)**2) ** 2 + (deltabeta / sin(beta)**2) ** 2) \
                / (1 / tan(alpha) + 1 / tan(beta)) ** 2)
                
#Renvoie les valeurs                

print(h) # En mètres
print(deltah) # En mètres

