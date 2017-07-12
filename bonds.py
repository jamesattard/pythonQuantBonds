#!/usr/bin/python

import datetime
import calendar

class IterRegistry(type):
    def __iter__(cls):
        return iter(cls._registry)

class Bond(object):
    __metaclass__ = IterRegistry
    _registry = []
    purchaseDate = datetime.datetime.strptime("31/12/16", "%d/%m/%y")

    def __init__(self, name, nominal, startDate, endDate, couponPercent, couponPeriod):
        self._registry.append(self)
        self.name = name
        self.nominal = nominal
        self.startDate = startDate
        self.endDate = endDate
        self.couponPercent = couponPercent
        self.couponPeriod = couponPeriod

def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)
    return next_month - datetime.timedelta(days=next_month.day)

bond1 = Bond('FXD_BOND_1',\
10000000,\
datetime.datetime.strptime("31/12/16", "%d/%m/%y"),\
datetime.datetime.strptime("31/12/17", "%d/%m/%y"),\
0.01,\
"Monthly")

bond2 = Bond('FXD_BOND_2',\
20000000,\
datetime.datetime.strptime("31/03/16", "%d/%m/%y"),\
datetime.datetime.strptime("31/03/20", "%d/%m/%y"),\
0.02,\
"Quarterly")

bond3 = Bond('FXD_BOND_3',\
30000000,\
datetime.datetime.strptime("30/06/16", "%d/%m/%y"),\
datetime.datetime.strptime("30/06/20", "%d/%m/%y"),\
0.03,\
"Semi-Annual")

bond4 = Bond('FXD_BOND_4',\
40000000,\
datetime.datetime.strptime("30/09/16", "%d/%m/%y"),\
datetime.datetime.strptime("30/09/26", "%d/%m/%y"),\
0.04,\
"Annual")

# for bond in Bond:
#     print bond.name, bond.startDate.date()

# Bond Level Data
# Represented as a list of objects
# Each Row is an object.

bondLevelData = []
row = 0
bond = bond4
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


for bondEntry in bondLevelData:
    print bondEntry['row'], bondEntry['cashFlowDate'], bondEntry['interestPayment'], bondEntry['principalPayment'], bondEntry['total']

# print bondLevelData
