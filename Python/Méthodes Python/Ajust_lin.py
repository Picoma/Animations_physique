# -*- coding: utf-8 -*-
"""
@author: ENS de Lyon

Objectif :  Faire l'ajustement linéaire d'un jeu de données, en prenant en compte les incertitudes en ordonnées et en abscisses.

Entrées :   - x : données en abscisse
            - ux : incertitudes-types sur l'abscisse
            - y : données en ordonnée
            - uy : incertitudes-types sur l'ordonnée
            
Sorties :   - popt : parametres d'ajustement optimaux
            - uopt : incertitudes-types sur ces parametres
            - Figure donnant les données, la régression linéaire et les paramètres associés

Référence : Physique expérimentale, M. Fruchart, P. Lidon, E. Thibierge, M. Champion, A. Le Diffon
"""
# import des bibliothèques python
import numpy as np
import scipy.optimize as spo
import matplotlib.pyplot as plt

# seuls les donnees experimentales et les labels sont a modifier

# donnees experimentales en mètres
x = np.array([1,2,3,4,5])
y = np.array([1,2,3,4,5])

# incertitudes types en mètres
ux = np.array([0.2,0.2,0.2,0.2,0.2])
uy = np.array([0.2,0.2,0.2,0.2,0.2])

# fonction f decrivant la courbe a ajuster aux donnees
def f(x,p):
	a,b = p
	return a*x+b

# derivee de la fonction f par rapport a la variable x
def Dx_f(x,p):
	a,b = p
	return a

# fonction d'ecart ponderee par les erreurs
def residual(p,y,x):
	return (y-f(x,p))/np.sqrt(uy**2 + (Dx_f(x,p)*ux)**2)

# estimation initiale des parametres
p0 = np.array([0,0])

# moindres carrees non-lineaires
result = spo.leastsq(residual,p0, args=(y,x), full_output=True)

# parametres d'ajustement optimaux
popt = result[0]

# incertitudes-types sur ces parametres
uopt = np.sqrt(np.abs(np.diagonal(result[1])))

# graphique
fig = plt.figure()
ax = fig.add_subplot(111)
ax.tick_params(labelsize=13)

plt.plot(np.linspace(min(x),max(x),100),popt[0]*np.linspace(min(x),max(x),100)+popt[1],linewidth=2,color=[0.8,0,0])
plt.errorbar(x, y, xerr=ux, yerr=uy,fmt='+',capthick=1,linewidth=1.5,ecolor=[0,0.55,0.55],color=[0,0.55,0.55])

# labels
plt.xlabel(r'$h\quad(\mathrm{m})$', fontsize=18)
plt.ylabel(r'$v^{2}\quad(\mathrm{m^{2}\cdot s^{-2}})$', fontsize=18)

# donnees ajustement
plt.text(0.1,0.9,r'$\mathrm{R\'egression\ lin\'eaire}\ :\ f(x) = ax+b$',transform = ax.transAxes)
plt.text(0.1,0.85,r'$a = {0:.2e} \pm {1:.2e}$'.format(popt[0],uopt[0]),transform = ax.transAxes)
plt.text(0.1,0.8,r'$b = {0:.2e} \pm {1:.2e}$'.format(popt[1],uopt[1]),transform = ax.transAxes)

plt.show()



