### Étude de l'équilibre de synthèse du trioxyde de soufre ###
'''
Ce programme calcule l'avancement à l'équilibre de la réaction
SO_2 + 1/2 O_2 = SO_3 en fonction des trois paramètres intensifs
que sont la pression totale, le titre molaire en O_2 et la température.
Cet équilibre est en effet caractérisé par une variance égale à 3.
'''

import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as sco
# pour l'interactivite du graphique :
from matplotlib.widgets import Slider, Button, RadioButtons

# Constantes physiques :
R = 8.314 # J/(K.mol)

# Calcul de la constante d'équilibre

def Konstante(T) :
    # Paramètres de la réaction :
    drH0 = -202.6+16.8*0.001*T  # en kJ/mol
    drS0 = -283.5 + 16.8 * np.log(T) # en J/(K.mol)
    
    drG0 = drH0*1000 - T*drS0 # en kJ/mol
    K = np.exp(-drG0/R/T)
    return K

# Calcul du quotient de réaction pour une composition donnée du système
def Quotient(PSO2, PSO3, PO2):
    return PSO3**2/PSO2**2/PO2

# Calcul des bornes de l'avancement min et max 
def ximin(PSO3i):
    return -PSO3i/2

def ximax(PO2i, PSO2i):
    return min(PSO2i/2,PO2i)
    
# Détermination de l'état d'équilibre :
def Avancement(P, T, PSO2i, PSO3i, PO2i):
    PSO2 = lambda x : PSO2i - 2*x           # Pression en SO2 en fonction de l'avancement
    PSO3 = lambda x : PSO3i + 2*x           # Pression en SO3 en fonction de l'avancement
    PO2 = lambda x : PO2i - x               # Pression en O2 en fonction de l'avancement
    f = lambda x : PSO3(x)**2-Konstante(T)*PSO2(x)**2*PO2(x)
    a = ximin(PSO3i)
    b = ximax(PO2i,PSO2i)
    if f(a)*f(b)>=0:
        return ximax, 2*ximax/PSO2i
    else:
        xi = sco.brentq(f,a, b)
        return xi,2*xi/PSO2i

## Création du graphique :

#  cree une figure et une tableau d'abscisses
fig = plt.figure()
ax = fig.add_subplot(111)
plt.subplots_adjust(bottom=0.3)   #  laisse un espace pour les barres interactives


# Paramètres initiaux :

NSO2i = 6.5 # en mol
NSO3i = 0 # en mol
NO2i = 11.5 # en mol
NTi0 = 100 # en mol

T = np.linspace(300,1500,200)
P0 = 1 # en bar
xO20 = 0.115

PSO2i0 = NSO2i/NTi0*P0 # en bar
PSO3i0 = NSO3i/NTi0*P0 # en bar
PO2i0 = NO2i/NTi0*P0 # en bar

Xi = np.ones(np.size(T))
Alpha = np.ones(np.size(T))

for i in np.arange(np.size(T)):
    Xi[i],Alpha[i] = Avancement(P0,T[i],PSO2i0,PSO3i0,PO2i0)

l, = plt.plot(T,Alpha, lw=2, color='red')
ax.set_ylim([0, 1.2])
plt.xlabel("Temperature(K)")
plt.ylabel("Taux de conversion")

# cree les glissieres pour ajuster P et xO2
axcolor = 'lightgoldenrodyellow'

axA  = plt.axes([0.25, 0.15, 0.65, 0.03], axisbg=axcolor)
axB = plt.axes([0.25, 0.1, 0.65, 0.03], axisbg=axcolor)

Curseur_P = Slider(axA, 'P', 0, 70, valinit=P0)
Curseur_xO2 = Slider(axB, 'xO2', 0, 1, valinit=xO20)

# procedure pour actualiser le graphique apr�s modification de xO2 ou P :
def update(val):
    global P, xO2, T
    P = Curseur_P.val
    xO2 = Curseur_xO2.val
    PO2 = xO2*P
    NT = 100+(100*xO2-11.5)/(1-xO2)
    PSO2 = NSO2i/NT*P
    PSO3 = 0

    for i in np.arange(np.size(T)):
        Xi[i],Alpha[i] = Avancement(P,T[i],PSO2,PSO3,PO2)
    l.set_ydata(Alpha)
    #fig.canvas.draw_idle()
    ax.set_ylim([0, 1.2])
    plt.draw()

# rendre les glissieres actives :
Curseur_P.on_changed(update)
Curseur_xO2.on_changed(update)

#  creer un bouton reset , pour les glissieres :
resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')
def reset(event):
    Curseur_P.reset()
    Curseur_xO2.reset()
button.on_clicked(reset)

plt.show()
