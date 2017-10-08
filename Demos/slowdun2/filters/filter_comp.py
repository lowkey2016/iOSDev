# -*- coding: utf-8 -*-

import utils.util_cons as Cons

class CompFilter(object):
	kVal = 'val'
	kColor = 'color'

	def __init__(self, val):
		self.val = val

	def filter(self, vals, decending=True):
		vals = sorted(vals, reverse=decending)
		desvals = []
		for v in vals:
			v = float(v)
			dic = {}
			dic[self.kVal] = v
			if decending:
				if val >= self.val:
					color = Cons.COLOR_GREEN
				else:
					color = Cons.COLOR_RED
			dic[self.kColor] = color
			desvals.append(dic)
		return desvals
