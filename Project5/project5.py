#!/usr/bin/python

import csv
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from matplotlib.backends.backend_pdf import PdfPages

def mean(x):
    mean = 0.0
    length = float(len(x))
    for val in x:
        mean+=val/length
    return mean

def sd(x):
    sdv = 0.0
    n = float(len(x))
    m = mean(x)
    for val in x:
        sdv+=((val-m)**2)/n
    sdv=sdv**(0.5)
    return sdv

def correlation(x1,x2):
    if len(x1)!=len(x2):
        print("ERROR: Invalid list sizes, lists must be of the same size")
        return float("nan")
    sd1 = sd(x1)
    sd2 = sd(x2)
    m1 = mean(x1)
    m2 = mean(x2)
    correlation = 0
    for i in range(len(x1)):
        correlation+=(x1[i]-m1)*(x2[i]-m2)
    correlation/=sd1*sd2*len(x1)
    return correlation

def logreturns(price):
    returns = []
    for j in range(len(price)):
        if j>0:
            returns.append(math.log(price[j])-math.log(price[j-1]))
    return returns

def percentreturns(x, timewindow):
    returns = []
    for i in range(len(x)):
        if (i+1)>=timewindow:
            returns.append(100*(x[i]-x[i-timewindow+1])/x[i-timewindow+1])
    return returns

def historicalvol(returns, timewindow):
    v = []
    for i in range(len(returns)):
        if (i+1)>=timewindow:
            vol = 0
            for j in range(timewindow):
                vol+=returns[i-j]**2
            ((252/timewindow)*vol)**0.5
            v.append(vol)
    return v

if __name__ == "__main__":

    with PdfPages("Project5_David_Grzan.pdf") as pdf:

        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        ax.text(0.05,0.3,"The correlation coefficient relating the percent returns \nand the volitility are negative in nearly all of the \nstocks analyzed. Meaning, the percent returns and the \nvolitility are inversily correlated. As can be \nseen clearly in the plots below, sharp spikes \nin the volitility occur in times when there are sharp \ndeclines in the percent returns. This visually confirms \nwhat the negative correlation coefficient suggests.",transform=fig.transFigure,size=15,color="black")

        plt.axis("off")
        pdf.savefig()
        plt.close()

        stocklist = [("GSPC","S&P 500"),("VIX","VIX"),("COST","Costco"),("CVX","Chevron"),("KO","Coca Cola"),("PEP","Pepsi"),("TGT","Target"),("WMT","Walmart"),("F","Ford"),("GE","General Electric")]

        whichstock = 0
        for stock,stockname in stocklist:
            whichstock+=1
            time = []
            price = []
            returns = []
            with open("/home/davidgrzan/Econophysics/Project1/"+stock+".txt") as tsv:

                #getting data from file
                for line in csv.reader(tsv,delimiter="\t"):
                    time.append(float(line[0]))
                    price.append(float(line[4]))

                #calculating
                timeL = time[1:]
                returnsL = logreturns(price)

                histvol = historicalvol(returnsL,21)
                timevol = time[21:]

                returnsP = percentreturns(price,252)
                timeP = time[252-1:]
                
                cor = correlation(histvol[252-21-1:],returnsP)

                #plotting
                fig1 = plt.figure(1)
                ax1 = fig1.add_subplot(2,1,1)
                ax2 = fig1.add_subplot(2,1,2)
                ax1.set_title("Trailing 12mo Percent Returns for the "+stockname,fontweight="bold")
                ax1.set_ylabel("Percent Return (%)",size=8)
                ax1.set_xlabel("Time (years)",size=8)
                ax2.set_title("Historical Volitility",fontweight="bold")
                ax2.set_ylabel("Volitility",size=8)
                ax2.set_xlabel("Time (years)",size=8)
                ax2.text(0.14,0.38,"Correlation Value: {:.2f}".format(cor),transform=fig1.transFigure,size=10,color="blue")

                ax1.plot(timeP,returnsP,color="black")
                ax2.plot(timevol[252-21-1:],histvol[252-21-1:],color="red")

                plt.subplots_adjust(hspace=0.5)
                pdf.savefig()
                plt.close()
                
                print("stock "+str(whichstock)+" written")
