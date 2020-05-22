import numpy as np
import matplotlib.pyplot as plt
import scipy.sparse
import scipy.sparse.linalg
import scipy.integrate
import matplotlib.animation as animation

#Cet algorithme calcule la solution de l'équation de Schrodinger
#dépendante du temps avec une condition initiale et un potentiel donné.
#Il a ici été adapté pour illustrer l'effet tunnel a travers une barrière rectangulaire

#Donnees sur l'effet tunnel----------------

largeur_de_barriere = 0.2
hauteur_de_barriere = 50
energie_de_particule_incidente = 10

#Autres donnees-------------------------------------
j = complex(0.,1.)

m = 1
hbar = 1.0

pas_de_quantification = 0.04
x = np.arange(-30,30,step=pas_de_quantification)

nombre_pas_temporels = 500
t_final = 3
t = np.linspace(0,t_final,num=nombre_pas_temporels)

#Hamiltonien cinetique---------------------------------------------------
Hk = np.zeros((3,x.size))
Hk[0,:] = -hbar**2/(2*m*pas_de_quantification**2) * (-2) * np.ones((x.size))
Hk[1,:] = -hbar**2/(2*m*pas_de_quantification**2) * (1) * np.ones((x.size))
Hk[2,:] = Hk[1,:]
Hk = scipy.sparse.dia_matrix((Hk,np.array([0,1,-1])),shape=(x.size,x.size))

"""
Remarque :
Le hamiltonien est stocké sous un format de matrice quasi-diagonale
qui optimise la vitesse du produit H*psi
Si besoin on peut le convertir en matrice complete avec la méthode H.to_array()
"""

#Potentiel----------------------------------------------------------------

def pot(x): #barriere carrée
    hauteur = hauteur_de_barriere
    largeur = largeur_de_barriere

    res = np.zeros((x.size))
    for i in range(x.size):
        if x[i]>0 and x[i]<largeur:
            res[i] = hauteur
    return res


V = scipy.sparse.dia_matrix((pot(x),np.array([0])),shape=(x.size,x.size))


#Equation de Schrodinger-------------------------------------------------

H = Hk + V

def schrodi(psi,t):
    psi_tmp = psi.view(np.complex128)
    Hpsi = -j*H.dot(psi_tmp)/hbar
    return Hpsi.view(np.float64)

"""
Remarque : le solveur odeint de scipy ne pouvant résoudre que des équations réelles,
l'équation est adaptée pour renvoyer séparément les parties réelles et
imaginaires de la fonction d'onde.
Cette manipulation se fait par la méthode .view() des np.ndarray,
celle-ci n'allouant pas de mémoire supplémentaire
"""

#Etat initial de la fontion d'onde----------------------------------------

def paquet_gaussien(x):
    position_initiale = -3
    k = np.sqrt(2*m*energie_de_particule_incidente)/hbar
    largeur = 1.0

    return 1/(np.sqrt(2*np.pi*largeur))*np.exp(-0.5*(x-position_initiale)**2/largeur**2)*np.exp(j*k*x)

psi0 = paquet_gaussien(x)
psi0 = psi0.view(np.float64) #conversion nécéssaire pour le solveur odeint

#Integration par le solveur odeint (tous les calculs se font ici) ------------------

psi = scipy.integrate.odeint(schrodi,psi0,t)

#Renormalisation et calcul des amplitudes de probabilité----------------------

amplitude = [] #tableau pour stocker les amplitudes de probabilité
for i in range(len(t)):
    tmp = psi[i,:].view(np.complex128)
    tmp = abs(tmp)**2
    tmp *= 1/np.linalg.norm(tmp)
    amplitude.append(tmp)

#Affichage et annimation--------------------------------------------------

fig = plt.figure()

plt.plot(x,pot(x),color='b')
line, = plt.plot(x,amplitude[0],color='r')
plt.ylim((0,amplitude[0].max()))
plt.xlabel('x')
plt.ylabel('Amplitude de probabilité de présence')
plt.title('Effet tunnel')

def animate(i):
    line.set_ydata(amplitude[i])

ani = animation.FuncAnimation(fig, animate, range(t.size),interval=40)

plt.show()
