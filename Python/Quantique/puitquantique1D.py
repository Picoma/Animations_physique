import numpy as np
import matplotlib.pyplot as plt
import scipy.sparse
import scipy.sparse.linalg
from math import *

#Cet algorithme calcule les solutions stationnaire de l'equation de Schrodinger
#avec un potentiel 1D

"""
Les lignes que peut changer l'utilisateur sont les suivantes :
    -le nombre de pas de quantification et les valeurs extremes de x avec pas_de_quantification, xmin, xmax
    -le nombre de fonctions propres à calcules avec nombre_de_vap
    -le potentiel, en changeant la fonction pot(x)

"""

#Donnees-------------------------------------
m = 1
hbar = 1

nombre_de_vap = 5 #nombre de valeurs d'énergie a calculer

pas_de_quantification = 0.05
xmin = -10
xmax = 10

x = np.arange(xmin,xmax,step=pas_de_quantification)

#Hamiltonien cinetique---------------------------------------------------
Hk = np.zeros((3,x.size))
Hk[0,:] = -hbar**2/(2*m*pas_de_quantification**2) * (-2) * np.ones((x.size))
Hk[1,:] = -hbar**2/(2*m*pas_de_quantification**2) * (1) * np.ones((x.size))
Hk[2,:] = Hk[1,:]
Hk = scipy.sparse.dia_matrix((Hk,np.array([0,1,-1])),shape=(x.size,x.size))

"""
Remarque :
Le hamiltonien est stocké sous un format de matrice quasi-diagonale
qui optimise la vitesse de diagonalisation
Si besoin on peut le convertir en matrice complete avec la méthode H.to_array()
"""

#Potentiel----------------------------------------------------------------

"""
Le potentiel se change ici
"""

def pot(x): #puit_carre
    hauteur = 1.0

    res = np.zeros((x.size))
    for i in range(x.size):
        if x[i]<-5 or x[i]>5:
            res[i] = hauteur
    return res
"""
def pot(x): #puit harmonique
    omega = 1
    return 0.5*m*omega**2*x**2
"""

V = scipy.sparse.dia_matrix((pot(x),np.array([0])),shape=(x.size,x.size))

#Diagonalisation du Hamiltonien---------------------------------------------

H = Hk + V

E, phi = scipy.sparse.linalg.eigsh(H, k=nombre_de_vap, which='SA')

"""
E[k] est la k-ieme valeur propre
phi[:,k] est un array contenant la fonction d'onde du k-ieme etat
"""

phi = phi**2 #si on veut tracer les probabilites de presence
for k in range(nombre_de_vap):
    phi[:,k] *= 1/np.linalg.norm(phi[:,k]) #normalisation

#Affichage du diagramme---------------------------------------------

ylim = E[-1] + 0.5
plt.plot(x,pot(x))
for k in range(nombre_de_vap):
    tmp, = plt.plot(x,phi[:,k]+E[k])
    plt.plot(x,np.ones((x.size))*E[k],color=tmp.get_color(),linestyle='dashed')
plt.ylim((0,ylim))
plt.xlabel('x')
plt.ylabel('Energies')
plt.title("Diagramme d'énergies pour un puit de potentiel 1D")

plt.show()
