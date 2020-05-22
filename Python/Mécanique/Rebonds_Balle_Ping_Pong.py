import math
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as spo
"""
Ce programme a pour but d affiche des graphiques qui correspondent au temps entre deux rebonds d une balle.
On veut determiner le coefficient de restitution de la balle grace a Delta_t = (2*v_0*e**i)/g. On va donc tracer ln(Delta_t) en fonction de i.

Entrées : - nb_rebonds : nombre de rebonds étudiés à chaque expérience
          - tps_rebonds : relevés des temps de chaques rebonds pour chaques expériences
          - u_temps : incertitude sur le relevé du temps du rebond
          -conditions_exp : pour afficher sur le graphe sur quel matérieau a été réalisé l'expérience

Sortie = - Figure donnant les données, la régression linéaire et les paramètres associés pour chaque expériences

"""


# Indice de temps avec 0 le debut de l'experience
nb_rebonds = 8 


# rebond[i][j] contient le jeme rebond de l'experience i+1. rebond[0][i] est le debut de l'experience i
tps_rebond = [[-1.452,-1.247, -1.055, -0.8720, -0.6990, -0.5370, -0.3820, -0.2370], #temps_rebonds
         [0, 0.4840, 0.9160, 1.3, 1.644, 1.956, 2.240, 2.498]]
         #[0, 0.4840, 0.9160, 1.3, 1.644, 1.956, 2.240, 2.498]]
conditions_exp =['bureau','sol']

u_temps = 0.001 #incertitude sur le temps indiqué

num_rebonds = [i for i in range(1,nb_rebonds)] 
delta = [[0] * (len(experience_i) - 1) for experience_i in tps_rebond] # delta[i][j] contient la difference de temps entre le rebond j et j+1 de l experience i+1.
# delta a donc un indice de moins que rebond pour chaque experience
ln_delta = [[0] * (len(experience_i) - 1) for experience_i in tps_rebond] # Pour obtenir ln_delta on a appliquer le log a tous les elements de delta
uy = [0]*len(num_rebonds) #on crée une liste pour contenir les incertitudes sur ln(Delta t)
u_delta=2*u_temps # incertitude sur la mesure d'un Delta t

# Double boucle sur les experiences puis chaque rebond et on calcul Delta t, son logarithme et l'incertitude associée
for ind_exp in range(len(tps_rebond)):
    for ind_temps in range(len(tps_rebond[ind_exp]) - 1):
        delta[ind_exp][ind_temps] = tps_rebond[ind_exp][ind_temps + 1] - tps_rebond[ind_exp][ind_temps]
        ln_delta[ind_exp][ind_temps] = math.log(delta[ind_exp][ind_temps])
        uy[ind_temps] = u_delta/delta[ind_exp][ind_temps] #propagation des incertitudes
        
    # donnees que l'on va tracer
    y = np.array(ln_delta[ind_exp])
    x = np.array(num_rebonds)
    
    # incertitudes types
    ux = 0
    uy2 = np.array(uy)

    # fonction f decrivant la courbe a ajuster aux donnees
    def f(x,p):
            a,b = p
            return a*x+b

    # derivee de la fonction f par rapport a la variable x
    def Dx_f(x,p):
            a,b = p
            return a

    # fonction d'ecart ponderee par les erreurs
    def residual(p,y,x):
            return (y-f(x,p))/np.sqrt(uy2**2 + (Dx_f(x,p)*ux)**2)

    # estimation initiale des parametres
    p0 = np.array([0,0])

    # moindres carrees non-lineaires
    result = spo.leastsq(residual,p0, args=(y,x), full_output=True)

    # parametres d'ajustement optimaux
    popt = result[0]

    # incertitudes-types sur ces parametres
    uopt = np.sqrt(np.abs(np.diagonal(result[1])))

    # graphique
    fig1 = plt.figure(1)
    # Titre general a tous les subplot
    st1 = fig1.suptitle("Coefficient de resititution d'une balle de ping-pong", fontsize="x-large")
    # Indique ou on va placer la figure dans le subplot
    axi = fig1.add_subplot(1,len(tps_rebond),ind_exp + 1)
    axi.tick_params(labelsize=13)
    axi.plot(np.linspace(min(x)-1,max(x)+1,100),popt[0]*np.linspace(min(x)-1,max(x)+1,100)+popt[1],linewidth=2,color=[0.8,0,0]) #plot la regression linéaire
    plt.errorbar(x, y, xerr=ux, yerr=uy2,fmt='+',capthick=1,linewidth=1.5,ecolor=[0,0.55,0.55],color=[0,0.55,0.55]) #plot les données expériementales + incertitudes

    # labels
    plt.xlabel(r'Rebonds sur le ' +conditions_exp[ind_exp], fontsize=18)
    plt.ylabel(r'$\ln(\Delta t)$', fontsize=18)

    # donnees ajustement
    plt.text(0.3,0.9,r'$\mathrm{R\'egression\ lin\'eaire}\ :\ f(x) = ax+b$',transform = axi.transAxes,fontsize=13)
    plt.text(0.3,0.85,r'$a = {0:.2e} \pm {1:.2e}$'.format(popt[0],uopt[0]),transform = axi.transAxes,fontsize=13)
    plt.text(0.3,0.8,r'$b = {0:.2e} \pm {1:.2e}$'.format(popt[1],uopt[1]),transform = axi.transAxes,fontsize=13)

    # Trois parametre qui evite le chevauchement d ecriture
    fig1.tight_layout()
    st1.set_y(0.95)
    fig1.subplots_adjust(top=0.85)

plt.show(1)


