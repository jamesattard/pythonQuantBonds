#!/usr/bin/python

import datetime
import calendar

START_YEAR = 2016
END_YEAR = 2027

class Bond(object):
    def __init__(self, name, nominal, startDate, endDate, couponPercent, couponPeriod):
        self.name = name
        self.nominal = nominal
        self.startDate = startDate
        self.endDate = endDate
        self.couponPercent = couponPercent
        self.couponPeriod = couponPeriod

def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)
    return next_month - datetime.timedelta(days=next_month.day)

def createBond(name, nominal, startDate, endDate, couponPercent, couponPeriod):
    bond = Bond(name, nominal, datetime.datetime.strptime(startDate, "%d/%m/%y"), datetime.datetime.strptime(endDate, "%d/%m/%y"), couponPercent, couponPeriod)
    return bond

def computeBondLevelData(bond):
    bondLevelData = []
    row = 0
    interestPayment = 0
    principalPayment = 0

    for year in range(START_YEAR, END_YEAR):
        for month in range(1, 13):
            cashFlowDate = last_day_of_month(datetime.datetime(year, month, 1))
            if cashFlowDate < bond.startDate or cashFlowDate > bond.endDate:
                break
            else:
                row += 1
                bondName = bond.name

                if bond.couponPeriod == "Monthly":
                    interestPayment = bond.couponPercent * bond.nominal / 12

                elif bond.couponPeriod == "Quarterly":
                    if month in [3,6,9,12]:
                        interestPayment = bond.couponPercent * bond.nominal / 4
                    else:
                        interestPayment = 0

                elif bond.couponPeriod == "Semi-Annual":
                    if month in [6,12]:
                        interestPayment = bond.couponPercent * bond.nominal / 2
                    else:
                        interestPayment = 0

                elif bond.couponPeriod == "Annual":
                    if month == 12:
                        interestPayment = bond.couponPercent * bond.nominal / 1
                    else:
                        interestPayment = 0

                if cashFlowDate == bond.endDate:
                    principalPayment = bond.nominal
                else:
                    principalPayment = 0

                total = interestPayment + principalPayment
                bondLevelData.append({'row': row, 'bondName': bondName, 'cashFlowDate': cashFlowDate.date(), 'interestPayment': format(interestPayment, '.2f'), 'principalPayment': principalPayment, 'total': total})

    return bondLevelData # Return an array of dictionaries each containing a cashflow entry per month

def computePortfolioLevelData(bondLevelData):
    portfolioLevelData = []
    buckets=[\
    [0, datetime.datetime.strptime("31/01/2017", "%d/%m/%Y").date()],\
    [0, datetime.datetime.strptime("31/03/2017", "%d/%m/%Y").date()],\
    [0, datetime.datetime.strptime("31/12/2017", "%d/%m/%Y").date()],\
    [0, datetime.datetime.strptime("31/12/2019", "%d/%m/%Y").date()],\
    [0, datetime.datetime.strptime("31/12/2021", "%d/%m/%Y").date()],\
    [0, datetime.datetime.strptime("31/12/2023", "%d/%m/%Y").date()],\
    [0, datetime.datetime.strptime("31/12/2025", "%d/%m/%Y").date()],\
    [0, datetime.datetime.strptime("31/12/2025", "%d/%m/%Y").date()]\
    ]

    for bondEntry in bondLevelData:
        if bondEntry['cashFlowDate'] <= buckets[0][1]:
            buckets[0][0] += bondEntry['total']
        elif bondEntry['cashFlowDate'] > buckets[0][1] and bondEntry['cashFlowDate'] <= buckets[1][1]:
            buckets[1][0] += bondEntry['total']
        elif bondEntry['cashFlowDate'] > buckets[1][1] and bondEntry['cashFlowDate'] <= buckets[2][1]:
            buckets[2][0] += bondEntry['total']
        elif bondEntry['cashFlowDate'] > buckets[2][1] and bondEntry['cashFlowDate'] <= buckets[3][1]:
            buckets[3][0] += bondEntry['total']
        elif bondEntry['cashFlowDate'] > buckets[3][1] and bondEntry['cashFlowDate'] <= buckets[4][1]:
            buckets[4][0] += bondEntry['total']
        elif bondEntry['cashFlowDate'] > buckets[4][1] and bondEntry['cashFlowDate'] <= buckets[5][1]:
            buckets[5][0] += bondEntry['total']
        elif bondEntry['cashFlowDate'] > buckets[5][1] and bondEntry['cashFlowDate'] <= buckets[6][1]:
            buckets[6][0] += bondEntry['total']
        elif bondEntry['cashFlowDate'] > buckets[6][1]:
            buckets[7][0] += bondEntry['total']

    for bucket in buckets:
        portfolioLevelData.append(bucket[0])

    return portfolioLevelData

def main():
    bond1 = createBond("FXD_BOND_1", 10000000, "31/12/16", "31/12/17", 0.01, "Monthly")
    bond2 = createBond("FXD_BOND_2", 20000000, "31/03/16", "31/03/20", 0.02, "Quarterly")
    bond3 = createBond("FXD_BOND_3", 30000000, "30/06/16", "30/06/20", 0.03, "Semi-Annual")
    bond4 = createBond("FXD_BOND_4", 40000000, "30/09/16", "30/09/26", 0.04, "Annual")

    for bond in [bond1, bond2, bond3, bond4]:
        print ""
        print "Bond Level Data computation for " + bond.name + ":"
        print "-------------------------------------------"
        print "Row , " + "Bond Name , " + "Cash Flow Date , " + "Interest Payment , " + "Principal Payment"
        bondLevelData = computeBondLevelData(bond)
        for bondEntry in bondLevelData:
            print bondEntry['row'], ",", bondEntry['bondName'], ",", bondEntry['cashFlowDate'], ",", bondEntry['interestPayment'], ",", bondEntry['principalPayment']

        print ""
        print "Portfolio Level Data computation for " + bond.name + ":"
        print "------------------------------------------------"
        print "Bond Name , " +  "<= 1m , " + ">1m <=3m , " + ">3m <=1y , " + ">1y <= 2y , " + ">2y <=3y ," + ">3y <=4y, " + ">4y <= 5y, " + "Remaining"
        portfolioLevelData = computePortfolioLevelData(bondLevelData)
        print bondEntry['bondName'], ",", portfolioLevelData[0], "," , portfolioLevelData[1], "," ,portfolioLevelData[2], "," ,portfolioLevelData[3], "," ,portfolioLevelData[4], "," ,portfolioLevelData[5], "," ,portfolioLevelData[6], "," ,portfolioLevelData[7]

if __name__ == "__main__":
    main()
