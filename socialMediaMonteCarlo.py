import random

def runTrial():
    numFB = 0
    numTweets = 0
    
    #Generate tweets and FB posts according to probabilities
    for i in range(2):
        if random.random() > 0.2:
            numTweets += 1
            
        if random.random() > 0.4:
            numFB += 1
        
    #Return True if there is at least 1 FB post AND at least 1 tweet
    if (numFB > 0) and (numTweets > 0):
        return True
    else:
        return False
            
def runSimulation(numTrials, printProb=True, storeResults=True):
    #Setup variables to store results from trials
    numSuccesses = 0
    trialNum = []
    probVsTrialNum = []
    
    #Run N trials
    for i in range(numTrials):
        #Increment successes if trial returns True
        if runTrial():
            numSuccesses += 1
        
        #Store history of results every 1000th trial
        if i%1000 == 0 and storeResults:
            trialNum.append(i+1)
            probVsTrialNum.append(float(numSuccesses)/(i+1))
            
    #Calculate probability based on trials
    probFromSim = float(numSuccesses)/numTrials
    
    if printProb:
        print "Probability is %f" % probFromSim
    
    return probFromSim, trialNum, probVsTrialNum
    
#Run some number of simulations and average the results
#averageProb = 0
#numSims = 10
#trialsPerSim = 10**7
#
#for i in range(numSims):
#    pSim, tN, pVstN = runSimulation(trialsPerSim, False, False)
#    averageProb += pSim
#    
#averageProb /= numSims
#print "Probability is %f" % averageProb
