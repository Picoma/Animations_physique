#Animation de construction d'un paquet d'onde par ajout succesif d'harmonique

#contact : clement.pelletmary@gmail.com


import numpy as np
import numpy.fft as fft
import matplotlib.pyplot as plt
import matplotlib.animation as animation

sigmax=1
deltax=20
x0=0
n=2**14
f0=10
keep=40

fig,ax=plt.subplots()
plt.ylim(-1,1)
dx=deltax/(n-1)
deltaf=0.5/dx
sigmaf=1/sigmax



@np.vectorize
def gauss(x,x0,sigma):
    return 1/(np.sqrt(2*np.pi)*sigma)*np.exp(-(x-x0)**2/(2*sigma**2))
@np.vectorize
def cos(x,f):
    return np.cos(2*np.pi*f*x)
    
x=np.linspace(-deltax/2,deltax/2,n)
paquet=gauss(x,x0,sigmax)*cos(x,f0)
aprox,=ax.plot(x,x)

def update(k) :
    fourier=fft.fft(paquet)
    ampl=np.sort(abs(fourier))
    for i in range(n) :
        if abs(fourier[i]) < ampl[-k-1] :
            fourier[i]=0

    y=np.real(fft.ifft(fourier))
    aprox.set_ydata(y)
    return aprox

ani = animation.FuncAnimation(fig, update, keep,interval=200, repeat=False)

plt.show()



    