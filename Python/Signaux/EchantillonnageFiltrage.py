# -*- coding: utf-8 -*-

#Nom du programme : EchantillionageFiltrage

#Auteurs : David Delgove, Arnaud Raoux et la prépa agreg de Montrouge
#Adresse : Departement de physique de l'Ecole Normale Superieure
#		24 rue Lhomond
#		75005 Paris
#Contact : arnaud.raoux@ens.fr
#
#Année de création : 20167
#Version : 1.00

#Liste des modifications
#v 1.00 : 2017-06-09 Première version complète

#Version de Python
#3.5

#LICENCE
#Cette oeuvre, création, site ou texte est sous licence Creative Commons Attribution - Pas d'Utilisation Commerciale 4.0 International. Pour accéder à une copie de cette licence, merci de vous rendre à l'adresse suivante http://creativecommons.org/licenses/by-nc/4.0/ ou envoyez un courrier à Creative Commons, 444 Castro Street, Suite 900, Mountain View, California, 94041, USA.

#AVERTISSEMENT
#Pour un affichage optimal, il est recommandé de mettre la fenêtre en plein écran.

#Description : 
#Ce programme a pour objectif de mettre en évidence l'effet d'échantionnage, ainsi que l'effet de filtrage sur un signal analogique.

import math
import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# --- Définitions des paramètres sur lesquels on peut agir --------------------
# =============================================================================

### Signal analogique ###
Forme_signal = 0 # 0 cosinus / 1 : rectangulaire # forme du signal échantillongé
fe = 10 # fréquence du signal
Amplitude = 1.0 # Amplitude du signal

### Signal numérique d'entrée ###
Tacquisition = 1 # durée d'acquisition
fechantillonnage = 21 # fréquence d'échantillonnage

### Signal numérique post-filtre passe-bas ###
Plot_Action_filtre = False # Tracer ou non l'action du filtre passe-bas
fc = 0.5 # fréquence de coupure du filtre
    
# =============================================================================
# --- Fonction intermediaire qui échantillone le signal -----------------------
# =============================================================================

def TableSignalEntree(fe,fech,Tacq,A) : 
    '''
    fe : fréquence du signal
    fech : fréquence d'échantillonage
    Tacq : Temps d'acquisition
    A : amplitude du signal
    '''

    Npoint = int(fech*Tacq+1)
    temps=np.linspace(1,Npoint,Npoint)/fech
    
    if (Forme_signal): # Cas où le signal est rectangulaire
        test=round(2*temps*fe,0) %2
        signal=A*(2*test-1)
        
    else: # Cas où le signal est sinusoidal
        signal=A*np.cos(2*np.pi*fe*temps)
    
    return temps,signal
  
# =============================================================================
# --- Fonction qui applique le filtre passe-bas sur le signal -----------------
# =============================================================================
    
def PasseBas(fcoupure,fech,Entree) : 
    '''
    fcoupure : fréquence de coupure du filtre
    fech : fréquence d'échantillonnage du signal d'entrée
    Entree : table contenant le signal d'entrée
    '''

    Sortie = [0]
    for i in range(0,len(Entree)-1) :
        Sortie.append(Sortie[i]+2*math.pi*fcoupure/fech*(Entree[i]-Sortie[i]))
    return Sortie

    
# =============================================================================
# --- Code principal-----------------------------------------------------------
# =============================================================================

#Table du signal analogique (en fait échantilloné avec une très grande fréquence : aucun problème de repliement de spectre)
Table_vrai_signalx, Table_vrai_signaly = TableSignalEntree(fe,200*fe,Tacquisition,Amplitude)
    
#Table du signal échantilloné
Tablex,Tabley = TableSignalEntree(fe,fechantillonnage,Tacquisition,Amplitude)

# Calcul l'action du filtre 
if Plot_Action_filtre :
    sortie = PasseBas(fc,fechantillonnage,Tabley)

#Titre de la figure
fa, ax = plt.subplots(1, sharex=True)
if Plot_Action_filtre :
    ax.set_title(r'Filtre Passe-bas (fech='+str(fechantillonnage)+' Hz, fana='+str(fe)+' Hz, fc='+str(fc)+' Hz)')
    Msize = 0; Mtype = '.'
else :
    ax.set_title(r'Echantillonnage (fech='+str(fechantillonnage)+' Hz, fana='+str(fe)+' Hz)')
    Msize = 10; Mtype = 'x'

    
#Titres et dimensions des axes 
ax.set_ylim(-1.5*Amplitude,1.5*Amplitude)
ax.set_ylabel(r'U.A')
ax.set_xlim(0,Tacquisition)
ax.set_xlabel(r't(s)')
plt.grid(True)

#Trace le signal "analogique", le signal échantilloné et le signal filtré
ax.plot(Table_vrai_signalx,Table_vrai_signaly,color='blue',linewidth=1,label="Analogique")
ax.plot(Tablex,Tabley,color='red',marker=Mtype,markersize=Msize,linewidth=2,label="Numérique")

if Plot_Action_filtre :
    ax.plot(Tablex,sortie,color='black',marker=Mtype,markersize=Msize,linewidth=2,label="Sortie du filtre")

    
plt.legend(loc="upper left", bbox_to_anchor=[0, 1],ncol=3, shadow=True,fancybox=True)

plt.show()