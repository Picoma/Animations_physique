# -*- coding: utf-8 -*-
#Auteur : ENS de Lyon promotion 2017-2018
#Ce code permet d'illustrer le principe de la microscopie PALM (photo-activated localization microscopy) à partir d'une image sur la banque d'image "palm.png".
#Il faut mettre l'image "palm.png" dans le même dossier que le code.
#
#Ce programme :
#   - convertit la composante verte de l'image en niveaux de gris
#   - sélectionne un certain nombre de points dans cette image (nombre 'echantillons', créé une image ne contenant que ces pixels : 'image_e', c'est l'image traitée après une étape)
#   - leur applique un filtre gaussien pour simuler la limite de diffraction (génère une fausse image floue : 'image_d')
#   - répète cette opération 'N' fois, sans pour autant afficher le résulat
#   - affiche : 
#       - la première fausse image floue (étape N = 1)
#       - la première image traitée (étape N = 1)
#       - la somme des images floues qui simule l'image floue obtenue par de la microscopie classique
#       - la somme des images traitées qui simule le résultat obtenu grâce à la technique de microscopie PALM
#
# ATTENTION : ce programme ne reproduit pas réellement le principe de la microscopie PALM car elle traite l'image en entrée comme l'objet à imager
# La phase de sélection des pixels correspond à la phase d'excitation des fluorophores.






import random
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import scipy.ndimage.filters as flt

echantillons = 20000
N=10
taille_diffraction = 8

ax1 = plt.subplot(221)
ax2 = plt.subplot(222)
ax3 = plt.subplot(223)
ax4 = plt.subplot(224)

img = mpimg.imread("palm.png")
img_g = img[:,:,1]
l = np.shape(img)[0]
h = np.shape(img)[1]

random.seed(a=2333)

def selection_echantillons(largeur,hauteur,nombre_echantillons):
    """
    Fonction sélectionnant [nombre_échantillons] de couple de coordonnées pour des pixels compris pour x entre 0 et [largeur]-1  et pour y entre 0 et [hauteur]-1
    Cela simule une activation aléatoire des fluorophores
    """
    liste = []
    for k in range(nombre_echantillons):
        couple = random.randrange(0, largeur),random.randrange(0, hauteur)
        liste.append(couple)
    return(liste)
    

            
def echantillonage(liste_echantillons,image):
    """
    A partir d'une liste de coordonnées choisi aléatoirement [liste_echantillons] simulant une activation aléatoire de fluorophore sur une image [image].
    Cette fonction créé une image parfaitement résolu simulant l'émission de lumière par les fluorophores activés.
    C'est aussi l'image qu'on obtiendrais après détection des centres des figures de diffractions.
    """
    l = np.shape(image)[0]
    h = np.shape(image)[1]
    image_echantillonee = np.zeros([l,h])
    for k in range(len(liste_echantillons)):
#        print(liste[k])
        x0 = liste_echantillons[k][0]
        y0 = liste_echantillons[k][1]
        image_echantillonee[x0,y0] = image_echantillonee[x0,y0] + image[x0,y0]
    return(image_echantillonee)




def simulation_diffraction_filtre (image_echantillonee, sigma):
    """
    On simule ici la diffraction, on considère que les pixel sont disjoint et donc qu'un flou gaussien revient à simuler une diffraction par un diaphragme de chacun des pixel (qui sont des simulations de sources lumineuses).
    """
    return(flt.gaussian_filter(image_echantillonee,taille_diffraction))
    
    
    
liste_e = selection_echantillons(l,h,echantillons)
image_e = echantillonage(liste_e,img_g)
ax2.imshow(image_e,cmap="Greys_r")
ax2.set_title("Image lors d'une etape avec traitement",fontsize=17)

image_d = simulation_diffraction_filtre(image_e,10)
ax1.imshow(image_d,cmap="Greys_r")
ax1.set_title("Image lors d'une etape sans traitement",fontsize=17)



for k in range(N):
    print(k)
    l_e = selection_echantillons(l,h,echantillons)
    i_e = echantillonage(l_e,img_g)
    i_d = simulation_diffraction_filtre(i_e,20)

    image_e = image_e + i_e
    image_d = image_d + i_d

ax3.imshow(image_d,cmap="Greys_r")
ax3.set_title("Image obtenue avec la microscopie classique",fontsize=17)

ax4.imshow(image_e,cmap="Greys_r")
ax4.set_title("Image obtenue avec la microscopie PALM",fontsize=17)

#Ouvre la figure en plein écran 
#figManager = plt.get_current_fig_manager()
#figManager.window.showMaximized()
#plt.tight_layout()

plt.imsave('sans_palm.png',image_d,cmap="Greys_r")
plt.imsave('avec_palm.png',image_e,cmap="Greys_r")

plt.show()
