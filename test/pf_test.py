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

###############################################################################
#
#	Create Scenario
#
###############################################################################

scen = simScenario.simScenario()
scen.startDate = date(2018, 1, 1)
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
#	Run tests
#
###############################################################################


def test_null():
	'''!
	The null test checks to make sure that nothing changes throughout
	the scenario when no values are set. This scenario has no jobs,
	no investments, and no loans.
	'''
	scen.reset()
	scen.propagate()
	assert ( scen.finalCash == 10000 )


def test_add_jobs():
	'''!
	test_add_jobs() tests that job salaries are being applied correctly
	with no expenses, loans, or investments. job1 is added and the 
	scenario is run for a year. At the end of the year, we check that
	the cash is equal to a year's salary plus the initial scenario cash.
	Then job2 is added and the same test is performed
	'''
	scen.reset()
	scen.addJobs([job1])
	scen.propagate()
	assert ( 
			abs(
				scen.finalCash - \
				scen.initialCash + \
				sum(scen.taxesPaidHistory) - job1.initialSalary 
			) < 1e-6
			)


	scen.reset()
	scen.addJobs([job1,job2])
	scen.propagate()
	totalSalary = 0

	for job in scen.jobList:
		totalSalary += job.initialSalary

	assert ( 
			scen.finalCash - \
			scen.initialCash + \
			sum(scen.taxesPaidHistory) == totalSalary )


def test_addInvestments():
	'''!
	test_addInvestments() tests that investments are accruing correctly
	and that contributions are correctly being correctly applied to loans
	and removed from cash.
	Three investements are added to the scenario with randomized initial
	principal and interest rate.
	The first assertion checks that the final value of the investment is 
	initial investment plus all accrued interest and any contributions.
	The second assertion checks that the final cash in the scenario is
	equal to the full salary draw and initial cash minus contributions
	and cash leftover at the end of the scenario.
	'''

	scen.reset()
	scen.addJobs([job1,job2])
	scen.addInvestments([investment1, investment2, investment3])

	totalSalary = 0
	for job in scen.jobList:
		totalSalary += job.initialSalary

	scen.propagate()
	totalPrincipal = 0
	totalContribution = 0
	totalInterest = 0
	totalInitialPrincipal = 0

	for investment in scen.investmentList:
		totalPrincipal += investment.finalPrincipal
		totalInterest += sum(investment.interestHistory)
		totalContribution += sum(investment.contributionHistory)
		totalInitialPrincipal += investment.initialPrincipal

	assert (
		abs(
		totalPrincipal - \
		totalInterest - \
		totalContribution - \
		totalInitialPrincipal) < 1e-6
		)
	assert(
		abs(
			totalSalary + \
			scen.initialCash - \
			scen.currentCash - \
			totalContribution - \
			sum(scen.taxesPaidHistory)
			) < 1e-6
		)

def test_addExpenses():
	'''!
	test_addExpenses() tests that expenses are correctly being removed from
	cash supplies. There are the same two jobs as above with two expenses.
	There are no loans or investments in this scenario. The assertion makes
	sure that the total incoming cash (from salary) minus the final cash of 
	the scenario minus the total spend on the expenses plus the initial cash 
	of the scenario is zero
	'''
	scen.reset()
	scen.addExpenses([exp1,exp2])
	scen.addJobs([job1,job2])
	scen.propagate()

	totalSalary = 0
	for job in scen.jobList:
		totalSalary += job.initialSalary
	totalSpend = 0
	for expense in scen.expenseList:
		totalSpend += sum(expense.spendHistory)

	assert( 
		abs(
		totalSalary - \
		scen.currentCash - \
		sum(scen.taxesPaidHistory) - \
		totalSpend + \
		scen.initialCash
		) < 1e-6
		)


def test_addLoans():
	'''!
	test_addLoans() tests that loans are correctly applied. The same jobs
	as above are added to the scenario. The default behavior of the system
	is to pay minimum amounts to all loans on their payment DOM. The total
	paid is tracked. The asserts in this scenario check that the initial
	amount of the loan plus all accrued interest minus all payments during
	the scenario period.
	'''
	scen.reset()
	scen.addJobs([job1,job2])
	scen.addLoans([loan1,loan2,loan3])

	totalSalary = 0
	for job in scen.jobList:
		totalSalary += job.initialSalary

	scen.propagate()

	totalInterest = 0
	totalPayment = 0
	totalInitialPrincipal = 0
	totalFinalPrincipal = 0
	for loan in scen.loanList:
		totalInterest += sum(loan.accruedInterestHistory)
		totalPayment += sum(loan.paymentHistory)
		totalInitialPrincipal += loan.initialPrincipal
		totalFinalPrincipal += loan.currentPrincipal
	assert(
		abs(
			totalInterest + \
			totalInitialPrincipal - \
			totalPayment - \
			totalFinalPrincipal
			) < 1e-6
		)

	assert( 
		abs(
			totalSalary + \
			scen.initialCash - \
			scen.cashHistory[-1] - \
			sum(scen.taxesPaidHistory) - \
			totalPayment
			) < 1e-6
		)

# def test_withholding():
# 	scen.reset()
# 	scen.addJobs([job1,job2])
# 	scen.propagate()
# 	pdb.set_trace()








