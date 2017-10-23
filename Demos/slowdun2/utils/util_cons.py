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
COLOR_GRAY = '#EBEDF4'

INDUSTRY_ELETRIC_KITCHEN = '厨电行业'

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

def valover1_color_map_func(val):
	if val >= 1:
		return COLOR_GREEN
	else:
		return COLOR_RED

def valover0_map_func(val):
	if int(val) >= 0:
		return COLOR_GREEN
	else:
		return COLOR_RED

def divideby_360_func(val):
	if int(val) == 0:
		return 0
	else:
		return 360. / val

def FUNC_compto_historyave_margins_color_map_func(val, aveval, margins_up=0.3, margins_down=0.3):
	if val >= aveval:
		rate = val / aveval - 1
		if rate >= margins_up:
			return COLOR_RED
		else:
			return COLOR_GREEN
	else:
		rate = aveval / val - 1
		if rate >= margins_down:
			return COLOR_RED
		else:
			return COLOR_GREEN
