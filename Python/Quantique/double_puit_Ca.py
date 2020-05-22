# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 18:49:15 2018

@author: User
"""
import numpy as np
import matplotlib.pyplot as plt

'''On considère un double puits (le modèle est donné dans le Basdevant et Dalibard)
Le potentiel a pour formule :
  V(x) = +inf si x<-delta/2-a ou x>delta/2+a
       = 0 si -delta/2-a<x<-delta/2 ou delta/2<x<delta/2+a
       = V0 si -delta/2<x<delta/2
       
La résolution de l'équation de Schrôdinger et la condition de continuité de la fonction d'onde en x=+-delta/2
permet d'écrire :
    tan(ka)=-k/(Ktanh(Kdelta/2a)) cas symétrique
    tanh(ka)=-k/K*tanh(Kdelta/2a) cas antisymétrique
    
    avec k=sqrt(2mE)/hbar et K=sqrt(2m(V0-E))/hbar aprox K=sqrt(2mV0)/hbar=cste pour V0>>E
    on pose a=1 et hbar**2/2m =1 
    On résout les deux équations avec la méthode de dichotomie pour différents delta.
    On a alors accès à la valeur de k et donc la valeur de l'énergie propre E=k**2'''


def dichotomie(f,a,b,c,eps):
    '''calcule la valeur de x telle que f(x)=c pour a<x<b par dichotomie'''
    x=(a+b)/2
    while abs(f(x)-c)>eps :
        x=(a+b)/2
        if f(x)>c :
            b=x
        else :
            a=x
    return x

def fonc(x):
    return 2*np.tan(x*(np.pi/2))/(x*np.pi) #a=1 et k=x*pi/2


def fonc_S(delta,K):
    '''fonction symétrique avec a=1'''
    return -1/(K*np.tanh(K*delta/2))

def fonc_AS(delta,K):
    '''fonction antisymétrique avec a=1'''
    return -np.tanh(K*delta/2)/K

e1=[]
e2=[]
e3=[]
e4=[]
e5=[]
e6=[]
eps=1e-4
K=10
d=np.linspace(1e-5,2,100)
for j in range (len(d)):
    cs=fonc_S(d[j],K)
    cas=fonc_AS(d[j],K)
    e1.append(dichotomie(fonc,1,3,cs,eps)**2)
    e2.append(dichotomie(fonc,1,3,cas,eps)**2)
    e3.append(dichotomie(fonc,3,5,cs,eps)**2)
    e4.append(dichotomie(fonc,3,5,cas,eps)**2)
    e5.append(dichotomie(fonc,5,7,cs,eps)**2)
    e6.append(dichotomie(fonc,5,7,cas,eps)**2)#on calcule les six premiers niveaux d'énergie
    #à l'aide de la fonction dichotomie pour différentes valeurs de delta

    
plt.plot(d,e1)
plt.plot(d,e2)
plt.plot(d,e3)
plt.plot(d,e4)
plt.plot(d,e5)
plt.plot(d,e6)
plt.xlabel('delta/a')
plt.ylabel('Energies propres (six premiers niveaux)')
plt.show()