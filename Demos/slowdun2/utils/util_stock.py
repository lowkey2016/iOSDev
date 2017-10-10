# -*- coding: utf-8 -*-

import math
from models.fjsj import FJSJ
import utils.util_cons as Cons

class StockUtil(object):
	@classmethod
	def getLastFJSJ(self, stock, year):
		k = year
		k1 = '%s' % (int(k) - 1)
		if k1 in stock.fjsjs:
			fj_lst = stock.fjsjs[k1]
		else:
			fj_lst = FJSJ()
		return fj_lst

	@classmethod
	def getCurFJSJ(self, stock, year):
		k = year
		if k in stock.fjsjs:
			fj_cur = stock.fjsjs[k]
		else:
			fj_cur = FJSJ()
		return fj_cur


	## 求单个数值的方法

	@classmethod
	def getDivideVal(self, num, den, use_percent_format=False):
		if den == 0:
			return 0
		else:
			val = float(num) / den
			if use_percent_format:
				return val * 100
			else:
				return val

	@classmethod
	def getGrowRate(self, val_cur, val_lst, use_percent_format=True):
		if val_lst == 0:
			return 0
		else:
			rate = float(val_cur) / val_lst
			if use_percent_format:
				return (rate - 1) * 100
			else:
				return rate - 1

	@classmethod
	def getGrowVal(self, val_cur, val_lst):
		return val_cur - val_lst

	@classmethod
	def getCompRate(self, val_cur, val_lst, years, use_percent_format=True):
		if val_lst == 0 or years == 0:
			return 0
		else:
			val = float(val_cur) / val_lst
			rate = math.pow(val, 1. / years) - 1
			if use_percent_format:
				return rate * 100
			else:
				return rate

	@classmethod
	def numValueForKeyPath(self, stock, keypath):
		keys = keypath.split('.')
		assert len(keys) == 2
		pre = keys[0]
		suf = keys[-1]
		if pre.startswith('zcfzbs'):
			year = pre[len('zcfzbs')+1:-1]
			if year not in stock.zcfzbs:
				return 0.0
			else:
				zb = stock.zcfzbs[year]
				return zb.__dict__[suf]
		elif pre.startswith('gslrbs'):
			year = pre[len('gslrbs')+1:-1]
			if year not in stock.gslrbs:
				return 0.0
			else:
				lb = stock.gslrbs[year]
				return lb.__dict__[suf]
		elif pre.startswith('xjllb'):
			year = pre[len('xjllbs')+1:-1]
			if year not in stock.xjllbs:
				return 0.0
			else:
				xb = stock.xjllbs[year]
				return xb.__dict__[suf]
		elif pre.startswith('fjsj'):
			year = pre[len('fjsjs')+1:-1]
			if year not in stock.fjsjs:
				return 0.0
			else:
				fj = stock.fjsjs[year]
				return fj.__dict__[suf]
		else:
			return 0.0

	@classmethod
	def strValueForKeyPath(self, stock, keypath):
		keys = keypath.split('.')
		assert len(keys) == 2
		pre = keys[0]
		suf = keys[-1]
		if pre.startswith('zcfzbs'):
			year = pre[len('zcfzbs')+1:-1]
			if year not in stock.zcfzbs:
				return ''
			else:
				zb = stock.zcfzbs[year]
				return zb.__dict__[suf]
		elif pre.startswith('gslrbs'):
			year = pre[len('gslrbs')+1:-1]
			if year not in stock.gslrbs:
				return ''
			else:
				lb = stock.gslrbs[year]
				return lb.__dict__[suf]
		elif pre.startswith('xjllb'):
			year = pre[len('xjllbs')+1:-1]
			if year not in stock.xjllbs:
				return ''
			else:
				xb = stock.xjllbs[year]
				return xb.__dict__[suf]
		elif pre.startswith('fjsj'):
			year = pre[len('fjsjs')+1:-1]
			if year not in stock.fjsjs:
				return ''
			else:
				fj = stock.fjsjs[year]
				return fj.__dict__[suf]
		else:
			return ''

	@classmethod
	def get_weighted_dividedval(self, stock, numforms, numprop, denforms, denprop, year):
		numkeypath = '%s[%s].%s' % (numforms, year, numprop)
		numval = self.numValueForKeyPath(stock=stock, keypath=numkeypath)

		den1keypath = '%s[%s].%s' % (denforms, year, denprop)
		den1val = self.numValueForKeyPath(stock=stock, keypath=den1keypath)

		den0keypath = '%s[%d].%s' % (denforms, int(year) - 1, denprop)
		den0val = self.numValueForKeyPath(stock=stock, keypath=den0keypath)
		if int(den0val) == 0:
			denval = den1val
		else:
			denval = (den1val + den0val) / 2

		if denval == 0:
			return 0.0
		else:
			return numval / denval

	@classmethod
	def get_thisdividedlast(self, stock, numforms, numprop, denforms, denprop, year):
		numkeypath = '%s[%s].%s' % (numforms, year, numprop)
		numval = self.numValueForKeyPath(stock=stock, keypath=numkeypath)

		denkeypath = '%s[%d].%s' % (denforms, int(year) - 1, denprop)
		denval = self.numValueForKeyPath(stock=stock, keypath=denkeypath)

		if denval == 0:
			return 0
		else:
			return numval / denval


	## 求行业均值的方法

	@classmethod
	def get_ave_val(self, stocks, keypath):
		if len(stocks) == 0:
			return 0.0

		val = 0.0
		for stk in stocks:
			val += self.numValueForKeyPath(stock=stk, keypath=keypath)
		return (val / len(stocks))

	@classmethod
	def get_ave_dividedval(self, stocks, numerator, denominator):
		numtot = 0.0
		dentot = 0.0
		for stk in stocks:
			numval = self.numValueForKeyPath(stock=stk, keypath=numerator)
			denval = self.numValueForKeyPath(stock=stk, keypath=denominator)
			numtot += numval
			dentot += denval
		if dentot == 0:
			return 0.0
		else:
			return numtot / dentot

	@classmethod
	def get_ave_weighted_dividedval(self, stocks, numforms, numprop, denforms, denprop, year):
		numtot = 0.0
		dentot = 0.0
		for stk in stocks:
			numkeypath = '%s[%s].%s' % (numforms, year, numprop)
			numval = self.numValueForKeyPath(stock=stk, keypath=numkeypath)

			den1keypath = '%s[%s].%s' % (denforms, year, denprop)
			den1val = self.numValueForKeyPath(stock=stk, keypath=den1keypath)

			den0keypath = '%s[%d].%s' % (denforms, int(year) - 1, denprop)
			den0val = self.numValueForKeyPath(stock=stk, keypath=den0keypath)
			if int(den0val) == 0:
				denval = den1val
			else:
				denval = (den1val + den0val) / 2

			if denval != 0:
				numtot += numval
				dentot += denval

		if dentot == 0:
			return 0.0
		else:
			return numtot / dentot

	@classmethod
	def get_ave_thisdividedlast(self, stocks, numforms, numprop, denforms, denprop, year):
		numtot = 0.0
		dentot = 0.0
		for stk in stocks:
			numkeypath = '%s[%s].%s' % (numforms, year, numprop)
			numval = self.numValueForKeyPath(stock=stk, keypath=numkeypath)

			denkeypath = '%s[%d].%s' % (denforms, int(year) - 1, denprop)
			denval = self.numValueForKeyPath(stock=stk, keypath=denkeypath)

			if denval != 0:
				numtot += numval
				dentot += denval

		if dentot == 0:
			return 0.0
		else:
			return numtot / dentot

	@classmethod
	def get_ave_growrate(self, stocks, numerator, denominator):
		numtot = 0.0
		dentot = 0.0
		for stk in stocks:
			numval = self.numValueForKeyPath(stock=stk, keypath=numerator)
			denval = self.numValueForKeyPath(stock=stk, keypath=denominator)
			numtot += numval
			dentot += denval
		return self.getGrowRate(val_cur=numtot, val_lst=dentot, use_percent_format=False)

	@classmethod
	def get_ave_comprate(self, stocks, years, numerator, denominator):
		numtot = 0.0
		dentot = 0.0
		for stk in stocks:
			numval = self.numValueForKeyPath(stock=stk, keypath=numerator)
			denval = self.numValueForKeyPath(stock=stk, keypath=denominator)
			numtot += numval
			dentot += denval
		return self.getCompRate(val_cur=numtot, val_lst=dentot, years=years, use_percent_format=False)

	@classmethod
	def color_of_is_target(self, stock, target):
		if stock.symbol == target.symbol:
			return Cons.COLOR_PINK
		else:
			return Cons.COLOR_WHITE

	@classmethod
	def color_of_margins(self, val, compval, margin_up, margin_down, decending=True):
		if val == 0 or compval == 0:
			return Cons.COLOR_WHITE

		if decending:
			up = (val - compval) / abs(compval)
			down = (compval - val) / abs(compval)
			if up >= margin_up:
				return Cons.COLOR_GREEN
			elif down >= margin_down:
				return Cons.COLOR_RED
		else:
			up = (compval - val) / abs(compval)
			down = (val - compval) / abs(compval)
			if up >= margin_down:
				return Cons.COLOR_GREEN
			elif down >= margin_up:
				return Cons.COLOR_RED
		return Cons.COLOR_WHITE
