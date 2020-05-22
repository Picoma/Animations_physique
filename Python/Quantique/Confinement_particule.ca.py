"""
Particule confinée à une dimension.
Résolution par discrétisation de l'espace puis recherche de valeurs propres
 et vecteurs propores de la matrice obtenue.  

Code provenant de :
http://www.f-legrand.fr/scidoc/docimg/sciphys/quantique/confine/confine.html
(licence: https://creativecommons.org/licenses/by-nc-sa/2.0/fr/)

adapté par Grégoire Martouzet - gregoire.martouzet@ens-paris-saclay.fr 
"""

import numpy as np
import scipy.sparse as sparse
import scipy.sparse.linalg as linalg
import matplotlib.pyplot as plt 

""" ----- Paramètres de calcul ----- """
x_min = -1.0 # fenetre de calcul
x_max = 1.0

# Affichage:
#  1 - potentiel
#  2 - fct d'onde
#  3 - fct d'onde et potentiel
#  4 - energie
affichage = 4

N = 1000 # nombre de points (attention: on diagonalise une matrice NxN, pas mettre N trop grand !)

Nb_etats = 4 # nombre d'état que l'on souhaite calculer
# (on peut en principe en calculer N, mais en pratique il faut se limiter au premier pour ne pas avoir n'importe quoi)

periodique = True # indiquer ici si le potentiel est périodique ou non (modifie les conditions au limites)

# Potentiel que l'on souhaite
@np.vectorize
def potentiel_double_puit(x):
	if abs(x)>1.0:
		return 100
	elif abs(x)<0.5:
		return 50
	else:
		return 0

def potentiel_sinus(x):
	# potentiel périodique
	return (np.sin(40*np.pi*x)+1)*0.5*10000
	

# Indiquer ici le potentiel que l'on choisi
#potentiel = potentiel_double_puit
potentiel = potentiel_sinus
             
""" ------ Fonctions pour rechercher les états propres ----- """
# Cas d'un potentiel non périodique
def etats(x,V,nE,tol=0):
	N = V.size
	if x.size!=N:
		raise Exception("tailles de x et V incompatibles")
	alpha = 1.0/(x[1]-x[0])**2
	H = sparse.diags([-alpha/2,V+alpha,-alpha/2],[-1,0,1],shape=(N,N))
	E, phi = linalg.eigs(H,nE,which='SM',tol=tol)
	return np.real(E),phi
	
# Cas d'un potentiel périodique
def etats_periodique(x,V,nE,tol=0):
	N = V.size
	if x.size!=N:
		raise Exception("tailles de x et V incompatibles")
	alpha = 1.0/(x[1]-x[0])**2
	H = sparse.diags([-alpha/2,V+alpha,-alpha/2],[-1,0,1],shape=(N,N))
	H = H.toarray()
	H[0,N-1] = -alpha/2
	H[N-1,0] = -alpha/2
	E, phi = linalg.eigs(H,nE,which='SM',tol=tol)
	return np.real(E),phi

# Normalisation des fonctions d'onde obtenues
def normalize(phi, x):
	i = sum(np.absolute(phi))*(x[1]-x[0])
	return phi/i


# Recherche des états propres
x = np.linspace(x_min, x_max, N)
V = potentiel(x)

# Si potentiel non périodique
if not periodique:
	E, phi = etats(x,V,Nb_etats)
else:
	E, phi = etats_periodique(x,V,int(N/10))
	E = sorted(E)

E = np.array(E)
# Normalisation
for i in range(E.size):
	phi[:,i] = normalize(phi[:,i], x)

# affichage du potentiel
if (affichage == 1) or (affichage == 3):
	plt.plot(x, V, label="V")
	plt.xlabel("$x$")
	plt.ylabel("$V(x)$")

# affichage des fonctions d'onde (décalé en verticale de leur énergie pour plus de visiblité)
if (affichage == 2) or (affichage == 3):
	for i in range(E.size):
		plt.plot(x,np.square(np.absolute(phi[:,i])) + E[i],label="E%d=%f"%(i,E[i]))
	plt.xlabel("$x$")
	plt.ylabel("$|psi|^2$")
	plt.legend(loc='upper right')
	

# affichage des énergie calculées
if affichage==4:
	plt.plot(E,'o')
	plt.xlabel("$n$")
	plt.ylabel("$E_n$")

plt.grid()
plt.show()
