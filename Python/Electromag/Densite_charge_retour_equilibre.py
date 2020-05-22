'''
Ce programme trace l'évolution de la densité de charge au cours du temps
dans un milieu conducteur soumis à un échelon de champ électrique.
Les valeurs sont exprimées dans des unités arbitraires.
'''

from pylab import *
from matplotlib import pyplot as plt

tau=10
wp=1

temps=linspace(0,100,1000)
rho=[exp(-t/tau)*cos(wp*t) for t in temps]
env1=[exp(-t/tau) for t in temps]
env2=[-exp(-t/tau) for t in temps]

plt.figure()
plt.title("Densite de charge en fonction du temps")
plt.xlabel('$t$ (s)')
plt.xticks( [0, 20, 40, 60, 80, 100],
            [r'0',r'$2\tau$',r'$4\tau$',r'$6\tau$',r'$8\tau$',r'$10\tau$'])
plt.ylabel(r'$\rho/\rho_0$')
plt.ylim([-1,1])

plt.plot(temps,rho,color='b')
plt.plot(temps,env1,ls='dashed',color='r')
plt.plot(temps,env2,ls='dashed',color='r')


plt.show()
