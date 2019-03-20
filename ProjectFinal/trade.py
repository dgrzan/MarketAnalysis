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
            if stock1[index]>stock2[index]:
                self.stockS = stock1[index:]
                self.stockL = stock2[index:]
            else:
                self.stockS = stock2[index:]
                self.stockL = stock1[index:]
        else:
            if stock1[index]>stock2[index]:
                self.stockL = stock1[index:]
                self.stockS = stock2[index:]
            else:
                self.stockL = stock2[index:]
                self.stockS = stock1[index:]
        self.timelist = timelist[index:]
        self.starttime = starttime
        self.endtime = starttime
        self.startpriceL = self.stockL[0]
        self.endpriceL = self.stockL[0]
        self.startpriceS = self.stockS[0]
        self.endpricelS = self.stockS[0]
        self.inputamount = 0
        self.numberL = 0
        self.numberS = 0

    def set_inputamount(self,amount):
        self.inputamount = amount
        self.numberL = int((float(amount)/2)/self.startpriceL)
        self.numberS = int((float(amount)/2)/self.startpriceS)
        
    def get_starttime(self):
        return self.starttime
    
    def get_endtime(self):
        return self.endtime

    def get_startpriceL(self):
        return self.startpriceh

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
    

    
