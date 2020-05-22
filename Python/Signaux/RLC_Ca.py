# -*- coding: utf-8 -*-
"""
Created on Sun May 27 17:10:31 2018

@author: User
"""

import numpy as np
import matplotlib.pyplot as plt
'''CIRCUIT RLC SERIE PASSE BAS'''

def Us(x,Q):
    '''Réponse du circuit en tension'''
    return 1/(np.sqrt((1-x**2)**2+(x/Q)**2))

def Is(x,Q):
    '''Réponse du circuit en intensité'''
    return Q/(np.sqrt(Q**2*(x-1/x)**2+1))



x=np.linspace(0,3,10000)
Q=[0.5,1/np.sqrt(2),1,2,3,4]

for k in range(len(Q)):
    plt.plot(x,Us(x,Q[k]),label="Q={:05.3f}".format(Q[k]))

plt.xlabel('Pulsation réduite')
plt.ylabel('Us/U0')
plt.legend()
plt.grid()
plt.show()



for k in range(len(Q)):
    plt.plot(x,Is(x,Q[k]),label="Q={:05.3f}".format(Q[k]))
plt.legend()
plt.xlabel('Pulsation réduite')
plt.ylabel('Is/I0')
plt.grid()
plt.show(),