import math
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from scipy.optimize import curve_fit
import scipy.fftpack
from matplotlib.backends.backend_pdf import PdfPages
import random

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

#returns correlation function accross a time window for two sets of data
#correlation(data list 1, datalist 2, timewindow, time list)
def correlation(x1, x2, timewindow, timelist):
    if len(x1)>len(x2):
        x1=x1[len(x1)-len(x2):]
    if len(x1)<len(x2):
        x2=x2[len(x2)-len(x1):]
    if len(x1)==len(timedinow):
        
    cor = []
    for i in range(len(x1)):
        if i+1>=timewindow:
            for j in range(timewindow):
                cor.append(correlation(x1[i-timewindow+1:i],x2[i-timewindow+1:i]))
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
