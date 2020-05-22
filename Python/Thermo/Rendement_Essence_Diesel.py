import numpy as np
import matplotlib.pyplot as plt

def beauderochas(gamma,a,b,points): 
    # Gamma est une liste contenant l'ensemble des valeurs du coefficient isentropique que l'on veut tester
    # a et b sont les bornes du taux de compression r, et points le nombre de points à calculer dans cette intervalle
    plt.figure() #crée une page pour la figure
    for i in gamma: 
        x = np.linspace(a,b,points)
        y = 1-1/x**(i-1)
        plt.plot(x, y, label="Gamma = "+str(i))
        plt.xlabel("Taux de compression r")
        plt.ylabel("Efficacite")
        plt.legend()  
        plt.title("Evolution du rendement d'un moteur essence en fonction du taux de compression")
    plt.show()

def diesel(beta,gamma,a,b,points): 
    #beta est une liste de valeurs de rapports volumétriques
    #gamma est une valeur de coefficient isentropique à tester
    # a et b les bornes du taux de compression alpha
    plt.figure()
    for i in beta :
        x = np.linspace(a,b,points)
        y = 1-(x*i**(1-gamma) -i*x**(1-gamma)) /(gamma*(x-i))
        plt.plot(x, y, label="beta="+str(i))
        plt.xlabel("Taux de compression alpha")
        plt.ylabel("Efficacite")
        plt.legend()   
        plt.title("Evolution du rendement d'un moteur diesel en fonction du taux de compression")
    plt.show()

diesel([1,2,5,10],1.4,1,5,100)
beauderochas([1.2,1.4,1.667],1,5,100)