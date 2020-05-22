"""
Programme permettant de calculer la forme d'une goutte de fluide posée sur une surface superhydrophobe (angle de contact = 180°).

L'idée est de déterminer la position (r,z) de l'interface (r le rayon axi-symétrique et z la hauteur) selon un paramétrage theta défini à partir de l'horizontale.
Les équations sont données par l'égalisation de la pression de Laplace et la pression hydrostatique à l'interface.
Le tout est adimensionné par la longueur capillaire, ce qui rend la solution indépendante du fluide considéré.

Le paramètre theta varie de 0 (plateau horizontal en haut de la goutte) à 180° (angle de contact avec la surface).

Le paramètre à fixer pour modifier la taille est la surpression de laplace
  qui fixe directement la courbure (d'après la loi de Laplace adimensionnée DP*=Courbure*).
Plus la supression est elevée et plus la goutte sera petite (courbure en haut plus importante).
  
Certain point peuvent être important:
	r(90°) = rayon maximal de la goutte
	z(0°) = hauteur de la goutte

Méthode de calcul issue de l'article: SNOEIJER, BRUNET, AND EGGERS; PHYSICAL REVIEW E 79, 036307 (2009)

	Auteur: Grégoire Martouzet, gregoire.martouzet@ens-paris-saclay.fr

	27 mai 2018
"""

import matplotlib.pyplot as plt
from scipy.integrate import odeint
import numpy as np

# La liste suivante permet de choisir les pressions pour lesquelles on trace le profil
liste_pression = [0.1, 1.0, 2.0, 3.0, 10.0]

def calcul(Pt):
	
	# Fonction de dérivation
	def deriv(syst, theta):
		[r, z] = syst # Variables
		
		# Equations différentielles couplées entre r et z, la variable étant theta
		dr = np.cos(theta)/(Pt-z-np.sin(theta)/r)   
		dz = -np.sin(theta)/(Pt-z-np.sin(theta)/r)
		
		return [dr, dz]
	
	# Paramètres d'intégration
	theta_ini = 1/100000
	numsteps = 1000
	theta = np.linspace(theta_ini, np.pi, numsteps)

	# Conditions initiales et résolution
	r0 = 2*theta_ini/Pt
	z0 = -theta_ini/Pt

	# Tableau des conditions initiales
	syst_CI = np.array([r0, z0])
	
	# Résolution numérique des équations différentielles  
	Sols = odeint(deriv, syst_CI, theta)            

	# Récupération des solutions
	# Décomposition du tableau des solutions : Affectation avec transposition
	[r,z] = Sols.T        
	
	return r,z

# Calcul pour chaque pression
for i in liste_pression:
	r,z = calcul(i)
	
	
	z -= min(z)
	
	# On prend aussi le symétrique pour avoir une goutte symétrique
	z = list(z)
	rm = list(-1*r)
	r = list(r)	
	z = z[::-1]+z
	r = rm[::-1]+r
	
	plt.plot(r,z, label='$\Delta P$='+str(i))


# Affichage
plt.axhline(y=0.0, color='k')
plt.axes().set_aspect('equal', 'datalim')
plt.xlabel('$r^*$')
plt.ylabel('$z^*$')
plt.title("Formes de gouttes sur surface hydrophobe") 

plt.legend()
plt.show()
