#-----------------------------------------------------------------------
# Effet d'une rupture d'impédance sur une OPPM
#-----------------------------------------------------------------------
# Renseignements/bugs : Guillaume Dewaele <agreg(at)sci-phy.org>
#-----------------------------------------------------------------------

# Paramètres modifiables

# Pulsation de l'onde incidente

w = 1.0

# Célérité de l'onde incidente

cg = 0.3

#-----------------------------------------------------------------------

# Bibliothèques utilisées

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as ani
import matplotlib.widgets as mwg
from itertools import count

#-----------------------------------------------------------------------

# Détection utilisation hors Pyzo

if '__iep__' not in globals() :
    matplotlib.interactive(False)

# Calculs pour l'onde

cd = cg

def Onde(x, t, c) :
    return np.sin(w*(t-x/c))

# Affichage

Xg = np.linspace(-10, 0, 200)
Xd = np.linspace(0, 10, 200)

axTmp = plt.axes([0.08, 0.73, 0.4, 0.2])
axTmp.set_xlim(-10, 0)
axTmp.set_ylim(-1.5, 1.5)
axTmp.set_title("Onde incidente")
axTmp.grid()
crvi, = axTmp.plot(Xg, 0*Xg, 'b-', linewidth=2)
axTmp.axvspan(-10, 0, facecolor='b', alpha=0.2)

axTmp = plt.axes([0.08, 0.45, 0.4, 0.2])
axTmp.set_xlim(-10, 0)
axTmp.set_ylim(-1.5, 1.5)
axTmp.set_title("Onde réfléchie")
axTmp.grid()
crvr, = axTmp.plot(Xg, 0*Xg, 'b-', linewidth=2)
axTmp.axvspan(-10, 0, facecolor='b', alpha=0.2)

axTmp = plt.axes([0.52, 0.59, 0.4, 0.2])
axTmp.set_xlim(0, 10)
axTmp.set_ylim(-1.5, 1.5)
axTmp.set_title("Onde transmise")
axTmp.grid()
crvt, = axTmp.plot(Xd, 0*Xd, 'r-', linewidth=2)
axTmp.axvspan(0, 10, facecolor='r', alpha=0.2)

axTmp = plt.axes([0.1, 0.17, 0.8, 0.2])
axTmp.set_xlim(-10, 10)
axTmp.set_ylim(-1.5, 1.5)
axTmp.set_title("Total")
axTmp.grid()
crvg, = axTmp.plot(Xg, 0*Xg, 'b-', linewidth=2)
crvd, = axTmp.plot(Xd, 0*Xd, 'r-', linewidth=2)
axTmp.axvspan(-10, 0, facecolor='b', alpha=0.2)
axTmp.axvspan(0, 10, facecolor='r', alpha=0.2)

# Slider de configuration

axTmp = plt.axes([0.11, 0.035, 0.78, 0.035])
slider = mwg.Slider(axTmp, '', valmin=0.01, valmax=4.0, valinit=1.0)

plt.gcf().text(0.5, 0.095, r"Rapport des impédances $Z_D/Z_G$", ha='center', fontsize=14)

def UpdateZs(ratio) :
    global cd
    cd = cg*ratio

slider.on_changed(UpdateZs)

slider.set_val(0.75)

# Animation

def SizeChanged(ax, old=[]) :
    current = [ ax.bbox.width, ax.bbox.height ]
    if old != current :
        old[:] = current
        return True
    return False

def Update(t) :    
    T = 2*cd/(cd+cg)
    R = (cd-cg)/(cd+cg)
    
    Oi = np.vectorize(lambda x : Onde(x, t, cg))(Xg)
    Or = R*np.vectorize(lambda x : Onde(x, t, -cg))(Xg)
    Ot = T*np.vectorize(lambda x : Onde(x, t, cd))(Xd)
    crvi.set_data(Xg, Oi)
    crvr.set_data(Xg, Or)
    crvt.set_data(Xd, Ot)
    crvg.set_data(Xg, Oi+Or)
    crvd.set_data(Xd, Ot)
    
    if SizeChanged(plt.gca()) :
        plt.gcf().canvas.draw()
    
    return [crvi, crvr, crvt, crvg, crvd]
    
def Init() :
    crvi.set_data(Xg, np.ma.array(Xg, mask=True))
    crvr.set_data(Xg, np.ma.array(Xg, mask=True))
    crvt.set_data(Xd, np.ma.array(Xd, mask=True))
    crvg.set_data(Xg, np.ma.array(Xg, mask=True))
    crvd.set_data(Xd, np.ma.array(Xd, mask=True))
    
    return [crvi, crvr, crvt, crvg, crvd]

anim = ani.FuncAnimation(plt.gcf(), Update, count(0.0, 6.283/50.0), interval=20, blit=True, init_func=Init)

# Détection utilisation hors Pyzo

if '__iep__' not in globals() :
    plt.show()
