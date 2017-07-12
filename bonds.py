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

                elif bond.couponPeriod == "Semi-Annual":
                    if month in [6,12]:
                        interestPayment = bond.couponPercent * bond.nominal / 2

                elif bond.couponPeriod == "Annual":
                    if month == 12:
                        interestPayment = bond.couponPercent * bond.nominal / 1

                if cashFlowDate == bond.endDate:
                    principalPayment = bond.nominal
                else:
                    principalPayment = 0

                total = interestPayment + principalPayment
                bondLevelData.append({'row': row, 'bondName': bondName, 'cashFlowDate': cashFlowDate.date(), 'interestPayment': format(interestPayment, '.2f'), 'principalPayment': principalPayment, 'total': total})

    return bondLevelData # Return an array of dictionaries each containing a cashflow entry per month

def computePortfolioLevelData(bondLevelData):
    bucketOne = [0, datetime.datetime.strptime("31/01/2017", "%d/%m/%Y").date()]
    bucketTwo = [0, datetime.datetime.strptime("31/03/2017", "%d/%m/%Y").date()]
    bucketThree = [0, datetime.datetime.strptime("31/12/2017", "%d/%m/%Y").date()]
    bucketFour = [0, datetime.datetime.strptime("31/12/2019", "%d/%m/%Y").date()]
    bucketFive = [0, datetime.datetime.strptime("31/12/2021", "%d/%m/%Y").date()]
    bucketSix = [0, datetime.datetime.strptime("31/12/2023", "%d/%m/%Y").date()]
    bucketSeven = [0, datetime.datetime.strptime("31/12/2025", "%d/%m/%Y").date()]
    bucketEight = [0, datetime.datetime.strptime("31/12/2025", "%d/%m/%Y").date()]

    for bondEntry in bondLevelData:
        if bondEntry['cashFlowDate'] <= bucketOne[1]:
            bucketOne[0] += bondEntry['total']
        elif bondEntry['cashFlowDate'] > bucketOne[1] and bondEntry['cashFlowDate'] <= bucketTwo[1]:
            bucketTwo[0] += bondEntry['total']
        elif bondEntry['cashFlowDate'] > bucketTwo[1] and bondEntry['cashFlowDate'] <= bucketThree[1]:
            bucketThree[0] += bondEntry['total']
        elif bondEntry['cashFlowDate'] > bucketThree[1] and bondEntry['cashFlowDate'] <= bucketFour[1]:
            bucketFour[0] += bondEntry['total']
        elif bondEntry['cashFlowDate'] > bucketFour[1] and bondEntry['cashFlowDate'] <= bucketFive[1]:
            bucketFive[0] += bondEntry['total']
        elif bondEntry['cashFlowDate'] > bucketFive[1] and bondEntry['cashFlowDate'] <= bucketSix[1]:
            bucketSix[0] += bondEntry['total']
        elif bondEntry['cashFlowDate'] > bucketSix[1] and bondEntry['cashFlowDate'] <= bucketSeven[1]:
            bucketSeven[0] += bondEntry['total']
        elif bondEntry['cashFlowDate'] > bucketSeven[1]:
            bucketEight[0] += bondEntry['total']

    print format(bucketOne[0], '.2f'), format(bucketTwo[0], '.2f'), format(bucketThree[0], '.2f'), format(bucketEight[0], '.2f')

    bondEntry = ""
    portfolioLevelData = bondEntry
    return portfolioLevelData

def main():
    bond1 = createBond("FXD_BOND_1", 10000000, "31/12/16", "31/12/17", 0.01, "Monthly")
    bond2 = createBond("FXD_BOND_2", 20000000, "31/03/16", "31/03/20", 0.03, "Quarterly")
    bond3 = createBond("FXD_BOND_3", 30000000, "30/06/16", "30/06/20", 0.03, "Semi-Annual")
    bond4 = createBond("FXD_BOND_4", 40000000, "30/09/16", "30/09/26", 0.04, "Annual")

    #for bond in [bond1, bond2, bond3, bond4]:
    for bond in [bond1]:
        print ""
        print "Bond Level Data computation for " + bond.name + ":"
        print "-------------------------------------------"
        print "Row , " + "Bond Name , " + "Cash Flow Date , " + "Interest Payment , " + "Principal Payment"
        bondLevelData = computeBondLevelData(bond)
        for bondEntry in bondLevelData:
            print bondEntry['row'], ",", bondEntry['bondName'], ",", bondEntry['cashFlowDate'], ",", bondEntry['interestPayment'], ",", bondEntry['principalPayment']

        portfolioLevelData = computePortfolioLevelData(bondLevelData)
        print ""
        print portfolioLevelData

if __name__ == "__main__":
    main()
