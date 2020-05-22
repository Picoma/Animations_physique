# -*- coding: utf-8 -*-
#Auteur : ENS de Lyon promotion 2017-2018
#
#Programme permettant d'afficher les solutions de l'équation de Van der Pol simplifiée sous la forme : y'' - mu*(1-x^2)*x' + x = 0
#Le programme affiche à la fois la solution et le portrait de phase de cette solution et ce pour différents taux de variation d'amplitude initial.
#
#Des boutons permettent de changer la valeur du paramètre mu. Attention cependant les taux de variations initiaux ne sont pas identiques pour les différentes valeurs de mu,
# et ce, pour des raisons de lisibilité (affichage), idem pour la plage temporelle d'intégration.

#Importation des librairies et autre
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib import gridspec
import numpy as np
from matplotlib.widgets import RadioButtons

#Définition de l'équation de Van der Pol
def f(X, t):
    x, dx = X
    return [dx, mu * (1-x * x) * dx - x]

#Définition de la figure
gs = gridspec.GridSpec(2,2,width_ratios=[3,1])

#Définition des sous-figures
ax1 = plt.subplot(gs[0,:])
ax2 = plt.subplot(gs[1,0])
ax3 = plt.subplot(gs[1,1])

#Définition des boutons
radio = RadioButtons(ax3,("mu = -1","mu = 0.001","mu = 1","mu = 10"))



#On calcule les solutions pour les différentes valeurs de mu
    
#######################################################################
##########################    MU = -1   ###############################
#######################################################################
    
#On définit la rampe de temps pour l'intégration
t = np.linspace(0, 15, 512)

#Définition de mu
mu = -1

#On calcule les solutions pour différents taux de variation initiaux
#Ici on affiche aussi les courbes de la fenêtre graphique initiale
Xmum1 = []
for v in [.1, .25, .50, 1]:
    X = odeint(f, [0, v], t)
    Xmum1.append(X)
    ax1.plot(t, X[:, 0],lw=2,label="Taux de variation initial = "+str(v) + " /s")
    ax2.plot(X[:, 0], X[:, 1],lw=2,label="Taux de variation initial = "+str(v) + " /s")

#On enregistre les données importantes pour le fonctionnement des boutons, à savoir :
#La rampe de temps
#Les solutions
#La valeur de mu
#Taux de variations initiaux

tym1 = [t,Xmum1,-1,[.1, .25, .50, 1]]

#######################################################################
#########################    MU = 0.001   #############################
#######################################################################

#On définit la rampe de temps pour l'intégration
t = np.linspace(0, 45, 1024)

#Définition de mu
mu = 0.001

#On calcule les solutions pour différents taux de variation initiaux
Xmu0001 = []
for v in [.50, 1,2.]:
    X = odeint(f, [0, v], t)
    Xmu0001.append(X)

#On enregistre les données importantes pour le fonctionnement des boutons, à savoir :
#La rampe de temps
#Les solutions
#La valeur de mu
#Taux de variations initiaux

ty0001 = [t,Xmu0001,0.001,[.50, 1,2.]]

#######################################################################
##########################    MU = 1   ################################
#######################################################################

#On définit la rampe de temps pour l'intégration
t = np.linspace(0, 30, 512)

#Définition de mu
mu = 1

#On calcule les solutions pour différents taux de variation initiaux
Xmu1 = []
for v in [.001, .01, .1, 1]:
    X = odeint(f, [0, v], t)
    Xmu1.append(X)

#On enregistre les données importantes pour le fonctionnement des boutons, à savoir :
#La rampe de temps
#Les solutions
#La valeur de mu
#Taux de variations initiaux

ty1 = [t,Xmu1,1,[.001, .01, .1, 1]]

#######################################################################
##########################    MU = 10   ###############################
#######################################################################

#On définit la rampe de temps pour l'intégration
t = np.linspace(0, 120, 50000)

#Définition de mu
mu = 10

#On calcule les solutions pour différents taux de variation initiaux
Xmu10 = []
for v in [0.01,9.5,15.]:
    X = odeint(f, [0, v], t)
    Xmu10.append(X)

#On enregistre les données importantes pour le fonctionnement des boutons, à savoir :
#La rampe de temps
#Les solutions
#La valeur de mu
#Taux de variations initiaux

ty10 = [t,Xmu10,10,[0.01,7.5,15.]]

######################################################################
######################################################################
######################################################################

# On commence par tracer une solution.
ax1.set_title("Solutions de l'equation de Van der Pol",fontsize=17)
ax1.set_xlabel("Temps (s)",fontsize=17)
ax1.set_ylabel("Amplitude (1)",fontsize=17)
ax1.grid()
# Et son portrait de phase
ax2.set_title('Portrait de phase',fontsize=17)
ax2.set_xlabel("Amplitude (1)",fontsize=17)
ax2.set_ylabel("Taux de variation d'Amplitude (1/s)",fontsize=17)
ax2.grid()

#on définit la fonction qui va mettre à jour la figure
#cela a l'air complexe mais c'est simplement parce qu'il y a beaucoup de courbes et de figures à mettre à jour
def mufunc(label):
    mudict={"mu = -1":tym1,"mu = 0.001":ty0001,"mu = 1":ty1,"mu = 10":ty10}
    t0,ydata,mu0,v0 = mudict[label]
    ax1.clear()
    ax2.clear()
    for k in range(len(ydata)):
        ax1.plot(t0,ydata[k][:, 0],lw = 2,label="Taux de variation initial = "+str(v0[k]) + " /s")
        ax2.plot(ydata[k][:, 0],ydata[k][:, 1],lw = 2,label="Taux de variation initial = "+str(v0[k]) + " /s")
        plt.draw()
    ax1.set_title("Solutions de l'equation de Van der Pol",fontsize=17)
    ax1.set_xlabel("Temps (s)",fontsize=17)
    ax1.set_ylabel("Amplitude (1)",fontsize=17)
    ax1.grid()
    
    ax2.set_title('Portrait de phase',fontsize=17)
    ax2.set_xlabel("Amplitude (1)",fontsize=17)
    ax2.set_ylabel("Taux de variation d'Amplitude (1/s)",fontsize=17)
    ax2.grid()
    ax1.legend()
#on dit que la mise à jour se fait lorsqu'on clique
radio.on_clicked(mufunc)

#Ouvre la figure en plein écran 
#figManager = plt.get_current_fig_manager()
#figManager.window.showMaximized()

ax1.legend()
plt.show()


