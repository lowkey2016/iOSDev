# -*- coding: utf-8 -*-

import math

class MathUtil(object):
	@classmethod
	def log(self, x, y):
		if y < 0:
			return None
		elif y == 0:
			return 0
		elif y == 1:
			return x - 1
		else:
			return math.log(x, y) - 1

	@classmethod
	def nroot(self, x, y):
		if y == 0:
			return 0

		y = 1. / y
		return math.pow(x, y)

	@classmethod
	def comprateper(self, val, year):
		if year == 0:
			return 0

		year = 1. / year
		rate = math.pow(val, year)
		rate = (rate - 1) * 100
		return rate
