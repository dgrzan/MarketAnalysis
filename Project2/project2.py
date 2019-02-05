import matplotlib.pyplot as plt
import numpy as np
import random
from matplotlib.backends.backend_pdf import PdfPages
from scipy import stats
import math
from scipy.special import factorial
from scipy.optimize import curve_fit

def poisson(k,lamb):
    return (lamb**k/factorial(k)) * np.exp(-lamb)

if __name__ == "__main__":

    with PdfPages("Project2_David_Grzan.pdf") as pdf:

        #makes gaussian histogram
        n = 100000
        n2 = 100
        garray = []
        a = 0
        for j in range(0,n):
            for i in range(0,n2):
                a+=random.uniform(-1,1)
            garray.append(a*(float(n2/3))**(-1/2))
            a = 0
        plt.figure()
        plt.title("Gaussian Distribution")
        plt.hist(garray,100,density=0,range=(-4,4),facecolor="g")
        pdf.savefig()
        plt.close()

        #makes normalized gaussian histogram with fit
        m, s = stats.norm.fit(garray)
        line = stats.norm.pdf(np.linspace(-4,4,100),m,s)
        fig = plt.figure()
        plt.plot(np.linspace(-4,4,100),line)
        plt.title("Normalized Gaussian Distribution")
        plt.hist(garray,100,density=1,range=(-4,4),facecolor="r")
        plt.text(0.75,0.4,"Mean: {:.2f}, Sigma: {:.2f}".format(m,s),size=10) 
        pdf.savefig()
        plt.close()

        #makes poisson histogram
        e = math.e
        parray = []
        lamb = 5

        k = 0
        p = 1.0
        L = e**(-lamb)
        
        for i in range(0,100000):
            while p>L:
                k = k+1
                p = p*random.uniform(0,1)

            parray.append(k-1)
            p = 1.0
            k = 0

        plt.figure()
        plt.title("Poisson Distribution")
        plt.hist(parray,20,density=0,range=(-0.5,19.5),facecolor="g")
        pdf.savefig()
        plt.close()

        #makes normalized poisson histogram with fit
        
        plt.figure()
        plt.title("Normalized Poisson Distribution")
        entries, bin_edges, patches = plt.hist(parray,20,density=1,range=(-0.5,19.5),facecolor="r")
        print(bin_edges)
        bin_middles = 0.5*(bin_edges[1:] + bin_edges[:-1])
        parameters, cov_matrix = curve_fit(poisson, bin_middles, entries)
        xaxis = np.linspace(0,20,1000)
        plt.plot(xaxis, poisson(xaxis, *parameters))
        print(parameters)
        plt.text(10,0.125,"Lambda: {:.2f}".format(*parameters),size=10) 
        
        pdf.savefig()
        plt.close()
