import numpy as np

def computeFS(fs, production, r_tax, r_debt, w_pay, t0_i, n_collec_per):
    '''
    Calculates the balance sheet and income statement, in place, based
    on the balance sheet at time "Zero" indicated by t0_i, sales
    projections, production weights, tax rate, debt cost, etc, as
    shown below.

    fs -->  A (16,n) array consisting of past, present, and expected
            financial performance. Forecasted net sales and n_collec_per
            worth of previous sales numbers must be pre-populated in fs.
            In addition, COGS, OpEx, Net PPE, and LT Debt, CP must be
            included within the forecast window. Lastly, the complete
            balance sheet from one period prior to t0 must be included.

            Below is the row index dictionary, indicies 0-5 correspond
            to the income statement and 6-16 are the balance sheet:

            00: Net Sales
            01: Cost of Goods Sold
            02: Operating Expenses
            03: Earnings Before Interest and Taxes
            04: Taxes
            05: Net Profit
            06: Cash
            07: Accounts Receivable
            08: Inventory
            09: Net Plant, Property, and Equipment
            10: Accounts Payable
            11: Notes Payable
            12: Accured Taxes
            13: Long-term Debt, Current Portion
            14: Long-term Debt
            15: Shareholder's Equity

    production -->  The production schedule for the firm in terms
                    of the amount of COGS made per month

    r_tax -->  Corporate tax rate of the firm

    r_debt --> Cost of debt for the firm

    w_pay -->  Monthly balance of accounts payable as a fraction of
               net sales

    t0_i -->   Index within fs at which the financial analysis starts

    n_collec_per --> Average number of periods that it takes to collect
                     sales since they were added to accounts receivable

    '''
    for i in range(t0_i, fs.shape[1]):
        #Calculate IS values
        #Calculate EBIT
        fs[3,i] = fs[0,i] - fs[1,i] - fs[2,i]

        #Calculate taxes
        fs[4,i] = r_tax*(fs[3,i] - fs[11,i-1]*r_debt)

        #Calculate net profit
        fs[5,i] = fs[3,i] - fs[11,i-1]*r_debt - fs[4,i]

        #Calculate BS values
        #Calculate new value of accounts receivables
        fs[7,i] = fs[7,i-1] - fs[0,i-n_collec_per] + fs[0,i]

        #Calculate new inventory level
        fs[8,i] = fs[8,i-1] + production[i-t0_i] - fs[1,i]

        #Calculate PPE
        fs[9,i] = fs[9,i-1]

        #Calculate new accounts payable
        fs[10,i] = w_pay*fs[0,i]

        #Calculate new accrued taxes
        fs[12,i] = fs[12,i-1] + fs[4,i]

        #Pay taxes if it is March
        if (i-t0_i+1) % 12 == 3:
            #Pay accured taxes as of Dec year end
            fs[12,i] -= fs[12,i-3]

        #Pay esitmate of current years taxes if April, June, Sept, or Dec
        if (i-t0_i+1) % 12 in [4,9]:
            fs[12,i] -= 31
        elif (i-t0_i+1) % 12 in [6,12]:
            fs[12,i] -= 32

        #Calculate current portion of long-term debt
        fs[13,i] = fs[13,i-1]

        #Calculate long-term debt, $25 payments in June and Dec
        fs[14,i] = fs[14,i-1]
        if (i-t0_i+1 == 6) or (i-t0_i+1 == 12):
            fs[14,i] -= 25

        #Calculate share holder's equity
        fs[15,i] = fs[15,i-1] + fs[5,i]

        #Calculate cash
        fs[6,i] = fs[6,i-1] - \
                  (fs[7,i] - fs[7,i-1]) -  \
                  (fs[8,i] - fs[8,i-1]) -  \
                  (fs[9,i] - fs[9,i-1]) +  \
                  (fs[10,i] - fs[10,i-1]) + \
                  (fs[12,i] - fs[12,i-1]) + \
                  (fs[15,i] - fs[15,i-1])

        #Calculate notes payable payment
        if fs[6,i] > 175.0:
            fs[11,i] = max( 0, fs[11,i-1] - (fs[6,i] - 175) )
            fs[6,i] += fs[11,i] - fs[11,i-1]
        else:
            fs[6,i] = 175
            fs[11,i] = (fs[6,i] + fs[7,i] + fs[8,i] + fs[9,1]) - \
            (fs[10,i] + fs[12,i] + fs[13,i] + fs[14,i] + fs[15,i])
            
def plotTrialData(trialID, trials, t0):
    plt.figure(figsize=(8,5))
    months = range(1,13)
    plt.plot(months, trials[6,t0:,trialID], label='Cash')
    plt.plot(months, trials[7,t0:,trialID], label='AR')
    plt.plot(months, trials[8,t0:,trialID], label='Inventory')
    plt.plot(months, trials[11,t0:,trialID], label='Notes Payable')
    plt.title('Financials of Firm During Trial #%d' % trialID)
    plt.xlabel('Month')
    plt.ylabel("Value (000's of Dollars)")
    plt.legend(loc=2)
    plt.show()
