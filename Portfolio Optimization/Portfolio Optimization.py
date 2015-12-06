################################################################################

#Tools for analyzing and plotting datasets

#Stadia42, Bradford Lynch, 2014, Chicago, IL

################################################################################
import matplotlib.pyplot as plt
import pandas as pd
import pandas.io.data as web
import numpy as np
import scipy.optimize as sco

def getStockQuotes(symbols, source, startDate, endDate):
    quotes = pd.DataFrame()
    
    for symbol in symbols:
        quotes[symbol] = web.DataReader(symbol, data_source=source, start=startDate, end=endDate)['Adj Close']
        
    return quotes
    
def calcPortfolioPerf(weights, meanReturns, covMatrix):    
    #Calculate return and variance
    portReturn = np.sum( meanReturns*weights )
    portStdDev = np.sqrt(np.dot(weights.T, np.dot(covMatrix, weights)))
    
    return portReturn, portStdDev
    
def negSharpeRatio(weights, meanReturns, covMatrix, riskFreeRate):
    p_ret, p_var = calcPortfolioPerf(weights, meanReturns, covMatrix)
    
    return -(p_ret - riskFreeRate) / p_var
    
def getPortfolioVol(weights, meanReturns, covMatrix):
    return calcPortfolioPerf(weights, meanReturns, covMatrix)[1]

def getPortfolioVar(weights, meanReturns, covMatrix):
    p_ret, p_var = calcPortfolioPerf(weights, meanReturns, covMatrix)
    
    return p_var**2
    
def findMaxSharpeRatioPortfolio(weights, meanReturns, covMatrix, riskFreeRate):
    numAssets = len(weights)
    args = (meanReturns, covMatrix, riskFreeRate)
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bounds = tuple( (0,1) for asset in range(numAssets))
    
    opts = sco.minimize(negSharpeRatio, numAssets*[1./numAssets,], args=args, method='SLSQP', bounds=bounds, constraints=constraints)
    
    return opts
    
def findMinVariancePortfolio(weights, meanReturns, covMatrix):
    numAssets = len(weights)
    args = (meanReturns, covMatrix)
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bounds = tuple( (0,1) for asset in range(numAssets))
    
    opts = sco.minimize(getPortfolioVol, numAssets*[1./numAssets,], args=args, method='SLSQP', bounds=bounds, constraints=constraints)
    
    return opts
    
def findEfficientReturn(weights, meanReturns, covMatrix, targetReturn):
    numAssets = len(weights)
    args = (meanReturns, covMatrix)
    
    def getPortfolioReturn(weights):
        return calcPortfolioPerf(weights, meanReturns, covMatrix)[0]
    
    constraints = ({'type': 'eq', 'fun': lambda x: getPortfolioReturn(x) - targetReturn},
                   {'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bounds = tuple((0,1) for asset in range(numAssets))
    
    return sco.minimize(getPortfolioVol, numAssets*[1./numAssets,], args=args, method='SLSQP', bounds=bounds, constraints=constraints)
    
def findEfficientFrontier(weights, meanReturns, covMatrix, rangeOfReturns):
    efficientPortfolios = []
    for ret in rangeOfReturns:
        efficientPortfolios.append(findEfficientReturn(weights, meanReturns, covMatrix, ret))
        
    return efficientPortfolios
    

availStocks = ['GOOGL', 'AAPL', 'AMZN', 'MSFT', 'F', 'BMW.DE', 'TM', 'KO', 'PEP']
#stocks = availStocks
#stocks = ['GOOGL', 'TM', 'KO', 'PEP']
stocks = [availStocks[i] for i in np.random.random_integers(0,len(availStocks)-1, 3)]
numAssets = len(stocks)
source = 'yahoo'
start = '2010-01-01'
end = '2015-10-31'

#Retrieve data from online
#data = getStockQuotes(stocks, source, start, end)

#Load data from disk
data = pd.read_hdf('./stockData.h5', 'quotes').select(lambda x: x in stocks, 1)

#Calculate returns
riskFreeRate = 0.0021
dur = 20
numPeriodsAnnually = 252.0/dur
windowedData = data[::dur]
rets = (windowedData - windowedData.shift(1)) / windowedData.shift(1)
#rets = np.log(windowedData/windowedData.shift(1))

#Calculate stock mean-variance
meanDailyReturn = rets.mean()
covariance = rets.cov()

#Create a new figure
plt.figure(figsize=(8,4))

#Calculate portfolios
numPortfolios = 1
results = np.zeros((3,numPortfolios))

for i in range(numPortfolios):
    #Draw numAssets random numbers and normalize them to be the portfolio weights
    weights = np.random.random(numAssets)
    weights /= np.sum(weights)
    
    pret, pvar = calcPortfolioPerf(weights, meanDailyReturn, covariance)
    
    results[0,i] = pret*numPeriodsAnnually
    results[1,i] = pvar*np.sqrt(numPeriodsAnnually)
    results[2,i] = (results[0,i] - riskFreeRate)/results[1,i]
    
#Plot results of MC on portfolio weights
plt.scatter(results[1,:], results[0,:], c=results[2,:], marker='o')

#Find efficient frontier
targetReturns = np.linspace(0.09, 0.25, 50)/(252./dur)
efficientPortfolios = findEfficientFrontier(weights, meanDailyReturn, covariance, targetReturns)
plt.plot([p['fun']*np.sqrt(numPeriodsAnnually) for p in efficientPortfolios], targetReturns*numPeriodsAnnually, marker='x')

#Find portfolio with maximum Sharpe ratio
maxSharpe = findMaxSharpeRatioPortfolio(weights, meanDailyReturn, covariance, riskFreeRate)
rp, sdp = calcPortfolioPerf(maxSharpe['x'], meanDailyReturn, covariance)
plt.plot(sdp*np.sqrt(numPeriodsAnnually), rp*numPeriodsAnnually, 'r*', markersize=15.0)

#Find portfolio with minimum variance
minVar = findMinVariancePortfolio(weights, meanDailyReturn, covariance)
rp, sdp = calcPortfolioPerf(minVar['x'], meanDailyReturn, covariance)
plt.plot(sdp*np.sqrt(numPeriodsAnnually), rp*numPeriodsAnnually, 'y*', markersize=15.0)
    
plt.grid(True)
plt.xlabel('Expected Volatility')
plt.ylabel('Expected Return')
plt.colorbar(label='Sharpe Ratio')
plt.show()




