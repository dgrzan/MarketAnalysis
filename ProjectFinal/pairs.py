#!/usr/bin/python

import pairsfunctions as f
import math
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from scipy.optimize import curve_fit
import scipy.fftpack
from matplotlib.backends.backend_pdf import PdfPages
import random
import trade
import budgetcontrol


if __name__ == "__main__":

    #list of stocks that will be paired together, along with their names
    pairslist = [("CVX","Chevron","XOM","ExxonMobil")]
    portfolio = []

    #looping through pairs of stocks
    for stock1,stockname1,stock2,stockname2 in pairslist:
        time1 = []
        time2 = []
        price1 = []
        price2 = []
        
        #getting data from first stock
        with open("/home/davidgrzan/Econophysics/ProjectFinal/StockData/"+stock1+".txt") as tsv:
            for line in csv.reader(tsv,delimiter="\t"):
                time1.append(float(line[0]))
                price1.append(float(line[4]))
            tsv.close()
                
        #getting data from second stock
        with open("/home/davidgrzan/Econophysics/ProjectFinal/StockData/"+stock2+".txt") as tsv:
            for line in csv.reader(tsv,delimiter="\t"):
                time2.append(float(line[0]))
                price2.append(float(line[4]))
            tsv.close()

        #truncating list to include only the past 10 years
        time1 = time1[-2520:]
        time2 = time2[-2520:]
        price1 = price1[-2520:]
        price2 = price2[-2520:]
            
        #calculating quantities
        timecor252, cor252 = f.correlation(price1,price2,252,time1)
        timecor504, cor504 = f.correlation(price1,price2,504,time1)
        print(f.correlationall(price1,price2))
        timeratio, priceratio = f.ratio(price1,price2,time1)
        timesd3mo, movingsd3mo = f.movingsd(priceratio,63,timeratio)
        timeavg3mo, movingavg3mo = f.movingavg(priceratio,63,timeratio)
        timeavg5d, movingavg5d = f.movingavg(priceratio,5,timeratio)
        low1, high1 = f.sdbounds(movingavg3mo,movingsd3mo,1)
        zscoree = f.zscore(movingavg5d,movingavg3mo,movingsd3mo)
        when, whenlist = f.whentotrade(zscoree,timeavg3mo,1.5)
        #print(f.cointigration(price1[:],price1[:]))

        #instantiates trade objects
        trades = []
        for tradetime in when:
            location = np.sign(zscoree[f.indexoftime(timeavg3mo,tradetime)])
            trades.append(trade.trade(price1,price2,time1,tradetime,location))
            trades[len(trades)-1].set_inputamount(1000)

        totalreturns = 0
        for q in range(len(trades)):
            starttime = trades[q].get_starttime()
            startindex = f.indexoftime(timeavg3mo,starttime)
            timezscore = timeavg3mo[startindex:]
            for qq in range(len(zscoree[startindex:])-1):
                if (np.sign(zscoree[startindex+qq+1])==1 and np.sign(zscoree[startindex+qq])==-1) or (np.sign(zscoree[startindex+qq+1])==-1 and np.sign(zscoree[startindex+qq])==1):
                    trades[q].exittrade(timezscore[qq+1])
                    break

            totalreturns+=trades[q].get_totalreturns()
        print("Total Profit: "+str(totalreturns))

        portfolio.append(trades)
        
        #plotting
        fig1 = plt.figure(1,figsize=(16,8))
        ax1 = fig1.add_subplot(3,1,1)
        ax2 = fig1.add_subplot(3,1,2)
        ax3 = fig1.add_subplot(3,1,3)
        ax1.plot(time1,price1,color="red")
        ax1.plot(time2,price2,color="blue")
        ax2.plot(timeratio,priceratio,color="green")
        ax2.plot(timeavg3mo,movingavg3mo,color="orange")
        ax2.plot(timeavg5d,movingavg5d,color="black")
        ax2.plot(timeavg3mo,low1,color="red",linestyle="--")
        ax2.plot(timeavg3mo,high1,color="red",linestyle="--")
        ax3.plot(timecor252,cor252,color="green")
        ax3.plot(timecor504,cor504,color="black")

        fig2 = plt.figure(2,figsize=(16,8))
        ax21 = fig2.add_subplot(1,1,1)
        ax21.plot(timeavg3mo,zscoree,color="black")
        ax21.plot(timeavg3mo,whenlist,color="red")
        
        plt.show()
        plt.close()


    
