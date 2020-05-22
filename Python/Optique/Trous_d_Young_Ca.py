## Importations

import numpy as np
import matplotlib.pyplot as plt


## Constantes

# Longueur d'onde (en mètres)

lbda = 550*10**(-9)

# Distance entre la source et les trous d'Young (en mètres)

l = 0.3

# Ecart entre les trous (en mètres)

a = 0.001

# Distance entre les trous et l'écran (en mètres)

D = 1

def u(b):
    return(np.pi*a*b/(lbda*l))

# Intensité initiale

I0 = 1

## Position

# Valeur min (en mètres)

xmin = -0.0025

# Valeur max (en mètres)

xmax = +0.0025

# Nombre de points

Nbpt = 10000

x = np.linspace(xmin,xmax,Nbpt)

## Intensité

def I(x,b):
    
    I=I0*(1+(np.sinc(u(b)))*np.cos(2*np.pi*a*x/(lbda*D)))
    return(I)

def V(b):
    V=np.sin(u(b))/u(b)
    return(V)
    
## Tracé

def intensite(N):

# Valeur basse de l'épaisseur (en mètres)
    bmin = 0.0
# Valeur haute de l'épaisseur (en mètres), ne pas mettre 0
    bmax = 0.001
# Valeurs de la largeur de la fente (en mètres)
    b = np.linspace(bmin, bmax, N)
    
    for i in range(N):
        plt.plot(x,I(x,b[i]),label="b={} mm".format(1000*b[i]))
    
    plt.xlabel("Position sur l'écran $x$")
    plt.ylabel("Intensité $I$")
    
    plt.title("Intensité en fonction de la position.")
    plt.legend()
    plt.show()

def contraste(N):
# Valeur basse de l'épaisseur (en mètres)
    bmin = 0.0
# Valeur haute de l'épaisseur (en mètres), ne pas mettre 0
    bmax = 0.001
# Valeurs de la largeur de la fente (en mètres)
    b = np.linspace(bmin, bmax, N)
    
    for i in range(N):
        plt.plot(b,V(b))
    
    plt.xlabel("Largeur de la fente $b$")
    plt.ylabel("Contraste $V$")
    
    plt.title("Contraste en fonction de la largeur de la fente.")
    plt.legend()
    plt.show()