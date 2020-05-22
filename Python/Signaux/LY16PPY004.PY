# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 13:04:39 2015

@author: ENS de Lyon

Objectifs : Illustrer le filtrage spatial sur une image.

Entrées :   - image : l'image que l'on souhaite traiter. Si "PIL" n'est pas intallé, seul le format PNG est possible. Sinon, il est possible d'ouvrir "many file formats" (incluant jpeg, et bmp).
            - rayon : rayon du filtre passe haut ou passe-bas appliqué (équivalent de la fréquence de coupure)
            - filtre : tyoe de filtre utilisé.
            
Sorties :   - TF : transformée de Fourier de l'image
            - TF2 : transformée de Fourier de l'image multipliée par le filtre (c'est la TF de l'image filtrée)
            - image_2 : image filtrée
            - figure 1 : image et image filtrée
            - figure 2 : graphe de TF, filtre et TF2
"""

# Chargement des bibliothèques utiles
import numpy as np# Calcul numérique
import matplotlib.image as img# Chargement d'images
import matplotlib.pyplot as plt# Affichage d'images
import matplotlib.cm as cm# Échelles de gris

# Nettoyage des figures précédentes
plt.figure(1)
plt.clf()
plt.figure(2)
plt.clf()

# Lecture et affichage de l'image
image = img.imread('domaines.png')[:,:,0]# Chargement de l'image de test
plt.figure(1)
plt.subplot(121)
plt.title("Image originale")
plt.imshow(image, cmap = cm.Greys_r)# Affichage de l'image

# Calcul et affichage de la TF
TF = np.fft.fft2(image)# Calcul de la TF
plt.figure(2)
plt.subplot(221)
plt.imshow(np.log(np.abs(np.fft.fftshift(TF))), cmap = cm.Greys_r)# Affichage de la TF
plt.title("TF originale (échelle log)")
plt.colorbar()# Échelle de gris

# Calcul du filtre
rayon = 100# Rayon du filtre
(M,N) = image.shape# Dimensions de l'image
x,y = np.mgrid[0:M,0:N]
#filtre = 1+np.zeros((M,N))# Filtre identité (H=1)
#filtre = np.fft.ifftshift(0.5*(np.sign((x-M/2.)**2+(y-N/2.)**2-rayon**2)+1))# Filtre coupe-bas opaque
#filtre = np.fft.ifftshift(1-0.5*(np.sign((x-M/2.)**2+(y-N/2.)**2-rayon**2)+1))# Filtre passe-bas opaque
#filtre = np.fft.ifftshift(np.exp(-((x-M/2.)/rayon)**2-((y-N/2.)/rayon)**2))# Filtre passe-bas gaussien
filtre = np.fft.ifftshift(1-np.exp(-((x-M/2.)/rayon)**2-((y-N/2.)/rayon)**2))# Filtre passe-haut gaussien
plt.figure(2)
plt.subplot(222)
plt.title("Filtre (échelle log)")
plt.imshow(np.log(np.fft.fftshift(filtre)), cmap = cm.Greys_r)# Tracé du filtre
plt.colorbar()# Échelle de gris

# Application du filtre sur la TF
TF2 = TF*filtre# Application du filtre sur la TF
plt.figure(2)
plt.subplot(223)
plt.title("TF filtrée (échelle log)")
plt.imshow(np.log(np.abs(np.fft.fftshift(TF))), cmap = cm.Greys_r)# Affichage de la TF filtrée
plt.colorbar()# Échelle de gris

# Calcul de la TF-1 et affichage
image_2 = np.fft.ifft2(TF2)# Calcul de la TF-1
plt.figure(1)
plt.subplot(122)
plt.title("Image filtrée")
plt.imshow(np.abs(image_2), cmap = cm.Greys_r)# Affichage de l'image filtrée

