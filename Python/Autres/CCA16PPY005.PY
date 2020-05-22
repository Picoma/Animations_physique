# Ce programme permet d'expliquer le choix des paramètres d'un correcteur P.I. (proportionnel intégral) quand on connait la fonction de transfert en boucle ouverte d'un système sans correcteur. Elle permet notamment de voir à quelle situation conduit le choix des coefficients du PI obtenus par la méthode de Ziegler Nichols.
# On peut adapter cette application pour n'importe quel type de fonction de transfert passe bas jusqu'à l'ordre 3 en ajustant les coefficients a, b et c.
# Les curseurs permettent d'ajuster avec le souris Tc et Kc, les coefficients du PI 
# Le bouton "Reset" permet de ramener les coefficients à leur valeur initiale en début de programme. La plage de valeur explorée ainsi que la valeur initiale peuvent être ajustées.

import matplotlib.pyplot as plt
from pylab import *
from scipy.misc import derivative
from matplotlib.widgets import Slider, Button, RadioButtons

# On s'intéresse à un système, dont la fonction de transfert en B0 sans correction ni propotionnelle, ni PI est du troisième ordre
# Les paramètres de la fonction de transfert d'ordre 3 type Go/(1+a.p+b.p²+c.p3)
# pour trouver une valeur acceptable de ces coefficients à partir d'un relevé réel en gain et phase, ajuster la fonction qui donne la partie imaginaire de la fonction de transfert en imposant le gain statique
# Ne pas ajuster sur le module car on perd les infos sur la phase et l'ajustement ne peut pas donner des paramètres avec un encadrement acceptable
# Valeurs obtenues pour le contrôle de gain du flux lumineux pour une position donnée du récepteur par rapport à l'émetteur
#a=6.9*10**-7
#b=1.8*10**-12
#c=1.05*10**-18
#Go=0.27

a=6.9*10**-7
b=1.8*10**-12
c=1.05*10**-18
Go=0.27

#paramètre du correcteur PI : C(p)= Kc*(1+1/(Tc.p))
# Avec l'exemple de départ, le gain Kosc qui conduit à l'oscillation est 0,65 et la période des oscillations vaut 7,7µs
# Valeur trouvées pour Ziegler Nichols
#Kc=0.3
#Tc=6.4*10**-6

Kc=0.3
Tc=6.4*10**-6

# Echelle de travail en fréquence
Fmin=500
Fmax = 1000000000
pasFreq = 500

# Echelle d'affichage
MinX = -3.5
MaxX = 1.5
MinY = -4
MaxY = 1.5

# Mise en place de l'échelle de travail en fréquence
f = np.arange(Fmin, Fmax, pasFreq) 

#Mise en place des diagrammes de bode (gain et phase) du système en BO, du correcteur et de la BO avec le correcteur
plt.figure(figsize=(10,10))



# Mise en place de la feuille de tracé (cercle trigo, axes réel et imaginaire
# Tracé du cercle de rayon 1 et mise en place de la figure (légende, quadrillage...)

phicercle = np.arange(0, 360, 1)
rayon = 1
X = rayon*cos(phicercle/360*2*pi)
Y = rayon*sin(phicercle/360*2*pi)
plt.grid(b='on',which='both', axis='both', color='blue')
plt.xlabel('partie réelle')
plt.ylabel('partie imaginaire')
plt.plot (X, Y)
# Tracé des axes réel et imaginaire
plt.plot([MinX,MaxX], [0, 0], 'k-', label='line 1', linewidth=1)
plt.plot([0, 0],[MinY,MaxY], 'k-', label='line 2', linewidth=1)
# Mise en place de l'échelle du graphe et explication de la signification des différents graphes
plt.axis([MinX, MaxX, MinY, MaxY])
plt.title('méthode de Ziegler Nichols', color = 'black')
plt.text(MinX+0.5, MaxY-0.5, 'Cercle de rayon unité', fontsize=12, color = 'blue')
plt.text(MinX+0.5, MaxY-0.75, 'Système non corrigé', fontsize=12, color = 'green')
plt.text(MinX+0.5, MaxY-1, 'Système corrigé P.I.', fontsize=12, color = 'red')

# Calcul des points du lieu de Nyquist de la fonction de transfert en boucle ouverte 
# avec le gain K qui fait tout juste osciller en boucle fermée
XBO = Go*(1-b*(2*pi*f)**2)/((1-b*(2*pi*f)**2)**2+(a*2*pi*f-c*(2*pi*f)**3)**2)
YBO = Go*(c*(2*pi*f)**3-a*2*pi*f)/((1-b*(2*pi*f)**2)**2+(a*2*pi*f-c*(2*pi*f)**3)**2)
plt.plot(XBO, YBO)

# Calcul des points de la FTBO corrigée
XBOCo = Go*Kc*((c*(2*pi*f)**3-a*2*pi*f)*2*pi*f*Tc+(2*pi*f*Tc)**2*(1-b*(2*pi*f)**2))/(((1-b*(2*pi*f)**2)*2*pi*f*Tc)**2+((c*(2*pi*f)**3-a*2*pi*f)*2*pi*f*Tc)**2)
YBOCo = Go*Kc*((c*(2*pi*f)**3-a*2*pi*f)*(2*pi*f*Tc)**2-(2*pi*f*Tc)*(1-b*(2*pi*f)**2))/(((1-b*(2*pi*f)**2)*2*pi*f*Tc)**2+((c*(2*pi*f)**3-a*2*pi*f)*2*pi*f*Tc)**2)
NyquistBOCo, = plt.plot(XBOCo, YBOCo, lw=0.8, color='red')

# boutons de commande avec les curseurs pour changer les paramètres Tc et Kc du PI et le reset
axcolor = 'lightgoldenrodyellow'
axKc = plt.axes([0.08, 0.93, 0.85, 0.015], axisbg=axcolor)
axTc = plt.axes([0.08, 0.95, 0.85, 0.015], axisbg=axcolor)
sKc = Slider(axKc, 'Kc', 0.1*Kc, 10*Kc, valinit=Kc) # La valeur initiale du gain du PI est Kc obtenu par la méthode de Ziegler Nichols. Le choix de la plage de valeur de ce gain se fait entre 0.1.Kc et 10.Kc
sTc = Slider(axTc, 'Tc(µs)', 0.1*Tc*10**6, 10*Tc*10**6, valinit=Tc*10**6)# La valeur initiale de la constante d'intégration du PI est Tc obtenue par la méthode de Ziegler Nichols. Le choix de la plage de valeur de ce gain se fait entre 0.1.Tc et 10.Tc et la représentation avec les curseur est en µs d'où le facteur de multiplication par 10^6

# changement des figure suite à l'évolution des paramètres des curseurs
def update(val):
    gain = sKc.val
    ToC = 10**-6*sTc.val
    XBOCov =(Go*gain*((c*(2*pi*f)**3-a*2*pi*f)*2*pi*f*ToC+(2*pi*f*ToC)**2*(1-b*(2*pi*f)**2))/(((1-b*(2*pi*f)**2)*2*pi*f*ToC)**2+((c*(2*pi*f)**3-a*2*pi*f)*2*pi*f*ToC)**2))
    YBOCov =(Go*gain*((c*(2*pi*f)**3-a*2*pi*f)*(2*pi*f*ToC)**2-(2*pi*f*ToC)*(1-b*(2*pi*f)**2))/(((1-b*(2*pi*f)**2)*2*pi*f*ToC)**2+((c*(2*pi*f)**3-a*2*pi*f)*2*pi*f*ToC)**2))
    NyquistBOCo.set_xdata(XBOCov)
    NyquistBOCo.set_ydata(YBOCov)

sKc.on_changed(update)
sTc.on_changed(update)

resetax = plt.axes([0.45, 0.97, 0.08, 0.025])
button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')

def reset(event):
    sKc.reset()
    sTc.reset()
button.on_clicked(reset)


# On affiche les graphes
plt.show()