#!/usr/bin/env python

import pickle
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm


if __name__ == "__main__":

    bidAskSum_file = "all.pckl"
    """
    data  = []
    with open(bidAskSum_file, 'rb') as f:
        while True:
            try:
            	d = pickle.load(f)
            	if d[2]>10000:
                    data.append(d)
       	    except EOFError:
            	break
    """

    data = []
    with open(bidAskSum_file, 'rb') as f:
        data = [d for d in pickle.load(f) if d[2]>10000]


    #Unpack data 	 
    bidsum, asksum, market_price, time = zip(*data)

    """
    ################ plot full timeline #################
    #Convert time to date
    #86400 sec/day
    date = [datetime.fromtimestamp(x) for x in time]
    
    #Plot
    unit = 600  #in seconds
    fig, ax = plt.subplots()
    ax2 = ax.twinx()

    ax.plot(date[::unit], bidsum[::unit], marker='', linestyle='-', c='g', label='bids sum')
    ax.plot(date[::unit], asksum[::unit], marker='', linestyle='-', c='r', label='asks sum')
    ax.legend(loc='upper left')
    ax.set_xlabel('Time')
    ax.set_ylabel('Quantity BTC')

    ax2.plot(date[::unit], market_price[::unit], linestyle='-', c='grey', label='market price', alpha=0.5)
    ax2.set_ylabel('Market Price[USD]')
    ax2.legend(loc='upper right')
    plt.rc('grid', linestyle='--', color='grey')
    ax.grid()

    plt.tight_layout()
    plt.show()
    """
    
    ################ plot price increase vs bidsum/asksum ratio at different time intervals ################
    
    #define a range
    start = 0.0
    end = 1.0
    bidsum = bidsum[int(start*len(time)):int(end*len(time))]
    asksum = asksum[int(start*len(time)):int(end*len(time))]
    market_price = market_price[int(start*len(time)):int(end*len(time))]
    time = time[int(start*len(time)):int(end*len(time))]
    """
    #choose interval
    interval = 60*60*24*1 #seconds
    
    #create data
    ratio = np.zeros(len(time)) #bidsum/asksum ratio
    ratioinv = np.zeros(len(time)) #asksum/bidsum ratio
    priceratio = np.zeros(len(time))

    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Progress~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    for i in tqdm(range(len(time))):        
        pricenow = market_price[i]
        ratio[i] = bidsum[i]/asksum[i]

        if(ratio[i] > 10):
            ratio[i] = np.nan
            priceratio[i] = np.nan
            continue

        if(i+interval>=len(time)-1):
            ratio[i] = np.nan
            priceratio[i] = np.nan
            continue
        
        t = time[i+interval]
        j = 0

        while t>time[i]+interval:
            j+=1000
            t = time[i+interval-j]
        
        if(abs(t-(time[i]+interval))>2000):
            ratio[i] = np.nan
            priceratio[i] = np.nan
        else:
            ratio[i] = bidsum[i]/asksum[i]
            ratioinv[i] = asksum[i]/bidsum[i]
            priceratio[i] = market_price[i+interval-j]/pricenow
    
    fig, ax = plt.subplots()
    ax.scatter(ratioinv, priceratio, s=1)
    ax.grid()
    """
    ################ plot bid/ask ratio deviation  ################
    lookback = 24*60 #min
    
    reducedtime = time[::60]
    reducedask = asksum[::60]
    reducedbid = bidsum[::60]
    reducedprice = market_price[::60]
    datee = [datetime.fromtimestamp(x) for x in reducedtime]
    deviate = np.zeros(len(reducedtime))
    reducedratio = np.zeros(len(reducedtime))
    for i in tqdm(range(len(reducedtime))):
        reducedratio[i] = reducedbid[i]/reducedask[i]
        deviate[i] = np.nan
        if(i>lookback and reducedratio[i]>0):
            std = np.std(reducedratio[i-lookback:i])
            avg = np.mean(reducedratio[i-lookback:i])
            deviate[i] = (reducedratio[i]-avg)/std
    fig6, ax6 = plt.subplots()
    ax7 = ax6.twinx()
    #ax8 = ax6.twinx()
    #ax6.plot(datee, deviate, color="r")
    ax7.plot(datee, reducedprice, color="grey", alpha=0.5)
    ax6.plot(datee, reducedbid)
    
    """
    #return on investment vs intervals of bid/ask ratio
    y = np.zeros(10)
    x = range(10)
    for j in range(10):
        count = 0
        for i in range(len(time)):
            if(ratio[i]>x[j] and ratio[i]<x[j]+1):
                count += 1
                y[j] += priceratio[i]
        y[j] = y[j]/float(count)

    fig2, ax2 = plt.subplots()
    ax2.scatter(x,y)
    ax2.grid()
    
    #price and frequency of high bid/ask ratio histograms
    
    date = [datetime.fromtimestamp(x) for x in time]
    fig3, ax3 = plt.subplots()
    ax3.plot(time, market_price, color="grey")

    count = np.zeros(len(time))
    for i in range(len(time)):
        if(ratio[i]>2.5):
            count[i] = time[i]
        else:
            count[i] = np.nan
    ax4 = ax3.twinx()
    ax4.hist(count, 5000, alpha=0.5, color="g")

    countinv = np.zeros(len(time))
    for i in range(len(time)):
        if(ratioinv[i]>2.0):
            countinv[i] = time[i]
        else:
            countinv[i] = np.nan
    ax5 = ax3.twinx()
    ax5.hist(countinv, 5000, alpha=0.5, color="r")
    """
    
    plt.show()
    
