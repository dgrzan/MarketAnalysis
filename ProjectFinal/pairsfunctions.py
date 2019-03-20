import math
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from scipy.optimize import curve_fit
import scipy.fftpack
from matplotlib.backends.backend_pdf import PdfPages
import random
import statsmodels.api as sm
import pandas as pd

#returns mean for set of data
#mean(data list)
def mean(x):
    mean = 0.0
    length = float(len(x))
    for val in x:
        mean+=val/length
    return mean

#returns value of standard deviation for a set of data
#sd(data list)
def sd(x):
    sdv = 0.0
    n = float(len(x))
    m = mean(x)
    for val in x:
        sdv+=((val-m)**2)/n
    sdv=sdv**(0.5)
    return sdv

#returns correlation function number between two sets of data
#correlation(data list 1, data list 2)
def correlationall(x1,x2):
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

#returns correlation function accross a time window for two sets of data
#correlation(data list 1, datalist 2, timewindow, time list)
def correlation(x1, x2, timewindow, timelist):
    if len(x1)>len(x2):
        x1=x1[len(x1)-len(x2):]
        if len(x1)==len(timelist):
            timelist=timelist[len(x1)-len(x2):]
    if len(x1)<len(x2):
        x2=x2[len(x2)-len(x1):]
        if len(x2)==len(timelist):
            timelist=timelist[len(x2)-len(x1):]
    cor = []
    for i in range(len(x1)):
        if i+1>=timewindow:
            cor.append(correlationall(x1[i-timewindow+1:i],x2[i-timewindow+1:i]))
    return timelist[timewindow-1:], cor

#returns list of moving average of data
#movingavg(data list, time window, time list)
def movingavg(x,timewindow,timelist):
    n = len(x)
    if timewindow>n:
        print("ERROR: time window is greater than length of list")
        return float("nan")
    avg = []
    for i in range(n):
        if i+1>=timewindow:
            avg.append(mean(x[i+1-timewindow:i]))
    return timelist[timewindow-1:], avg

#returns list of moving standard deviation
#movingsd(data list, time window, time list)
def movingsd(x,timewindow,timelist):
    n = len(x)
    if timewindow>n:
        print("ERROR: time window is greater than length of list")
        return float("nan")
    movinsd = []
    for i in range(n):
        if i+1>=timewindow:
            movinsd.append(sd(x[i+1-timewindow:i]))
    return timelist[timewindow-1:], movinsd

#returns two lists of standard deviations around the mean
#sdbounds(moving average list, standard deviaion list, number of standard deviations from mean)
def sdbounds(mvavg, sdlist, sds):
    if len(mvavg)!=len(sdlist):
        print("ERROR: list sizes are not the same")
    high = []
    low = []
    for i in range(len(mvavg)):
        high.append(mvavg[i]+sds*sdlist[i])
        low.append(mvavg[i]-sds*sdlist[i])
    return low, high

#returns ratio of two stocks
#ratio(data list 1, data list 2)
def ratio(x1,x2,timelist):
    rat = []
    if len(x1)>len(x2):
        x1=x1[len(x1)-len(x2):]
        if len(x1)==len(timelist):
            timelist=timelist[len(x1)-len(x2):]
    if len(x1)<len(x2):
        x2=x2[len(x2)-len(x1):]
        if len(x2)==len(timelist):
            timelist=timelist[len(x2)-len(x1):]
    for i in range(len(x1)):
        rat.append(x1[i]/x2[i])
    return timelist, rat

#returns cointigration number for two stocks
#cointigration(x1, x2)
def cointigration(x1, x2):
    return sm.tsa.coint(x1,x2)

#returns z = (ratio-mean)/sd
#zscore(ratio,mean of ratio,sd of ratio)
def zscore(ratio,meann,sdev):
    z = []
    ratio = ratio[-len(meann):]
    for i in range(len(meann)):
        z.append((ratio[i]-meann[i])/sdev[i])
    return z

#returns a list of index of times for when to trade, and a list to plot when trades happened
#whentotrade(zscore list, time list, sd's threshold)
def whentotrade(zscoree,timelist,sds):
    when = []
    whenlist = []
    lastval = 0
    for i in range(len(zscoree)):
        whenlist.append(0)
        if (lastval<sds and lastval>-sds) and (zscoree[i]>sds or zscoree[i]<-sds):
            when.append(timelist[i])
            whenlist[i]+=1
        lastval = zscoree[i]
    return when, whenlist

#returns index of timelist where a given time is
#indexoftime(timelist,time)
def indexoftime(timelist,time):
    for i in range(len(timelist)):
        if timelist[i]==time:
            return i
    return -1
