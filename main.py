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

#add investment names
MFS.name = "MFS"
Putnam.name = "Putnam"
JennyTIAA.name = "TIAA - Jenny"
MattTIAA.name = "TIAA - Matt"

#add investment prinicipals
MFS.initialPrincipal = 64045.26
Putnam.initialPrincipal = 98738.90
JennyTIAA.initialPrincipal = 5914.13
MattTIAA.initialPrincipal = 11675.65

#Investment account interest is not constant.
#needs smarter model. Model as constant FTM
MFS.interestRate = 9.0
Putnam.interestRate = 9.0
JennyTIAA.interestRate = 9.0
MattTIAA.interestRate = 9.0

# MFS.contributionLevel = 500
# Putnam.contributionLevel = 500
# JennyTIAA.contributionLevel = 500
# MattTIAA.contributionLevel = 500

# MFS.contributionDOM = 5
# Putnam.contributionDOM = 5
# JennyTIAA.contributionDOM = 5
# MattTIAA.contributionDOM = 5


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

#add Matt's loan names
MattSallieMaeSmartOption.name = 'Sallie Matt Smart Option - Matt'
Matt1_04DirectLoan.name = '1-04 Direct Loan - Subsidized - Matt'
Matt1_05DirectLoan.name = '1-04 Direct Loan - Subsidized - Matt'
Matt1_06DirectLoan.name = '1-04 Direct Loan - Subsidized - Matt'
Matt1_07DirectLoan.name = '1-04 Direct Loan - Subsidized - Matt'

#add loan prinicipals
MattSallieMaeSmartOption.initialPrincipal = 43718.24
Matt1_04DirectLoan.initialPrincipal = 3500
Matt1_05DirectLoan.initialPrincipal = 6971.37
Matt1_06DirectLoan.initialPrincipal = 5500.00
Matt1_07DirectLoan.initialPrincipal = 3842.11

#add loan interest rates
MattSallieMaeSmartOption.interestRate = 3.5 #needs adjustment for Libor
Matt1_04DirectLoan.interestRate = 3.86
Matt1_05DirectLoan.interestRate = 3.86
Matt1_06DirectLoan.interestRate = 4.29
Matt1_07DirectLoan.interestRate = 4.29

MattSallieMaeSmartOption.minimumPayment = 362.46
Matt1_04DirectLoan.minimumPayment = 35.2
Matt1_05DirectLoan.minimumPayment = 69.56
Matt1_06DirectLoan.minimumPayment = 50.45
Matt1_07DirectLoan.minimumPayment = 39.06

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

#initialize Jobs
Jenny = accounts.job()
Jenny.salary = 100360
Jenny.payDOM = 20
Jenny.name = "Jenny"
Jenny.withholding = 1600
Jenny.addRetirementAccounts([JennyTIAA])
#initialize Jobs
Matt = accounts.job()
Matt.salary = 85000
Matt.payDOM = 20
Matt.name = "Matt"
Matt.withholding = 1600


###############################################################################
#
#	Add Expenses
#
###############################################################################

rent = accounts.expense()
rent.name = 'Rent'
rent.mean = 2500
rent.std = 0
rent.spendDOM = 1

other = accounts.expense()
other.name = 'other'
other.mean = 2000/30
other.std = 500/30
other.spendDOM = -1 #daily expenses get spendDOM = -1

###############################################################################
#
#	Set up simulation scenario
#
###############################################################################

#initialize sim scenario
scen = simScenario.simScenario()
scen.startDate = date(2018, 1, 1)
scen.currentCash = 10000
scen.addLoan([
	MattSallieMaeSmartOption,
	Matt1_04DirectLoan,
	Matt1_05DirectLoan,
	Matt1_06DirectLoan,
	Matt1_07DirectLoan
	])
scen.addInvestment([
	MFS,
	Putnam,
	JennyTIAA,
	MattTIAA
	])
scen.addJobs([
	Jenny,
	Matt
	])
scen.addExpenses([
	rent,
	other
	])
scen.initialCash = 1e5
scen.endTime = 365*10
scen.propagate()

totalLoanPrincipalHistory = \
	np.zeros(len(scen.timeHistory))
for loan in scen.loanList:
	pdb.set_trace()
	totalLoanPrincipalHistory += loan.principalHistory
	plt.plot(scen.timeHistory,loan.principalHistory)
plt.plot(scen.timeHistory,totalLoanPrincipalHistory)

totalInvestmentPrincipalHistory = \
	np.zeros(len(scen.timeHistory))
for investment in scen.investmentList:
	totalInvestmentPrincipalHistory += investment.principalHistory
	plt.plot(scen.timeHistory,investment.principalHistory)
plt.figure()
for loan in scen.loanList:
	plt.plot(np.cumsum(loan.accruedInterestHistory))
plt.figure()
for loan in scen.loanList:
	plt.plot(np.cumsum(loan.paymentHistory))

plt.show()
pdb.set_trace()