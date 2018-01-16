#! /usr/bin/env python3
###############################################################################
#
#	Title   : pf_tests.py
#	Author  : Matt Muszynski
#	Date    : 01/13/18
#	Synopsis: Vehicle portion of the explorer object model
# 
###############################################################################
import sys
sys.path.insert(0, '../util')
sys.path.insert(0, '../classes')
import accounts
import simScenario
import pdb
from datetime import date
import matplotlib.pyplot as plt
from numpy.random import normal
from numpy import cumsum

###############################################################################
#
#	Create Scenario
#
###############################################################################

scen = simScenario.simScenario()
scen.startDate = date(2017, 7, 1)
scen.initialCash = 10000

###############################################################################
#
#	Create Jobs
#
###############################################################################

job1 = accounts.job()
job1.payDOM = 20
job1.withholding = normal(5000)
job1.initialSalary = 123456.

job2 = accounts.job()
job2.payDOM = 10
job2.withholding = normal(5000)
job2.initialSalary = 654321.

###############################################################################
#
#	Create Investments
#
###############################################################################

investment1 = accounts.investment()
investment2 = accounts.investment()
investment3 = accounts.investment()

investment1.initialPrincipal = normal(10000.,3000)
investment2.initialPrincipal = normal(10000.,3000)
investment3.initialPrincipal = normal(10000.,3000)

investment1.interestRate = normal(9.,3)
investment2.interestRate = normal(9.,3)
investment3.interestRate = normal(9.,3)

###############################################################################
#
#	Create Expenses
#
###############################################################################

exp1 = accounts.expense()
exp1.mean = 10
exp1.std = 3
exp2 = accounts.expense()
exp2.mean = 100
exp2.std = 10

###############################################################################
#
#	Create Loans
#
###############################################################################

loan1 = accounts.loan()
loan2 = accounts.loan()
loan3 = accounts.loan()

loan1.name = 'Loan 1'
loan2.name = 'Loan 2'
loan3.name = 'Loan 3'	

loan1.initialPrincipal = normal(10000,2000)
loan2.initialPrincipal = normal(10000,2000)
loan3.initialPrincipal = normal(10000,2000)

loan1.interestRate = normal(4,1)
loan2.interestRate = normal(4,1)
loan3.interestRate = normal(4,1)

loan1.minimumPayment = loan1.initialPrincipal/100
loan2.minimumPayment = loan2.initialPrincipal/100
loan3.minimumPayment = loan3.initialPrincipal/100

###############################################################################
#
#	Conservation tests. Each object has a quantity that must be conserved.
#	These are codified in the checkConserved() method of each class.
#
###############################################################################

def test_investmentConservedQuantity():
	#this test is weak. we need to define some investment contributions
	#for it to be finished
	scen.reset()
	scen.addJobs([job1, job2])
	scen.addInvestments([investment1, investment2, investment3])
	scen.propagate()
	for investment in scen.investmentList:
		assert( investment.checkConserved() )

def test_loanConservedQuantity():
	scen.reset()
	scen.addJobs([job1, job2])
	scen.addLoans([loan1, loan2, loan3])
	scen.propagate()
	for loan in scen.loanList:
		assert( loan.checkConserved() )

def test_jobConservedQuantity():
	scen.reset()
	scen.addJobs([job1, job2])
	scen.propagate()
	for job in scen.jobList:
		assert( job.checkConserved() )

def test_cashConserved():
	scen.reset()
	scen.addJobs([job1, job2])
	scen.addLoans([loan1, loan2, loan3])
	scen.addInvestments([investment1, investment2, investment3])
	scen.addExpenses([exp1, exp2])
	scen.propagate()
	for investment in scen.investmentList:
		assert( investment.checkConserved() )
	for loan in scen.loanList:
		assert( loan.checkConserved() )
	assert( scen.checkConserved() )


