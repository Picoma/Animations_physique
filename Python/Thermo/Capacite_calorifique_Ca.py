## Ce code trace la capacit� thermique d'un syst�me � plusieurs niveaux d'�nergie en utilisant les formules qu'on d�montre
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

# Les fonctions pr�c�dentes calculeront les valeurs des diff�rentes fonctions

# M contr�le le nombre de micro�tats et T la temp�rature (on trace en fonction de T).

M=2
T = numpy.linspace(0.01,10,100)
figure()
e1 = moy_e(M,T)
de1 = ecart_e(M,T)
plot(T,e1)
errorbar(T,e1,yerr=de1/2,ecolor='r',fmt=None)
xlabel("T")
ylabel("e moyenne d'1 particule pour M={} micro�tats".format(M))
grid()

#cv1 = Cv(M,T)
# #figure()
#plot(T,cv1)
#xlabel("T")
#ylabel("Cv")
#grid()

show()