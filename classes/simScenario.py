#! /usr/bin/env python3
###############################################################################
#
#	Title   : simScenario.py
#	Author  : Matt Muszynski
#	Date    : 12/23/17
#	Synopsis: Vehicle portion of the explorer object model
# 
###############################################################################
from numpy import empty, hstack, array, cumsum, zeros, repeat
from numpy.random import normal
from datetime import timedelta, datetime
import matplotlib.pyplot as plt
from sys import exit
import pdb

class simScenario:
	def __init__(self):
		self.startDate = -1
		self.startTime = 0
		self.endTime = self.startTime + 365
		self.timeStep = 1
		self.initialCash = 0
		self.initialSavings = 0
		self.initialMutualFundAPR = 0

		#lists of objects belonging to scenario
		self.loanList = []
		self.mutualFundList = []
		self.IRAList = []
		self.jobList = []
		self.TIAAList = []
		self.expenseList = []
		self.mutualFundAPRHistory = []

		#use reset method to initialize current values
		#and history arrays
		self.resetCurrent()
		self.resetHistory()

	def reset(self):
		self.resetCurrent()
		self.resetHistory()
		self.resetChildren()

	def resetCurrent(self,**kwargs):
		#clear items belonging to scenario itself
		#clear current values
		try:
			if kwargs['resetTime'] == 1: self.currentTime = 0
		except:
			pass
		try:
			if kwargs['resetCash'] == 1: 
				self.currentCash = self.initialCash
		except:
			pass
		try:
			if kwargs['resetSavings'] == 1: 
				self.currentSavings = self.initialSavings
		except:
			pass
		try:
			if kwargs['resetMF'] == 1: 
				self.currentMutualFundAPR = self.initialMutualFundAPR
		except:
			pass

		self.currentTaxesPaid = 0
		self.currentTaxBill = 0
		self.currentFICABill = 0
		self.currentSpendingMoney = 0
		

	def resetHistory(self):
		#clear history arrays
		self.timeHistory = []
		self.cashHistory = []
		self.savingsHistory = []
		self.taxesPaidHistory = []
		self.taxBillHistory = []
		self.FICABillHistory = []
		self.spendingMoneyHistory = []

	def resetChildren(self):
		#clear investments
		for investment in self.mutualFundList:
			investment.resetCurrent(resetPrincipal=1)
			investment.resetHistory()
			investment.resetChildren()
		self.mutualFundList = []

		for investment in self.IRAList:
			investment.resetCurrent(resetPrincipal=1)
			investment.resetHistory()
			investment.resetChildren()
		self.IRAList = []

		for investment in self.TIAAList:
			investment.resetCurrent(resetPrincipal=1)
			investment.resetHistory()
			investment.resetChildren()
		self.TIAAList = []

		#clear loans
		for loan in self.loanList:
			loan.resetCurrent(resetPrincipal=1)
			loan.resetHistory()
			loan.resetChildren()
		self.loanList = []

		#clear jobs
		for job in self.jobList:
			job.resetCurrent(resetSalary=1)
			job.resetHistory()
			job.resetChildren()
		self.jobList = []

		#clear expenses
		for expense in self.expenseList:
			expense.resetCurrent()
			expense.resetHistory()
			expense.resetChildren()
		self.expenseList = []

	def recordValues(self):
		self.timeHistory = hstack([
			self.timeHistory, self.currentTime])
		self.cashHistory = hstack([
			self.cashHistory, self.currentCash])
		self.savingsHistory = hstack([
			self.savingsHistory, self.currentSavings])
		self.taxesPaidHistory = hstack([
			self.taxesPaidHistory, self.currentTaxesPaid])
		self.taxBillHistory = hstack([
			self.taxBillHistory, self.currentTaxBill])
		self.FICABillHistory = hstack([
			self.FICABillHistory, self.currentFICABill])
		self.spendingMoneyHistory = hstack([
			self.spendingMoneyHistory, self.currentSpendingMoney])
		self.mutualFundAPRHistory = hstack([
			self.mutualFundAPRHistory, self.currentMutualFundAPR])

	def recordFinalValues(self):
		self.finalTime = self.timeHistory[-1]
		self.finalCash = self.cashHistory[-1]
		self.finalSavings = self.savingsHistory[-1]
		self.finalTaxesPaid = self.taxesPaidHistory[-1]
		self.finalTaxBill = self.taxBillHistory[-1]
		self.finalFICABill = self.FICABillHistory[-1]

	def addLoans(self,loanList):
		for loan in loanList:
			loan.simScenario = self
			self.loanList.append(loan)

	def addMutualFunds(self,investmentList):
		for investment in investmentList:
			investment.simScenario = self
			self.mutualFundList.append(investment)

	def addIRAs(self,investmentList):
		for investment in investmentList:
			investment.simScenario = self
			self.IRAList.append(investment)

	def addTIAAs(self,investmentList):
		for investment in investmentList:
			investment.simScenario = self
			self.TIAAList.append(investment)

	def addExpenses(self,expenseList):
		for expense in expenseList:
			expense.simScenario = self
			self.expenseList.append(expense)


	def addJobs(self,jobList):
		for job in jobList:
			job.simScenario = self
			self.jobList.append(job)

	def checkConserved(self):
		totalSpend = 0
		totalPayment = 0
		totalPaycheck = 0
		totalContribution = 0
		totalWithdrawl = 0
		for expense in self.expenseList:
			totalSpend += cumsum(expense.spendHistory)
		for loan in self.loanList:
			totalPayment += cumsum(loan.paymentHistory)
		for job in self.jobList:
			totalPaycheck += cumsum(job.monthlyPayHistory)
		for investment in self.mutualFundList:
			totalContribution += cumsum(investment.contributionHistory)
			totalWithdrawl += cumsum(investment.withdrawlHistory)
		for investment in self.IRAList:
			totalContribution += cumsum(investment.contributionHistory)
			totalWithdrawl += cumsum(investment.withdrawlHistory)
		for investment in self.TIAAList:
			totalContribution += cumsum(investment.contributionHistory)
			totalWithdrawl += cumsum(investment.withdrawlHistory)

		conservedQuantity = \
			self.cashHistory + \
			self.savingsHistory + \
			totalSpend + \
			totalPayment - \
			totalWithdrawl - \
			totalPaycheck + \
			totalContribution + \
			cumsum(self.taxesPaidHistory)
		isConserved = sum(abs(conservedQuantity - self.initialCash))/\
			len(conservedQuantity) < 1e-6

		return isConserved

	# def checkTaxConserved(self):
	# 	conservedQuantity = 
	# 	payHistory
	# 	pdb.set_trace()
	# 	isConserved = True
	# 	return isConserved

	def payTaxes(self,taxType):
		taxableIncome = 0.
		withholding = 0.
		thisYear = (self.startDate + timedelta(self.currentTime)).year
		lastYear = thisYear - 1
		yearArray = array([(self.startDate + \
			timedelta(i)).year for i in self.timeHistory])
		ind = yearArray == lastYear

		for job in self.jobList:
			lastYearIRA = sum(job.IRAContributionHistory[ind])
			lastYear401k = sum(job._401kContributionHistory[ind])
			lastYearPay = sum(job.payHistory[ind])
			taxableIncome += lastYearPay
			taxableIncome -= max([lastYearIRA, 18500])
			taxableIncome -= max([lastYear401k, 5500])
			#also remove monthly pretax payments

		if taxType == 'California':
			standardDeduction = 8472
			dollarAmt = array([
				16030,38002,59978,83258,105224,
				537500,644998,1074996,1e12
			])

			percent = array([
				1, 2, 4, 6, 8, 9.3,
				10.3, 11.3, 12.3
				])
			self.currentFICABill += 0
			personalExemption = 222

		elif taxType == 'Federal':
			for job in self.jobList: 
				withholding += sum(job.withheldTaxHistory[ind])
				job.currentWithheldTax = 0.
				#also remove monthly pretax payments

			standardDeduction = 24000

			dollarAmt = array([
				19050, 77400, 165000, 315000,
				400000, 600000, 1e12
				])

			percent = array([
				10, 12, 22, 24, 32, 35, 37
				])
			personalExemption = 0

			socialSecurityBill = min([taxableIncome,118500])*0.062
			medicareBill = taxableIncome*0.0145

			self.currentFICABill += socialSecurityBill + medicareBill

		#this is ugly AF
		taxableIncome -= standardDeduction
		if taxableIncome < 0: taxableIncome = 0
		ind = dollarAmt < taxableIncome
		if sum(ind) > 0:
			lowerBrackets = \
			sum((dollarAmt[ind] -hstack([0,dollarAmt[ind][0:-1]]))*percent[ind]/100)
			highestAmount = dollarAmt[ind][-1]
			highestPercent = percent[sum(ind)]
			highestBracket = (taxableIncome - highestAmount)*highestPercent/100
		else:
			highestBracket = taxableIncome*percent[0]/100
			lowerBrackets = 0

		self.currentTaxBill = highestBracket + lowerBrackets

		self.currentTaxesPaid += (self.currentTaxBill + self.currentFICABill - withholding)
		self.currentCash -= (self.currentTaxBill + self.currentFICABill - withholding)

	def plotLoanPrincipal(self):
		f, ax = plt.subplots()
		totalLoanPrincipalHistory = \
			zeros(len(self.timeHistory))
		for loan in self.loanList:
			totalLoanPrincipalHistory += loan.principalHistory
			ax.plot(self.timeHistory,loan.principalHistory,label=loan.name)
		ax.plot(self.timeHistory,totalLoanPrincipalHistory,
			label='Total Loan Principal')
		ax.set_title('Loan Principals')
		ax.set_xlabel('Days Since Sim Start')
		ax.set_ylabel('Dollars')
		ax.legend(prop={'size': 8})
		return ax

	def plotLoanInterest(self):
		f, ax = plt.subplots()
		totalLoanInterest = \
			zeros(len(self.timeHistory))
		for loan in self.loanList:
			totalLoanInterest += loan.interestHistory
			ax.plot(self.timeHistory, cumsum(loan.interestHistory),
				label=loan.name)
		ax.plot(self.timeHistory, cumsum(totalLoanInterest), 
			label='Total Loan Interest')
		ax.set_title('Accrued Loan Interest')
		ax.set_xlabel('Days Since Sim Start')
		ax.set_ylabel('Dollars')
		ax.legend(prop={'size': 8})
		return ax

	def plotLoanPayment(self):
		f, ax = plt.subplots()
		totalLoanPayment = \
			zeros(len(self.timeHistory))
		for loan in self.loanList:
			totalLoanPayment += loan.paymentHistory
			ax.plot(self.timeHistory, cumsum(loan.paymentHistory),
				label=loan.name)
		ax.plot(self.timeHistory, cumsum(totalLoanPayment), 
			label='Total Loan Payment')
		ax.set_title('Accrued Loan Payment')
		ax.set_xlabel('Days Since Sim Start')
		ax.set_ylabel('Dollars')
		ax.legend(prop={'size': 8})
		return ax



	def plotInvestmentPrincipal(self):
		f, ax = plt.subplots()
		totalInvestmentPrincipalHistory = \
			zeros(len(self.timeHistory))
		for investment in self.mutualFundList:
			totalInvestmentPrincipalHistory += investment.principalHistory
			plt.plot(self.timeHistory,investment.principalHistory,
				label=investment.name)
		for investment in self.IRAList:
			totalInvestmentPrincipalHistory += investment.principalHistory
			plt.plot(self.timeHistory,investment.principalHistory,
				label=investment.name)
		for investment in self.TIAAList:
			totalInvestmentPrincipalHistory += investment.principalHistory
			plt.plot(self.timeHistory,investment.principalHistory,
				label=investment.name)

		plt.plot(self.timeHistory,totalInvestmentPrincipalHistory,
			label='Total Investment Principal')
		plt.title('Investment Principals')
		plt.xlabel('Days Since Sim Start')
		plt.ylabel('Dollars')
		ax.legend(prop={'size': 8})
		return ax

	def plotInvestmentInterest(self):
		f, ax = plt.subplots()
		totalInvestmentInterest = \
			zeros(len(self.timeHistory))
		for investment in self.mutualFundList:
			totalInvestmentInterest += investment.interestHistory
			ax.plot(self.timeHistory, cumsum(investment.interestHistory),
				label=investment.name)
		for investment in self.IRAList:
			totalInvestmentInterest += investment.interestHistory
			ax.plot(self.timeHistory, cumsum(investment.interestHistory),
				label=investment.name)
		for investment in self.TIAAList:
			totalInvestmentInterest += investment.interestHistory
			ax.plot(self.timeHistory, cumsum(investment.interestHistory),
				label=investment.name)
		ax.plot(self.timeHistory, cumsum(totalInvestmentInterest), 
			label='Total Loan Interest')
		ax.set_title('Accrued Investment Interest')
		ax.set_xlabel('Days Since Sim Start')
		ax.set_ylabel('Dollars')
		ax.legend(prop={'size': 8})
		return ax


	def plotInvestmentContribution(self):
		f, ax = plt.subplots()
		totalInvestmentContribution = \
			zeros(len(self.timeHistory))
		for investment in self.mutualFundList:
			totalInvestmentContribution += investment.contributionHistory
			ax.plot(self.timeHistory, cumsum(investment.contributionHistory),
				label=investment.name)
		for investment in self.IRAList:
			totalInvestmentContribution += investment.contributionHistory
			ax.plot(self.timeHistory, cumsum(investment.contributionHistory),
				label=investment.name)
		for investment in self.TIAAList:
			totalInvestmentContribution += investment.contributionHistory
			ax.plot(self.timeHistory, cumsum(investment.contributionHistory),
				label=investment.name)
		ax.plot(self.timeHistory, cumsum(totalInvestmentContribution), 
			label='Total Investment Contribution')
		ax.set_title('Accrued Investment Contributions')
		ax.set_xlabel('Days Since Sim Start')
		ax.set_ylabel('Dollars')
		ax.legend(prop={'size': 8})
		return ax

	def plotInvestmentWithdrawl(self):
		f, ax = plt.subplots()
		totalInvestmentWithdrawl = \
			zeros(len(self.timeHistory))
		for investment in self.mutualFundList:
			totalInvestmentWithdrawl += investment.withdrawlHistory
			ax.plot(self.timeHistory, cumsum(investment.withdrawlHistory),
				label=investment.name)
		for investment in self.IRAList:
			totalInvestmentWithdrawl += investment.withdrawlHistory
			ax.plot(self.timeHistory, cumsum(investment.withdrawlHistory),
				label=investment.name)
		for investment in self.TIAAList:
			totalInvestmentWithdrawl += investment.withdrawlHistory
			ax.plot(self.timeHistory, cumsum(investment.withdrawlHistory),
				label=investment.name)
		ax.plot(self.timeHistory, cumsum(totalInvestmentWithdrawl), 
			label='Total Investment Contribution')
		ax.set_title('Accrued Investment Contributions')
		ax.set_xlabel('Days Since Sim Start')
		ax.set_ylabel('Dollars')
		ax.legend(prop={'size': 8})
		return ax

	def plotPayHistory(self):
		f, ax = plt.subplots()
		totalPayHistory = \
			zeros(len(self.timeHistory))
		for job in self.jobList:
			totalPayHistory += job.payHistory
			ax.plot(self.timeHistory, cumsum(job.payHistory),
				label=job.name)
		ax.plot(self.timeHistory, cumsum(totalPayHistory), 
			label='Total Pay History')
		ax.set_title('Pay History')
		ax.set_xlabel('Days Since Sim Start')
		ax.set_ylabel('Dollars')
		ax.legend(prop={'size': 8})
		return ax

	def plotWitholdingHistory(self):
		f, ax = plt.subplots()
		totalWithheldTax = \
			zeros(len(self.timeHistory))
		for job in self.jobList:
			totalWithheldTax += job.withheldTaxHistory
			ax.plot(self.timeHistory, cumsum(job.withheldTaxHistory),
				label=job.name)
		ax.plot(self.timeHistory, cumsum(totalWithheldTax), 
			label='Total Pay History')
		ax.set_title('Tax Withholding History')
		ax.set_xlabel('Days Since Sim Start')
		ax.set_ylabel('Dollars')
		ax.legend(prop={'size': 8})
		return ax

	def plotInsurancePayments(self):
		f, ax = plt.subplots()
		totalInsurancePayments = \
			zeros(len(self.timeHistory))
		for job in self.jobList:
			totalInsurancePayments += job.insurancePaymentHistory
			ax.plot(self.timeHistory, cumsum(job.insurancePaymentHistory),
				label=job.name)
		ax.plot(self.timeHistory, cumsum(totalInsurancePayments), 
			label='Total Pay History')
		ax.set_title('Insurance Payment History')
		ax.set_xlabel('Days Since Sim Start')
		ax.set_ylabel('Dollars')
		ax.legend(prop={'size': 8})
		return ax

	def plotAll(self):
		self.plotLoanPrincipal()
		self.plotLoanInterest()
		self.plotLoanPayment()
		self.plotInvestmentPrincipal()
		self.plotInvestmentInterest()
		self.plotInvestmentContribution()
		self.plotInvestmentWithdrawl()
		self.plotPayHistory()
		self.plotWitholdingHistory()
		self.plotInsurancePayments()

	def springForce(self,x,k,sigma,mean,restPoint):
		u = normal(mean,sigma)
		return -k*(x - restPoint) + u

	def calculateMutualFundAPR(self):
		'''!
		calculateMutualFundAPR() is used to pre-calculate the mutual fund
		annual percentage rate. With model I came up with, I only wanted
		APR to be updated once a month, and rather than put an if statement
		in the main simulation loop.
		'''
		self.mutualFundAPR = array([self.initialMutualFundAPR])
		scenarioDuration = self.endTime-self.startTime
		for i in range(int(scenarioDuration/30)):
			currentAPR = self.mutualFundAPR[-1]
			self.mutualFundAPR = hstack([self.mutualFundAPR,
				currentAPR + \
				self.springForce(currentAPR,0.1,2.,0.,9.)])
		self.mutualFundAPR = \
			repeat(self.mutualFundAPR,30)[0:scenarioDuration+1]

	def propagate(self):
		#record initial states as state at t0
		start = datetime.now()
		self.currentTime = self.startTime
		self.timeHistory = []
		self.currentCash = self.initialCash
		self.cashHistory = []
		self.currentSavings = self.initialSavings
		self.savingsHistory = []
		self.currentMutualFundAPR = self.initialMutualFundAPR
		self.mutualFundAPRHistory = []
		###############################################################
		#
		# Initialize Values
		#
		# I think I can clean this up a bit with some reset functions
		#
		###############################################################

		for loan in self.loanList:
			loan.currentPrincipal = loan.initialPrincipal
			loan.principalHistory = loan.currentPrincipal
			loan.accruedInterestHistory = []
			loan.paymentHistory = []
			loan.principalHistory = []

		for investment in self.mutualFundList:
			investment.currentPrincipal = investment.initialPrincipal
			investment.principalHistory = investment.currentPrincipal
			investment.principalHistory = []
			investment.interestHistory = []
			investment.contributionHistory = []

		for investment in self.IRAList:
			investment.currentPrincipal = investment.initialPrincipal
			investment.principalHistory = investment.currentPrincipal
			investment.principalHistory = []
			investment.interestHistory = []
			investment.contributionHistory = []

		for investment in self.TIAAList:
			investment.currentPrincipal = investment.initialPrincipal
			investment.principalHistory = investment.currentPrincipal
			investment.principalHistory = []
			investment.interestHistory = []
			investment.contributionHistory = []

		for job in self.jobList:
			job.currentSalary = job.initialSalary
			job.monthlyPayHistory = []
			job.withheldTaxHistory = []
			job.salaryHistory = []

		print(datetime.now() - start)

		###############################################################
		#
		# Main Simulation Loop
		#
		###############################################################
		while self.currentTime <= self.endTime:
			print(datetime.now() - start)
			self.currentTime += self.timeStep
			self.currentDate = self.startDate + timedelta(
				self.currentTime)

			###########################################################
			#
			# Loans accrue interest continually. It is calculated
			# at each time step. loan.makePayment() is called at
			# each time step as well, but it will only do anything
			# if the DOM is equal to the day that loan is paid
			#
			###########################################################

			#makePayment with no keyword argument will pay minimum
			#further payment may be made below
			if self.currentDate.day == 1: 
				self.currentMutualFundAPR += \
					self.springForce(self.currentMutualFundAPR,0.1,2.,0.,9.)
				for loan in self.loanList:
					loan.makePayment()
			for loan in self.loanList:
				loan.accrue()

			###########################################################
			#
			# Investments accrue interest continually. It is calculated
			# at each time step. 
			#
			###########################################################

			for investment in self.mutualFundList:
				investment.accrue()
			for investment in self.IRAList:
				investment.accrue()
			for investment in self.TIAAList:
				investment.accrue()

			###########################################################
			#
			# Jobs pay once a month. The amount paid is equal to the
			# job's salary divided by 12 less any monthly withholding,
			# social security, and medicare payments
			#
			###########################################################

			for job in self.jobList:
				job.payday()

			###########################################################
			#
			#	Taxes are paid once a year on 4/15 and a 2% cost of
			#	living raise is applied each 1/1
			#
			###########################################################


			if self.currentTime%365 == 105:
				self.payTaxes('Federal')
				self.payTaxes('California')

			# if self.currentTime%365 == 1:
			# 	for job in self.jobList:
			# 		job.salary *= 1.02

			###########################################################
			#
			#	Pay expenses and once a month make payments to 
			#	loans/investments
			#
			###########################################################

			for expense in self.expenseList:
				expense.spend()

			# put $1000 into savings on 1st of each month.
			if self.currentDate.day == 1:
				spendingMoney = self.currentCash - 3000
				self.currentSpendingMoney = spendingMoney

				savingsTransfer = 1000
				spendingMoney -= savingsTransfer
				self.currentCash -= savingsTransfer
				self.currentSavings += savingsTransfer

				#sort loan list by interest rate
				self.loanList.sort(key=lambda x: x.interestRate, reverse=True)
				for loan in self.loanList:
					if loan.currentPrincipal > 0:
						spendingMoney -= 1000
						loan.makePayment(amt=1000)
						break

				for investment in self.IRAList:
					investment.contribute(230*0.9)
					spendingMoney-=230

				for investment in self.mutualFundList:
					investment.contribute(spendingMoney/2*0.9)

				spendingMoney = 0

				self.currentCash -= spendingMoney
				self.currentSavings += spendingMoney


			###########################################################
			#
			# 	Record Current values
			#
			#	I feel like I might want to move these into functions
			#	of some sort. Not really sure how. There are a lot
			#	of values I'd like to capture (like interest between
			#	loan payments)
			#
			###########################################################

			self.recordValues()
			self.resetCurrent(resetTime=0,resetCash=0)

			for loan in self.loanList:
				loan.recordValues()
				loan.resetCurrent()

			for investment in self.mutualFundList:
				investment.recordValues()
				investment.resetCurrent()
			for investment in self.IRAList:
				investment.recordValues()
				investment.resetCurrent()
			for investment in self.TIAAList:
				investment.recordValues()
				investment.resetCurrent()

			for job in self.jobList:
				job.recordValues()
				job.resetCurrent()

			for expense in self.expenseList:
				expense.recordValues()
				expense.resetCurrent()

		###############################################################
		#
		# 	Record Final values
		#
		###############################################################
		for loan in self.loanList:
			loan.recordFinalValues()

		for investment in self.mutualFundList:
			investment.recordFinalValues()
		for investment in self.IRAList:
			investment.recordFinalValues()
		for investment in self.TIAAList:
			investment.recordFinalValues()

		for job in self.jobList:
			job.recordFinalValues()

		for expense in self.expenseList:
			expense.recordFinalValues()

		self.recordFinalValues()
