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

    #relavent variables to change:
    uppersigma = 1.5
    lowersigma = 1
    longavgtime = 21*3
    lookback = 252*30
    shortavgtime = 2
    
    #list of stocks that will be paired together, along with their names
    pairslist = [("CVX","Chevron","XOM","ExxonMobil"),("KO","Coca Cola","PEP","Pepsi"),("DUK","Duke Energy","NEE","NextEra Energy"),("LOW","Lowe's","HD","Home Depot"),("MCD","McDonald's","YUM","Yum! Brands"),("UPS","UPS","FDX","FedEx"),("WMT","Walmart","TGT","Target"),("V","Visa","AXP","American Express"),("WBA","Walmart","CVS","CVS"),("VZ","Verizon","T","AT&T"),("BUD","Budweiser","TAP","Coors")]
    #do not use: ("HPQ","HP","IBM","IBM") cor=-0.63
    #do not use: ("UAA","Unde Armour","NKE","Nike") cor = 0.65
    #do not use: ("SNE","Sony","MSFT","Microsoft")
    portfolio = []
    totalprofit = 0
    
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
        lookbacktime = lookback
        if len(price1)<lookbacktime or len(price2)<lookbacktime:
            if len(price1)<len(price2):
                lookbacktime=len(price1)
            else:
                lookbacktime=len(price2)
        time1 = time1[-lookbacktime:]
        time2 = time2[-lookbacktime:]
        price1 = price1[-lookbacktime:]
        price2 = price2[-lookbacktime:]

        if stock1=="KO": totaltime = time1
            
        #calculating quantities
        timecor252, cor252 = f.correlation(price1,price2,21*3,time1)
        timecor504, cor504 = f.correlation(price1,price2,504,time1)
        print("Correlation between "+stockname1+" and "+stockname2+": "+str(f.correlationall(price1,price2)))
        timeratio, priceratio = f.ratio(price1,price2,time1)
        timesd3mo, movingsd3mo = f.movingsd(priceratio,21*3,timeratio)
        timeavg3mo, movingavg3mo = f.movingavg(priceratio,21*3,timeratio)
        timeavg5d, movingavg5d = f.movingavg(priceratio,2,timeratio)
        low1, high1 = f.sdbounds(movingavg3mo,movingsd3mo,1.5)
        zscoree = f.zscore(movingavg5d,movingavg3mo,movingsd3mo)
        when, whenlist = f.whentotrade(zscoree,timeavg3mo,cor252,1.5)
        #print("Cointigration Value: "+str(f.cointigration(price1,price2)))

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
            zscoreupdate = zscoree[startindex:]
            sigbounds = 1
            for qq in range(len(zscoreupdate)-2):
                trades[q].exittrade(timezscore[qq+2])
                if trades[q].get_totalreturns()<-100:
                    #print("RETURNS BELOW -100")
                    starttt=trades[q].get_starttime()
                    #print("index: "+str(q))
                    #print("time: "+str(starttt))
                    #if f.indexoftime(timeavg3mo,starttt)-1>=0: print(movingavg3mo[f.indexoftime(timeavg3mo,starttt)]-movingavg3mo[f.indexoftime(timeavg3mo,starttt)-1])
                    break
                else:
                    trades[q].unexittrade()
                if (zscoreupdate[qq+1]<sigbounds and zscoreupdate[qq]>sigbounds) or (zscoreupdate[qq+1]>-sigbounds and zscoreupdate[qq]<-sigbounds):
                    trades[q].exittrade(timezscore[qq+2])
                    break

            totalreturns+=trades[q].get_totalreturns()
            if stock1=="CVX": print(trades[q].get_totalreturns(),q)
            #print(trades[q].get_expectedratiodirection(),trades[q].get_ratiodirection())
            #print("Long Prices: "+str((trades[q].get_startpriceL(),trades[q].get_endpriceL())))
            #print("Short Prices: "+str((trades[q].get_startpriceS(),trades[q].get_endpriceS())))
            if stock1=="CVX": teststarttime = trades[481].get_starttime()
            if stock1=="CVX": testendtime = trades[481].get_endtime()

        print("Total Trades: "+str(len(trades)))
        print("Total Profit: "+str(totalreturns))
        totalprofit+=totalreturns
        portfolio.append(trades)

        if stock1=="CVX":   
            #plotting
            fig11 = plt.figure(11,figsize=(16,8))
            fig12 = plt.figure(12,figsize=(16,8))
            fig13 = plt.figure(13,figsize=(16,8))
            ax1 = fig11.add_subplot(1,1,1)
            ax2 = fig12.add_subplot(1,1,1)
            ax3 = fig13.add_subplot(1,1,1)
            ax1.plot(time1,price1,color="red")
            ax1.plot(time2,price2,color="blue")
            ax1.set_title("Prices of "+stockname1+" and "+stockname2,size=20)
            ax1.set_xlabel("Time (years)")
            ax1.set_ylabel("Price (USD)")
            ax2.plot(timeratio,priceratio,color="green")
            ax2.plot(timeavg3mo,movingavg3mo,color="orange")
            ax2.plot(timeavg5d,movingavg5d,color="black")
            ax2.plot(timeavg3mo,low1,color="red",linestyle="--")
            ax2.plot(timeavg3mo,high1,color="red",linestyle="--")
            ax2.set_title("Spread Ratio of "+stockname1+" and "+stockname2,size=20)
            ax2.set_xlabel("Time (years)")
            ax2.set_ylabel("Ratio of price")
            ax3.plot(timecor252,cor252,color="green")
            #ax3.plot(timecor504,cor504,color="black")
            ax3.set_title("Correlation Function (3 Months)",size=20)
            ax2.set_xlabel("Time (years)")
            ax2.set_ylabel("Correlation Value")
            
            fig2 = plt.figure(2,figsize=(16,8))
            ax21 = fig2.add_subplot(1,1,1)
            ax21.plot(timeavg3mo,zscoree,color="black")
            #ax21.plot(timeavg3mo,whenlist,color="red")
            ax21.plot(timeavg3mo,np.zeros(len(timeavg3mo))+1,color="blue",linestyle="--")
            ax21.plot(timeavg3mo,np.zeros(len(timeavg3mo))+1.5,color="green",linestyle="--")
            ax21.plot(timeavg3mo,np.zeros(len(timeavg3mo))-1,color="blue",linestyle="--")
            ax21.plot(timeavg3mo,np.zeros(len(timeavg3mo))-1.5,color="green",linestyle="--")
            ax21.plot(timeavg3mo,np.zeros(len(timeavg3mo)),color="red",linestyle="--")
            ax21.set_title("Z-Score of Spread Ratio",size=20)
            ax21.set_xlabel("Time (years)")
            ax21.set_ylabel("Z-score (standard deviations from mean)")
            
            fig3 = plt.figure(3,figsize=(16,8))
            ax31 = fig3.add_subplot(3,1,1)
            ax32 = fig3.add_subplot(3,1,3)
            ax33 = fig3.add_subplot(3,1,2)
            ax31.plot(timeavg5d[f.indexoftime(timeavg5d,teststarttime):f.indexoftime(timeavg5d,testendtime)],movingavg5d[f.indexoftime(timeavg5d,teststarttime):f.indexoftime(timeavg5d,testendtime)])
            #ax31.plot(timeavg3mo,movingavg3mo,color="orange")
            #ax31.plot(timeavg3mo,low1,color="red",linestyle="--")
            #ax31.plot(timeavg3mo,high1,color="red",linestyle="--")
            ax31.plot(timeavg3mo[f.indexoftime(timeavg3mo,teststarttime):f.indexoftime(timeavg3mo,testendtime)],movingavg3mo[f.indexoftime(timeavg3mo,teststarttime):f.indexoftime(timeavg3mo,testendtime)],color="orange")
            ax31.plot(timeavg3mo[f.indexoftime(timeavg3mo,teststarttime):f.indexoftime(timeavg3mo,testendtime)],low1[f.indexoftime(timeavg3mo,teststarttime):f.indexoftime(timeavg3mo,testendtime)],color="red",linestyle="--")
            ax31.plot(timeavg3mo[f.indexoftime(timeavg3mo,teststarttime):f.indexoftime(timeavg3mo,testendtime)],high1[f.indexoftime(timeavg3mo,teststarttime):f.indexoftime(timeavg3mo,testendtime)],color="red",linestyle="--")
            ax32.plot(time1[f.indexoftime(timeratio,teststarttime):f.indexoftime(timeratio,testendtime)],price1[f.indexoftime(timeratio,teststarttime):f.indexoftime(timeratio,testendtime)],color="red")
            ax32.plot(time2[f.indexoftime(timeratio,teststarttime):f.indexoftime(timeratio,testendtime)],price2[f.indexoftime(timeratio,teststarttime):f.indexoftime(timeratio,testendtime)],color="blue")
            ax33.plot(timeavg3mo[f.indexoftime(timeavg3mo,teststarttime):f.indexoftime(timeavg3mo,testendtime)],zscoree[f.indexoftime(timeavg3mo,teststarttime):f.indexoftime(timeavg3mo,testendtime)])
            
            #plt.show()
            #plt.close()

    print("Total Pairs Profit: "+str(totalprofit))

    profitlist = np.zeros(len(totaltime))
    totalprofitss = 0
    numberoftrades = np.zeros(len(totaltime))
    for i in range(len(portfolio)):
        trades = portfolio[i]
        for j in range(len(trades)):
            tradeendi = f.indexoftime(totaltime,trades[j].get_endtime())
            profitlist[tradeendi]+=trades[j].get_totalreturns()
            totalprofitss+=trades[j].get_totalreturns()
            tradestarti = f.indexoftime(totaltime,trades[j].get_starttime())
            numberoftrades[tradestarti]+=1
            numberoftrades[tradeendi]-=1

    cumulativeprof = np.zeros(len(profitlist))
    cumuprof = 0
    cumulativetrades = np.zeros(len(numberoftrades))
    cumutrades = 0
    for i in range(len(profitlist)):
        cumuprof+=profitlist[i]
        cumulativeprof[i]=cumuprof
        cumutrades+=numberoftrades[i]
        cumulativetrades[i]=cumutrades

    fig4 = plt.figure(4,figsize=(16,8))
    ax41 = fig4.add_subplot(1,1,1)
    ax41.plot(totaltime,cumulativeprof,color="green")
    ax41.set_title("Cumulative Profit",size=20)
    ax41.set_xlabel("Time (years)")
    ax41.set_ylabel("Total Profit (USD)")

    fig5 = plt.figure(5,figsize=(16,8))
    ax51 = fig5.add_subplot(1,1,1)
    ax51.plot(totaltime,cumulativetrades,color="blue")
    ax51.set_title("Number of Active Trades",size=20)
    ax51.set_xlabel("Time (years)")
    ax51.set_ylabel("Number of Active Trades")
    
    print("Total: "+str(totalprofitss))
    
    plt.show()
    plt.close()
    
