# -*- coding: utf-8 -*-
"""
Created on Sun Dec 10 15:46:30 2017

@author: User
"""
import numpy as np
import matplotlib.pyplot as plt



'''DIFFRACTION PAR DES SRUCTURES PERIODIQUES'''
def eclairement(phi,n,norm):
    return (np.sin(n*phi/2)/(norm*np.sin(phi/2)))**2

N=2#Nombre de fentes pour le 1er graphe
Nprim=10#Nombre de fentes pour le 2eme graphe
eclaire=np.vectorize(eclairement)
xmax=3.5
x=np.linspace(-xmax,xmax,1000)
xprim=2*np.pi*x


plt.plot(x,(eclaire(xprim,N,N)))
plt.xlabel('Déphasage (x 2 pi)')
plt.ylabel('I/I0')
plt.title('Figure de diffraction pour {0} fentes'.format(N))
plt.show()
    
plt.plot(x,(eclaire(xprim,N,N)),label='{0} fentes'.format(N))
plt.plot(x,(eclaire(xprim,Nprim,Nprim)),label='{0} fentes'.format(Nprim))
plt.xlabel('Déphasage (x 2 pi)')
plt.ylabel('I/I0')
plt.legend()
plt.title('Figure de diffraction pour {0} et {1} fentes'.format(N,Nprim))
plt.show()



def eclairement2(phi,n,norm,ratio):
    return (np.sinc(phi*ratio/2))**2*(np.sin(n*phi/2)/(norm*np.sin(phi/2)))**2

N=2#Nombre de fentes pour le 1er graphe
Nprim=10#Nombre de fentes pour le 2eme graphe
eclaire2=np.vectorize(eclairement2)
xmax=10.5
x=np.linspace(-xmax,xmax,1000)
xprim=2*np.pi*x

     
ratio=0.05#rapport des dimensions des fentes b/a        
plt.plot(x,eclaire2(xprim,N,N,ratio))
plt.xlabel('Déphasage (x 2 pi)')
plt.ylabel('I/I0')
plt.title('Figure de diffraction pour {0} fentes'.format(N))
plt.show()

ratio=0.05#b/a        
plt.plot(x,eclaire2(xprim,N,N,ratio),label='{0} fentes'.format(N))
plt.plot(x,eclaire2(xprim,Nprim,Nprim,ratio),label='{0} fentes'.format(Nprim))
plt.xlabel('Déphasage (x 2 pi)')
plt.ylabel('I/I0')
plt.title('Figure de diffraction pour {0} et {1} fentes'.format(N, Nprim))
plt.legend()
plt.show()





