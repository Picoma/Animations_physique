## Ce code trace la capacité thermique d'un système à plusieurs niveaux d'énergie en utilisant les formules qu'on démontre
## avec l'ensemble canonique. Il provient de : http://www.f-legrand.fr/scidoc/docimg/sciphys/physistat/boltzmann2/boltzmann2.html

from matplotlib.pyplot import *
import numpy


def moy_e(M,T):
    return 1.0/(numpy.exp(1.0/T)-1)-M/(numpy.exp(M/T)-1)
    
def var_e(M,T):
    return numpy.exp(1.0/T)/(numpy.exp(1.0/T)-1)**2-M**2*numpy.exp(-M/T)/(1-numpy.exp(-M/T))**2
    
def ecart_e(M,T):
    return numpy.sqrt(var_e(M,T))
    
def Cv(M,T):
    return var_e(M,T)/T**2

# Les fonctions précédentes calculeront les valeurs des différentes fonctions

# M contrôle le nombre de microétats et T la température (on trace en fonction de T).

M=2
T = numpy.linspace(0.01,10,100)
figure()
e1 = moy_e(M,T)
de1 = ecart_e(M,T)
plot(T,e1)
errorbar(T,e1,yerr=de1/2,ecolor='r',fmt=None)
xlabel("T")
ylabel("e moyenne d'1 particule pour M={} microétats".format(M))
grid()

#cv1 = Cv(M,T)
# #figure()
#plot(T,cv1)
#xlabel("T")
#ylabel("Cv")
#grid()

show()