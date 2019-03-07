#!/usr/bin/python

import functions as f
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

if __name__ == "__main__":

    #creates things to plot
    t, y = f.randomwalk(10000,stepsize=1,m=0)
    t3, y3 = f.randomwalk(10000,stepsize=1,m=0)
    linepara = f.fitline(t,y)
  
    print(f.correlation(f.timediff(y),f.timediff(y3)))
    print(f.autocorrelation(f.timediff(y),1))
    print("")
    
    t2, y2 = f.brownianwalk(1000,0,3,m=0)
    brownianhist = f.timediff(y2)

    f1, s1 = f.powerspectrum(y2)
    
    linepara2 = f.fitline(np.log10(f1)[:],np.log10(s1)[:])

    t3, noise = f.whitenoise(10000,0,1)
    f3, s3 = f.powerspectrum(noise)

    t4, vol = f.volitility(y2,10)
    t5, avg = f.movingavg(y2,10)
    t6 ,avg2 = f.movingavg(y2,100)

    #creates figures
    fig = plt.figure(1,figsize=(10,7))
    ax = fig.add_subplot(1,1,1)
    ax.set_title("Random walk")
    ax.set_xlabel("time")

    fig2 = plt.figure(2,figsize=(10,7))
    ax2 = fig2.add_subplot(2,1,1)
    ax3 = fig2.add_subplot(2,1,2)
    ax3.set_xlabel("time difference")
    ax2.set_title("Brownian walk")
    ax2.set_xlabel("time")

    fig3 = plt.figure(3,figsize=(10,7))
    ax4 = fig3.add_subplot(1,1,1)
    ax4.set_title("Power spectrum")
    ax4.set_yscale("log")
    ax4.set_xscale("log")

    fig4 = plt.figure(4,figsize=(10,7))
    ax5 = fig4.add_subplot(2,1,1)
    ax6 = fig4.add_subplot(2,1,2)

    fig5 = plt.figure(5,figsize=(10,7))
    ax7 = fig5.add_subplot(2,1,1)
    ax8 = fig5.add_subplot(2,1,2)
    ax7.set_title("volitility test")
    
    #plots
    ax.plot(t,y,color="r")
    ax.plot(t,f.line(np.array(t),*linepara))
    ax2.plot(t2,y2)
    values, bounds, patches = ax3.hist(brownianhist,100)
    gausspara = f.fitgauss(f.bincenters(bounds),values)
    ax3.plot(f.bincenters(bounds),f.gauss(f.bincenters(bounds),*gausspara))
    ax4.plot(f1,s1,"o",markerfacecolor="None")
    ax4.plot(f1,f.logline(f1,*linepara2))
    ax5.plot(t3, noise)
    ax6.plot(f3,s3,"o",markerfacecolor="None")
    ax6.set_yscale("log")
    ax6.set_xscale("log")
    ax7.plot(t2,y2,color="black")
    ax7.plot(t5,avg,color="blue")
    ax7.plot(t6,avg2,color="green")
    ax8.plot(t4,vol,color="red")
    
    plt.show()
