# -*- coding: utf-8 -*-

import utils.util_cons as Cons

class MarginsFilter(object):
	kVal = 'val'
	kColor = 'color'

	def __init__(self, margin_up, margin_down):
		self.margin_up = margin_up
		self.margin_down = margin_down

	def filter(self, vals, ave, decending=True):
		vals = sorted(vals, reverse=decending)
		desvals = []
		for v in vals:
			v = float(v)
			dic = {}
			dic[self.kVal] = v
			if ave == 0:
				color = Cons.COLOR_WHITE
			else:
				if decending:
					if (v / ave - 1) >= margin_up:
						color = Cons.COLOR_GREEN
					elif (ave / v - 1) >= margin_down:
						color = Cons.COLOR_RED
					else:
						color = Cons.COLOR_WHITE
				else:
					if (ave / v - 1) >= margin_down:
						color = Cons.COLOR_GREEN
					elif (v / ave - 1) >= margin_up:
						color = Cons.COLOR_RED
					else:
						color = Cons.COLOR_WHITE
			dic[self.kColor] = color
			desvals.append(dic)
		return desvals
