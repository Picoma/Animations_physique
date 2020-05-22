# -*- coding: utf-8 -*-
"""
fourier_images.py
@author: ENS de Lyon

Ce programme:
- ouvre une image [1]
- la convertit en nuances de gris
- calcule la transformée de Fourier
- applique un filtre sur la transformée de Fourier
- recalcule l'image à partir de la transformée de Fourier modifiée.

Les valeurs à modifier sont :
- ligne 67 : le chemin relatif du fchier image
- ligne 109 : la valeur de seuil pour la strioscopie (rayon)
- ligne 121 : le sens de l'inéquation, pour garder les hautes ou basses fréquences


[1] Apparemment la gamme de formats est assez large ; le script a été testé
avec les formats .jpg, .png, .gif, .bmp et .eps.


Script de départ :
http://kmdb.pagesperso-orange.fr/_src/_python/_formation_2010/python_formation_images.html

Image d'exemple :
http://www.publicdomainpictures.net/view-image.php?image=151142&picture=requin-baleine-rhincodon-typus
"""


"""
Bibliothèques
"""
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from scipy import misc


"""
Fonctions de normalisation : ramènent les éléments de la matrice à des valeurs 
comprises entre 0 et 255, pour un affichage en nuances de gris.
"""
# Fonction de normalisation
def norma(mat):
    mat1 = mat.real
    mini = mat1.min()
    maxi = mat1.max()
    mat2 = (mat1 - mini)/maxi*255.0
    return mat2

# Fonction de normalisation sur une échelle logarithmique
def normalog(mat):
    mat1 = norma(mat)
    mat2 = np.log(1 + mat1)
    maxi = mat2.max()
    mat3 = mat2/maxi*255.0
    return mat3


"""
Le code commence. On charge une image, la fonction va la convertir en nuances
de gris, et renvoyer un tableau. Chaque case du tableau correspond alors à un
pixel, et la valeur dans le tableau (entre 0 et 255) indique la nuance de gris.
"""

image_gs = misc.imread('tp.jpg', flatten=True)

print "Image originale en nuances de gris :"
plt.imshow(image_gs, cmap = mpl.cm.Greys_r)
plt.axis('off')
plt.show()


"""
On calcule la transformée de Fourier discrète, et on centre les basses 
fréquences spatiales (les hautes fréquences sont donc sur les extrémités).
On calcule ensuite l'amlitude de la TF que l'on affiche.
"""

image_fft = np.fft.fft2(image_gs)

image_fft_centre = np.fft.fftshift(image_fft)

image_fft_abs_centre = abs(image_fft_centre)

print "Transformée de Fourier (éhelle log) :"
plt.imshow(normalog(image_fft_abs_centre), cmap = mpl.cm.Greys_r)
plt.axis('off')
plt.show()


"""
C'est ici qu'on effectue la "strioscopie". On découpe un cercle au centre du 
spectre, et on ne garde que ce qui est dedans ou dehors, pour ne garder que les
basses ou hautes fréquences spatiales.
"""

nblignes = image_gs.shape[0]
nbcolonnes = image_gs.shape[1]

centre_x = abs( (nbcolonnes-1)/2 )
centre_y = abs( (nblignes-1)/2 )

"""
On peut changer le rayon du cercle.
Attention à l'échelle log qui peut être trompeuse lors de l'affichage.
"""
rayon = 300

for i in range(nblignes):
    for j in range(nbcolonnes):
        
        d2 = np.power((j-centre_x),2) + np.power((i-centre_y),2)
        
        """
        En changeant le sens de l'inéquation, on coupe les éléments à
        l'intérieur ou à l'extérieur du cercle, ce qui ne laisse que les hautes
        ou basses fréquences.
        """
        if d2 < rayon^2:
            image_fft_centre[i][j] = 0


"""
On recalcule l'amplitude de la TF pour afficher le spectre découpé.
"""

image_fft_abs_centre = abs(image_fft_centre)

print "Transformée de Fourier modifiée (échelle log) :"
plt.imshow(normalog(image_fft_abs_centre), cmap = mpl.cm.Greys_r)
plt.axis('off')
plt.show()


"""
Enfin, on calcule la TF inverse à partir du spectre modifié : l'image est 
modifiée en conséquence.
"""

image_2 = np.fft.ifft2(image_fft_centre)

print "Image modifiée :"
plt.imshow(norma(abs(image_2)), cmap = mpl.cm.Greys_r)
plt.axis('off')
plt.show()

