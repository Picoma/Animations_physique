# Programme simulant la diffusion de N particules initialement en x=0 par marche aléatoire. Peut également afficher la solution (gaussienne) de l'équation de diffusion correspondant. (modele = True ou False)

#contact : clement.pelletmary@gmail.com

from math import sqrt,exp
import numpy as np
import matplotlib.pyplot as plt
import random as rand
import matplotlib.animation as animation


N0=5000 # nombre de particules initiales
n=100 #nombre d'étapes
dt=1 #pas de temps entre chaque étape (s.)
lpm=1 #distance parcourue à chaque étape (m.)
D=lpm**2/(8*dt) #sigma loi binomiale = sqrt(n/4)*lpm 
# et sigma de la diffusion = sqrt(2*D*t) avec t=n*dt
modele=True #afficher le modèle gaussien ou non


absc=np.linspace(-n/2*lpm,n/2*lpm,num=n+1)
fig,ax=plt.subplots()
plt.xlabel('distance (m)')
plt.ylabel('densité particulaire (m-1)')
binom,=ax.plot(absc,absc,'d')
gauss,=ax.plot(absc,np.zeros(n+1))

plt.xlim(-5*sqrt(n/4)*lpm,5*sqrt(n/4)*lpm) #limites en abscisse à 5 sigma de la valeur finale
plt.ylim(0,N0/lpm)

pos=np.full(N0,n)





def update(k) :
    plt.title('Distribution pour t='+str(n*dt)+'s.')
    if k==0 :
        for j in range(N0) :
            pos[j]=n
    for j in range(2) :
        histo=np.zeros(2*n+1)
        for i in range(N0) :
            if rand.random() < 0.5 :
                pos[i]=pos[i]+1
            else :
                pos[i]=pos[i]-1
            histo[pos[i]]=histo[pos[i]]+1
    histo2=np.zeros(n+1)
    for i in range(n+1) :
        histo2[i]=histo[2*i]
    binom.set_ydata(histo2)
    theo=np.zeros(n+1)
    for i in range(n+1) :
        theo[i]=N0/(sqrt(4*np.pi*D*2*(k+1)*dt))*exp(-(absc[i])**2/(4*D*2*(k+1)*dt))
    if modele :
        gauss.set_ydata(theo)
    return [binom,gauss]


theo=np.zeros(n+1)
for i in range(n+1) :
    theo[i]=N0/(sqrt(4*np.pi*D*n*dt))*exp(-(absc[i])**2/(4*D*n*dt))
    
    
ani = animation.FuncAnimation(fig, update, n//2,interval=100, blit=False, repeat=True)

plt.show()
    
    