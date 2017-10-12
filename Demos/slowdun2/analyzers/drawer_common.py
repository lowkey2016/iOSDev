# -*- coding: utf-8 -*-

from models.zcfzb import ZCFZB
from models.fjsj import FJSJ
from models.stock import Stock
from utils.util_stock import StockUtil
from utils.util_res import ResUtil
from utils.util_html import HTMLUtil
from utils.util_math import MathUtil
import utils.util_cons as Cons

class CommonDrawer(object):
	def __init__(self, stock, keys):
		if stock is None:
			return
		self.stock = stock
		self.html_util = HTMLUtil()
		self.keys = keys

	def add_start(self):
		html_util = self.html_util
		html_util.add_start()

	def add_title_and_table_head(self, title, caption, two_ths):
		html_util = self.html_util
		keys = self.keys

		assert len(two_ths) == 2
		# 标题部分
		html_util.add_title(title=title)
		html_util.add_table_start(caption=caption)
		# 标题行
		html_util.add_table_head_start()
		html_util.add_table_head_th(th=two_ths[0], colspan=1, color=Cons.COLOR_WHITE)
		html_util.add_table_head_th(th=two_ths[1], colspan=1, color=Cons.COLOR_WHITE)
		for k in keys:
			html_util.add_table_head_th(th=k, colspan=2)
		html_util.add_table_head_th_recommend()
		html_util.add_table_head_end()
		# 内容部分
		html_util.add_table_body_start()
		html_util.add_table_body_tr_start()

	def add_table_end(self):
		html_util = self.html_util
		html_util.add_table_body_end()
		html_util.add_table_end()

	def add_end_and_save_to_stock_file(self, fname):
		html_util = self.html_util
		html_util.add_end()
		html_util.save_to_stock_file(stock=self.stock, fname=fname)

	def add_dividedval_table_line(self, two_tds, td_colors, num_forms, num_prop, den_forms, den_prop, two_units, last_td, only_dividedval_column=False, dividedval_color_map_func=None):
		html_util = self.html_util
		keys = self.keys

		assert len(two_tds) == 2
		assert len(td_colors) == len(two_tds)
		assert len(two_units) == 2
		html_util.add_table_body_td(td=two_tds[0], color=td_colors[0])
		html_util.add_table_body_td(td=two_tds[1], color=td_colors[1])
		for k in keys:
			numkeypath = '%s[%s].%s' % (num_forms, k, num_prop)
			denkeypath = '%s[%s].%s' % (den_forms, k, den_prop)
			numval = StockUtil.numValueForKeyPath(stock=self.stock, keypath=numkeypath)
			denval = StockUtil.numValueForKeyPath(stock=self.stock, keypath=denkeypath)
			
			if two_units[1] == Cons.Percent:
				use_percent_format = True
			else:
				use_percent_format = False
			rate = StockUtil.getDivideVal(num=numval, den=denval, use_percent_format=False)

			if dividedval_color_map_func:
				color = dividedval_color_map_func(rate)
			else:
				color = Cons.COLOR_WHITE
			if only_dividedval_column:
				html_util.add_table_body_td_val(val=rate, color=color, unit=two_units[0])
				html_util.add_table_body_td_empty()
			else:
				html_util.add_table_body_td_val(val=numval, color=color, unit=two_units[0])
				html_util.add_table_body_td_val(val=rate, color=color, unit=two_units[1])
		html_util.add_table_body_td(td=last_td, color=Cons.COLOR_WHITE)
		html_util.add_table_body_tr_end()

	def add_growrate_table_line(self, forms, prop, last_td):
		html_util = self.html_util
		keys = self.keys

		html_util.add_table_body_td(td='同比年增长率', color=Cons.COLOR_WHITE)
		html_util.add_table_body_td_empty()
		for k in keys:
			numkeypath = '%s[%s].%s' % (forms, k, prop)
			denkeypath = '%s[%d].%s' % (forms, int(k) - 1, prop)
			numval = StockUtil.numValueForKeyPath(stock=self.stock, keypath=numkeypath)
			denval = StockUtil.numValueForKeyPath(stock=self.stock, keypath=denkeypath)
			rate = StockUtil.getGrowRate(val_cur=numval, val_lst=denval, use_percent_format=False)
			html_util.add_table_body_td_val(val=rate, color=Cons.COLOR_WHITE, unit=Cons.Percent)
			html_util.add_table_body_td_empty()
		if last_td:
			last_td = '(本年/去年 - 1) * 100%；%s' % last_td
		else:
			last_td = '(本年/去年 - 1) * 100%'
		html_util.add_table_body_td(td=last_td, color=Cons.COLOR_WHITE)
		html_util.add_table_body_tr_end()

	def add_comprate_table_line(self, forms, prop, last_td):
		html_util = self.html_util
		keys = self.keys

		html_util.add_table_body_td(td='复合年增长率', color=Cons.COLOR_WHITE)
		html_util.add_table_body_td_empty()
		for k in keys:
			k0 = int(keys[-1])
			numkeypath = '%s[%s].%s' % (forms, k, prop)
			denkeypath = '%s[%d].%s' % (forms, k0, prop)
			years = int(k) - k0
			assert years >= 0
			numval = StockUtil.numValueForKeyPath(stock=self.stock, keypath=numkeypath)
			denval = StockUtil.numValueForKeyPath(stock=self.stock, keypath=denkeypath)
			rate = StockUtil.getCompRate(val_cur=numval, val_lst=denval, years=years, use_percent_format=False)
			html_util.add_table_body_td_val(val=rate, color=Cons.COLOR_WHITE, unit=Cons.Percent)
			html_util.add_table_body_td_empty()
		if last_td:
			last_td = '以最初的年份为基数；%s' % last_td
		else:
			last_td = '以最初的年份为基数'
		html_util.add_table_body_td(td=last_td, color=Cons.COLOR_WHITE)
		html_util.add_table_body_tr_end()

	def add_val_growrate_comprate_table_lines(self, two_tds, td_colors, num_forms, num_prop, den_forms, den_prop, two_units, last_td):
		html_util = self.html_util
		keys = self.keys

		# 数额
		self.add_dividedval_table_line(
			two_tds=two_tds,
			td_colors=td_colors,
			num_forms=num_forms,
			num_prop=num_prop,
			den_forms=den_forms,
			den_prop=den_prop,
			two_units=two_units,
			last_td=last_td)

		# 同比年增长率
		self.add_growrate_table_line(
			forms=num_forms,
			prop=num_prop,
			last_td='')

		# 复合年增长率
		self.add_comprate_table_line(
			forms=num_forms,
			prop=num_prop,
			last_td=last_td)

	def add_weightedave_dividedval_table_line(self, two_tds, td_colors, num_forms, num_prop, den_forms, den_prop, two_units, last_td, func=None, color_map_func=None):
		html_util = self.html_util
		keys = self.keys

		assert len(two_tds) == 2
		assert len(td_colors) == len(two_tds)
		assert len(two_units) == 2
		html_util.add_table_body_td(td=two_tds[0], color=td_colors[0])
		html_util.add_table_body_td(td=two_tds[1], color=td_colors[1])
		for k in keys:
			numkeypath = '%s[%s].%s' % (num_forms, k, num_prop)
			denkeypath = '%s[%s].%s' % (den_forms, k, den_prop)
			# numval = StockUtil.numValueForKeyPath(stock=self.stock, keypath=numkeypath)
			# denval = StockUtil.numValueForKeyPath(stock=self.stock, keypath=denkeypath)
			aveval = StockUtil.get_weighted_dividedval(stock=self.stock, numforms=num_forms, numprop=num_prop, denforms=den_forms, denprop=den_prop, year=k)
			if func:
				aveval = func(aveval)
			if color_map_func:
				color = color_map_func(aveval)
			else:
				color = Cons.COLOR_WHITE
			html_util.add_table_body_td_val(val=aveval, color=color, unit=two_units[0])
			html_util.add_table_body_td_empty()
		html_util.add_table_body_td(td=last_td, color=Cons.COLOR_WHITE)
		html_util.add_table_body_tr_end()

	def add_str_table_line(self, two_tds, td_colors, forms, prop, last_td):
		html_util = self.html_util
		keys = self.keys

		assert len(two_tds) == 2
		assert len(td_colors) == len(two_tds)
		html_util.add_table_body_td(td=two_tds[0], color=td_colors[0])
		html_util.add_table_body_td(td=two_tds[1], color=td_colors[1])
		for k in keys:
			keypath = '%s[%s].%s' % (forms, k, prop)
			val = StockUtil.strValueForKeyPath(stock=self.stock, keypath=keypath)
			html_util.add_table_body_td(td=val, color=Cons.COLOR_WHITE)
			html_util.add_table_body_td_empty()
		html_util.add_table_body_td(td=last_td, color=Cons.COLOR_WHITE)
		html_util.add_table_body_tr_end()

	def add_num_table_line(self, two_tds, td_colors, forms, prop, unit, last_td, val_color_map_func=None, val_map_func=None):
		html_util = self.html_util
		keys = self.keys

		assert len(two_tds) == 2
		assert len(td_colors) == len(two_tds)
		html_util.add_table_body_td(td=two_tds[0], color=td_colors[0])
		html_util.add_table_body_td(td=two_tds[1], color=td_colors[1])
		for k in keys:
			keypath = '%s[%s].%s' % (forms, k, prop)
			val = StockUtil.numValueForKeyPath(stock=self.stock, keypath=keypath)
			if val_color_map_func:
				color = val_color_map_func(val)
			else:
				color = Cons.COLOR_WHITE
			if val_map_func:
				val = val_map_func(val)
			html_util.add_table_body_td_val(val=val, color=color, unit=unit)
			html_util.add_table_body_td_empty()
		html_util.add_table_body_td(td=last_td, color=Cons.COLOR_WHITE)
		html_util.add_table_body_tr_end()

	def add_2nums_table_line(self, two_tds, td_colors, two_forms, two_props, two_units, last_td):
		html_util = self.html_util
		keys = self.keys
		
		assert len(two_tds) == 2
		assert len(td_colors) == len(two_tds)
		assert len(two_forms) == 2
		assert len(two_props) == 2
		assert len(two_units) == 2
		html_util.add_table_body_td(td=two_tds[0], color=td_colors[0])
		html_util.add_table_body_td(td=two_tds[1], color=td_colors[1])
		for k in keys:
			num0keypath = '%s[%s].%s' % (two_forms[0], k, two_props[0])
			num1keypath = '%s[%s].%s' % (two_forms[1], k, two_props[1])
			num0val = StockUtil.numValueForKeyPath(stock=self.stock, keypath=num0keypath)
			num1val = StockUtil.numValueForKeyPath(stock=self.stock, keypath=num1keypath)
			html_util.add_table_body_td_val(val=num0val, color=Cons.COLOR_WHITE, unit=two_units[0])
			html_util.add_table_body_td_val(val=num1val, color=Cons.COLOR_WHITE, unit=two_units[1])
		html_util.add_table_body_td(td=last_td, color=Cons.COLOR_WHITE)
		html_util.add_table_body_tr_end()
