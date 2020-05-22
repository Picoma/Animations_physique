# -*- coding: utf-8 -*-
"""
Animation pour montrer l'influence de la position du point de réfraction dans
le calcul de la durée du parcours.
On peut jouer aussi sur la vitesse dans chacun des milieux
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import matplotlib.patches as patches


def duree(x,v1,v2):
    AI = np.sqrt((xA-x)**2+yA**2)
    BI = np.sqrt((xB-x)**2+yB**2)
    return AI/v1+BI/v2
xI_liste = np.linspace(-2,2,200)
xA,yA = -1,1
xB,yB = 1,-1
xI_ini = 0
v1_ini, v2_ini = 1, 2
t_ensemble = duree(xI_liste,v1_ini,v2_ini)

fig = plt.figure()
plt.subplots_adjust(left=0.15, bottom=0.25)
axcolor = 'lightgoldenrodyellow'
axI = plt.axes([0.25, 0.12, 0.65, 0.03], axisbg=axcolor)
sxI = Slider(axI, 'xI', -2, 2, valinit=0)
axV1 = plt.axes([0.25, 0.07, 0.65, 0.03], axisbg=axcolor)
sV1 = Slider(axV1, 'v1', 1, 3, valinit=1)
axV2 = plt.axes([0.25, 0.02, 0.65, 0.03], axisbg=axcolor)
sV2 = Slider(axV2, 'v2', 1, 3, valinit=2)

ax1 = fig.add_subplot(121)
ax1.set_title("trajectoire")
ax1.add_patch(patches.Rectangle((-2.2, -2), 5, 2,facecolor='grey',alpha=0.5))
l1a, = ax1.plot([xA,xI_ini,xB], [yA,0,yB],'-ok',ms=8)
plt.xlabel("position x")
plt.ylabel("position y")
l1b, = ax1.plot([xI_ini],[0],'or',ms=8)
ax1.set_xlim(-2.1,2.1)
ax1.set_ylim(-1.1,1.1)
    
ax2 = fig.add_subplot(122)
ax2.set_title("durée du parcours")
plt.xlabel("position x")
plt.ylabel("temps")
ax2.set_ylim(0.8,4)
l2a, = ax2.plot(xI_liste,t_ensemble,'b')
l2b, = ax2.plot([xI_ini],[duree(xI_ini,v1_ini, v2_ini)],'og',ms=8)

def update(val):
    xIc = sxI.val
    v1 = sV1.val
    v2 = sV2.val
    l1a.set_data([xA,xIc,xB], [yA,0,yB])
    l1b.set_data([xIc],[0])
    l2a.set_ydata(duree(xI_liste,v1,v2))
    l2b.set_data([xIc],[duree(xIc,v1,v2)])
    fig.canvas.draw_idle()
    
sxI.on_changed(update)
sV1.on_changed(update)
sV2.on_changed(update)

resetax = plt.axes([0.03, 0.07, 0.1, 0.04])
button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')

def reset(event):
    sxI.reset()
button.on_clicked(reset)

plt.show()
