#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
@author: ENS de Lyon

Le but de ce programme est, à partir d'une acquisition de bruit dur Latis Pro, de tracer l'histogramme des valeurs et la fonction d'autocorrélation. On illustre ainsi la différence entre bruit blanc et bruit rose.

Ce programme nécessite un fichier externe, le nom de fichier étant indiqué par la variable "chain" dans le code. Ce fichier est généré par Latis pro, la première ligne contenant du texte. Les lignes suivantes contiennent deux colonnes, séparées par des ';'. La première colonne indique le temps, la seconde les valeurs du bruit. Le séparateur décimal est la ','.

"""
### Un fichier type sorti par Latis Pro contient deux colonnes. Sur la première ligne, est noté "Temps" et la sortie choisie (ex: EA0). 
### Les lignes suivantes correspondent aux valeurs de la sortie pour les différents temps. Les valeurs sont séparées par des ";", sans espace.

import matplotlib.pyplot as P
import numpy as N
import matplotlib.mlab as mlab
from scipy.signal import correlate
P.ion()

#Première étape : importer le fichier contenant le bruit
chain="pink_noise_1.txt"  
tab=N.loadtxt(open(chain),dtype='str',delimiter=';',skiprows=1) 

#Sur Latis Pro, la première ligne du fichier contient du texte : on saute la première ligne. Les séparateurs sont des ';'
#Le problème qui se pose avec l'exportation sur Latis Pro est que les réels sont écrits avec des virgules à la place des points
#Il faut donc importer le tableau en string pour ne pas avoir d'erreur, puis remplacer la virgule par un point et enfin convertir en float. C'est ce qu'on fait dans la suite

n=tab[:,0].size
for i in range(n):
	for j in range(2):
		number=("{}".format(tab[i,j]))[2:-1]
		tab[i,j]=number.replace(',','.')

final=N.array(tab,dtype=float) #final est le tableau que l'on cherche à obtenir : 2 colonnes avec les valeurs des temps et de tensions correspondantes

time=final[:,0] #Données des temps d'acquisition
noise=final[:,1] #Données des valeurs du bruit
variance=noise.var() #Variance du bruit
mean=noise.mean() #Moyenne du bruit

#samples = N.random.normal(mean, std, size=n)

r = correlate(noise, noise, mode = 'same') #Calcule la fonction d'autocorrélation.
#Le mode "full" permet de voir aussi les décalages temporels négatifs

P.grid(True)

#On va représenter les résultats : histogramme du bruit et fonction d'autocorrélation
P.subplot(211)
P.plot(N.arange(-n//2,n//2)*time[1],r/N.max(r),color='black',linewidth=2) #On normalise la fonction d'autocorrélation, et on le représente sur un intervalle de temps centré sur zéro
P.xlim((-time[n//4],time[n//4]))
P.xlabel(r'$\tau$',fontsize=15)
P.ylabel(r'$C(\tau)$',fontsize=15)

P.subplot(212)
m, bins, patches = P.hist(noise,100, normed=1, facecolor='red', alpha=0.8)
y = mlab.normpdf(bins, mean,1) #On représente la densité de proba normale associée
P.plot(bins, N.sqrt(2*N.pi)*N.max(m)*y, linewidth=2)
P.xlabel(r'$U$',fontsize=15)
P.ylabel(r'$N$',fontsize=15)
P.ylim((-0.1,N.max(m)+0.1))
P.xlim(-3,3)




