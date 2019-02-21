import csv
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from matplotlib.backends.backend_pdf import PdfPages

if __name__ == "__main__":

    with PdfPages("Project4_David_Grzan.pdf") as pdf:

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
                time = time[1:]
                
                for j in range(len(price)):
                    if j>0:
                        returns.append(math.log(price[j])-math.log(price[j-1]))

                #plotting data
                num = 100     #number of bins
                fig = plt.figure(1)
                ax = fig.add_subplot(1,1,1)
                ax.set_title(stockname+" Log Returns")
                ax.set_xlabel("Log Returns")
                ax.set_ylabel("Counts")
                n, bins, patches = ax.hist(returns,num,density=0,facecolor="g")

                #fitting
                m, s = stats.norm.fit(returns)
                line = stats.norm.pdf(np.linspace(bins[0],bins[len(bins)-1],num),m,s)
                weight =(float((bins[len(bins)-1]-bins[0])/num))*len(returns)
                for k in range(len(line)):
                    line[k]*=weight
                ax.plot(np.linspace(bins[0],bins[len(bins)-1],num),line,color="red")
                ax.set_xlim([m-5*s,m+5*s])
                kurt = 0
                for k in range(len(returns)):
                    kurt+=((returns[k]-m)**4)/(len(returns)*s**4)
                ax.text(0.6,0.7,"Kurtosis Value: {:.1f}".format(kurt),transform=fig.transFigure,size=10,color="black")

                #calculating kurtosis of gaussian
                kurt = 0
                xaxis = np.linspace(bins[0],bins[len(bins)-1],num)
                capN = 0
                for k in range(len(line)):
                    capN+=line[k]
                    kurt+=((xaxis[k]-m)**4)*line[k]

                kurt/=(capN*s**4)
                    
                print(kurt)    
                
                pdf.savefig()
                plt.close()
                
                #plotting log plot
                fig2 = plt.figure(2)
                ax = fig2.add_subplot(1,1,1)
                ax.set_title(stockname+" Log Returns (Log plot)")
                ax.set_xlabel("Log Returns")
                ax.set_ylabel("Counts (log scale)")
                ax.hist(returns,num,density=0,facecolor="blue")

                #fitting log plot
                ax.plot(np.linspace(bins[0],bins[len(bins)-1],num),line,color="red")
                ax.set_yscale("log")
                ax.set_xlim([m-5*s,m+5*s])
                ax.set_ylim([1,1.1*max(n)])
                ax.text(0.6,0.8,"Tail excess can be clearly seen here, \nclearly indicating a leptokurtic \ndistribution",transform=fig2.transFigure,size=7,color="black")

                pdf.savefig()
                plt.close()
                
                del time, price, returns, fig, fig2, ax, n, bins, patches, m, s, line

                print("stock "+str(whichstock)+" written")
