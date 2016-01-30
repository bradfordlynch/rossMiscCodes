import numpy as np
import pandas as pd
import scipy.special as sp
from inventoryManagement import *
import matplotlib.pyplot as plt

def existingATReorderPolicy(mu):
    if mu <= 0:
        return -1
    elif mu > 0 and mu <= 5:
        return np.floor(5.0/12*mu)
    elif mu > 5 and mu < 50:
        return np.floor(5.0/12*mu)
    else:
        return np.floor(mu/3.0)
        
def existingATMILPolicy(mu):
    if mu <= 0:
        return 0
    elif mu > 0 and mu <= 5:
        return np.ceil(mu)
    elif mu > 5 and mu < 50:
        return np.ceil(2.0/3*mu)
    else:
        return np.ceil(mu/2.0)
        
def proposedATReorderPolicy(inputs):
    if inputs[0] <= 0:
        return -1
    else:
        return np.floor( 1.4*inputs[0]*(inputs[1]+10)/365.0 )
        
def proposedATMILPolicy(mu):
    if mu <= 0:
        return 0
    elif mu > 0 and mu <= 5:
        return np.ceil(mu)
    elif mu > 5 and mu < 50:
        return np.ceil(2.0/3*mu)
    else:
        return np.ceil(mu/2.0)
    
def calculatePerformance(atData, reorderPolicy, reorderVariable, milPolicy, milVariable):
    atData['Daily Demand'] = atData['Total Usage']/365.0
    atData['theta'] = atData['Daily Demand'] * atData['Lead Time (days)']
    atData['r'] = [ reorderPolicy(mu) for mu in atData[reorderVariable] ]
    atData['mil'] = [ milPolicy(mu) for mu in atData[milVariable] ]
    atData['Q'] = atData['mil'] - atData['r']
    atData['Order Frequency'] = atData['Total Usage']/atData['Q']
    atData['Order Interval'] = 365.0/atData['Order Frequency']
    atData['Service Level'] = [GPoisson(r, theta) for r, theta in zip(atData['r'], atData['theta'])]
    atData['Fill Rate'] = [SPoisson(Q, r, theta) for Q, r, theta in zip(atData['Q'], atData['r'], atData['theta'])]
    atData['Backorder Level'] = [ BPoisson(Q, r, theta) for Q, r, theta in zip(atData['Q'], atData['r'], atData['theta']) ]
    atData['Inventory Level'] = [ IPoisson(Q, r, theta, b) for Q, r, theta, b in zip(atData['Q'], atData['r'], atData['theta'], atData['Backorder Level']) ]
    atData['Implied A'] = atData['Q']**2*atData['Unit Cost']/(2*atData['Total Usage'])
    
#Load A&T data
atRawData = pd.read_csv('dcData.csv', ',')

#Analyze current performance
atCurrent = atRawData.copy(deep=True)
calculatePerformance(atCurrent, existingATReorderPolicy, 'Total Usage', existingATMILPolicy, 'Total Usage')