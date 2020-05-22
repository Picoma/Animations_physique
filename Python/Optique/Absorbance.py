#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: ENS de Lyon

Vérification de la loi exponentielle pour l'absorption d'un faisceau laser (ou simplement lumineux) par un liquide

De quoi a besoin le script ?
1/ d'une photo du faisceau absorbé. Attention, le faisceau doit y être horizontal,
2/ d'une photo prise lorsque le faisceau est éteint (image du fond). Attention, ne pas bouger l'appareil photo/webcam entre les 2 photos.
3/ d'une distance horizontale étalon notée D

Que fait le script ? #Et l'utilisateur ?
------Tracé du profil d'intensité---------------------------------
1/  #Renseigner les ### Données ### (noms des images et longueur de l'étalon),
2/  Charge les 2 photos : celle du fond et celle du faisceau,
3/  Soustrait le fond à l'image du faisceau et l'affiche,
4/  #Sélectionner les extrémités de l'étalon sur l'image par simples clics,
5/  #Sélectionner les extrémités du faisceau lumineux par simples clics,
6/  Trace le profil d'intensité le long du faisceau laser pour les trois couleurs de l'image (R, G, B)-> Voir légende,
7/  #Choisir le profil le plus exploitable (ie : qui ressemble le plus à une exponentielle) en tapant R, G ou B suivi de 'Entrée' sur son clavier,
------Ajustement exponentiel du profil choisi----------------------
8/  Affiche le profil choisi,
9/  #Sélectionner les bornes pour l'ajustement par simples clics (sélectionner la zone où on a un profil exponentiel-compatible),
10/ Ajuste la portion de profil sélectionnée par a*exp(-b*x) avec a,b les paramètres à ajuster. 
11/ Trace sur un même graphe : - la portion de profil sélectionnée,
                               - l'exponentielle ajustée,
                               - la valeur des coefficients a,b
                        
Attention : le tracé du profil d'intensité se fait selon l'ordonnée moyenne des 2 extrémités du faisceau. (ie : Si les extrémités du faisceau ont pour coordonnées A=(xA,yA) et B=(xB,yB) alors le tracé se fait selon l'ordonnée (yA+yB)/2). Le faisceau doit donc être le plus horizontal possible sur la photo.

Ce script nécessite des fichiers externes. Il est nécessaire de fournir deux images (voir "De quoi a besoin le script ?").

"""
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
import matplotlib.image as mpimg
import scipy.optimize as spo

#################################################
################# Données  ######################
#################################################
"""A compléter avant tout ! Il n'y a rien d'autre à modifier"""

# nom de l'image du fond
ImageduFond  = 'C2fond.jpg'
# nom de l'image du faisceau laser
Faisceau     = 'C2.jpg'
# Soustraction des images ou non (True/False)
Soustraction = False
# longueur de l'étalon (en m)
D  = 8e-2
# incertitude sur D (en m)
uD = 1e-2
#################################################
#################################################


######################################################################################################################################
######################################################   Script   ####################################################################
######################################################################################################################################
"""Attention : pas de modification nécessaire"""

# Chargement des images
fond  = mpimg.imread(ImageduFond)
laser = mpimg.imread(Faisceau)
## Soustraction des images
if Soustraction:
    Diff = laser-fond
else:
    Diff = laser
## Affichage de l'image soustraite pour sélection de l'étalon puis des extrémités du faisceau
plt.figure(u'Etalonnage de l\'axe horizontal : Choisir les extrémités d\'un étalon \n puis cliquer sur les extrémités du faisceau laser')
plt.imshow(Diff)

print(u'Cliquer sur les extrémités d\'un étalon, puis cliquer sur les extrémités du faisceau laser')
etalon = np.array(plt.ginput(2))   # recupère les coordonnées des points sélectionnés
print(u'Cliquer sur les extrémités du faisceau laser')
position=np.array(plt.ginput(2))
print('Merci !')
plt.close()

## On arrondi à l'unité les coordonnées pour l'étalon et les extrémités du faisceau
position = position.astype(int)
etalon   = etalon.astype(int)

# Etalonnage de l'axe horizontal
DX  = abs(etalon[0,0]-etalon[1,0])  # DX est la longueur en pixel de l'étalon
uDX = 1 # erreur sur DX : avec l'arrondi DX est connue à +/- 1 pixel
r   = D/DX                         # r est le coefficient d'étalonnage
ur  = np.sqrt((uD/DX)**2+(D*uDX/DX**2)**2) # propagation des erreurs sur r

## Définition des min/max des coordonnées des extrémités du faisceau
xmin = min(position[:,0])
xmax = max(position[:,0])
ymin = min(position[:,1])
ymax = max(position[:,1])
y    = int(np.mean(position[:,1]))   # On tracera le profil d'intensité selon l'ordonnée y. On ne peut tracer un profil que selon un axe horizontal donc on trace le profil selon la moyenne de yA et yB pour minimiser les erreurs.

## Définition du segment d'intérêt dont on a choisit les extrémités
profil = Diff[y,xmin:xmax,:]

## Tracé des profils pour les trois couleurs de l'image (R,G,B) et choix de la courbe à ajuster
plt.figure(u'Choix de la courbe à ajuster')
plt.plot(profil)
plt.legend(['R','G','B'])
plt.show(block=False)
plt.pause(0.1)


## Choix de la courbe à ajuster (La verte (G) est souvent la meilleure)
var=0
while var==0:
    n=input('Entrez le nom de la courbe a ajuster : R, G ou B puis taper sur <Entree>')  # Récupère le choix qu'entre l'utilisateur sur son clavier
    if n=='R':
        profil=profil[:,0]
        var=1
    elif n=='G':
        profil=profil[:,1]
        var=1
    elif n=='B':
        profil=profil[:,2]
        var=1
plt.close()

## Détermination des bornes pour l'ajustement
plt.figure('Choix des bornes pour l\'ajustement')
plt.plot(profil)
bornes=np.array(plt.ginput(2)) 
plt.close()

## Comme précedemment arrondi des coordonnées, sélection des abscisses, redéfinition du segment d'intérêt
bornes = bornes.astype(int)
bornes = bornes[:,0]
profil = profil[bornes[0]:bornes[1]]

## Définition des données pour l'ajustement et calibrage des abscisses
x = np.arange(np.size(profil))*r
y = profil
y = y-np.min(y) # facilite l'ajustement (une inconnue en moins)

# incertitudes types (= même erreur pour tous les points)
ux = ur*np.ones(np.size(x))  
uy = 1e-4*np.ones(np.size(y))  # pas d'incertitude sur les intensités mesurées pas la caméra/appareil photo. Mais l'algorithme ne gère pas une erreur nulle (uy=0) donc on indique une erreur très faible qui n'altèrera pas l'ajustement.

# fonction f decrivant la courbe a ajuster aux donnees
def f(x,p):
	a,b = p
	return a*np.exp(-b*x)

# derivee de la fonction f par rapport a la variable x
def Dx_f(x,p):
	a,b = p
	return -a*b*np.exp(-b*x)

# fonction d'ecart ponderee par les erreurs
def residual(p,y,x):
	return (y-f(x,p))/np.sqrt(uy**2 + (Dx_f(x,p)*ux)**2)

# estimation initiale des parametres
p0 = np.array([10,10])

# moindres carrees non-lineaires
result = spo.leastsq(residual,p0, args=(y,x), full_output=True)

# parametres d'ajustement optimaux
popt = result[0]

# incertitudes-types sur ces parametres
uopt = np.sqrt(np.abs(np.diagonal(result[1])))

# graphique
fig = plt.figure(u'Ajustement exponentiel du profil d\'intensité le long du faisceau')
ax = fig.add_subplot(111)
ax.tick_params(labelsize=13)

plt.plot(np.linspace(min(x),max(x),100),popt[0]*np.exp(-popt[1]*np.linspace(min(x),max(x),100)),linewidth=2,color=[0.8,0,0])
plt.errorbar(x, y, xerr=ux, yerr=uy,fmt='+',capthick=1,linewidth=1.5,ecolor=[0,0.55,0.55],color=[0,0.55,0.55])

# labels
plt.xlabel(r'$x\quad(\mathrm{m})$', fontsize=18)
plt.ylabel(r'$I\quad(\mathrm{u.a})$', fontsize=18)

# donnees ajustement
plt.text(0.1,0.9,r'$\mathrm{R\'egression\ exponentielle}\ :\ f(x) = a*exp(-bx)$',transform = ax.transAxes)
plt.text(0.1,0.85,r'$a = {0:.2e} \pm {1:.2e}$'.format(popt[0],uopt[0]),transform = ax.transAxes)
plt.text(0.1,0.8,r'$b = {0:.2e} \pm {1:.2e}$'.format(popt[1],uopt[1]),transform = ax.transAxes)


plt.show()





