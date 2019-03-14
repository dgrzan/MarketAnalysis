import math
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from scipy.optimize import curve_fit
import scipy.fftpack
from matplotlib.backends.backend_pdf import PdfPages
import random

#returns array of a random walk with drift and time list
#randomwalkdrift(number of time steps, timestep, slope of trend, y-intercept of trend)
def randomwalk(n,stepsize=1,timestep=1,m=0,b=0):
    y = []
    t = np.linspace(0,n*timestep,n)
    bounds = [-stepsize,stepsize]
    for i in range(n):
        if (i==0):
            y.append(b)
        else:
            y.append(bounds[random.randint(0,1)]+m*timestep+y[i-1])
    return t, y

#returns array of a walk determined by simple Brownian motion
#brownianwalk(number of time steps, mean, standard deviation, timestep, slope of trend, y-intercept of trend)
def brownianwalk(n,mean,sd,timestep=1,m=0,b=0):
    y = []
    t = np.linspace(0,n*timestep,n)
    for i in range(n):
        if (i==0):
            y.append(0)
        else:
            y.append(random.gauss(mean,sd)+m*timestep+y[i-1])
    return t, y

#returns array of a white noise process
#whitenoise(number of time steps, mean, standard deviation, timestep)
def whitenoise(n,mean,sd,timestep=1):
    noise = []
    t = np.linspace(0,n*timestep,n)
    for i in range(n):
        noise.append(random.gauss(mean,sd))
    return t, noise

#linear fit function
#line(input, slope, y-intercept)
def line(x,slope,b):
    return slope*x + b

#linear function in logx logy coordinates mapped to x y coordinates
#logline(input, slope in log space, intercept in log space)
def logline(x,slope,b):
    return (10**b)*x**slope

#gaussian fit function
#gauss(input, mean, standard deviation)
def gaussnorm(x,m,s):
    return (1/(s*(2*math.pi)**(0.5)))*math.e**((-0.5)*((x-m)**2)/s**2)

#gaussian function
#gauss(input, amp (weight), mean, standard deviation)
def gauss(x,a,m,s):
    return (a/(s*(2*math.pi)**(0.5)))*math.e**((-0.5)*((x-m)**2)/s**2)

#returns linear fit parameters for a given data set
#fitline(x-axis list, y-xaxis list)
def fitline(x,y,verb=1):
    parameters, cov_matrix = curve_fit(line, x, y)
    slopeerr, intercepterr = np.diag(cov_matrix)
    if verb==1:
        print("Line Fit Parameters~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("slope: "+str(parameters[0])+" +- "+str(slopeerr)+"\n"+"intercept: "+str(parameters[1])+" +- "+str(intercepterr))
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
    return parameters

#fits a power relation to a dataset
#fitpower(x-axis list, y-axis list)
def fitpower(x,y,verb=1):
    parameters, cov_matrix = curve_fit(logline,x,y)
    slopeerr, intercepterr = np.diag(cov_matrix)
    if verb==1:
        print("Exp Fit Parameters~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("slope: "+str(parameters[0])+" +- "+str(slopeerr)+"\n"+"intercept: "+str(parameters[1])+" +- "+str(intercepterr))
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
    return parameters

#returns gaussian fit parameters for a given data set
#fitgauss(x-axist list, y-axist list)
def fitgauss(x,y,verb=1):
    binwidth = x[1]-x[0]
    count = 0
    for val in y:
        count+=val
    weight = count*binwidth
    for i in range(len(y)):
        y[i]/=weight
    parameters, cov_matrix = curve_fit(gaussnorm, x, y)
    para = [weight]
    for i in range(len(parameters)):
        para.append(parameters[i])
    meanerr,sderr = np.diag(cov_matrix)
    if verb==1:
        print("Gaussian Fit Parameters~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("weight: "+str(para[0])+"\n"+"mean: "+str(para[1])+" +- "+str(meanerr)+"\n"+"sd: "+str(para[2])+" +- "+str(sderr))
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
    return para

#returns list of bin centers from histogram bounds list
#bincenters(
def bincenters(bounds):
    return 0.5*(bounds[1:]+bounds[:-1])

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

#returns weight of set of data
#weight(data list)
def weight(x):
    weight = 0
    for i in range(len(x)):
        weight+=x[i]
    return weight

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
    
#returns autocorrelation function number from a set of data
#autocorrelation(data list,time lag (in steps))
def autocorrelation(x,timelag):
    if timelag>=len(x):
        print("ERROR: Time lag is greater than lengh of array")
    m = mean(x)
    sdv = sd(x)
    n = len(x)
    correlation = 0
    for i in range(n):
        if i>=timelag:
            correlation+=(x[i-timelag]-m)*(x[i]-m)
    correlation/=sdv*sdv*n
    return correlation

#returns time difference list from a data list
#timediff(data list, timesteps between points that you take the difference of)
def timediff(x,timesteps=1):
    diff = []
    for i in range(len(x)):
        if i>timesteps-1:
            diff.append(x[i]-x[i-timesteps])
    return diff

#returns power spectrum (|x(f)|^2) of set of data and its frequency list
#powerspectrum(data list, time between each data point)
def powerspectrum(x,timestep=1):
    n = len(x)
    timestep = float(timestep)
    f = np.linspace(0,1/(2*timestep),n//2)
    s = np.abs(scipy.fftpack.fft(x))
    s = s*s
    s = s[:n//2]
    snozero = []
    fnozero = []
    for i in range(len(s)):
        if s[i]>0 and f[i]>0:
            snozero.append(s[i])
            fnozero.append(f[i])
    return fnozero, snozero

#returns volitility of a dataset and time list ascociated with it
#volitility(data list, time window (steps))
def volitility(x,timewindow):
    n = len(x)
    if timewindow>n:
        print("ERROR: time window is greater than length of list")
        return float("nan")
    t = []
    v = []
    for i in range(n):
        if i+1>=timewindow:
            t.append(i)
            v.append(sd(x[i+1-timewindow:i]))
    return t, v

#returns standard deviation of log returns annualized to 1 year
#historicalvolitility(data list, time window (steps))
def historicalvolitility(x, timewindow):
    v = []
    for i in range(len(x)):
        if (i+1)>=timewindow:
            vol = 0
            for j in range(timewindow):
                vol+=x[i-j]**2
            ((252/timewindow)*vol)**0.5
            v.append(vol)
    return v

#returns a list of the log returns
#logreturns(data list)
def logreturns(x):
    returns = []
    for j in range(len(x)):
        if j>0:
            returns.append(math.log(x[j])-math.log(x[j-1]))
    return returns

#returns a list of the percent returns
#percentreturns(data list, time period over which to compare values)
def percentreturns(x, timewindow):
    returns = []
    for i in range(len(x)):
        if (i+1)>=timewindow:
            returns.append(100*(x[i]-x[i-timewindow+1])/x[i-timewindow+1])
    return returns

#returns list of moving average of data
#movingavg(data list, time window)
def movingavg(x,timewindow):
    n = len(x)
    if timewindow>n:
        print("ERROR: time window is greater than length of list")
        return float("nan")
    t = []
    avg = []
    for i in range(n):
        if i+1>=timewindow:
            t.append(i)
            avg.append(mean(x[i+1-timewindow:i]))
    return t, avg

#returns list of exponentially weighted moving average
#movingaveexp(data list, time window, half life of exp)
