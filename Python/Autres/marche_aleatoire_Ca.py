# -*- coding: utf-8 -*-
"""
Created on Thu Apr  5 14:07:57 2018

@author: User
"""



'''MARCHE DE L IVROGNE'''
'''Lhomme ivre se déplace sur un axe. A chaque instant, il peut se déplacer d'une case vers la droite ou
vers la gauche avec une probabilité 1/2. Livrogne part à chaque fois du milieu de laxe.'''

import random as rd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def hasard(p,lim):
    '''Cette fonction renvoie la position de lhomme ivre à l' instant ultérieur connaissant sa position antérieure p.
    On impose des conditions aux limites pérodiques'''
    a=rd.randint(0,1)
    if a==0 :
        return (p-1)%lim
    elif a==1 :
        return (p+1)%lim
    
def somme(L):
    '''Cette fonction calcule la somme des termes de la liste L'''
    s=0
    for k in range(len(L)):
        s+=L[k]
    return s

def gauss(x,a,b,c):
    '''fonction gaussienne'''
    return a*np.exp(-(x-c)**2/(2*b))

def lineaire(x,a):
    '''fonction linéaire'''
    return x*a

lim=100 #longueur de laxe x sur lequel se déplace l'ivrogne


pas=[10,50,100] # liste donnant les nombres de pas que l'on impose à l'ivrogne
x0=np.linspace(0,lim,lim)
essai=100000

for j in range (len(pas)):
    L=np.zeros(lim) 
    x=[]
    y=[]
    for k in range(essai):#Pour chaque nombre de pas imposé à livrogne, 
    #on répète lexpérience plusieurs fois pour obtenir une statistique
        p=lim//2 #livrogne part du milieu de laxe
        for m in range (int(pas[j])):
            p=hasard(p,lim)  
        L[p]+=1#A la fin de l'expérience on note la position de l'ivrogne
    a=somme(L)
    for k in range (len(L)):
        if pas[j]%2==1 and k%2==1 :
            x.append(x0[k])
            y.append(L[k]/a)
            #Dans le cas où l'on a imposé un nombre de pas impair,
            #lhomme ivre ne pourra que se positionner à la fin sur une cas de numéro impair
            #On ne garde alors que les positions impairs
        elif pas[j]%2==0 and k%2==0 :
            x.append(x0[k])
            y.append(L[k]/a)
             #Dans le cas où l'on a imposé un nombre de pas pair, 
             #lhomme ivre ne pourra que se positionner à la fin sur une cas de numéro pair
            #On ne garde alors que les positions pairs
    
    popt, pcov = curve_fit(gauss,x,y,bounds=([0,0,lim//2-10], [1.,lim**2, lim//2+10]))
    plt.plot(x0,gauss(x0,popt[0],popt[1],popt[2]),'k')#on ajuste les données de la simulation par une fonction gaussienne
    plt.plot(x,y,"o ",label='{0} pas'.format(pas[j]) )
plt.xlabel('Position (u.a.)')
plt.ylabel('Probabilité de présence')
plt.title('Probabilité de présence en fonction de la position \n (points : données obtenues par la simulation, tracées noirs : ajustement gaussiens)')
plt.legend()
plt.show()
    
    
pas=np.arange(10,100,10) # liste donnant les nombres de pas que l'on impose à l'ivrogne
sigma=np.zeros(len(pas)) 
sigma_err=np.zeros(len(pas))
x0=np.linspace(0,lim-1,lim)

essai=100000

for j in range (len(pas)):
    L=np.zeros(lim) 
    x=[]
    y=[]
    for k in range(essai):#Pour chaque nombre de pas imposé, 
    #on répète lexpérience plusieurs fois pour obtenir une statistique
        p=lim//2 #livrogne part du milieu
        for m in range (int(pas[j])):
            p=hasard(p,lim)  
        L[p]+=1#A la fin de l'expérience on note la position de l'ivrogne
    a=somme(L)
    for k in range (len(L)):
        if pas[j]%2==1 and k%2==1 :
            x.append(x0[k])
            y.append(L[k]/a) 
            #Dans le cas où l'on a imposé un nombre de pas impair,
            #lhomme ivre ne pourra se positionner à la fin que sur une cas de numéro impair
            #On ne garde alors que les positions impairs
        elif pas[j]%2==0 and k%2==0 :
            x.append(x0[k])
            y.append(L[k]/a)
             #Dans le cas où l'on a imposé un nombre de pas pair, 
             #lhomme ivre ne pourra se positionner à la fin que sur une cas de numéro pair
            #On ne garde alors que les positions pairs
    popt, pcov = curve_fit(gauss,x,y,bounds=([0,0,lim//2-10], [1.,lim**2, lim//2+10]))
    #On ajuste la statistique par une fonction gaussienne
    sigma_err[j]=3*np.sqrt(pcov[1,1])
    sigma[j]=popt[1]

popt, pcov = curve_fit(lineaire,pas,sigma)

plt.errorbar(pas,sigma,yerr=sigma_err,fmt="b+",ecolor="b")#On trace la variance de la distribution en fonction du nombre de pas imposé
plt.plot(pas,lineaire(pas,popt[0]),'r')#On ajuste les points par une droite
plt.xlabel('Nombre de pas')
plt.ylabel('Variance de la distribution gaussienne')
plt.title('Variance de la distribution en fonction du \n nombre de pas imposé')
plt.show()  

