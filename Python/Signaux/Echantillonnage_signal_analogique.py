# -*- coding: utf-8 -*-

#Nom du programme : Echantillonnage_signal_analogique

#Auteurs : David Delgove, Arnaud Raoux et la prépa agreg de Montrouge, modifié par ENS de Lyon promotion 2017-2018
#Adresse : Departement de physique de l'Ecole Normale Superieure
#		24 rue Lhomond
#		75005 Paris
#Contact : arnaud.raoux@ens.fr

#Version de Python
#3.5

#LICENCE
#Cette oeuvre, création, site ou texte est sous licence Creative Commons Attribution - Pas d'Utilisation Commerciale 4.0 International. Pour accéder à une copie de cette licence, merci de vous rendre à l'adresse suivante http://creativecommons.org/licenses/by-nc/4.0/ ou envoyez un courrier à Creative Commons, 444 Castro Street, Suite 900, Mountain View, California, 94041, USA.

#AVERTISSEMENT
#Pour un affichage optimal, il est recommandé de mettre la fenêtre en plein écran.

#Description : 
#Ce programme a pour objectif de mettre en évidence l'effet d'échantionnage, ainsi que l'effet de filtrage sur un signal analogique.

# La promotion 2017/2018 de l'ENS de Lyon a simplement rajouté un slider permettant de voir l'influence de la fréquence d'échantillonage de manière interactive.
# Nous avons aussi enlevé la fonction filtrage, car nous n'en voulions pas, ainsi que le choix d'un signal carré.

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as wd

# =============================================================================
# --- Définitions des paramètres sur lesquels on peut agir --------------------
# =============================================================================

### Signal analogique ###
fe = 10 # fréquence du signal
Amplitude = 1.0 # Amplitude du signal

### Signal numérique d'entrée ###
Tacquisition = 1 # durée d'acquisition
fechantillonnage = 21 # fréquence d'échantillonnage

    
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


    signal=A*np.cos(2*np.pi*fe*temps)
    
    return temps,signal
  
    
# =============================================================================
# --- Code principal-----------------------------------------------------------
# =============================================================================

#Table du signal analogique (en fait échantilloné avec une très grande fréquence : aucun problème de repliement de spectre)
Table_vrai_signalx, Table_vrai_signaly = TableSignalEntree(fe,200*fe,Tacquisition,Amplitude)
    
#Table du signal échantilloné
Tablex,Tabley = TableSignalEntree(fe,fechantillonnage,Tacquisition,Amplitude)


#Titre de la figure
fa, ax = plt.subplots(1, sharex=True)

ax.set_title(r'Echantillonnage (frequence echantillonnage='+str(fechantillonnage)+' Hz, frequence='+str(fe)+' Hz)',fontsize=18)
Msize = 10; Mtype = 'x'

    
#Titres et dimensions des axes 
ax.set_ylim(-1.5*Amplitude,1.5*Amplitude)
ax.set_ylabel(r'Amplitude (1)',fontsize=18)
ax.set_xlim(0,Tacquisition)
ax.set_xlabel(r'Temps (s)',fontsize=18)
plt.grid(True)

#Trace le signal "analogique", le signal échantilloné et le signal filtré
ax.plot(Table_vrai_signalx,Table_vrai_signaly,color='blue',linewidth=1,label="Analogique")
l, = plt.plot(Tablex,Tabley,color='red',marker=Mtype,markersize=Msize,linewidth=2,label="Numerique")


#Définition du slider et fonction de mise-à-jour du plot
axfreqech = plt.axes([0.2, 0.03, 0.6, 0.01])
freqech = wd.Slider(axfreqech, 'Freq', 8, 200, valinit=fechantillonnage)

def update(val):
    freq = freqech.val
    frequ = round(freq, 2)
    Tablex1,Tabley1 = TableSignalEntree(fe,frequ,Tacquisition,Amplitude)
    fa.canvas.draw_idle()
    l.set_ydata(Tabley1)
    l.set_xdata(Tablex1)
    ax.set_title(r'Echantillonnage (frequence echantillonnage='+str(frequ)+' Hz, frequence='+str(fe)+' Hz)',fontsize=18)
freqech.on_changed(update)

#Ouvre la figure en plein écran 
#figManager = plt.get_current_fig_manager()
#figManager.window.showMaximized()

plt.show()
