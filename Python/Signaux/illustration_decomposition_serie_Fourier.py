# -*- coding: utf-8 -*-

'''
Ce programme illustre l'approximation de deux signaux périodiques par leur
décomposition en série de Fourier. L'un des deux signaux est pair, l'autre
impair ; dans chaque cas, seule la série des termes cosinus (resp. des sinus)
est représentée pour ne pas alourdir la figure. Le slider permet de faire
varier l'ordre auquel on souhaite pousser l'approximation.
'''

#import des bibliothèques python
from __future__ import unicode_literals
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, CheckButtons, RadioButtons

# =============================================================================
# --- Defaults values ---------------------------------------------------------
# =============================================================================


"""
Fonctions de définition des coefficients et du signal théorique
"""

def A(n):   # Amplitude du n-ième terme de la série
    return 1.0/n**2  * 4/np.pi**2 * (np.cos(n*np.pi)-1)

def B(n):   # Amplitude du n-ième terme de la série
    return 0

def tr(x):     # Triangle théorique
    pi = np.pi
    u = x % (2*pi)
    if u < pi:
        return u/(pi/2)-1
    else:
        return 3-u/(pi/2)

def cr(x):
    pi = np.pi
    u = abs(x % (2*pi))
    if u < pi:
        return 1
    else:
        return -1

def C(n):
    return 0

def D(n):
    if n%2==0:
        return 0
    return 1./n*4/np.pi

# =============================================================================
# --- Utility functions -------------------------------------------------------
# =============================================================================

def triangle(abscisses,N):
    return [tr(x) for x in abscisses]

def approx_triangle(abscisses,N):
    return [sum([A(n)*np.cos(n*x)+B(n)*np.sin(n*x) for n in range(1,int(N))]) for x in abscisses]   # On somme une à une les composantes jusqu'à N = 1

def creneau(abscisses, N):
    return [cr(x) for x in abscisses]

def approx_creneau(abscisses,N):
    return [sum([C(n)*np.cos(n*x)+D(n)*np.sin(n*x) for n in range(1,int(N))]) for x in abscisses]

N=30
choix=0 #0 pour triangle, 1 pour creneau

# =============================================================================
# --- Creation de la figure ---------------------------------------------------
# =============================================================================

fig,ax=plt.subplots()
plt.subplots_adjust(bottom=0.25)

fig1 = plt.subplot(121)
abscisses = np.arange(-5, 5, 0.01)
plt.title('Fonction (rouge) et approximation (bleu)')
plt.axis([abscisses[0], abscisses[-1], -2, 2])

# Creation de la trace de la fonction s en fonction de abscisses.

PLOTS = {}
PLOTS['Triangle'] = plt.plot(abscisses, triangle(abscisses, 1),
                             lw=2, color='red')[0]
PLOTS['AT'] = plt.plot(abscisses, approx_triangle(abscisses, 1),
                             lw=1, ls='-', color='blue')[0]

PLOTS['Creneau'] = plt.plot(abscisses, creneau(abscisses, 1), lw=1.5,
                                     color='red', visible=False)[0]
PLOTS['AC'] = plt.plot(abscisses, approx_triangle(abscisses, 1),
                             lw=1, ls='-', color='blue',visible=False)[0]

# Positionnement des barres de modification
axcolor = 'lightgoldenrodyellow'  # Choix de la couleur
ax_N = plt.axes([0.35, 0.07, 0.55, 0.03], axisbg=axcolor)

fig2 = plt.subplot(222)
abscisses2 = np.arange(1, N, 1)
plt.title('Coefficients de Fourier en valeur absolue')
plt.ylabel('Triangle (coef. pairs)')
plt.axis([0, abscisses2[-1], 0, 1.5])
PLOTS['TFT'] = plt.bar(abscisses2, [abs(A(n)) for n in abscisses2],
                   color='green')[0]
fig4 = plt.subplot(224)
abscisses2 = np.arange(1, N, 1)
plt.xlabel(r'Indice $n$')
plt.ylabel('Creneau (coef. impairs)')
plt.axis([0, abscisses2[-1], 0, 1.5])
PLOTS['TFC'] = plt.bar(abscisses2, [abs(D(n)) for n in abscisses2],
                   color='green')[0]


# Noter les valeurs initiales
s_N = Slider(ax_N, 'N', 0, 30, valinit=1)

def update(val):
    """
    Met a jour le graphe a partir des valeurs des sliders.
    """
    N = s_N.val  # On recupere la valeur de la barre s_N

    t = triangle(abscisses, N)
    at = approx_triangle(abscisses,N)
    c = creneau(abscisses, N)
    ac = approx_creneau(abscisses,N)
     
    PLOTS['Triangle'].set_ydata(t)  # On met a jour la forme
    PLOTS['AT'].set_ydata(at)
    PLOTS['Creneau'].set_ydata(c)  # On met a jour la structure
    PLOTS['AC'].set_ydata(ac)

    if (N-int(N) != 0):
        s_N.set_val(int(s_N.val))

    # On provoque la mise a jour du graphique (pas automatique par defaut)
    fig.canvas.draw_idle()

# Chaque fois qu'un slider est modifie, on appelle la fonction update
s_N.on_changed(update)

# Creation du menu de selection des traces a afficher
cax = plt.axes([0.1, 0.03, 0.15, 0.1], axisbg=axcolor)
radio = RadioButtons(cax,
                     ('Triangle','Creneau'),
                     (True, False))

# Definition de la fonction qui passe un affichage de visible a invisible
def chooseplot(label):
    if label=='Triangle':
        PLOTS['Triangle'].set_visible(True)
        PLOTS['AT'].set_visible(True)
        PLOTS['Creneau'].set_visible(False)
        PLOTS['AC'].set_visible(False)
    else:
        PLOTS['Triangle'].set_visible(False)
        PLOTS['AT'].set_visible(False)
        PLOTS['Creneau'].set_visible(True)
        PLOTS['AC'].set_visible(True)
        
    fig.canvas.draw_idle()  # On provoque la mise a jour du graphique

# Lorsqu'on coche un de ces boutons, on appelle la fonction chooseplot
radio.on_clicked(chooseplot)


plt.show()  # On provoque l'affichage a l'ecran
