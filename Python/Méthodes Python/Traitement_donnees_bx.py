# -*- coding: utf-8 -*-

"""
Fichier de régression quelconque et d'estimation des incertitudes (méthode chi² réduit) à partir d'un fichier contenant des données expérimentales.

A modifier pour s'en servir :
- le nom et chemin d'accès au fichier contenant les données (le fichier doit être un csv avec des "." en guise de "," pour les décimales et un séparateur de colonne : ";"
- éventuellement le délimiteur pour la lecture du fichier csv ainsi que le nom des variables
- la fonction d'ajustement (nommée "fonc") ainsi que le nom et le nombre de paramètres à ajuster
- Le titre et les légendes des axes (en fin de fichier)
Référence : BUP 928, Incertitudes expérimentales, FX Bally et JM Berroir, p.995

par la suite on pourra commenter (ou décommenter) une partie du script en sélectionnant et en appuyant "Ctlr" + "r" (ou "Ctlr" + "t")
"""


## Importation des bibliotheques

from pylab import *
from scipy import *
from numpy import *
import pandas as pd
from scipy.optimize import curve_fit


## Lectures des données à partir d'un fichier & conversions si nécessaires

# au choix entre trois méthodes pour extraire les données

# première méthode : si on souhaite récupérer les données dans des tableaux séparés

A=open("nom_du_fichier.csv", 'r')       # ouvre le fichier nom_du_fichier.csv
A.readline()                            # enlève la première ligne où il y a le nom de la variable
X=array([])                             # cree une liste pour la variable x
Y=array([])
for i in A:
    var=i.split(";")  # decoupe la ligne i en mots et i part depuis la deuxieme ligne avec le separateur de colonnes ";"
    x=float(var[0])                     # transforme le mot de la premiere colonne en variable
    y=float(var[1])
    X=append(X,x)                       # on concatene la liste precedente de x avec le x de la ligne i
    Y=append(Y,y)
print(X,Y)

# deuxième méthode : si on souhaite tout laisser dans une matrice

data = pd.read_csv("./nom_du_fichier.csv", delimiter=';') 
# on va chercher dans le répertoire considéré le fichier "dat.csv et on enregistre
# attention, avec cette méthode il ne faut qu'une seule ligne de commentaire dans le fichier CSV
print(data)                           # on affiche la matrice du fichier
X = data['X']                         # un tableau X sera affecté des valeurs de la colonne nommée "X" dans le fichier
Y = data['Y']           # 'Y' est le nom de la colonne dans le fichier CSV, et Y est la variable

# troisième méthode : on insère directement dans un tableau les valeurs mesurées
X=array([1.,2.,3.,4.,5.,6.,7.,8.,9.,10.])
Y=array([2.9,5.,7.1,8.7,10.3,13.,14.9,17.1,18.8,21.])
print(X,Y)

# on fait des conversions si nécessaire : exemple : X2 = X + 273 (pour passer de degrés Celsius en Kelvin)


## ajustement par un modèle : x = variable, (a,b) = paramètres

def fonc(x,a,b):                        # définition de la fonction à ajuster
    return a*x+b
    
# nom des fonctions : SQRT(), EXP(), LOG10(), LOG() correspond à ln()

# param=[5,1]                 # initialisation des parametres dans le but d aider le programme a optimiser si nécessaire
popt, pcov = curve_fit(fonc, X, Y)      # rajouter dans "curve_fit" : ",param"
[a,b] = popt                            # popt renvoie les parametres optimises


## ajout des incertitudes et des erreurs : chi2_red = paramètre à mettre proche de 1 avec nos incertitudes

errX=0.01*X+0.1                         # erreur sur X ici on prend par exemple 1 pourcent + 0.1 (si 1 digit et affichage = 101,3 alors +0,1)
errY=0.01*Y +0.1                        # on peut aussi la rapporter du fichier csv en rajoutant une colonne et une liste
sigma_exp = sqrt(errY**2+errX**2)
yth = fonc(X,a,b)                       # fonction theorique a partir des parametres de l'ajustement
chi2 = sum(((yth - Y)/sigma_exp)**2)    # définition deu chi2 réduit
chi2_red = chi2/(len(X) - 2)            # le chiffre "2" est le nombre de variables ajustées
[erra,errb]= np.sqrt(diag(pcov)/chi2_red)  # incertitude sur les parametres a et b à partir du chi2_réduit

print("a=(",a,"+/-",erra,") unités")     # affichage de a et b sur le shell
print("b=(",b,"+/-",errb,") unités")


## Tracer des courbes : expérimentales + ajustement + barres d'erreurs

fig, ax = plt.subplots(1)               # cette commande va nous permettre de rajouter du texte
# plot(X,Y,'o',label='experimental')    # courbe provenant des points sans les incertitudes
plot(X,yth,'r',label='ajustement')      # plot du fit
errorbar(X,Y,errY,errX,fmt='bo',label='expérimental')        # ajout des erreurs sur la courbe
# ax.axis([xmin,xmax,ymin,ymax])        # on fixe les limites du graphique
xlabel('Variable X')                    # légend de l'axe x
ylabel('Variable Y')
title('Tracer de Y en fonction de X avec ajustement')
grid(True)                              # quadrille le graphique

# ajout d un texte sur le plot : ajout des parametres
textstr = "Y=a*X+b\n\
a= (%.2e +/- %.2e) unit\n\
b= (%.2e +/- %.2e) unit\n\
chi2_red = %.2f"  %(a,erra,b,errb,chi2_red)
ax.text(0.10, 0.70, textstr,transform=ax.transAxes, fontsize=12, verticalalignment='top') # position de la légende
legend(loc=2)                           # position de la légende

# Ajout d'une autre fenêtre avec une courbe
#fig2, ax = plt.subplots(1)
#plot(X,Y,'ro',label='données_autre')

show()
