# -*- coding: utf-8 -*-

"""

Created on Mon May 15 10:48:35 2017



@author: ENS de Lyon

Objectif : Pour l'étude thermique en régime transitoire de la barre de cuivre il est nécessaire de calculer le paramètre
alpha zero (sans dimension) qui est la première solution de l'équation alpha*tan(alpha) = L*h/lambda avec L la longueur de la barre,
h le coefficient de la loi de convection de Newton avec l'air et lambda la conductivité du cuivre.
Pour déterminer alpha zero on trace tan(alpha) et l*h/(lambda*alpha) en fonction de alpha. L'intersection des
deux courbes nous permet de lire graphiquement alpha zero. 
pour prendre en compte l'incertitude que l'on a sur h/lambda, on trace 2 fois l*h/(lambda*alpha), une fois en 
majorant h/lambda par son incertitude et une autre en le minorant. On obtient alors deux alpha zero, un pour 
la majoration et un pour la minoration. La moyenne des deux donne alpha zero et l'écart à la moyenne l'incertitude.

Entrées :
            L : longueur de la barre de cuivre en mètre
            HSurLambda : coefficient h/lambda définit au dessus par mètre (m^-1)
            incertitudeHSurLambda : incertitude sur h/lambda par mètre (m^-1)

Sortie : 
            Graphe permettant la détermination graphique de alpha zero (voir au dessus)
"""

import numpy as np
import matplotlib.pyplot as plt


L = 0.25 #longeur de la barre de cuivre en mètre
HSurLambda = 3.6 #rapport du coefficient h de Newton (pour les échanges thermiques avec l'air) et de la conductivité thermique du cuivre en m-1
incertitudeHSurLambda = 0.4 #incertitude sur le rapport précédent en m-1

alpha = (np.arange(3000)*0.0001)+0.7 #on fait une liste pour de alpha variant entre 0.7 et 1, on sait que le alpha que l'on cherche est compris dedans

tanalpha= np.tan(alpha) #on calcule la tangente de alpha
UnSuralpha1 = L* (HSurLambda+incertitudeHSurLambda)/alpha #on calcule L*h/(lamba*alpha) en majorant h/lambda par son incertitude
UnSuralpha2 = L* (HSurLambda-incertitudeHSurLambda)/alpha #on calcule L*h/(lamba*alpha) en minorant h/lambda par son incertitude

plt.figure()#on crée la figure
plt.clf()
plt.plot(alpha,tanalpha,label='tangente') # on trace la tangente

#on trace ce à quoi doit être égale la tangent en majorant et minorant h/lambda
plt.plot(alpha,UnSuralpha1,label='un sur alpha max')
plt.plot(alpha,UnSuralpha2,label='un sur alpha min')

plt.xlabel('alpha')
plt.title('Determination graphique de alpha zero')
plt.legend()

plt.show()#on affiche il ne rest plus qu'à faire une lecture graphique pour obtenir alpha max et min et donc alpha zero et son incertitude
