import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate
from matplotlib.widgets import Slider

#Ce script est conçu pour l'étude de la cascade sous-harmonique du pendule amorti et forcé
#Il trace les solutions en fonction du temps, le portrait de phase, et la section de poincaré, pour une excitation réglable avec un slider

#Cette simulation a été inspirée de celle réalisée dans "Mécanique Classique", de John R. Taylor

#Donnees---------------------------------------

t_min = 50 #le regime permanent doit etre atteint avent cet instant, utile pour la section de poincaré
t_max = 100 #le calcul n'ira pas au dela de cet instant
"""
t_min = 10 #le regime permanent doit etre atteint avent cet instant, utile pour la section de poincaré
t_max = 60000 #le calcul n'ira pas au dela de cet instant
"""
pas_de_calcul = 0.01
t = np.arange(0,t_max,step=pas_de_calcul)
periode = int(1/pas_de_calcul) #la période supposée de l'oscillateur, un nombre entier, en unité du pas de calcul (si vous multipliez ce nombre par le pas de calcul vous avez la période), elle détermine quels seront les points relevés pour le diagramme

tracer_a_partir_de = 7000 #on ignore tous les points avant celui-ci lors du tracé, utile pour tracer uniquement l'état stationnaire

excitation_min = 1.04
excitation_max = 1.1
excitation_init = 1.04

#Systeme d'equations a resoudre-----------------

assert type(periode) == int

"""
La fonction sys doit renvoyer une liste contenant
la dérivée de x et celle de x'
Pour l'oscillateur harmonique le retour est donc [x',-x]
"""

def sys(y,t,excitation=1.07):
    x, xprime = y

    #Les valeurs sont celles prises dans "Mécanique Classique", de John R. Taylor, avec ces valeurs la cascade sous-harmonique se situe entre 1.066 et 1.083
    omega = 2*np.pi #pulsation d'excitation
    omega0 = 1.5*omega #pulsation propre
    beta = omega0/4 #coefficient d'amortissement
    return [xprime, -2*(beta)*xprime -(omega0**2)*np.sin(x) + excitation*(omega0**2)*np.cos(omega*t)] #Pendule amorti et forcé

#Liste de conditions initiales-------------------

"""
Les conditions initiales sont sous la forme [x(0),x'(0)]
"""

y0 = [-np.pi/2,0.0]

#Integration par le solveur odeint---------------------------------

excitation = 0.9

sol = scipy.integrate.odeint(sys,y0,t,args=(excitation_init,))

poincare = []
i=periode
for index in range(len(t)):
    if t[index]<t_min:
        continue
    if t[index]>t_max:
        break
    if i/periode==1: #on sélectionne les points espacés d'une période
        poincare.append((sol[index,0],sol[index,1]))
        i=0
    i+=1

#Affichage---------------------------------------------

start = tracer_a_partir_de
#sol = solution[0]

fig = plt.figure()
plt.subplots_adjust(bottom=0.20)

ax1 = plt.subplot(131)
line1, = plt.plot(t[start:],sol[start:,0]) #pour tracer la solution en fonction du temps
plt.xlabel("Temps")
plt.ylabel("Position")
plt.title("Solution de l'equation")
plt.ylim((-np.pi,np.pi))

ax2 = plt.subplot(132)
line2, = plt.plot(sol[start:,0],sol[start:,1]) #pour tracer le portrait de phase
plt.xlabel("Position")
plt.ylabel("Vitesse")
plt.xlim((-np.pi,np.pi))
plt.ylim((-25,25))
#plt.axis('equal')
plt.grid()
plt.title("Portrait de phase")

ax3 = plt.subplot(133)
line3, = plt.plot(*zip(*poincare),marker='+',ms=5,ls='')
plt.xlabel('Position')
plt.ylabel('Vitesse')
plt.xlim((-np.pi,np.pi))
plt.ylim((-30,30))
plt.grid()
plt.title("Section de Poincaré")


#Slider d'excitation
axExc = plt.axes([0.20,0.08,0.65,0.03])
sExc = Slider(axExc, 'Excitation', valmin=excitation_min, valmax=excitation_max, valinit=excitation_init)
sExc.valfmt = u'%1f'
sExc.set_val(excitation_init)
def update(val):
    excitation = sExc.val
    sol = scipy.integrate.odeint(sys,y0,t,args=(excitation,))
    poincare = []
    i=periode
    for index in range(len(t)):
        if t[index]<t_min:
            continue
        if t[index]>t_max:
            break
        if i/periode==1: #on sélectionne les points espacés d'une période
            poincare.append((sol[index,0],sol[index,1]))
            i=0
        i+=1
    line1.set_ydata(sol[start:,0])
    line2.set_xdata(sol[start:,0])
    line2.set_ydata(sol[start:,1])
    line3.set_data(*zip(*poincare))
sExc.on_changed(update)


plt.show()
