## Ce code calcule la capacité thermique d'un système à plusieurs niveaux d'énergie
## en utilisant le facteur de Boltzmann comme probabilité.
## Ce code provient de : http://www.f-legrand.fr/scidoc/docimg/sciphys/physistat/boltzmann2/boltzmann2.html

from matplotlib.pyplot import *
import numpy


import math
import random

## Définition de fonctions utilisées par la suite, rien à changer ici.

class Particules:
    def __init__(self,N,M):
        self.N = N
        self.M = M
        self.etats_particules = numpy.zeros(N)
        self.energies_particules = numpy.zeros(N)
        self.niveaux_energie = numpy.arange(1,M+1)
        self.sommes_energies = numpy.zeros(N)
        self.somme_E = 0.0
        self.sommes_energies_2 = numpy.zeros(N)
        self.somme_E_2 = 0.0
        self.compteur = 0
        self.n_rejets = 0
                    
    def initialiser_sommes(self):
        for k in range(self.N):
            self.sommes_energies[k] = 0.0
            self.sommes_energies_2[k] = 0.0
        self.somme_E = 0.0
        self.somme_E_2 = 0.0
        self.compteur = 0
                    
    def nouvel_etat(self):
        k = random.randrange(self.N)
        rejet = True
        while rejet:
            i = random.randrange(self.M)
            e = self.niveaux_energie[i]
            if random.random() < math.exp(-self.beta*e):
                rejet = False
                self.etats_particules[k] = i
                self.energies_particules[k] = e
            else:
                self.n_rejets += 1

                     
    def sommes(self):
        for k in range(self.N):
            e = self.energies_particules[k]
            self.sommes_energies[k] += e
            self.sommes_energies_2[k] += e*e
        E = numpy.sum(self.energies_particules)
        self.somme_E += E
        self.somme_E_2 += E*E
        self.compteur += 1
               
                      
    def iterations(self,n1,n2,T,methode="directe"):
        self.n_rejets = 0
        self.beta = 1.0/T
        self.exp = math.exp(-self.beta)
        if methode=="directe":
            for i in range(n1):
                for j in range(n2):
                    self.nouvel_etat()
                self.sommes()
        elif methode=="metropolis":
            for i in range(n1):
                for j in range(n2):
                    self.nouvel_etat_metropolis()
                self.sommes()
        
        moy_E = self.somme_E/self.compteur
        var_E = self.somme_E_2/self.compteur-moy_E**2
        ecart_E = math.sqrt(var_E)
        print("Systeme : E = %f, dE = %f, dE/E = %f"%(moy_E,ecart_E,ecart_E/moy_E))
        moyennes_energies = self.sommes_energies/self.compteur
        moy_e = numpy.mean(moyennes_energies)
        moyennes_energies_2 = self.sommes_energies_2/self.compteur
        var_e = numpy.mean(moyennes_energies_2)-moy_e**2
        ecart_e = math.sqrt(var_e)
        print("Particule : e = %f, de = %f, de/e = %f"%(moy_e,ecart_e,ecart_e/moy_e))
        taux_rejet = self.n_rejets*1.0/(n1*n2)
        print("Taux de rejet : %f"%(taux_rejet))
        return (moy_E,ecart_E,taux_rejet)

                     
    def nouvel_etat_metropolis(self):
        k = random.randrange(self.N)
        i = int(self.etats_particules[k])
        delta_i = 0
        if i==0:
            delta_i = 1
        elif i==self.M-1:
            delta_i = -1
        else:
            if random.randint(1,2)==1:
                delta_i = -1
            else:
                delta_i = 1
        
        j = i+delta_i
        dE = self.niveaux_energie[j]-self.niveaux_energie[i]
        if dE <= 0.0:
            self.etats_particules[k] = j
            self.energies_particules[k] = self.niveaux_energie[j]
        else:
            if random.random() < self.exp:
                self.etats_particules[k] = j
                self.energies_particules[k] = self.niveaux_energie[j]
      

from particules import Particules

## 2 algorithmes sont proposés. Le premier "courbe_T" fonctionne très bien.

def courbe_T(N,M,nT,n1,n2):
    particules = Particules(N,M)
    T= numpy.arange(1,nT+1)*0.5
    E = numpy.zeros(nT)
    dE = numpy.zeros(nT)
    rejet = numpy.zeros(nT)
    for k in range(nT):
        print("T = %f"%T[k])
        (E[k],dE[k],rejet[k])=particules.iterations(n1,n2,T[k],"directe")
        particules.initialiser_sommes()
    figure()
    #subplot(211) ## Ces lignes contrôlent l'affichage, on peut changer ici des paramètres pour mettre un titre, des légendes, etc.
    errorbar(T,E,yerr=dE,fmt=None)
    plot(T,E,'o')
    axis([0,numpy.max(T),0,numpy.max(E)*2])
    xlabel("T")
    ylabel("E")
    grid()
    #subplot(212)
    #plot(T,rejet,'o')
    xlabel('T')
    #ylabel('rejet')
    grid()

def courbe_T_metropolis(N,M,nT,n1,n2):
    particules = Particules(N,M)
    T= numpy.arange(1,nT+1)*0.5
    E = numpy.zeros(nT)
    dE = numpy.zeros(nT)
    for k in range(nT):
        print("T = %f"%T[k])
        particules.iterations(n1,n2,T[k],"metropolis")
        (E[k],dE[k],rejet)=particules.iterations(n1,n2,T[k],"metropolis")
        particules.initialiser_sommes()
    figure()
    errorbar(T,E,yerr=dE,fmt=None)
    plot(T,E,'o')
    axis([0,numpy.max(T),0,numpy.max(E)*2])
    xlabel("T")
    ylabel("E")
    grid()

                  

## Paramètres à changer :
## N nombre de particules, M nombre de niveaux, nT température
## ces paramètres sont les seuls à changer éventuellement.

N=1
M=2
nT=20
n1=2000
n2=100

## On choisit l'algorithme utilisé en fonction de la fonction qu'on appelle.
# une ligne d'erreur apparaît après que le code a tourné mais ça n'est rien de grave
# il suffit ensuite de faire show() pour avoir la courbe

courbe_T(N,M,nT,n1,n2)


#courbe_T_metropolis(N,M,nT,n1,n2)$

