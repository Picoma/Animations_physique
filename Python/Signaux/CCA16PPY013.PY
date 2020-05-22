# Ce programme permet d'étudier le comportement fréquentiel en gain et en phase d'un filtre passe-bas du second ordre de fréquence centrale fo et de facteur de qualité Q.
# Le diagramme asymptotique du gain est représenté en noir
# L'échelle de gain en décibel est à gauche, l'échelle de déphasage en degrés est à droite
# On utilise une échelle relative en fréquence en travaillant en fonction de f/fo et non en fonction de f
# Les curseurs permettent d'ajuster le gain maximal Gmax et le facteur de qualité Q
# Le bouton "reset" permet de ramener les coefficients ajustables à la souris avec les curseurs à leur valeur initiale


import matplotlib.pyplot as plt
from pylab import *
from matplotlib.widgets import Slider, Button, RadioButtons
import numpy as np

#Ce programme permet d'étudier le comportement d'un filtre passe-bas du second ordre de fréquence centrale fo et de facteur d'amortissement m.

fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.30)

# on prépare l'échelle de fréquence sachant qu'on représente en fonction de f/fo si fo est la fréquence de coupure
pasFreq = 0.001 # pas en fréquence
Fmin = 0.001 #rapport f/fo min
Fmax = 1000 #rapport f/fo max
f = np.arange(Fmin, Fmax, pasFreq)
# on donne la valeur initiale des coefficients importants : gain statique et amortissement
G0 = 1
m = 1

# on définit les fonction de gain en dB, le diagramme asymptotique, et de phase
Gain = 20*log10(G0/sqrt((1-(f/1)**2)**2+(2*m*f/1)**2))
GainAssympt = 20*log10(G0)-(((1+pasFreq/100-f)/sqrt((1+pasFreq/100-f)**2)-1)/2)*20*log10((1/f)**2)
Phi = -180/pi*arctan(2*m*(f/1)/(1+pasFreq/100-(f/1)**2))+180*(((1+pasFreq/100-f)/sqrt((1+pasFreq/100-f)**2)-1)/2)


# on prépare les échelles sur les axes, gain à gauche, phase à droite et échelle de fréquence en log    
wave1, = plt.semilogx(f, Gain, lw=2, color='red')
wave2, = plt.semilogx(f, GainAssympt, lw=0.5, color='black')
# on prend 3 décades avant la coupure et trois décade après et on observe entre -80dB et 25dB
plt.axis([Fmin, Fmax, -80, 25])
plt.grid(b='on',which='both', axis='both', color='red')
plt.xlabel('f / fo')
ax.set_ylabel('GdB (rouge)')
ax2 = ax.twinx()
# pour la phase, on observe entre -190° et 10° afin d'utiliser au mieux l'échelle
ax2.set_ylim(-190, 10)
ax2.set_ylabel('Phase (°) (bleu)', color='black')
plt.grid(b='on',which='both', axis='both', color='blue')
wave3, = plt.semilogx(f, Phi, lw=0.5, color='blue')


# mise en place des curseurs pour ajuster la gain statique et l'amortissement
axcolor = 'lightgoldenrodyellow'
axgain = plt.axes([0.25, 0.10, 0.65, 0.03], axisbg=axcolor)
axamort = plt.axes([0.25, 0.15, 0.65, 0.03], axisbg=axcolor)

sgain = Slider(axgain, 'Go', 0.1, 10, valinit=G0) # on veut explorer pour un gain statique entre 0,1 et 10
samort = Slider(axamort, 'ammortissement', 0.1, 10, valinit=m) # on veut explorer pour un amortissement entre 0,1 et 10

# mise à jour des graphes en fonction des positions des curseurs
def update(val):
    gain = sgain.val
    amort = samort.val
    #fonctions à modifier 
    wave1.set_ydata(20*log10(gain/sqrt((1-(f/1)**2)**2+(2*amort*f/1)**2)))
    wave2.set_ydata(20*log10(gain)-(((1+pasFreq/100-f)/sqrt((1+pasFreq/100-f)**2)-1)/2)*20*log10((1/f)**2))
    wave3.set_ydata(-180/pi*arctan(2*amort*(f/1)/(1+pasFreq/100-(f/1)**2))+180*(((1+pasFreq/100-f)/sqrt((1+pasFreq/100-f)**2)-1)/2))
    fig.canvas.draw_idle()
sgain.on_changed(update)
samort.on_changed(update)

# bouton reset pour remettre les curseurs en position initiale
resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')


def reset(event):
    sgain.reset()
    samort.reset()
button.on_clicked(reset)


def colorfunc(label):
    l.set_color(label)
    fig.canvas.draw_idle()


plt.show()