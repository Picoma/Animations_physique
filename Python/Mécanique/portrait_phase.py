import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate
from math import *

#Ce script trace le portrait de phase
#d'un oscillateur 1D

#On peut également s'en servir pour tracer les solutions
#en fonction du temps

"""
Les lignes que peut changer l'utilisateur sont les suivantes :
    -Le nombre de pas d'integration et le temps final
    -L'équation du mouvement à intégrer, en modifiant la fonction sys
    -La condition initiale, en modifiant y0
    -Le tracé au choix du portrait de phase ou de la solution en fonction du temps, en modifiant le booleen tracer_portrait_phase
"""

#Donnees---------------------------------------

nombre_pas = 20000
t_final = 300
t = np.linspace(0,t_final,num=nombre_pas)

tracer_portrait_phase = True

#Systeme d'equations a resoudre-----------------

"""
La fonction sys doit renvoyer une liste contenant
la dérivée de x et celle de x'
Pour l'oscillateur harmonique le retour est donc [x',-x]
"""

def sys(y,t):
    x, xprime = y

    #changer la ligne suivante pour un oscillateur different
    return [xprime, -x] #oscillateur harmonique
    #return [xprime, -x-0.1*xprime] #oscillateur harmonique amorti
    #return [xprime, -np.sin(x)-0.1*xprime] #pendule simple amorti
    #return [xprime, (0.2-x**2)*xprime -x] #oscillateur de Van der Pol

#Liste de conditions initiales-------------------

"""
Les conditions initiales sont sous la forme [x(0),x'(0)]
y0 est un tableau devant contenir autant de conditions
initiales qu'il y a de portraits de phase a tracer
exple : pour 3 courbes y0 = [[10,0],[10,2],[8,5]]
"""

y0 = [[1.5,1.5],[1.5,1.],[-6.,2.5],[-6,1]]
#y0 = [[-np.pi/2,0.0],[-np.pi/2+0.01,0.0]]

#Integration par le solveur odeint---------------------------------

solution = []
for ci in y0:
    solution.append(scipy.integrate.odeint(sys,ci,t))

#Affichage---------------------------------------------

for sol in solution:
    if tracer_portrait_phase:
        plt.plot(sol[:,0],sol[:,1]) #pour tracer le portrait de phase
    else:
        plt.plot(t[3000:6000],sol[3000:6000,0]) #pour tracer la solution en fonction du temps
plt.xlabel("Position")
plt.ylabel("Vitesse")
plt.axis('equal')
plt.grid()
plt.title("Portrait de phase")

#plt.xlim((-2*np.pi,2*np.pi))

plt.show()
