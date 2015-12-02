################################################################################

#Simple Supply Chain Model Based on Stanford GSB HP Case

#Bradford Lynch, 2015, Ann Arbor, MI

################################################################################

import numpy as np
import scipy.stats as st
from matplotlib import pyplot as plt

weeklyDemand = 23108.6/4
weeklyStdDev = np.sqrt(6244**2/4)
leadTime = 6
stockoutProb = 0.02
duration = 52
numTrials = 10**2

def replenishSimulation(meanWeeklyDemand, stdDevWeeklyDemand, leadTime, stockoutProb, durInWeeks, numTrials):
    #Results storage
    detailedPipelineResults = np.zeros((numTrials, durInWeeks))
    detailedSafteyStockResults = np.zeros((numTrials, durInWeeks))
    simAvgPipelineVolume = 0.0
    
    #Initialize pipeline and safety stock
    pipeline = [ meanWeeklyDemand for i in range(leadTime) ]
    safetyStock = st.norm.ppf(1.0 - stockoutProb)*np.sqrt(leadTime)*stdDevWeeklyDemand
    
    stockouts = 0
    
    #Run trials
    for trial in range(numTrials):
        trialAvgPipelineVol = 0.0
        for week in range(durInWeeks):
            currentDemand = np.random.normal(meanWeeklyDemand, stdDevWeeklyDemand)
            safetyStock -= currentDemand
            safetyStock += pipeline.pop()
            
            if safetyStock <= 0:
                stockouts += 1
            
            detailedSafteyStockResults[trial, week] = safetyStock
            pipeline.insert(0, currentDemand)
            
            pipelineVolume = np.sum(pipeline)
            detailedPipelineResults[trial, week] = pipelineVolume
            trialAvgPipelineVol += pipelineVolume
        
        trialAvgPipelineVol /= durInWeeks
        simAvgPipelineVolume += trialAvgPipelineVol
        
    simAvgPipelineVolume /= numTrials
    stockoutProbResult = float(stockouts)/(numTrials*durInWeeks)
    
    print "Average pipeline volume is %f units" % simAvgPipelineVolume
    print "Stockout probability is %f" % stockoutProbResult
    
    #Plot average pipeline volume for each trial
    plt.figure()
    for trial in range(numTrials):
        plt.plot(detailedPipelineResults[trial,:])
    plt.xlim(0,durInWeeks-1)
    plt.title("Volume in Pipeline")
    plt.xlabel("Week Number")
    plt.ylabel("Number of Units")
    
    #Plot average safety stock volume
    plt.figure()
    for trial in range(numTrials):
        plt.plot(detailedSafteyStockResults[trial,:])
    plt.xlim(0,durInWeeks-1)
    plt.title("Volume in Safety Stock")
    plt.xlabel("Week Number")
    plt.ylabel("Number of Units")
    
    #Plot a single case
    caseNumber = np.random.choice(numTrials, 1)[0]
    plt.figure()
    plt.plot(detailedPipelineResults[caseNumber, :], label="Pipeline")
    plt.plot(detailedSafteyStockResults[caseNumber, :], label="Safety Stock")
    plt.title("Volume in Inventory for Trial %d" % caseNumber)
    plt.xlabel("Week Number")
    plt.ylabel("Number of Units")
    
    plt.show()
    
replenishSimulation(weeklyDemand, weeklyStdDev, leadTime, stockoutProb, duration, numTrials)