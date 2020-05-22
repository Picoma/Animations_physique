"""
=================================================
           ETUDE DE LA RMN (oscillations de Rabi)
           
- Permet d'obtenir les oscillations de Rabi,
  en fonction du temps et de la fréquence
- Possiblité de modifer la fréquence de l'onde excitatrice en direct (omega)
- Modification possible de l'amplitude du champ constant (B0),
  et du champ excitateur (B1)
- Rapport gyromagnétique gamma
- Calcul automatique des pulsations du système
- les variables w_min et w_max permettent de choisir les bornes en fréquence
=================================================

Grégoire MARTOUZET - gregoire.martouzet@ens-paris-saclay.fr

Sources pour les OdG des champs (depuis un TP):
http://phytem.ens-paris-saclay.fr/servlet/com.univ.collaboratif.utils.LectureFichiergw?CODE_FICHIER=1416382926599&ID_FICHE=7111
OdG pour RMN commerciale: B0=1 à 20 T (-> omega0 ~ 100MHz )
"""

import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import numpy as np


""" ----- Paramètres physiques ----- """
# rapport gyromagnétique (rad/s/T)
gamma = 267.513e6 # (proton) 
#gamma = 67.262e6 # C13


# CHAMPS MAGNETIQUES (en Tesla)
# RMN à 15 MHz, B0 = f0/gamma
B0 = 15e6*2*np.pi / gamma
B1 = 12e-4

# vitesse angulaire du champ (fixé à la freq de résonance pour commencer)
w = gamma*B0
# omega0 = pulsation de larmor: w0 = gamma*B0
w0 = gamma*B0
# omega1 = pulsation de larmor du champ tournant B1
w1 = gamma*B1

delta = w - w0 # écart en fréquence 
Omega = np.sqrt(delta**2 + w1**2)

""" ----- Paramètres de calcul ----- """
N = 500 # nombres de points

t_max = 10/Omega # temps maximum
w_min = np.log10(7e7) # borne inférieure de la fréquence
w_max = np.log10(2e8) # borne supérieure de la fréquence

t = np.linspace(0.0, t_max, N)
frequence = np.logspace(w_min, w_max, 10*N)

""" ----- Création de la fenetre ----- """
fig = plt.figure()
fig.canvas.set_window_title('Résonance')

# Axes et configuration
ax_tps = plt.axes([0.1, 0.6, 0.8, 0.35])
ax_tps.set_xlabel('$t (\mu s)$')
ax_tps.set_ylabel('$P_{1}$')
ax_frq = plt.axes([0.1, 0.15, 0.8, 0.35])
ax_frq.set_xlabel('$\omega (rad/s)$')
ax_frq.set_ylabel('$P_{1, max}$')

ax_frq.set_xscale('log')
#ax_frq.set_yscale('log')

ax_tps.axis([0.0, t_max*1e6, -0.1, 1.1])
ax_frq.axis([10**w_min, 10**w_max, 1e-4, 1.1])

""" ----- Oscillation de Rabi ----- """
# en fct du temps
def rabi(t, w):
	Omega = np.sqrt((w-w0)**2 + w1**2)
	return (w1/Omega)**2 * np.sin(Omega*t/2)**2
	
# en fct de la fréquence (amplitude)
def rabi_frq(w):	
	return (w1/np.sqrt((w-w0)**2 + w1**2))**2

""" ----- Tracé ----- """
y = rabi(t, w)
l, = ax_tps.plot(t*1e6, y)

amp = rabi_frq(frequence)
ax_frq.plot(frequence, amp)

l2, = ax_frq.plot(w, rabi_frq(w), 'or')
vline = ax_frq.vlines(x=w, ymin=0.0, ymax=rabi_frq(w), colors = 'r', lw=2)

""" ----- Widgets pour changer les paramètres ----- """
# Zones des Widgets
ax_slider = plt.axes([0.1, 0.01, 0.8, 0.04])
ax_btn = plt.axes([0.1, 0.06, 0.05, 0.05])

# Fonctions des Widgets
def maj_slider(val):
	w = 10**val
	
	y = rabi(t, w)
	
	l.set_ydata(y)
	l2.set_data(w, rabi_frq(w))
	
	vline.set_paths([[[w,0.0],[w,rabi_frq(w)]]])

# rétabli omega à la résonance
def btn_Reset(event):
	se.reset()

# Widgets
se = Slider(ax_slider, '$\omega=10^x$', w_min, w_max, valinit=np.log10(w0))
se.on_changed(maj_slider)

btn=Button(ax_btn, 'R')
btn.on_clicked(btn_Reset)

""" ----- Affichage ----- """
plt.show()
