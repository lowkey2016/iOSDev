# -*- coding: utf-8 -*-

Yi = 100000000
Wan = 10000
MIN_FLOAT = 0.0000000001
MAX_FLOAT = 9999999999
Percent = '%'

# 求平均值
_ave_ = '_ave_'

# http://www.peise.net/
COLOR_WHITE = '#FFFFFF'
COLOR_BLACK = '#000000'
COLOR_GREEN = '#77C34F'
COLOR_RED = '#EB3F2F'
COLOR_PINK = '#FF6E97'
COLOR_YELLOW = '#FFB86C'
COLOR_BLUE = '#2E68AA'
COLOR_PURPLE = '#8F1D78'

def roe_color_map_func(val):
		compval = 15
		val *= 100
		if int(val) >= compval:
			return COLOR_GREEN
		else:
			return COLOR_RED

def roa_color_map_func(val):
	compval = 7.5
	val *= 100
	if int(val) >= compval:
		return COLOR_GREEN
	else:
		return COLOR_RED

def rateover0_color_map_func(val):
	val *= 100
	if int(val) >= 0:
		return COLOR_GREEN
	else:
		return COLOR_RED

def valover1_oris0_color_map_func(val):
	if val >= 1 or val == 0:
		return COLOR_GREEN
	else:
		return COLOR_RED

def valover0_map_func(val):
	if int(val) >= 0:
		return COLOR_GREEN
	else:
		return COLOR_RED
