# Ce programme permet d'étudier le comportement fréquentiel en gain et en phase d'un filtre passe-bande du second ordre de fréquence centrale fo et de facteur de qualité Q.
# Le diagramme asymptotique du gain est représenté en noir
# L'échelle de gain en décibel est à gauche, l'échelle de déphasage en degrés est à droite
# On utilise une échelle relative en fréquence en travaillant en fonction de f/fo et non en fonction de f
# Les curseurs permettent d'ajuster le gain maximal Gmax et le facteur de qualité Q
# Le bouton "reset" permet de ramener les coefficients ajustables à la souris avec les curseurs à leur valeur initiale

import matplotlib.pyplot as plt
from pylab import *
from matplotlib.widgets import Slider, Button, RadioButtons
import numpy as np

fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.30)
# On étudie la fonction de transfert trois décades avant et après fo, fréquence centrale du filtre passe-bande
# Mise en place de l'échelle de calcul en fréquence avec un pas fréquentiel pasFreq
# La fréquence est représentée en valeur relative f/fo
pasFreq = 0.001
Fmin = 0.001
Fmax = 1000
f = np.arange(Fmin, Fmax, pasFreq)
# On part d'un filtre avec un gain max de 1 et un facteur de qualité de 1
G0 = 1
Q0 = 1
Gain = 20*log10(G0/sqrt(1+(Q0*(f/1-1/f))**2))
GainAssympt = 20*log10(G0/(Q0))+(1-f)/sqrt((1+pasFreq/10-f)**2)*20*log10(f)
Phi = -180/pi*arctan(Q0*(f/1-1/f))

# Bornes d'échelles en amplitude
GdBMax = 20*log10(G0)+60
GdBMin = 20*log10(G0)-20*(1/2)*log10(Fmax/Fmin)

# Mise en place des figures avec le gain en dB en rouge, le diagramme asymtotique en noir (échelle de gain sur l'axe gauche) et la phase en bleu (échelle sur l'axe droit)
ax1 = plt.subplot(1, 1, 1)
wave1, = plt.semilogx(f, Gain, color='red')
wave2, = plt.semilogx(f, GainAssympt, color='black') 
plt.grid(b='on',which='both', axis='both', color='red')
plt.axis([Fmin, Fmax, GdBMin, GdBMax])
plt.ylabel('Gain(dB) (rouge)')
plt.xlabel('f/fo')
axdroit1 = ax1.twinx()
axdroit1.set_ylim(-100, 100)
axdroit1.set_ylabel('Phase (bleu)(°)',color='blue')
wave3, = plt.semilogx(f, Phi, color ='blue')
plt.grid(b='on',which='both', axis='both', color='blue')

# boutons de commande avec les curseurs pour changer les paramètres Q et Gmax
#~Sur le programme de départ, le gain peut évoluer entre 0.1 et 10 et le facteur de qualité peut évoluer entre 0.1 et 5
axcolor = 'lightgoldenrodyellow'
axgain = plt.axes([0.10, 0.10, 0.80, 0.03], axisbg=axcolor)
axqual = plt.axes([0.10, 0.15, 0.80, 0.03], axisbg=axcolor)
sgain = Slider(axgain, 'Gmax', 0.1, 10, valinit=G0) # Gmax peut évoluer entre 0.1 et 10, changer si nécessaire
squal = Slider(axqual, 'Q', 0.1, 5, valinit=Q0) # Q peut évoluer entre 0.1 et 5, changer si nécessaire

# changement des figures suite à l'évolution des paramètres des curseurs
def update(val):
    gain = sgain.val
    qual = squal.val
    wave1.set_ydata(20*log10(gain)-10*log10(1+(qual*(f/1-1/f))**2))
    wave2.set_ydata(20*log10(gain/(qual))+(1-f)/sqrt((1+pasFreq/10-f)**2)*20*log10(f))
    wave3.set_ydata(-180/pi*arctan(qual*(f/1-1/f)))
    fig.canvas.draw_idle()
sgain.on_changed(update)
squal.on_changed(update)

resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')


def reset(event):
    sgain.reset()
    squal.reset()
button.on_clicked(reset)

plt.show()