# Auteur: Grégoire Martouzet, gregoire.martouzet@ens-paris-saclay.fr

import numpy as np
import matplotlib.pyplot as plt

"""
La masse M est en contact plan avec le solide S2 et est reliée au solide S1
par un ressort de constante k.
Le solide S2 est en mouvement par rapport au solide S1.

======            -----
[ S1 ]~~~~~~k~~~~~| M |
======            -----
              ==============
              [     S2     ]
              ==============
"""

# Constantes
g = 9.81

m   = 1 # masse
k   = 10 # coefficient de raideur

# Liaison entre M et S2
fs  = 0.5	# coefficient de frottement statique
fd  = 0.35	# coefficient de frottement dynamique

vs  = 0.02 # vitesse de S2/S1

# Paramètres de simulation
t_max = 50 # temps maximum
dt = 1e-3 # pas de temps
N = int(t_max/dt) # nombre de points

# Notations pour ce code:
#  - xm  : positin de M / S1 (élongation du ressort par rapport à son équilibre)
#  - vs : vitesse S2/S1 (constante)
#  - vrm : vitesse M/S2
#  - vm  : vitesse M/S1

# Paramètres initiaux
xm = 0.0 # position initiale du mobile M
vm = vs  #  vitesse M/S1 non nulle
vrm = 0.0 # vitesse M/S2 relative nulle -> glissement
am = 0
mvt = False # pas de mouvement relative de M / S2 -> glissement 

# Listes résultats
temps = np.arange(0, t_max, dt)
x     = np.zeros(N)
vr    = np.zeros(N)
v     = np.zeros(N)
a     = np.zeros(N)

for i in range(N):
	x[i] = xm
	vr[i] = vrm
	v[i] = vm
	a[i] = am
	
	# si mouvement
	if mvt:
		# acceleration (PFD)
		am = (fd*m*g-k*xm)/m
		vm += am*dt # vitesse par integration de l'acceleration
	else:
		am = 0
		vm = vs # le mobile est fixe par rapport au support (même vitesse)
		
	xm += vm*dt # position
	
	# vitesse relative M/S2
	vrm = vm-vs
	
	# Glisssement ou pas lors du pas suivant ?
	if mvt:
		# si glissement et vitesse relative positive ? fin de mouvement
		if vrm > 0:
			mvt = False
	else:
		# si pas de mouvement et si la force de rappel est supérieure à la force de frottement alors mise en mouvement
		if (k*xm >= fs*m*g):
			mvt = True

""" Affichage """
plt.plot(temps,x)
#plt.plot(temps,v)
plt.show()
