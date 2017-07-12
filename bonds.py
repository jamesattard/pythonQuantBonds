#!/usr/bin/python

import datetime
import calendar

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

    for year in range(2016, 2027): # Replace with constants
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

    return bondLevelData

bond1 = createBond("FXD_BOND_1", 10000000, "31/12/16", "31/12/17", 0.01, "Monthly")
bond2 = createBond("FXD_BOND_2", 20000000, "31/03/16", "31/03/20", 0.03, "Quarterly")
bond3 = createBond("FXD_BOND_3", 30000000, "30/06/16", "30/06/20", 0.03, "Semi-Annual")
bond4 = createBond("FXD_BOND_4", 40000000, "30/09/16", "30/09/26", 0.04, "Annual")

print "Bond Level Data computation..."
print "Row , " + "Bond Name , " + "Cash Flow Date , " + "Interest Payment , " + "Principal Payment"
for bond in [bond1, bond2, bond3, bond4]:
    bondLevelData = computeBondLevelData(bond)
    for bondEntry in bondLevelData:
        print bondEntry['row'], ",", bondEntry['bondName'], ",", bondEntry['cashFlowDate'], ",", bondEntry['interestPayment'], ",", bondEntry['principalPayment']
