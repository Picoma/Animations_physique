import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.widgets import Slider, Button

#Ce script affiche la courbe de la loi d'emission du corps noir de Planck, avec un slider pour pouvoir changer la temperature. Il affiche egalement la couleur associée a l'émission, avec un algorithme basé sur des lois empiriques convertissant la temperature en donnees RGB

#Rq : uniquement la couleur de l'émission est représentée, par son intensité, comme elle varie en T^4 il est difficile d'afficher de telles variations sur un écran

#Constantes-------------------------
h = 6.63e-34
c = 3e8
k = 1.38e-23

lamda = np.arange(0,5,0.001)

#----------------------------------
#Temperature en RGB. Les lois de conversion proviennent d'un ajustement numerique que l'on pourra trouver a l'url http://www.tannerhelland.com/4435/convert-temperature-rgb-algorithm-code/ (url active le 16 fevrier 2017)
def get_color(T):
    #Red
    if T < 6600:
        r = 255
    else:
        r = 329.698727446 * (T/100.-60)**(-0.1332047592)
        if r<0:
            r=0
        elif r>255:
            r=255
    #Green
    if T < 6600:
        g = 99.4708025861 * np.log(T/100.) - 161.1195681661
    else:
        g = 288.1221695283 * (T/100.-60)**(-0.0755148492)
    if g<0:
        g=0
    elif g>255:
        g=255
    #Blue
    if T>6600:
        b=255
    elif T<1900:
        b=0
    else:
        b = 138.5177312231 * np.log(T/100.-10) - 305.0447927307
    if b<0:
        b=0
    elif b>255:
        b=255
    r *= 1/255.
    g *= 1/255.
    b *= 1/255.
    return (r,g,b)

#----------------------------------

T = 8000
u = 2*h*c**2/(lamda*1e-6)**3 * 1 / (np.exp(h*c/(lamda*1e-6*k*T))-1)

fig = plt.figure()
plt.subplots_adjust(bottom=0.20)

ax1 = plt.subplot(121)
line, = plt.plot(lamda,u)
plt.xlabel("Longueur d'onde, en $\mu m$")
plt.ylabel("Luminance énergétique spectrale, en $W\cdot m^{-2}\cdot sr^{-1} \cdot Hz^{-1}$")
plt.title('Loi de Planck')
plt.xticks(np.arange(0,5,0.4))
plt.grid(axis='x')

ax2 = plt.subplot(122,axisbg='black')
circle = ax2.add_patch(
        patches.Circle(
            (0.5,0.5),0.4,color=get_color(T)
        )
)
ax2.set_yticklabels([])
ax2.set_xticklabels([])
plt.title('Couleur correspondante')

#Slider de temperature
axTemp = plt.axes([0.20,0.08,0.65,0.03])
sTemp = Slider(axTemp, 'Temperature (en $K$)', valmin=1000, valmax=15000, valinit=6000)
def update(val):
    T = sTemp.val
    u = 2*h*c**2/(lamda*1e-6)**3 * 1 / (np.exp(h*c/(lamda*1e-6*k*T))-1)
    line.set_ydata(u)
    circle.set_facecolor(get_color(T))
    circle.set_edgecolor(get_color(T))
sTemp.on_changed(update)

#Rescale button
axBout = plt.axes([0.35,0.8,0.1,0.05])
Breset = Button(axBout, 'Rescale')
def rescale(event):
    ax1.relim()
    ax1.autoscale_view()
Breset.on_clicked(rescale)


plt.show()
