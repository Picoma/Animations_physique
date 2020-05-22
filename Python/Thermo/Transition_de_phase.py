# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 16:04:40 2017

@author: ENS de Lyon

Ce code traite de la transition de phase d'un fluide de Van der Waals à partir de l'étude du potentiel libre G* dont l'expression ainsi que tout le raisonnement qui suit peuvent être trouvés dans le Diu de thermodynamiquue. Pour cela, le code traite les différentes routines suivantes : 
- Détermination des points de la spinodale, c'est-à-dire des limites de métastabilité de la phase liquide et de la phase vapeur
- Détermination des minima de G* et de la pression de vapeur saturante
- Tracé de G*
- Tracé de la dérivée partielle de G* par rapport au volume pour la détermination de la pression d'équilibre
- Tracé de l'isotherme de Van der Waals à partir de G* et sa dérivée.

Entrées du code : ce sont les paramètres indiqués tout au début du code (a,b) ainsi que certaines pressions de tracé dans la partie du code sur le tracé des courbes.
Sorties du code : pression de vapeur saturante, tracés de G* et de sa dérviée partielle par rapport au volume, le tout en fonction du volume, l'isotherme d'Andrews, et un tracé dynamique de G* en fonction du volume où on peut faire varier la pression.
"""

"""
Importation des bibliothèques utiles.
"""

from tkinter import * # On importe la bibliothèque TKinter qui permet de créer des interfaces graphiques
import matplotlib.pyplot as plt # Bibliothèque de tracé de Python
import numpy as np # Bibliothèque de Python qui gère les tableaux

"""
Paramètres pour les tracés, il est possible de les modifier pour traiter le fluide de son choix (entrée).
"""

R = 8.314 # Constante d'état des gaz parfaits (en J/K/mol)
T = 573.15 # Température de tracé (en Kelvins)
a = 5.537e-1 # Valeur de a pour l'eau (en Pa.m^-6/mol^2) issue du Handbook
b = 0.0305e-3 # Valeur de b pour l'eau (en m^3/mol) issue du Handbook

"""
Détermination des points d'inflexion de G* en fonction de v, c'est-à-dire de la 
fin de la métastabilité d'une des 2 phases.
"""

x=np.roots(np.array([1,-2*a/(R*T),4*a*b/(R*T),-2*a*b**2/(R*T)])) # Détermination des solutions en v qui annulent les dérivées première et seconde de G*, ces dernières sont contenues dans le tableau x et sont solutions du polynôme de degré 3 dont les coefficients sont données par le tableau en argument de la fonction roots.
p=1e-5*(R*T/(x-b)-a/x**2) # Détermination des pressions (en bars) qui assurent la fin de la métastabilité : on les détermine à partir des volumes solutions contenues dans x en utilisant tout simplement l'expression de l'isotherme de Van der Waals 
if len(p[p>0])<2 :
    pplus=np.sort(p[p>0])[-1] # Aux températures usuelles, la phase liquide reste métastable pour toute pression, il n'y a donc qu'une pression solution positive, correspondant à la fin d'une phase vapeur métastable
    metastab_nombre=1 
else :
    pmoins=np.sort(p[p>0])[0] # S'il y a deux solutions positives, la plus basse correspond à la fin de la métastabilité de la phase liquide...
    pplus=np.sort(p[p>0])[-1] # ... et la plus haute la fin de la phase vapeur métastable
    metastab_nombre=2

"""
Détermination des minima de G* et de la pression de vapeur saturante psat.
"""

gmin1=[] # Initialisation de la liste contenant les valeurs des minima de G* pour la phase liquide
gmin2=[] # Initialisation de la liste contenant les valeurs des minima de G* pour la phase gazeuse
if metastab_nombre==1:
    P=np.arange(0.3,pplus,0.1) # Tableau contenant les valeurs des pressions à sonder (en bars) : la phase vapeur ne correspond à un minimum de G* que pour ppplus (c'est la définition de pplus)
else:
    P=np.arange(pmoins,pplus,0.1) # Tableau contenant les valeurs des pressions à sonder (en bars) : les phases liquide et vapeur correspondent toutes les deux à un minimum de G* uniquement entre pmoins et pplus (c'est la définition de ces pressions)
for p0 in P:
    y=np.roots([p0*1e5,-p0*1e5*b-R*T,a,-a*b]) # Détermination des volumes qui correspondent aux extrema de G* et stockage dans le tableau y, pour cela on résout le polynôme de degré 3 dont les coefficients sont contenus dans la liste en argument de la fonction roots.
    y=np.sort(y) # Classement des valeurs de y par valeurs croissantes
    def gmin(v):
        """
        Fonction qui calcule la valeur minimale de G*.
        """
        return b/(v-b)-2*a/(v*R*T)-np.log(v-b)
    gmin1+=[gmin(y[0])] # On enregistre dans la liste la valeur de G* pour la phase liquide (car la phase liquide est de volume molaire moins grand que celui de la phase vapeur)
    gmin2+=[gmin(y[2])] # On enregistre dans la liste la valeur de G* pour la phase vapeur
diffmin=np.array(gmin1)-np.array(gmin2) # On crée le tableau qui contient la différence entre les deux minima
i=np.argmin(np.absolute(diffmin)) # On détermine l'indice qui correspond à la plus petite valeur d'écart entre les deux minima : cela va correspondre à la transition de phase
psat=P[i] # Pression de vapeur saturante à la température T de travail.

"""
Construction des courbes les plus représentatives de G* en fonction de v (sortie).
"""

fig1,ax1=plt.subplots() # Création de la figure et des axes
pliq= 300 # Choix de la pression de tracé pour une phase liquide seule stable (en bars) : on la choisit suffisamment haute (mais elle est modifiable)
pmetaplus=0.5*(pplus+psat) # Choix de la pression de tracé pour une phase liquide stable et une phase vapeur métastable (on la choisit médiane entre la transition de phase et la limite de métastabilité de la phase vapeur)
pvap= 1 # Choix de la pression de tracé pour une phase liquide métastable et une phase vapeur stable (en bars) : on la choisit suffisamment basse (mais elle est modifiable)
if metastab_nombre==2:
    pmetamoins=0.5*(pmoins+psat) # Choix de la pression de tracé pour une phase liquide métastable et une phase vapeur stable dans le cas où la phase liquide n'est pas constamment métastable
v = np.arange(0.0, 110., 0.002) # Création du tableau contenant les volumes molaires en L/mol
gsat = -(np.log(v*1e-3-b)+a/(v*1e-3*R*T)+1)+psat*1e5*v*1e-3/(R*T) # Calcul de G* à la transition de phase en unités de RT
gplus = -(np.log(v*1e-3-b)+a/(v*1e-3*R*T)+1)+pplus*1e5*v*1e-3/(R*T) # Calcul de G* à la fin de la métastabilité de la phase vapeur en unités de RT
gliq = -(np.log(v*1e-3-b)+a/(v*1e-3*R*T)+1)+pliq*1e5*v*1e-3/(R*T) # Calcul de G* pour une phase liquide stable seule à p=pliq
gmetaplus= -(np.log(v*1e-3-b)+a/(v*1e-3*R*T)+1)+pmetaplus*1e5*v*1e-3/(R*T) # Calcul de G* pour une phase liquide stable et une phase vapeur métastable à p=pmetaplus
gvap = -(np.log(v*1e-3-b)+a/(v*1e-3*R*T)+1)+pvap*1e5*v*1e-3/(R*T) # Calcul de G* pour une phase vapeur stable et une phase liquide métastable à p=pvap
if metastab_nombre==2:
    gmetamoins= -(np.log(v*1e-3-b)+a/(v*1e-3*R*T)+1)+pmetamoins*1e5*v*1e-3/(R*T) # Calcul de G* pour une phase liquide métastable et une phase vapeur stable à p=pmetamoins
    gmoins = -(np.log(v*1e-3-b)+a/(v*1e-3*R*T)+1)+pmoins*1e5*v*1e-3/(R*T) # Calcul de G* à la fin de la métastabilité de la phase liquide en unités de RT
ax1.semilogx(v,gliq,label=r'$\mathregular{p_{0}>p_{lim}^{+}}$',color='orange',linewidth=2) # Tracé de G* en fonction de v pour une phase liquide stable seule 
ax1.semilogx(v,gplus,label=r'$\mathregular{p_{0}=p_{lim}^{+}}$',color='crimson',linewidth=2) # Tracé de G* en fonction de v pour la limite de la métastabilité de la phase vapeur
ax1.semilogx(v,gmetaplus,label=r'$\mathregular{p_{sat}<p_{0}<p_{lim}^{+}}$',color='darkcyan',linewidth=2) # Tracé de G* en fonction de v pour une phase liquide stable et une phase vapeur métastable
ax1.semilogx(v,gsat,label=r'$\mathregular{p_{0}=p_{sat}}$',color='limegreen',linewidth=2) # Tracé de G* en fonction de v à la transition de phase
if metastab_nombre==1:
    ax1.semilogx(v,gvap,label=r'$\mathregular{p_{0}<p_{sat}}$',color='dimgray',linewidth=2) # Tracé de G* en fonction de v pour une phase vapeur stable et une phase liquide métastable
if metastab_nombre==2:
    ax1.semilogx(v,gvap,label=r'$\mathregular{p_{0}<p_{lim}^{-}}$',color='dimgray',linewidth=2) # Tracé de G* en fonction de v pour une phase vapeur stable et une phase liquide métastable
    ax1.semilogx(v,gmoins,label=r'$\mathregular{p_{0}=p_{lim}^{-}}$',color='indigo',linewidth=2) # Tracé de G* en fonction de v pour la limite de la métastabilité de la phase liquide (si elle existe)
    ax1.semilogx(v,gmetamoins,label=r'$\mathregular{p_{lim}^{-}<p_{0}<p_{sat}}$',linewidth=2,color='olive') # Tracé de G* en fonction de v pour une phase liquide métastable et une phase vapeur stable
ax1.set_xlabel('Volume molaire (L/mol)',fontsize=18) # Légende de l'axe des abscisses
ax1.set_ylabel('Potentiel G* molaire (en unites de RT)',fontsize=18) # Légende de l'axe des ordonnées
ax1.tick_params(labelsize=18)
ax1.set_ylim(2,10) # Choix des valeurs minimale et maximale sur l'axe des ordonnées
ax1.legend(loc=0,fontsize=18) # Mise en place de la légende
fig1.show() # Affichage de la figure

"""
Tracé de la dérivée partielle de G* en fonction de v à p=psat (sortie).
"""

fig2,ax2=plt.subplots() # Création de la figure et des axes pour le tracé
v = np.arange(0.0, 110., 0.001) # Création du tableau contenant les volumes molaires en L/mol
diffg=psat*1e5/(R*T)-1/(v*1e-3-b)+a/(v**2*1e-6*R*T) # Calcul de la dérivée de G* en fonction de v à p=psat
ax2.semilogx(v,diffg,color='mediumslateblue',linewidth=2,label=r'$\partial\mathregular{ G^{*}/}\partial$v') # Trace la dérivée du potentiel enthalpie libre en fonction du volume molaire à p=psat
ax2.semilogx(v,(psat-pliq)*1e5/(R*T)*np.ones(len(v)),linewidth=2,color='orange',label=r'$\mathregular{(p_{sat}-p_{0})/RT}$ pour $\mathregular{p_{0}>p_{lim}^{+}}$') # Tracé de psat-p0 en unités de RT pour déterminer le volume à l'équilibre quand p0=pliq
ax2.semilogx(v,(psat-pplus)*1e5/(R*T)*np.ones(len(v)),linewidth=2,color='crimson',label=r'$\mathregular{(p_{sat}-p_{0})/RT}$ pour $\mathregular{p_{0}=p_{lim}^{+}}$') # Tracé de psat-p0 en unités de RT pour déterminer le volume à l'équilibre quand p0=pplus
ax2.semilogx(v,(psat-pmetaplus)*1e5/(R*T)*np.ones(len(v)),linewidth=2,color='darkcyan',label=r'$\mathregular{(p_{sat}-p_{0})/RT}$ pour $\mathregular{p_{sat}<p_{0}<p_{lim}^{+}}$') # Tracé de psat-p0 en unités de RT pour déterminer le volume à l'équilibre quand p0=pmetaplus
ax2.semilogx(v,(psat-psat)*1e5/(R*T)*np.ones(len(v)),linewidth=2,color='limegreen',label=r'$\mathregular{(p_{sat}-p_{0})/RT}$ pour $\mathregular{p_{0}=p_{sat}^{+}}$') # Tracé de psat-p0 en unités de RT pour déterminer le volume à l'équilibre quand p0=psat
if metastab_nombre==1:
    ax2.semilogx(v,(psat-pvap)*1e5/(R*T)*np.ones(len(v)),linewidth=2,color='dimgray',label=r'$\mathregular{(p_{sat}-p_{0})/RT}$ pour $\mathregular{p_{0}<p_{sat}}$') # Tracé de psat-p0 en unités de RT pour déterminer le volume à l'équilibre quand p0=pvap avec une phase liquide toujours métastable
if metastab_nombre==2:
    ax2.semilogx(v,(psat-pvap)*1e5/(R*T)*np.ones(len(v)),linewidth=2,color='dimgray',label=r'$\mathregular{(p_{sat}-p_{0})/RT}$ pour $\mathregular{p_{0}<p_{lim}^{-}}$') # Tracé de psat-p0 en unités de RT pour déterminer le volume à l'équilibre quand p0=pvap avec une phase liquide pouvant devenir instable
    ax2.semilogx(v,(psat-pmoins)*1e5/(R*T)*np.ones(len(v)),linewidth=2,color='indigo',label=r'$\mathregular{(p_{sat}-p_{0})/RT}$ pour $\mathregular{p_{0}=p_{lim}^{-}}$') # Tracé de psat-p0 en unités de RT pour déterminer le volume à l'équilibre quand p0=pmoins
    ax2.semilogx(v,(psat-pmetamoins)*1e5/(R*T)*np.ones(len(v)),linewidth=2,color='olive',label=r'$\mathregular{(p_{sat}-p_{0})/RT}$ pour $\mathregular{p_{lim}^{-}<p_{0}<p_{sat}}$') # Tracé de psat-p0 en unités de RT pour déterminer le volume à l'équilibre quand p0=pmetamoins
ax2.set_ylim(-10000,25000) 
ax2.set_xlim(b*1e3,110)
ax2.tick_params(labelsize=18)
ax2.set_xlabel('Volume molaire (L/mol)',fontsize=18)
ax2.set_ylabel(r'$\partial\mathregular{ G^{*}/}\partial$v en unites de RT',fontsize=18)
ax2.legend(loc=0,fontsize=18)
fig2.show()

"""
Construction de l'isotherme de Van der Waals à partir des minima de G* (sortie).
"""

p=np.arange(1.0,300.0,0.1) # Tableau contenant les pressions (en bars) pour le tracé de l'isotherme
v=[] # Création du tableau qui va accueillir les valeurs de volume molaire (en L/mol) pour le tracé des isothermes
pmetaliq=[] # Création du tableau contenant les pressions qui ont des solutions métastables liquides
pmetavap=[] # Création du tableau contenant les pressions qui ont des solutions métastables vapeurs
vmetaliq=[] # Création du tableau contenant les volumes molaires pour les phases liquides métastables
vmetavap=[] # Création du tableau contenant les volumes molaires pour les phases vapeur métastables
for p0 in p:
    y=np.roots([p0*1e5,-p0*1e5*b-R*T,a,-a*b]) # Détermination des volumes qui correspondent aux extrema de G*
    if (metastab_nombre==2 and p0<pmoins):
        v+=[y[0]] # Il n'y a qu'une seule valeur de volume à l'équilibre ici qui correspond à la première valeur du tableau
    elif (p0<psat):
        y=np.sort(y) # On trie les valeurs de volume molaire solutions par valeurs croissantes
        v+=[y[-1]] # La phase la plus stable est la phase vapeur, donc celle de plus grand volume molaire
        pmetaliq+=[p0]
        vmetaliq+=[y[0]] # La phase liquide (de plus faible volume molaire) est métastable
    elif (p0>psat and p0<pplus):
        y=np.sort(y) # On trie les valeurs de volume molaire solutions par valeurs croissantes
        v+=[y[0]] # La phase la plus stable est la phase liquide, donc celle de plus faible volume molaire
        pmetavap+=[p0]
        vmetavap+=[y[-1]] # La phase liquide (de plus grand volume molaire) est métastable
    elif (p0>pplus):
        v+=[y[-1]] # Il n'y a qu'une seule valeur de volume à l'équilibre ici qui correspond à la première valeur du tableau
v=np.real(np.array(v))*1e3 # On passe les volumes molaires en L/mol (la partie réelle sert à faire passer les volumes du type 'complex' au type 'float')
vmetaliq=np.real(np.array(vmetaliq))*1e3 # Idem qu'avant
vmetavap=np.real(np.array(vmetavap))*1e3 # Idem qu'avant
vbrut=np.arange(np.min(v),110.0,0.002) # Tableau contenant les volumes molaires pour le tracé de l'isotherme brute de Van der Waals
pbrut=(R*T/(vbrut*1e-3-b)-a/(vbrut**2*1e-6))*1e-5 # Tableau contenant les pressions calculées directement à partir de l'isotherme de Van der Waals (en bars)
fig3,ax3=plt.subplots() # Construction de la figure et des axes pour le tracé des isothermes
ax3.semilogx(v,p,label='Isotherme reelle', linewidth=2,color='mediumvioletred',linestyle='-')
ax3.semilogx(vmetaliq,pmetaliq,label='Spinodale liquide',linewidth=2,color='olive',linestyle='--')
ax3.semilogx(vmetavap,pmetavap,label='Spinodale vapeur', linewidth=2,color='darkcyan',linestyle='--')
ax3.semilogx(vbrut,pbrut,label='Isotherme brute', linewidth=2,color='k',linestyle='-.')
ax3.legend(loc=0,fontsize=18) 
ax3.set_xlabel('Volume molaire (L/mol)',fontsize=18)
ax3.set_ylabel('Pression (bar)',fontsize=18)
ax3.tick_params(labelsize=18)
ax3.set_ylim(-50,np.max(p))
fig3.show()


""" 
Construction d'une fenêtre dynamique pour le tracé du potentiel G* (sortie).
"""

fenetre = Tk() # On crée la fenêtre principale

p0=DoubleVar() # Crée un widget demandant la pression de tracé du potentiel enthalpie libre molaire (en unités de RT) en fonction du volume molaire v (en L/mol)
scale=Scale(fenetre,variable=p0,from_=0, to=100,resolution=0.1,label='Pression (bars)') # Précise la borne inférieure, supérieure de p0 ainsi que la résolution pour sa variation
fig,ax=plt.subplots() # Crée la figure pour le tracé
def trace_g():
    v = np.arange(0.0, 110., 0.002) # Crée le tableau contenant les valeurs de volume molaire (en L/mol) de la 1ère valeur à la 2ème valeur, le pas étant fixé par la troisième valeur
    R = 8.314 # Constante d'état des gaz parfaits (en J/K/mol)
    T = 373.15 # Température de tracé (en Kelvins) : pour cette température, la pression de vapeur saturante indiquée par le HandBook est de 1.37 bars
    a = 5.537e-1 # Valeur de a pour l'eau (en bar.m^6/mol^2) issue du Handbook
    b = 0.0305e-3 # Valeur de b pour l'eau (en m^3/mol) issue du Handbook
    g = -(np.log(v*1e-3-b)+a/(v*1e-3*R*T)+1)+float(p0.get())*1e5*v*1e-3/(R*T) # Calcul de l'enthalpie libre molaire en unités de RT
    plt.cla() # Permet d'effacer le tracé précédent
    ax.semilogx(v,g,color='mediumvioletred',linewidth=2,label=r'G$^{*}$') # Trace le potentiel enthalpie libre en fonction du volume molaire
    ax.set_xlabel('Volume molaire (L/mol)') # Légende de l'axe des abscisses
    ax.set_ylabel(r'Potentiel G$^{*}$ molaire (en unites de RT)') # Légende de l'axe des ordonnées
    ax.set_ylim(2,10) # Choix des valeurs minimale et maximale sur l'axe des ordonnées
    fig.show() # Affichage de la figure
    fig.canvas.draw()


scale.pack()
b=Button(fenetre,text='TRACER',command=trace_g) # Création du bouton tracé pour lancer le nouveau tracé de G* qui effectue à chaque clic la fonction "trace"
b.pack()

fenetre.mainloop()


