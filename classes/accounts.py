#! /usr/bin/env python3
###############################################################################
#
#	Title   : accounts.py
#	Author  : Matt Muszynski
#	Date    : 01/08/18
#	Synopsis: Vehicle portion of the explorer object model
# 
###############################################################################
from numpy import hstack, exp, array
from datetime import date
from numpy.random import normal
import sys
import pdb
sys.path.insert(0, 'util')

class investment:
	def __init__(self):
		self.name = -1
		self.interestRate = -1
		self.contributionDOM = 1
		self.taxed = -1
		self.initialPrincipal = 0

		#use reset methods to initialize values and history arrays
		self.resetCurrent(resetPrincipal=1)
		self.resetHistory()

	def resetCurrent(self, **kwargs):
		#clear current values
		try:
			if kwargs['resetPrincipal'] == 1: 
				self.currentPrincipal = self.initialPrincipal
		except:
			pass
		self.currentInterest = 0
		self.currentContribution = 0
	def resetHistory(self):
		#clear history arrays
		self.principalHistory = []
		self.interestHistory = []
		self.contributionHistory = []
	def resetChildren(self):
		pass

	def recordValues(self):
		self.principalHistory = hstack([
			self.principalHistory, self.currentPrincipal])
		self.interestHistory = hstack([
			self.interestHistory, self.currentInterest])
		self.contributionHistory = hstack([
			self.contributionHistory, self.currentContribution])

	def recordFinalValues(self):
		self.finalPrincipal = self.principalHistory[-1]
		self.finalInterest = self.interestHistory[-1]
		self.finalContribution = self.contributionHistory[-1]

	def accrue(self):
		# A = P*e^(rt)
		# A = P*(1+r/n)^(nt))
		P = self.currentPrincipal
		r = self.interestRate/100.
		t = self.simScenario.timeStep/365.

		newPrincipal = P*exp(r*t)
		self.currentInterest = newPrincipal - self.currentPrincipal 
		self.currentPrincipal = newPrincipal 

	def contribute(self,amount):
		self.currentPrincipal += amount
		self.currentContribution += amount
		self.simScenario.currentCash -= amount

class loan:
	def __init__(self):
		self.name = -1
		self.interestRate = -1
		#Initial values
		self.initialPrincipal = 0
		#use reset methods to initialize values and history arrays
		self.resetCurrent(resetPrincipal=1)
		self.resetHistory()

	def resetCurrent(self, **kwargs):
		#clear current values
		try:
			if kwargs['resetPrincipal'] == 1: 
				self.currentPrincipal = self.initialPrincipal
		except:
			pass

		self.currentAccruedInterest = 0
		self.currentPayment = 0
		self.currentPrincipal = 0

	def resetHistory(self):
		#clear history arrays
		self.accruedInterestHistory = []
		self.paymentHistory = []
		self.principalHistory = []

	def resetChildren(self):
		pass

	def recordFinalValues(self):
		self.finalAccruedInterest = self.accruedInterestHistory[-1]
		self.finalPayment = self.paymentHistory[-1]
		self.finalPrincipal = self.principalHistory[-1]

	def accrue(self):
		# A = P*e^(rt)
		# A = P*(1+r/n)^(nt))
		self.currentAccruedInterest = 0
		self.currentPayment = 0
		P = self.currentPrincipal
		r = self.interestRate/100.
		t = self.simScenario.timeStep/365.
		newPrincipal = P*exp(r*t)
		self.currentAccruedInterest = \
			newPrincipal - P
		self.currentPrincipal = newPrincipal

	def makePayment(self,**kwargs):
		try:
			amt = kwargs['amt']
		except:
			amt = self.minimumPayment

		paymentDOM = 1

		if self.simScenario.currentDate.day == 1:
			if self.currentPrincipal > amt:
				self.currentPrincipal -= amt
				self.simScenario.currentCash -= amt
				self.currentPayment += amt
			else:
				self.simScenario.currentCash -= self.currentPrincipal
				self.currentPayment += self.currentPrincipal
				self.currentPrincipal = 0

class job:
	def __init__(self):
		self.name = -1
		self.payDOM = -1
		self.monthlyPay = -1
		self.withholding = 0
		self.initialSalary = 0
		#use reset methods to initialize values and history arrays
		self.resetCurrent(resetSalary=1)
		self.resetHistory()
		self.resetChildren()

	def resetCurrent(self,**kwargs):
		#clear current values
		try:
			if kwargs['resetSalary'] == 1:
				self.currentSalary = self.initialSalary
		except:
			pass

		self.currentIRAContributions = 0
		self.current401kContributions = 0
		self.currentMonthlyPay = 0
		self.currentWithheldTax = 0
		self.currentYearToDatePay = 0

	def resetHistory(self):
		#clear history arrays
		self.salaryHistory = []
		self.IRAContributionHistory = []
		self._401kContributionHistory = []
		self.monthlyPayHistory = []
		self.withheldTaxHistory = []
		self.yearToDatePayHistory = []

	def resetChildren(self):
		self.retirementAccounts = []

	def recordValues(self):
		self.salaryHistory = hstack([
			self.salaryHistory, self.currentSalary])
		self.IRAContributionHistory = hstack([
			self.IRAContributionHistory, self.currentIRAContributions])
		self._401kContributionHistory = hstack([
			self._401kContributionHistory, self.current401kContributions])
		self.monthlyPayHistory = hstack([
			self.monthlyPayHistory, self.currentMonthlyPay])
		self.withheldTaxHistory = hstack([
			self.withheldTaxHistory, self.currentWithheldTax])
		self.yearToDatePayHistory = hstack([
			self.yearToDatePayHistory, self.currentYearToDatePay])

	def recordFinalValues(self):
		self.finalSalary = self.salaryHistory[-1]
		self.finalIRAContributions = self.IRAContributionHistory[-1]
		self.final401kContributions = self._401kContributionHistory[-1]
		self.finalMonthlyPay = self.monthlyPayHistory[-1]
		self.finalWithheldTax = self.withheldTaxHistory[-1]
		self.finalYearToDatePay = self.yearToDatePayHistory[-1]



	def payday(self):
		if self.simScenario.currentDate.day == self.payDOM:
			self.currentMonthlyPay = self.currentSalary/12
			self.currentYearToDatePay += self.currentMonthlyPay
			#pay taxes
			self.withhold()

			#pay to 401k account
			self.contribute()

			self.simScenario.currentCash += self.currentMonthlyPay

	def contribute(self):
		for investment in self.retirementAccounts:
			#employee contributions deduct from monthlyPay
			self.monthlyPay -= investment.contributionLevel
			investment.currentPrincipal += investment.contributionLevel
			self.current401kContributions += investment.contributionLevel

			#employer contributions do not
			investment.currentPrincipal += \
				self.salary*investment.employerContributionPercent/100/12

	def withhold(self):
		self.monthlyPay -= self.withholding
		self.currentWithheldTax += self.withholding


	def addRetirementAccounts(self, accounts):
		for account in accounts:
			self.retirementAccounts.append(account)


class expense:
	def __init__(self):
		self.name = -1
		self.spendDOM = -1

		#use reset methods to initialize values and history arrays
		self.resetCurrent()
		self.resetHistory()

	def spend(self):
		if self.spendDOM == -1:
			self.currentSpend = normal(self.mean,self.std)
			self.simScenario.currentCash -= self.currentSpend		
		elif self.simScenario.currentDate.day == self.spendDOM :
			self.currentSpend = normal(self.mean,self.std)
			self.simScenario.currentCash -= self.currentSpend
		else:
			self.currentSpend = 0

	def resetCurrent(self):
		self.currentSpend = 0

	def resetHistory(self):
		self.spendHistory = []

	def recordValues(self):
		self.spendHistory = hstack([
			self.spendHistory, self.currentSpend])

	def recordFinalValues(self):
		self.finalSpend = self.spendHistory[-1]

	def resetChildren(self):
		pass

class home:
	def __init__(self):
		self.name = -1
		self.mortgageCurrentPrincipal = -1
		self.mortgagePayment = -1
		self.downPayment = -1
		#Initial and current values
		self.currentValue = -1

		#lists of historic values
		self.mortgagePrincipalHistory = []
		self.valueHistory = []

		#lists of objects belonging to home object
		


