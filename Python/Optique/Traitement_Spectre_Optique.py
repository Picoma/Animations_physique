# Import package
import numpy as np
import matplotlib.pyplot as plt
"""
Ce programme a pour but d'afficher les spectres d'émission reçus avec des polariseurs croisés et parallèles.

Entrées : 4 fichiers .txt contenant
    * le spectre du noir intitulé "noir.txt"
    * de l'intensité reçue sans polariseurs intitulé "Iref.txt"
    * avec les polariseurs croisés (90°) intitulé "I90.txt"
    * avec les polariseurs parallèles (0°) intitulé "I0.txt"
          

Sortie = - Graphe représentant les 3 spectres (noir soustrait)
         - Graphe représentant I90/Iref et I0/Iref en fonction de la longueur d'onde

"""

nom_fichier = ["noir", "I0", "I90", "Iref"]

def main(filenames):
    """
    main prend en argument une list de fichier a importer
    Celui de reference doit etre en derniere position et le noir en première position.
    """

    # Liste des valeurs
    values = [0] * len(filenames)

    with open(filenames[0] + ".txt") as fichier:
            # On charge le fichier dans un numpy array en changeant tous les ","
            # par des "." (en python on ecrit 0.5 et non pas 0,5 pour 1/2)
            noir = np.loadtxt((x.replace(',','.') for x in fichier))
            
    # Premiere figure avec tous les txt.
    plt.figure(0)
    # On boucle sur tous les fichiers
    for i in range(1,len(filenames)):
        # On ouvre le fichier
        with open(filenames[i] + ".txt") as fichier:
            # On charge le fichier dans un numpy array en changeant tous les ","
            # par des "." (en python on ecrit 0.5 et non pas 0,5 pour 1/2)
            values[i] = np.loadtxt((x.replace(',','.') for x in fichier))
            values[i][:,1] = values[i][:,1] - noir[:,1]
            
        # On plot les valeurs avec en legend le nom du fichier
        plt.plot(values[i][:,0],values[i][:,1], label=filenames[i])
    # On affiche la legend
    plt.legend()
    # On affiche les deux axes
    plt.xlabel('Lambda(nm)')
    plt.ylabel('Intensite')
    # On affiche le Titre
    plt.title('Spectres')

    # Seconde figure avec I0/Iref et I90/Iref
    plt.figure(1)
    # On boucle sur les 2 fichiers I90 et I0
    for i in range(1,len(filenames) - 1):
        plt.plot(values[i][:,0],values[i][:,1]/values[len(filenames)-1][:,1], label=filenames[i])
    # On affiche la legend
    plt.legend()
    plt.axis([375, 817, -0.01, 1.1])
    # On affiche les deux axes
    plt.xlabel('Lambda(nm)')
    plt.ylabel('Intensite')
    # On affiche le Titre
    plt.title('Intensité transmise relative')
    # On affiche les deux graphes dans une fenetre separer
    plt.show()

main(nom_fichier)
