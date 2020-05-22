import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation
from matplotlib.widgets import Slider

#Ce script anime une chaine unidimensionnelle d'atome subissant des vibrations collectives, afin d'illustrer le concept de phonons
#Les effets de bords sont négligés

#Constantes-------------------------------

a = 1.0 #pas du reseau
N = 25 #nombre d'atomes
amplitude = 0.3 #amplitude des vibrations

lamda = 2 #cette longueur d'onde pourra etre changée par un slider

omega0 = 2*np.pi
t = np.arange(0,100,0.01)

#Calculs----------------------------

def omega(lamda): #si jamais on veut utiliser une relation de dispersion
    #return 2*omega0*abs(np.sin(np.pi*a/lamda)) 
    return omega0

class Atome(object):
    #Une classe permettant de gérer plus facilement l'affichage des atomes
    def __init__(self,ax,position=(0,0),color='blue',radius=0.1):
        self._circle = ax.add_patch(
                patches.Circle(
                    position,radius,color=color))
    def deplacer(self,position):
        self._circle.center = position

fig = plt.figure()
plt.subplots_adjust(bottom=0.20)

#Tracé des atomes
ax1 = plt.subplot(211)
plt.xlabel('x')
ax1.set_yticklabels([])
chaine_back = [Atome(ax1,position=(a*i,0),color='green',radius=0.05) for i in range(N)] #pour marquer les positions d'équilibre en vert derrière les atomes
chaine = [Atome(ax1,position=(a*i,0)) for i in range(N)]
plt.plot([-1,a*N],[0,0],'g-')
plt.xlim((-1,a*N))
plt.ylim((-1,1))
plt.title("Modes de vibration normaux d'une chaine d'atomes unidimensionnelle")

#Tracé des amplitudes des déplacements
ax2 = plt.subplot(212)
plt.xlabel('x')
plt.ylabel('Amplitude')
plt.xlim((-1,a*N))
plt.ylim((-amplitude,amplitude))
deplacements = [0 for i in range(N)]
line, = plt.plot(range(N),deplacements,'-')

#Animation
def animate(i,lamda=2):
    for j in range(N):
        chaine[j].deplacer((a*j+amplitude*np.cos(omega(lamda)*t[i]-a*j*2*np.pi/lamda),0))
    line.set_ydata([amplitude*np.cos(omega(lamda)*t[i]-a*j*2*np.pi/lamda) for j in range(N)])
ani = animation.FuncAnimation(fig, animate, range(t.size),fargs=[lamda],interval=50) #l'option interval represente la duree entre chaque frame, en ms

#Slider pour la longueur d'onde a afficher 
axLambda = plt.axes([0.20,0.08,0.65,0.03])
sLambda = Slider(axLambda, "Longueur d'onde", valmin=2, valmax=N, valinit=2)
sLambda.valfmt = u'%d'
sLambda.set_val(2)
def update(val):
    lamda = int(sLambda.val)
    ani._args = [lamda]
sLambda.on_changed(update)

plt.show()

