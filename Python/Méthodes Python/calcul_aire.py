import random
import numpy as np
import matplotlib.pyplot as plt

#Ce script permet de calculer l'aire d'une courbe définie par un nuage de points expérimentaux
#(Par exemple pour avoir l'aire d'un diagramme P,V )
# Il faut bien définir le chemin vers le fichier texte utilisé, dans le programme  : C:/Users\physique164\Desktop/test_stirling/stirling.txt
# Vous devrez sauver votre fichier texte sur cet ordinateur et ensuite taper le bon chemin en ligne 30

#IMPORTANT : DONNER LE POINT ORIGININE, S'IL N'EST PAS A L'INTERIEUR DU CYCLE LE SCRIPT NE PEUT PAS FONCTIONNER

"""
L'algorithme repose sur le principe suivant :
    1-on prend un point d'origine qui doit etre dans l'aire et qui servira de base aux calculs
    2-on sépare le plan angulairement a partir de l'origine
    3-pour chaque orceau ainsi défini, on calcule la moyenne des points expérimentaux
    4-on calcule l'aire a partir des points précédemment moyennées

Parmi les variables que l'utilisateur peut/doit modifier il y a :
    filename : le chemin vers le fichier qui contient les points a traiter, sous la forme d'un fichier de donnees texte a deux colonnes, en cas d'erreur changer les backslash de windows en /
    origine : un point a l'interieur du cycle qui servira de base de calcul
    pas : le pas de decoupage angulaire du calcul. Un pas plus petit augmente la précision mais ralentit le script et augmente le risque d'erreurs
"""

#Chargement des donnees--------------------------------

#Il faut charger les x dans xdata et les y dans ydata, qui doivent
#etre des np.array

filename = 'C:/Users\physique164\Desktop/test_stirling/stirling.txt'
data = np.genfromtxt(filename, delimiter='\t', skip_header=1) #ici on charge des donnees en colonne espacées par des tabulations avec un header d'une ligne
xdata = data[:,0]
ydata = data[:,1]

#----------------------------------------------------------

#Generation de points pour tester le programme, cette portion de code est inutile lors d'une utilisation classique
def test():
    """
    Cette fonction génère un cercle avec des points 
    répartis de façon a simuler un processus de mesure aléatoire
    """
    np_points = 2500
    rayon = 1
    xdata = np.zeros(np_points)
    ydata = np.zeros(np_points)
    for i in range(np_points):
        theta = 2*np.pi*random.random()
        r = rayon + 0.1*(random.random()-0.5)
        xdata[i] = r*np.cos(theta)
        ydata[i] = r*np.sin(theta)
    return xdata,ydata

#xdata, ydata = test()

#-------------------------------------------------------

#Ici il faut donner un point situé dans l'aire de la figure, proche du centre (mais pas besoin d'etre très précis sur cette donnée), qui servira de base de calcul, sous la forme origine = (x,y)

origine = (2.0,2.8)

#Calculs-------------------------------------------------
#--------------------------------------------------------


#Découpage angulaire du plan et moyennage des points

pas = 0.01*(2*np.pi) #pas de découpage, en radian

angles = np.arange(-np.pi-pas/2,np.pi+pas/2, step=pas)
x_calcules = np.zeros(angles.size)
y_calcules = np.zeros(angles.size)
for i in range(angles.size):
    theta = angles[i]
    x_tmp = []
    y_tmp = []
    for j in range(xdata.size):
        y_rel = ydata[j]-origine[1]
        x_rel = xdata[j]-origine[0]
        phi = 2*np.arctan(y_rel/(x_rel+np.sqrt(x_rel**2+y_rel**2)))
        if (phi>=theta) and (phi<theta+pas):
            x_tmp.append(xdata[j])
            y_tmp.append(ydata[j])
    x_tmp = np.array(x_tmp)
    y_tmp = np.array(y_tmp)

    x_calcules[i] = x_tmp.mean()
    y_calcules[i] = y_tmp.mean()


#Nettoyage, pour tout de même afficher le résultat si jamais il y a eu des erreurs de calcul
#(on enlève les nan du tableau final)
new_x = []
new_y = []
for i in range(x_calcules.size):
    x = x_calcules[i]
    y = y_calcules[i]
    if not np.isnan(x) and not np.isnan(y):
        new_x.append(x)
        new_y.append(y)

#Enfin, le calcul de l'aire

aire = 0.0
for i in range(0,len(new_x)-1):
    aire += 0.5*abs(new_x[i]*new_y[i-1] - new_y[i]*new_x[i-1] )

print('Aire : '+str(aire))


#Et l'affichage pour que l'utilisateur vérifie le moyennage
plt.plot(xdata,ydata,'g+')
plt.plot(new_x,new_y,'r-')
plt.xlabel('x')
plt.ylabel('y')
plt.title("Calcul d'aire")
plt.show()
