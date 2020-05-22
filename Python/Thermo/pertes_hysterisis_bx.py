#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 29 16:29:03 2018

@author: alexandre
"""

import numpy as np
import matplotlib.pyplot as plt

plt.close("all")

# Chargement du fichier
filename='transfo.csv'
Matrix=np.loadtxt(filename, delimiter=',',skiprows=3)

t=Matrix[:,0] # temps
X=Matrix[:,1]*20.345*100*1e-3 # H 
Y=-Matrix[:,2]*50.1*1*1e-3 # B

# Partie basse du cycle
X1 = X[(t>=6) & (t<15.8)]
Y1 = Y[(t>=6) & (t<15.8)]

# Partie haute du cyle
X2 = X[(t>=15.8) & (t<26)]
Y2 = Y[(t>=15.8) & (t<26)]

plt.figure(1)
plt.plot(X1,Y1,'b')
plt.plot(X2,Y2,'r')
plt.grid()
plt.show()

# Aire sous la courbe de 1
aire1=np.trapz(Y1, X1)
# Aire sous la courbe de 2
aire2=np.trapz(Y2, X2)

print((aire2-aire1))