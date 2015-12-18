################################################################################

#Tools for FIN503

#Bradford Lynch, 2015, Ann Arbor, MI

################################################################################

import numpy as np

class Bond(object):
    def __init__(self, parValue, couponRate, maturity, currentYield, yieldToMaturity, price):
        '''
        Creates a bond security, potentially with some missing data.
        '''
        self.par = parValue
        self.cr = couponRate
        self.mat = maturity
        self.cy = currentYield
        self.ytm = yieldToMaturity
        self.pr = price
        
    def calcPrice(self):
        if self.par != None and self.cr != None and self.cy != None:
            self.pr = (self.par*self.cr)/self.cy
        elif self.par != None and self.cr != None and self.ytm != None:
            self.pr = -1*np.pv(0.5*self.ytm, 2.0*self.mat, 0.5*self.par*self.cr, self.par)
            
        print "Bond price = $%.2f" % self.pr
        
    def calcYTM(self):
        self.ytm = 2*np.rate(2*self.mat, 0.5*self.par*self.cr, -1*self.pr, self.par)
        
        print "Bond's YTM = %0.2f%%" % (self.ytm*100)
        
    def calcCR(self):
        if self.par != None and self.cy != None and self.pr != None:
            self.cr = (self.cy*self.pr)/self.par
            
        print "Bond's CR = %0.2f%%" % (self.cr*100)
        
    def calcCY(self):
        if self.pr != None and self.par != None and self.cr != None:
            self.cy = (self.par*self.cr)/self.pr
            
        print "Bond's CY = %0.2f%%" % (self.cy*100)