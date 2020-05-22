#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  7 17:18:46 2018

@author: alexandre
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons

plt.close("all")

r=np.linspace(0.1,4,100)

K=2
C=1
m=2

Epeff = - K/r + m*C**2/(2*r**2)

plt.figure(1)
plt.plot(r,Epeff)
plt.xlim([0,4])
plt.ylim([-3,2])


e0=1
p=2
phi = np.linspace(0,2*np.pi,100)
r = p/(1+e0*np.cos(phi))

plt.figure(2)
x=r*np.cos(phi)
y=r*np.sin(phi)
plt.plot(x,y,'o')
plt.xlim([-4,1])
plt.ylim([-3,3])

fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.25)

plt.plot([0], [0], 'ok')
l, = plt.plot(x, y, 'o')
plt.xlim([-4,1])
plt.ylim([-8,8])
plt.xlabel("pulsation")
plt.ylabel("Io/Imax")

axcolor = 'lightgoldenrodyellow'
axN = plt.axes([0.25, 0.12, 0.65, 0.03], axisbg=axcolor)


ioN = Slider(axN, 'N', 0, 2,valfmt='%0.2f',valinit=e0) # définition de l'intervalle des valeurs de e

def update(val):
    e = ioN.val
    p=2*e
    l.set_xdata(p/(1+e*np.cos(phi))*np.cos(phi))
    l.set_ydata(p/(1+e*np.cos(phi))*np.sin(phi))
    fig.canvas.draw_idle()
ioN.on_changed(update)

resetax = plt.axes([0.03, 0.07, 0.1, 0.04])
button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')


def reset(event):
    ioN.reset()
button.on_clicked(reset)
