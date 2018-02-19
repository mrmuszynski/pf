#! /usr/bin/env python3
###############################################################################
#
#	Title   : main.py
#	Author  : Matt Muszynski
#	Date    : 12/23/17
#	Synopsis: Wrapper script for explorer
#
###############################################################################

import sys
sys.path.insert(0, 'classes')
sys.path.insert(0, 'util')

import accounts, simScenario
import numpy as np
import matplotlib.pyplot as plt
import pdb
from numpy.random import normal
from datetime import date


###############################################################################
#
#	Add Investment Accounts
#
###############################################################################

#initialize investments
MFS = accounts.investment()
Putnam = accounts.investment()
JennyTIAA = accounts.investment()
MattTIAA = accounts.investment()
MFSIRA = accounts.investment()
PutnamIRA = accounts.investment()

#add investment names
MFS.name = "MFS"
Putnam.name = "Putnam"
MFSIRA.name = "MFS IRA"
PutnamIRA.name = "Putnam IRA"
JennyTIAA.name = "TIAA - Jenny"
MattTIAA.name = "TIAA - Matt"

#add investment prinicipals
MFS.initialPrincipal = 50368.27
Putnam.initialPrincipal = 81222.72
MFSIRA.initialPrincipal = 16763.95
PutnamIRA.initialPrincipal = 13216.02
JennyTIAA.initialPrincipal = 5914.13
MattTIAA.initialPrincipal = 11675.65

#Investment account interest is not constant.
#needs smarter model. Model as constant FTM
MFS.interestRate = 9.0
Putnam.interestRate = 9.0
MFSIRA.interestRate = 9.0
PutnamIRA.interestRate = 9.0
JennyTIAA.interestRate = 9.0
MattTIAA.interestRate = 9.0


###############################################################################
#
#	Add Loan Accounts
#
###############################################################################

#initialize loans
MattSallieMaeSmartOption = accounts.loan()
Matt1_04DirectLoan = accounts.loan()
Matt1_05DirectLoan = accounts.loan()
Matt1_06DirectLoan = accounts.loan()
Matt1_07DirectLoan = accounts.loan()
JennySallieMaeSmartOption = accounts.loan()
Jenny1_04DirectLoan = accounts.loan()
Jenny1_05DirectLoan = accounts.loan()
Jenny1_06DirectLoan = accounts.loan()
Jenny1_07DirectLoan = accounts.loan()

#add Matt's loan names
MattSallieMaeSmartOption.name = 'Sallie Mae Smart Option - Matt'
Matt1_04DirectLoan.name = '1-04 Direct - Subsidized - Matt'
Matt1_05DirectLoan.name = '1-05 Direct - Unsubsidized - Matt'
Matt1_06DirectLoan.name = '1-06 Direct - Subsidized - Matt'
Matt1_07DirectLoan.name = '1-07 Direct - Unsubsidized - Matt'
JennySallieMaeSmartOption.name = 'Sallie Mae Smart Option - Jenny'
Jenny1_04DirectLoan.name = '1-04 Direct - Subsidized - Jenny'
Jenny1_05DirectLoan.name = '1-05 Direct - Unsubsidized - Jenny'
Jenny1_06DirectLoan.name = '1-06 Direct - Subsidized - Jenny'
Jenny1_07DirectLoan.name = '1-07 Direct - Unsubsidized - Jenny'

#add loan prinicipals
MattSallieMaeSmartOption.initialPrincipal = 36883.89
Matt1_04DirectLoan.initialPrincipal = 3500.00
Matt1_05DirectLoan.initialPrincipal = 6971.37
Matt1_06DirectLoan.initialPrincipal = 5500.00
Matt1_07DirectLoan.initialPrincipal = 3842.11
JennySallieMaeSmartOption.initialPrincipal = 43718.24
Jenny1_04DirectLoan.initialPrincipal = 3500.00
Jenny1_05DirectLoan.initialPrincipal = 6982.4
Jenny1_06DirectLoan.initialPrincipal = 4000.00
Jenny1_07DirectLoan.initialPrincipal = 8042.30

#add loan interest rates
MattSallieMaeSmartOption.interestRate = 3.5 #needs adjustment for Libor
Matt1_04DirectLoan.interestRate = 3.86
Matt1_05DirectLoan.interestRate = 3.86
Matt1_06DirectLoan.interestRate = 4.29
Matt1_07DirectLoan.interestRate = 4.29
JennySallieMaeSmartOption.interestRate = 8.875
Jenny1_04DirectLoan.interestRate = 3.86
Jenny1_05DirectLoan.interestRate = 3.86
Jenny1_06DirectLoan.interestRate = 4.29
Jenny1_07DirectLoan.interestRate = 4.29

MattSallieMaeSmartOption.minimumPayment = 364.73
Matt1_04DirectLoan.minimumPayment = 35.20
Matt1_05DirectLoan.minimumPayment = 70.12
Matt1_06DirectLoan.minimumPayment = 56.45
Matt1_07DirectLoan.minimumPayment = 39.43
JennySallieMaeSmartOption.minimumPayment = 550.85
Jenny1_04DirectLoan.minimumPayment = 32.20
Jenny1_05DirectLoan.minimumPayment = 70.23
Jenny1_06DirectLoan.minimumPayment = 41.05
Jenny1_07DirectLoan.minimumPayment = 82.54

#Set flag for whether contributions should be
#applied pre or post tax
MFS.taxed = 1
Putnam.taxed = 1
JennyTIAA.taxed = 0
MattTIAA.taxed = 0

JennyTIAA.employerContributionPercent = 5

###############################################################################
#
#	Add Jobs
#
###############################################################################

Jenny = accounts.job()
Jenny.initialSalary = 100360
Jenny.payDOM = 20
Jenny.name = "Jenny"
Jenny.withholding = 1800
Jenny.employer401kContributionPercent = 5
Jenny.employer401kContributionStart = 182
Jenny.employee401kContribution = 375
Jenny.addRetirementAccounts([JennyTIAA])
Jenny.insurancePremium = 0

Matt = accounts.job()
Matt.initialSalary = 85000
Matt.payDOM = 20
Matt.name = "Matt"
Matt.withholding = 1600
Matt.employer401kContributionPercent = 5
Matt.employer401kContributionStart = 182
Matt.employee401kContribution = 375
Matt.addRetirementAccounts([MattTIAA])
Matt.insurancePremium = 0


###############################################################################
#
#	Add Expenses
#
###############################################################################

rent = accounts.expense()
other = accounts.expense()

rent.name = 'Rent'
other.name = 'other'

rent.mean = 3000
other.mean = 4000/30

rent.std = 0
other.std = 500/30

rent.spendDOM = 1
other.spendDOM = -1 #daily expenses get spendDOM = -1

###############################################################################
#
#	Set up simulation scenario
#
###############################################################################

#initialize sim scenario
scen = simScenario.simScenario()
scen.startDate = date(2018, 1, 1)
scen.initialMutualFundAPR = 19

scen.firstHomeDate = 365*2
scen.firstHomeDateSTD = 180
scen.firstHomeCost = 8e5
scen.firstHomeCostSTD = 2e5
scen.firstChildDate = 365*2
scen.firstChildSTD = 180
scen.monthlyChildCost = 2000
scen.childCostSTD = 1000

scen.addLoans([
	MattSallieMaeSmartOption,
	Matt1_04DirectLoan,
	Matt1_05DirectLoan,
	Matt1_06DirectLoan,
	Matt1_07DirectLoan,
	JennySallieMaeSmartOption,
	Jenny1_04DirectLoan,
	Jenny1_05DirectLoan,
	Jenny1_06DirectLoan,
	Jenny1_07DirectLoan
	])
scen.addMutualFunds([
	MFS,
	Putnam
	])
scen.addIRAs([
	MFSIRA,
	PutnamIRA
	])
scen.addJobs([
	Jenny,
	Matt
	])
scen.addExpenses([
	rent,
	other
	])
scen.initialCash = 1e4
scen.endTime = 365*35
scen.propagate()

scen.plotAll()
plt.figure()
plt.plot(scen.mutualFundAPRHistory)
plt.show()
# scen.plotLoanPrincipal()
# scen.plotLoanInterest()
# scen.plotInvestmentPrincipal()
# scen.plotInvestmentInterest()
# scen.plotLoanPayment()
# plt.show()
pdb.set_trace()