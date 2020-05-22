'''
Ce programme trace, de façon dynamique (échelle de temps non respectée),
l'évolution de la composante transverse du champ électrique à une interface
vide-conducteur en fonction de la profondeur.
'''

from pylab import *
from matplotlib import animation

dt = 0.01
w=2*pi
k=2*pi
delta=1

zed=linspace(0,10,1000)
env1=[exp(-z/delta) for z in zed]
env2=[-exp(-z/delta) for z in zed]

fig=figure()
title("Effet de peau")
xlabel('$z$ (m)')
ylabel(r'$E_x/E_0$')
ylim([-1,1])
xlim([0,10])
line,=plot([],[])



# fonction à définir quand blit=True
# crée l'arrière de l'animation qui sera présent sur chaque image
def init():
    line.set_data([],[])
    plt.plot(zed,env1,ls='dashed',color='r')
    plt.plot(zed,env2,ls='dashed',color='r')
    matplotlib.pyplot.xticks( [0, 2, 4, 6, 8, 10],
            [r'0',r'$2\delta$',r'$4\delta$',r'$6\delta$',r'$8\delta$',r'$10\delta$'])
    return line,

def animate(i): 
    t = i * dt
    E=[exp(-z/delta)*cos(w*t-k*z) for z in zed]
    line.set_data(zed,E)
    return line,
 
ani = animation.FuncAnimation(fig, animate, init_func=init, frames=2000, blit=True, interval=20, repeat=False)

show()
