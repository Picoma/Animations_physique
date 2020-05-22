#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 22 15:03:15 2018

@author: alexandre
"""

from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt

plt.close("all")

filename='angle_pendule.txt'
Matrix=np.loadtxt(filename, delimiter=' ',skiprows=2)

t=Matrix[:,0]
theta=Matrix[:,1]

theta_p=np.gradient(theta,t)

plt.figure(1)
plt.plot(theta,theta_p)
plt.xlabel(r'$\theta$')
plt.ylabel(r'$dot{\theta}$')
plt.savefig('manip_portrait_phase.png',dpi=300)

plt.figure(2)
plt.plot(t,theta)
plt.xlabel('t (s)')
plt.ylabel(r'$\theta$ (degres)')
plt.savefig('manip_angle_temps.png',dpi=300)

theta_red=theta[0:300]
t_red=t[0:300]

tf=np.fft.fft(theta_red)
f=np.fft.fftfreq(n=t_red.shape[-1],d=np.mean(np.diff(t_red)))
psd=np.square(np.abs(tf))
psdn=psd/psd.max()

plt.figure(3)
plt.semilogy(f,psdn)
plt.ylim([1e-5,2])
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.xlim(0,2)
plt.show()
plt.savefig('manip_fourier.png',dpi=300)