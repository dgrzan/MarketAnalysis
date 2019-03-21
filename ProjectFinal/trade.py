import numpy as np
import pairsfunctions as f

#This class handles a single pairs trade and when to end it
class trade:

    shortreturn = 0
    longreturn = 0
    exitedtrade = 0
    
    def __init__(self,stock1,stock2,timelist,starttime,location):
        index = f.indexoftime(timelist,starttime)
        if location>0:
            self.stockS = stock1[index:]
            self.stockL = stock2[index:]
        else:
            self.stockL = stock1[index:]
            self.stockS = stock2[index:]
        self.stock1 = stock1[index:]
        self.stock2 = stock2[index:]
        self.timelist = timelist[index:]
        self.starttime = starttime
        self.endtime = starttime
        self.startpriceL = self.stockL[0]
        self.endpriceL = self.stockL[0]
        self.startpriceS = self.stockS[0]
        self.endpriceS = self.stockS[0]
        self.inputamount = 0
        self.numberL = 0
        self.numberS = 0
        self.direction = -1*location

    def get_expectedratiodirection(self):
        return self.direction

    def get_ratiodirection(self):
        if self.exitedtrade==1:
            ratiofirst = self.stock1[0]/self.stock2[0]
            ratiosecond = self.stock1[f.indexoftime(self.timelist,self.endtime)]/self.stock2[f.indexoftime(self.timelist,self.endtime)]
            return np.sign(ratiosecond-ratiofirst)
        else:
            return 0

    def set_inputamount(self,amount):
        self.inputamount = amount
        self.numberL = int((float(amount)/2)/self.startpriceL)
        self.numberS = int((float(amount)/2)/self.startpriceS)
        
    def get_starttime(self):
        return self.starttime
    
    def get_endtime(self):
        return self.endtime

    def get_startpriceL(self):
        return self.startpriceL

    def get_startpriceS(self):
        return self.startpriceS

    def get_endpriceL(self):
        return self.endpriceL

    def get_endpriceS(self):
        return self.endpriceS

    def get_inputamount(self):
        return self.inputamount

    def exittrade(self,endtime):
        index = f.indexoftime(self.timelist,endtime)
        self.endtime = endtime
        self.endpriceL = self.stockL[index]
        self.endpriceS = self.stockS[index]
        self.exitedtrade = 1

    def unexittrade(self):
        self.exitedtrade = 0
        self.endtime = self.starttime
        self.endpriceL = self.startpriceL
        self.endpriceS = self.startpriceS
        self.shortreturn = 0
        self.longreturn = 0

    def get_shortreturn(self):
        if self.exitedtrade==1:
            self.shortreturn = self.numberS*(self.startpriceS-self.endpriceS)
            return self.shortreturn
        else:
            return 0
        
    def get_longreturn(self):
        if self.exitedtrade==1:
            self.longreturn = self.numberL*(self.endpriceL-self.startpriceL)
            return self.longreturn
        else:
            return 0

    def get_totalreturns(self):
        return self.get_shortreturn()+self.get_longreturn()
    

    
