#! /usr/bin/env python3
###############################################################################
#
#	Title   : vehicles.py
#	Author  : Matt Muszynski
#	Date    : 12/23/17
#	Synopsis: Vehicle portion of the explorer object model
# 
###############################################################################
from numpy import hstack, exp
from scipy.linalg import norm, inv
from scipy.integrate import ode
from datetime import date
import sys
sys.path.insert(0, 'util')

class investment:
	def __init__(self):
		self.name = -1
		self.interestRate = -1
		self.initialPrincipal = -1
		self.currentPrincipal = -1
		self.contributionDOM = -1
		self.taxed = -1
		self.principalHistory = []

	def accrue(self):
		# A = P*e^(rt)
		# A = P*(1+r/n)^(nt))
		P = self.currentPrincipal
		r = self.interestRate/100
		t = self.simScenario.timeStep/365

		self.currentPrincipal = P*exp(r*t)
	
	def contribute(self):
		if self.taxed == 0: return
		if self.simScenario.currentTime % 30 == self.contributionDOM:
			self.currentPrincipal += self.contributionLevel

class loan:
	def __init__(self):
		self.name = -1
		self.interestRate = -1
		self.initialPrincipal = -1
		self.principalHistory = []
		self.paymentAmount = -1

	def accrue(self):
		# A = P*e^(rt)
		# A = P*(1+r/n)^(nt))
		P = self.currentPrincipal
		r = self.interestRate/100
		t = self.simScenario.timeStep/365

		self.currentPrincipal = P*exp(r*t)

	def makePayment(self):
		paymentDOM = 1
		paymentAMT =  self.paymentAmount
		if self.simScenario.currentTime % 30 == 1:
			if self.currentPrincipal > self.paymentAmount:
				self.currentPrincipal -= self.paymentAmount
			else:
				self.currentPrincipal = 0

class job:
	def __init__(self):
		self.name = -1
		self.salary = -1
		self.payDOM = -1
		self.montlyPay = -1
		self.untaxedInvestments = []

	def payday(self):
		if self.simScenario.currentTime % 30 == self.payDOM:
			self.montlyPay = self.salary/12
			#make contribtions to pretax investments
			self.contribute()

			#pay for insurance pretax
			self.spendPretax()

			#pay taxes
			self.withhold()

			self.simScenario.currentCash += self.montlyPay

	def contribute(self):
		for investment in self.untaxedInvestments:
			if investment.taxed == 1: return
			investment.currentPrincipal += investment.contributionLevel
		return 

	def spendPretax(self):
		return 

	def withhold(self):
		taxRate = 0.22
		self.montlyPay = self.montlyPay*(1 - taxRate)

	def addInsurance(self):
		return

	def addUntaxedInvestments(self, investments):
		for investment in investments:
			self.untaxedInvestments.append(investment)
		return


class expense:
	def __init__(self):
		self.name = -1
		self.salary = -1
		self.payDOM = -1


class home:
	def __init__(self):
		self.name = -1
		self.mortgageCurrentPrincipal = -1
		self.mortgagePrincipalHistory = []
		self.mortgagePayment = -1
		self.downPayment = -1
		self.currentValue = -1
		self.valueHistory = []
		

