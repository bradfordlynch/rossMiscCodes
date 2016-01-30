import numpy as np
import scipy.special as sp
import numba

maxArg = 700

@numba.jit
def gammaP(a, x):
    if (a <= 0) or (x < 0):
        raise ValueError
    elif x < (a + 1):
        return sp.gammainc(a, x)
    else:
        return 1 - sp.gammainc(a, x)
        
@numba.jit
def gammaQ(a, x):
    if (x <= 0) or (a <= 0):
        raise ValueError
    elif x < a + 1:
        return 1 - sp.gammainc(a, x)
    else:
        return sp.gammainc(a, x)
    
@numba.jit
def gZero(r, theta):
    global maxArg
    if r < 0:
        return 1.
    elif r == 0:
        if theta > maxArg:
            return 1.
        else:
            return 1. - np.exp(-theta)
    else:
        return gammaP(r + 1, theta)
       
@numba.jit 
def BigG(r, theta):
    global maxArg
    if r < 0:
        return 0.
    elif r == 0:
        if theta > maxArg:
            return 0
        else:
            return np.exp(-theta)
    else:
        return gammaQ(r, theta)
        
@numba.jit
def littleG(r, theta):
    global maxArg
    
    if r < 0:
        return 0
    else:
        arg = r * np.log(theta) - theta - sp.gammaln(r + 1)
        
        if arg < -maxArg:
            return 0
        if arg >= -maxArg:
            return np.exp(arg)
    
@numba.jit
def gee1(r, theta):
    if r <= 0:
        return theta
    else:
        return -(r - theta) * gZero(r, theta) + theta * littleG(r, theta)
        
@numba.jit
def gee2(r, theta):
    if r <= 0:
        return theta * theta / 2
    else:
        return (((r-theta)**2+r)*gZero(r,theta)-theta*(r-theta)*littleG(r,theta))/2
    
@numba.jit
def GPoisson(r, theta):
    return BigG(r, theta)

@numba.jit
def SPoisson(Q, r, theta):
    theta = float(theta)
    if r < 0:
        abar = 0.
        for i in range(int(r + 1), int(r + Q + 1)):
            abar += gZero(i - 1, theta)
        abar /= Q
    else:
        abar = (gee1(r, theta) - gee1(r + Q, theta)) / Q
        
    return 1 - abar
    
@numba.jit
def BPoisson(Q, r, theta):
    if r < 0:
        bbar = 0
        for i in range(int(r + 1), int(r + Q + 1)):
            bbar += gee1(i, theta)
        bbar /= Q
    else:
        bbar = (gee2(r, theta) - gee2(r + Q, theta)) / Q
        
    return bbar
    
@numba.jit
def IPoisson(Q, r, theta, B):
    return float(Q + 1) / 2 + r - theta + B


    
