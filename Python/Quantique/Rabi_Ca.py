# -*- coding: utf-8 -*-
"""
Created on Sun May 27 17:59:17 2018

@author: User
"""
'''OSCILLATIONS DE RABI'''

import numpy as np
import matplotlib.pyplot as plt

def Rabi(delta_w,w1,t):
    '''Calcule la probabilité de transition dans le cadre de l'expérience de Rabi'''
    Omega=np.sqrt(delta_w**2+w1**2)
    return (w1/Omega)**2*np.sin(Omega*t/2)**2

w1=1
delta_w=np.linspace(0,3,4)*w1

t=np.linspace(0,20,1000)
for k in range(len(delta_w)):
    plt.plot(t,Rabi(delta_w[k],w1,t),label="w=w0+{0} x w1".format(int(delta_w[k])))
    
plt.xlabel('Temps (s)')
plt.ylabel('Probabilité de transition de l\'état |+> vers l\'état |-> ')
plt.grid()
plt.legend()
plt.show()