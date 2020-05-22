 
################################################################################
############################ VENTS GEOSTROPHIQUES ##############################
################################################################################


## Importation


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as ani

import scipy.optimize as opt
from scipy.interpolate import interp1d
from scipy import misc

from matplotlib.widgets import Slider, Button, RadioButtons, CheckButtons

## Physique du probleme et plan du code

# Le but ici est de decrire les vents terrestres geostrophiques dus à la force
# de Coriolis. Les calculs et les formules présentees peuvent etre trouves dans
# le livre Physique PC Tout le programme 2014 sous forme d exercices corriges
# edition Pearson page 68 et suivantes.

# On commence par appliquer l equation de Navier Stokes a l atmosphere dans un
# repere cartesien. Ce repere est appele repere meteorologique et il s agit d un
# repere cartesien qui coincide avec le repere spherique et permet de decrire 
# localement les vents.

# On soustrait le poids et la pression d equilibre avec l equilibre 
# hydrostatique. Il ne reste alors que deux equations pour la pression qui sont 

# v_x = -(1/rho*f)dP/dy
# v_y = 1/(rho*f)dP/dx

# avec f=2*Omega*sin(lambda) le parametre de Coriolis, Omega la vitesse de
# rotation de la Terre sur elle meme selon un axe K donne et fixe
# et lambda la latitude.

# On peut effectuer un changement de coordonnées. On repere desormais un point
# par lambda defini comme precedemment, r qui est le meme r que le repere
# spherique et un autre angle alpha qui sera l angle entre un axe A fixe,
# orthogonal et l axe R=OM.
# L interet est de considerer des grands cercles pour pouvoir exploiter
# l invariance de la pression par rapport a alpha (en premiere approx.).
# On a alors : dx = R_T dlambda et dy = R_T dalpha. On obtient :

# v_x = 0 (car dP/dalpha=0)
# v_y = 1/(rho*f*R_T)dP/dphi
# avec R_T le rayon terrestre
# attention dphi = -dlambda

# Le code commence par retranscrire le profil de pression donne p.70 de la
# reference. Il fait ensuite un ajustement sinusoidale (en premiere approx.)
# pour obtenir des valeurs de pression. Il calcule ensuite v_y grace a la
# formule precedente et trace enfin le resultat obtenu.


## Constantes du probleme

R_T = 6400000 # en m
rho = 1.225 # en kg.m^(-3)
Omega = 2*np.pi/(24*3600) # en s^(-1)

def f(x):
    f = 2*Omega*np.sin(x*np.pi/180)
    return(f)


## Pression atmospherique : equation sinusoidale obtenue par un test du chi2


# Valeurs de la pression recuperees d apres le graphe de la reference p.70

rapport_pression = 40/2 # HPa par cm
rapport_lambda = 90/4.2 # degre par cm

pression_cm = np.array([1.9 , 1.7 , 1. , 0.25 , 0.75 , 1.35 , 2.2 , 2.05 , 1.])
lambda_cm = np.array([0. , 0.5 , 1. , 1.5 , 2. , 2.5 , 3. , 3.5 , 4.2])

err_pression = 1/100 # pourcentage d erreur sur les valeurs (arbitraire)
err_lambda = 1/100 # idem

pression_err = rapport_pression*np.sqrt((np.array([0.05 , 0.05 , 0.05 , 0.05 , 0.05 , 0.05 , 0.05 , 0.05 , 0.05])*(1/np.sqrt(3)))**2+(err_pression*pression_cm)**2)
lambda_err = rapport_lambda*np.sqrt((np.array([0.05 , 0.05 , 0.05 , 0.05 , 0.05 , 0.05 , 0.05 , 0.05 , 0.05])*(1/np.sqrt(3)))**2+(err_lambda*lambda_cm)**2)

pression = 990+rapport_pression*pression_cm # la pression est en hPa ici
lambda_deg = (4.2-lambda_cm)*rapport_lambda

#plt.errorbar(lambda_deg,pression,xerr=lambda_err,yerr=pression_err) # Permet d'afficher les donnees de la pression
#plt.show()

freq = 1/75 # par degre

# Ajustement par un sinus. Modele : P(lambda) = P_0*sin(lambda*2*pi*freq+phi)+P_1

def chi2(x): # test du chi2
    
    P_0 = x[0]
    P_1 = x[1]
    phi = x[2]
    freq_t = x[3]
    
    pression_modele = P_0*np.sin(lambda_deg*2*np.pi*freq_t+phi)+P_1
    
    chi2 = sum(((pression_modele-pression)/pression_err)**2)
    
    return(chi2)

x0 = np.array([15,1010,0.1,1/75]) # choix initial (arbitraire)

result = opt.minimize(chi2,x0,method='Powell') # resultat de l ajustement

#print(result)
#print(chi2(result.x)) # Lignes utiles pour voir la valeur du test du chi2

def pression_1(x): # Formule donnant la pression dans le cadre de ce modele
    
    pression_aux = result.x[0]*np.sin(2*np.pi*result.x[3]*x+result.x[2])+result.x[1]
    
    return(pression_aux)


# x = np.linspace(0,90,100) # Permet d'afficher la pression
# plt.plot(x,pression_1(x))
# plt.show()


## Pression atmospherique : equation obtenue par interpolation


pression_2 = interp1d(lambda_deg, pression, kind='cubic')

# x=np.linspace(0,90,100) # Permet d'afficher la pression
# plt.plot(x,pression_2(x))
# plt.show()


## Calcul de la vitesse v_y


# Choix du modele # Cette partie permet de choisir le modele de pression pour l animation et la carte de vitesse en couleur

print("Indiquez le modele choisi pour la pression : 0 pour le modele sinusoidal ou 1 pour l interpolation")

modele = float(input())

if modele == 0:
    
    pression_def = pression_1

else:
    
    pression_def = pression_2

# Calcul des vitesses

Nbpts = 80
dlambda = 90*np.pi/(Nbpts*180) # il faut repasser en radian

lambda_val = np.linspace(10,89,Nbpts) # le 10 evite la divergence, le modele ne convient plus dans ce cas (proche de l equateur)
# le 89 est là pour pouvoir utiliser le modele d interpolation sans sortir des valeurs accessibles de lambda

pression_tab = pression_def(lambda_val)

dPdlambda = [(pression_tab[2]-pression_tab[0])/(2*dlambda)]

for i in range(1,Nbpts-1):
    
    aux = (pression_tab[i-1]-pression_tab[i+1])/(-2*dlambda)
    dPdlambda.append(aux)

dPdlambda.append((pression_tab[Nbpts-1]-pression_tab[Nbpts-3])/(2*dlambda))

# calcul de la vitesse en fonction de lambda

v_x = 0
v_y = -(1/(rho*f(lambda_val)*R_T))*dPdlambda*100 #*100 pour avoir la pression en Pa
# attention, le signe moins vient de dphi = -dlambda


# en termes de fonctions

# Pour la pression voulue

def dPdlambda_f(x):
    return(misc.derivative(pression_def,x))

def v_y_f(x):
    return((-1/(rho*f(x)))*dPdlambda_f(x)*(1/R_T)*100*180/np.pi)

# Pour chaque modèle de pression

def dPdlambda_f_1(x):
    return(misc.derivative(pression_1,x))

def v_y_f_1(x):
    return((-1/(rho*f(x)))*dPdlambda_f_1(x)*(1/R_T)*100*180/np.pi)
    
def dPdlambda_f_2(x):
    return(misc.derivative(pression_2,x))

def v_y_f_2(x):
    return((-1/(rho*f(x)))*dPdlambda_f_2(x)*(1/R_T)*100*180/np.pi)

# plt.plot(lambda_val,v_y_f(lambda_val)) # Permet d'afficher la vitesse
# plt.show()

## Carte des vitesses v_y en couleur

# Construit la carte de couleur

tranche = v_y

trac = np.array([])

for i in range(2*Nbpts):
    trac = np.concatenate((trac,tranche))

trac=np.reshape(trac,(2*Nbpts,Nbpts))

trac = np.transpose(trac)

## Trace final

x = np.linspace(10,89,100)

fig = plt.figure()

plt.subplot(221)

plt.errorbar(pression,lambda_deg,yerr=pression_err,xerr=lambda_err,c='cornflowerblue',label="Valeurs expérimentales")
plt.plot(pression_1(x),x, c='darkorange',label="Modèle sinusoïdal")
plt.plot(pression_2(x),x, c='forestgreen', label = "Modèle par interpolation")
plt.xlabel("Pression $P$ (hPa)")
plt.ylabel("Latitude $\lambda$ (°)")
plt.title("Pression en fonction de la latitude")
plt.legend()



plt.subplot(223)

plt.plot(v_y_f_1(x),x, c='darkorange', label="Modèle sinusoïdal")
plt.plot(v_y_f_2(x),x, c='forestgreen', label="Modèle par interpolation")
plt.xlabel("Vitesse $v_y$ (m.s$^{-1}$)")
plt.ylabel("Latitude $\lambda$ (°)")
plt.title("Vitesse $v_y$ en fonction de la latitude")
plt.legend()

plt.subplot(224)

plt.imshow(trac)
plt.colorbar()
plt.xlabel("Longitude $\Theta$ (°)")
plt.ylabel("Latitude $\lambda$ (°)")
plt.title("Vitesse $v_y$ (m.s$^{-1}$) en fonction de $(\Theta , \lambda)$")

plt.show()


## Animation
 

# Animation

# Set up pour l animation

fig = plt.figure()

ax = plt.axes(xlim=(0, 180), ylim=(0, 90))
dot, = ax.plot([5], [5], 'ro')
 
axcolor = 'lightgoldenrodyellow'
axlambda = plt.axes([0.25, 0.1, 0.65, 0.03], axisbg=axcolor)
slambda = Slider(axlambda, '$\lambda$ (°)', 0, 90.0, valinit=45)

# initialisation

def init():
    return dot,


# fonction animation

def animate(i):
    lambda_p = slambda.val
    test = dot.get_xdata()[0] + v_y_f(lambda_p)*(1/(R_T))
    if test <0:
        new_x = 180
    else:
        if test > 180:
            new_x = 0
        else :
            new_x = dot.get_xdata()[0] + R_T*v_y_f(lambda_p)*1/(R_T)
    new_y = lambda_p 
    dot.set_data([new_x], [new_y])
    return dot,

## Attention, l'axe des ordonnées est inversé!!! (ce n'est pas grave mais il faut le savoir).

# generation de l animation

anim = ani.FuncAnimation(fig, animate, init_func=init,
                               frames=500, interval=20, blit=False)

plt.xlabel("Longitude $\Theta$ (°)")
plt.ylabel("Latitude $\lambda$ (°)")
plt.title("Vitesse $v_y$ en fonction de $(\Theta , \lambda)$")
plt.show()
# Les légendes et le titre s'affichent autour du slider, il suffit de commenter les 3 lignes précédentes
# sauf le plt.show() pour les enlever

# Pour avoir un affichage + joli, on peut déplacer l'animation sur la place laissée vide dans la figure générée juste avant

# Quand on ferme les images, une ligne d'erreur apparaît, mais elle n'est pas importante.
