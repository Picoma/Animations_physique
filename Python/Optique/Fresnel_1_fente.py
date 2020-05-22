###                   DIFFRACTION PAR 1 FENTES                  ###
###    formule de Fresnel , on varie la distance d'oservation Z ###



# pour les calculs de tableaux :
import numpy as np
# pour le nombre pi :
from math import pi
# pour les graphiques :
import matplotlib.pyplot as plt
# pour l'interactivite du graphique :
from matplotlib.widgets import Slider, Button, RadioButtons


#  cree une figure et une tableau d'abscisses
fig = plt.figure()
ax = fig.add_subplot(111)
plt.subplots_adjust(bottom=0.25)


# parametres initiaux 
mu=1e-6        # 1 micron
a0 = 50*mu     # largeur de fente
z0 = 0.001     # postion de l'ecran
lambda0=500e-9 # longueur d'onde
k=2*pi/lambda0 # vecteur d'onde


# nombre de points d'integration sur la fente d'entree par longueur d'onde 
NpL=5
# nombre de points du tableau d'ascisse ( position sur l'ecran)
Nx=500

# fonction calculant la figure de diffraction par integration :
def diff(x,a,z):
    E=np.zeros(len(x))*1j  #creer un tableau d'amplitude comlpexe nulle
    global lambda0,k  # pour garder les valeurs de lambda et k definies en parametres
    xa=np.linspace(-a/2,a/2,int(a/lambda0*NpL))  # tableau du domaine d'integration
    for i in range(len(x)):   # pour chaque x de l'ecran
        for j in range(len(xa)):   # integration sur la largeur de la fente 
            r=np.sqrt(z**2+(x[i]-xa[j])**2)
            E[i]+=z/(1j*lambda0*r**2)*np.exp(-1j*k*r)*(1+1/(1j*k*r))
    return E



#tracer initial :
xM0=3*z0*lambda0/a0+2*a0     # extension approxiamative de la figure de diffraction en z0
#(3 fois la tache du sinc pour le champ lointain + 2 fois la largeur de la fente pour le champ proche)
x0=np.linspace(-xM0,xM0,Nx) #creer le tableau d'abscisses
y=diff(x0,a0,z0)     #calcul de l'amplitude diffractee

l, = plt.plot(x0*1e3,np.abs(y)**2,'.-', lw=2, color='red')   #  tracer de l'intensite
ax.set_xlim([-xM0*1e3,xM0*1e3])   #  re-echelle du plot en [mm]


# creer la glissiere pour controler la distance z de l'ecran
axcolor = 'lightgoldenrodyellow'
axA  = plt.axes([0.25, 0.05, 0.65, 0.03], axisbg=axcolor)
sA = Slider(axA, 'log10( Z [m])', -6, -1, valinit=np.log10(z0)) #glissire logaritmique



# creer la procedure de reactualisation du graphe 
def update(val):
    global lambda0,a0
    z1 = 10**(sA.val)
    print ('Z en mm :' ,  z1*1e3)
    xM=3*z1*lambda0/a0+2*a0
    x1=np.linspace(-xM,xM,Nx)

    y1=diff(x1,a0,z1)
    l.set_ydata(np.abs(y1)**2)
    l.set_xdata(x1*1e3)

    ax.set_ylim([0, max(np.abs(y1)**2)])
    ax.set_xlim([-xM*1e3,xM*1e3])
    plt.draw()
#rendre la gilssiere active :
sA.on_changed(update)


# afficher le graphe :
plt.show()
