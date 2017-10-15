# -*- coding: utf-8 -*-

from models.zcfzb import ZCFZB
from models.gslrb import GSLRB
from models.xjllb import XJLLB
from models.fjsj import FJSJ
from models.stock import Stock
from utils.util_res import ResUtil
from utils.util_stock import StockUtil
from utils.util_html import HTMLUtil
import utils.util_cons as Cons

class GroupDrawer(object):
	def __init__(self, industry, stocks_group, target):
		assert len(industry) > 0
		if stocks_group is None or len(stocks_group) == 0:
			return
		self.industry = industry
		self.stocks_group = stocks_group
		self.target = target
		self.margin_up = 0.5
		self.margin_down = 0.5

	def draw(self):
		years = len(self.stocks_group[0].zcfzbs)

		keys = [k for k in sorted(self.stocks_group[0].zcfzbs)]
		keys.reverse()

		html_util = HTMLUtil()
		html_util.add_start(title=self.industry)
		self.draw_curfds_quaility(html_util, keys)
		self.draw_accorece_quality(html_util, keys)
		self.draw_inve_quality(html_util, keys)
		self.draw_prodasset_quality(html_util, keys)
		self.draw_inveasset_quality(html_util, keys)
		self.draw_inc_quality(html_util, keys)
		self.draw_cashflow_quality(html_util, keys)
		self.draw_safety_quality(html_util, keys)
		self.draw_growth_quality(html_util, keys)
		self.draw_earns_quality(html_util, keys)
		self.draw_managers_quality(html_util, keys)
		self.draw_roe_quality(html_util, keys)
		html_util.add_end()
		html_util.save_to_file(self.industry)

	def add_divideval_table(self, html_util, keys, caption, three_tds, last_td, num_forms, num_property, den_forms, den_property, func, units, decending):
		assert len(three_tds) == 3
		assert len(units) == len(three_tds)
		if func is None:
			func = lambda x:x
		html_util.add_table_start(caption=caption)
		# 标题行
		html_util.add_table_head_start()
		for k in keys:
			html_util.add_table_head_th(th=k, colspan=3)
		html_util.add_table_head_th_recommend()
		html_util.add_table_head_end()
		# 副标题行
		html_util.add_table_body_start()
		html_util.add_table_body_tr_start()
		for k in keys:
			html_util.add_table_body_td(td=three_tds[0])
			html_util.add_table_body_td(td=three_tds[1])
			html_util.add_table_body_td(td=three_tds[2])
		html_util.add_table_body_td(td=last_td)
		html_util.add_table_body_tr_end()
		# 排序和计算均值
		groups_list = []
		aves_dic = {}
		for k in keys:
			numkeypath = '%s[%s].%s' % (num_forms, k, num_property)
			denkeypath = '%s[%s].%s' % (den_forms, k, den_property)
			group = sorted(self.stocks_group, key=lambda stk: func(StockUtil.getDivideVal(num=StockUtil.numValueForKeyPath(stock=stk, keypath=numkeypath), den=StockUtil.numValueForKeyPath(stock=stk, keypath=denkeypath), use_percent_format=False)), reverse=decending)
			groups_list.append(group)
			ave = StockUtil.get_ave_dividedval(stocks=self.stocks_group, numerator=numkeypath, denominator=denkeypath)
			ave = func(ave)
			aves_dic[k] = ave
		# 内容行
		for line in range(len(self.stocks_group)):
			html_util.add_table_body_tr_start()
			for k in keys:
				idx = int(keys[0]) - int(k)
				group = groups_list[idx]
				stk = group[line]
				ave = aves_dic[k]
				numkeypath = '%s[%s].%s' % (num_forms, k, num_property)
				denkeypath = '%s[%s].%s' % (den_forms, k, den_property)
				#
				is_target_color = StockUtil.color_of_is_target(stock=stk, target=self.target)
				html_util.add_table_body_td(td=stk.name, color=is_target_color)
				#
				html_util.add_table_body_td_val(val=StockUtil.numValueForKeyPath(stock=stk, keypath=numkeypath), color=is_target_color, unit=units[1])
				#
				val = StockUtil.getDivideVal(num=StockUtil.numValueForKeyPath(stock=stk, keypath=numkeypath), den=StockUtil.numValueForKeyPath(stock=stk, keypath=denkeypath), use_percent_format=False)
				val = func(val)
				margins_color = StockUtil.color_of_margins(val=val, compval=ave, margin_up=self.margin_up, margin_down=self.margin_down, decending=decending)
				html_util.add_table_body_td_val(val=val, color=margins_color, unit=units[2])
			html_util.add_table_body_td_empty()
			html_util.add_table_body_tr_end()
		# 均值行
		html_util.add_table_body_tr_start()
		for k in keys:
			val = aves_dic[k]
			html_util.add_table_body_td_empty()
			html_util.add_table_body_td_empty()
			html_util.add_table_body_td_val(val=val, color=Cons.COLOR_YELLOW, unit=units[2])
		html_util.add_table_body_tr_end()
		# 表格结束
		html_util.add_table_body_end()
		html_util.add_table_end()

	def add_growrate_table(self, html_util, keys, caption, three_tds, last_td, forms, prop, func, units, decending):
		assert len(three_tds) == 3
		assert len(units) == len(three_tds)
		if func is None:
			func = lambda x:x
		html_util.add_table_start(caption=caption)
		# 标题行
		html_util.add_table_head_start()
		for k in keys:
			html_util.add_table_head_th(th=k, colspan=3)
		html_util.add_table_head_th_recommend()
		html_util.add_table_head_end()
		# 副标题行
		html_util.add_table_body_start()
		html_util.add_table_body_tr_start()
		for k in keys:
			html_util.add_table_body_td(td=three_tds[0])
			html_util.add_table_body_td(td=three_tds[1])
			html_util.add_table_body_td(td=three_tds[2])
		html_util.add_table_body_td(td=last_td)
		html_util.add_table_body_tr_end()
		# 排序和计算均值
		groups_list = []
		aves_dic = {}
		for k in keys:
			numkeypath = '%s[%s].%s' % (forms, k, prop)
			denkeypath = '%s[%d].%s' % (forms, int(k)-1, prop)
			group = sorted(self.stocks_group, key=lambda stk: func(StockUtil.getGrowRate(val_cur=StockUtil.numValueForKeyPath(stock=stk, keypath=numkeypath), val_lst=StockUtil.numValueForKeyPath(stock=stk, keypath=denkeypath), use_percent_format=False)), reverse=decending)
			groups_list.append(group)
			ave = StockUtil.get_ave_growrate(stocks=self.stocks_group, numerator=numkeypath, denominator=denkeypath)
			ave = func(ave)
			aves_dic[k] = ave
		# 内容行
		for line in range(len(self.stocks_group)):
			html_util.add_table_body_tr_start()
			for k in keys:
				idx = int(keys[0]) - int(k)
				group = groups_list[idx]
				stk = group[line]
				ave = aves_dic[k]
				numkeypath = '%s[%s].%s' % (forms, k, prop)
				denkeypath = '%s[%d].%s' % (forms, int(k)-1, prop)
				#
				is_target_color = StockUtil.color_of_is_target(stock=stk, target=self.target)
				html_util.add_table_body_td(td=stk.name, color=is_target_color)
				#
				html_util.add_table_body_td_val(val=StockUtil.numValueForKeyPath(stock=stk, keypath=numkeypath), color=is_target_color, unit=units[1])
				#
				val = StockUtil.getGrowRate(val_cur=StockUtil.numValueForKeyPath(stock=stk, keypath=numkeypath), val_lst=StockUtil.numValueForKeyPath(stock=stk, keypath=denkeypath), use_percent_format=False)
				val = func(val)
				margins_color = StockUtil.color_of_margins(val=val, compval=ave, margin_up=self.margin_up, margin_down=self.margin_down, decending=decending)
				html_util.add_table_body_td_val(val=val, color=margins_color, unit=units[2])
			html_util.add_table_body_td_empty()
			html_util.add_table_body_tr_end()
		# 均值行
		html_util.add_table_body_tr_start()
		for k in keys:
			val = aves_dic[k]
			html_util.add_table_body_td_empty()
			html_util.add_table_body_td_empty()
			html_util.add_table_body_td_val(val=val, color=Cons.COLOR_YELLOW, unit=units[2])
		html_util.add_table_body_tr_end()
		# 表格结束
		html_util.add_table_body_end()
		html_util.add_table_end()

	def add_comprate_table(self, html_util, keys, caption, three_tds, last_td, forms, prop, func, units, decending):
		assert len(three_tds) == 3
		assert len(units) == len(three_tds)
		if func is None:
			func = lambda x:x
		html_util.add_table_start(caption=caption)
		# 标题行
		html_util.add_table_head_start()
		for k in keys:
			html_util.add_table_head_th(th=k, colspan=3)
		html_util.add_table_head_th_recommend()
		html_util.add_table_head_end()
		# 副标题行
		html_util.add_table_body_start()
		html_util.add_table_body_tr_start()
		for k in keys:
			html_util.add_table_body_td(td=three_tds[0])
			html_util.add_table_body_td(td=three_tds[1])
			html_util.add_table_body_td(td=three_tds[2])
		html_util.add_table_body_td(td=last_td)
		html_util.add_table_body_tr_end()
		# 排序和计算均值
		groups_list = []
		aves_dic = {}
		for k in keys:
			numkeypath = '%s[%s].%s' % (forms, k, prop)
			denkeypath = '%s[%s].%s' % (forms, keys[-1], prop)
			years = int(k) - int(keys[-1])
			group = sorted(self.stocks_group, key=lambda stk: func(StockUtil.getCompRate(val_cur=StockUtil.numValueForKeyPath(stock=stk, keypath=numkeypath), val_lst=StockUtil.numValueForKeyPath(stock=stk, keypath=denkeypath), years=years, use_percent_format=False)), reverse=decending)
			groups_list.append(group)
			ave = StockUtil.get_ave_comprate(stocks=self.stocks_group, years=years, numerator=numkeypath, denominator=denkeypath)
			ave = func(ave)
			aves_dic[k] = ave
		# 内容行
		for line in range(len(self.stocks_group)):
			html_util.add_table_body_tr_start()
			for k in keys:
				idx = int(keys[0]) - int(k)
				group = groups_list[idx]
				stk = group[line]
				ave = aves_dic[k]
				numkeypath = '%s[%s].%s' % (forms, k, prop)
				denkeypath = '%s[%s].%s' % (forms, keys[-1], prop)
				years = int(k) - int(keys[-1])
				#
				is_target_color = StockUtil.color_of_is_target(stock=stk, target=self.target)
				html_util.add_table_body_td(td=stk.name, color=is_target_color)
				#
				html_util.add_table_body_td_val(val=StockUtil.numValueForKeyPath(stock=stk, keypath=numkeypath), color=is_target_color, unit=units[1])
				#
				val = StockUtil.getCompRate(val_cur=StockUtil.numValueForKeyPath(stock=stk, keypath=numkeypath), val_lst=StockUtil.numValueForKeyPath(stock=stk, keypath=denkeypath), years=years, use_percent_format=False)
				val = func(val)
				margins_color = StockUtil.color_of_margins(val=val, compval=ave, margin_up=self.margin_up, margin_down=self.margin_down, decending=decending)
				html_util.add_table_body_td_val(val=val, color=margins_color, unit=units[2])
			html_util.add_table_body_td_empty()
			html_util.add_table_body_tr_end()
		# 均值行
		html_util.add_table_body_tr_start()
		for k in keys:
			val = aves_dic[k]
			html_util.add_table_body_td_empty()
			html_util.add_table_body_td_empty()
			html_util.add_table_body_td_val(val=val, color=Cons.COLOR_YELLOW, unit=units[2])
		html_util.add_table_body_tr_end()
		# 表格结束
		html_util.add_table_body_end()
		html_util.add_table_end()

	def add_str_table(self, html_util, keys, caption, two_tds, last_td, forms, prop, func):
		assert len(two_tds) == 2
		if func is None:
			func = lambda x:x
		html_util.add_table_start(caption=caption)
		# 标题行
		html_util.add_table_head_start()
		for k in keys:
			html_util.add_table_head_th(th=k, colspan=2)
		html_util.add_table_head_th_recommend()
		html_util.add_table_head_end()
		# 副标题行
		html_util.add_table_body_start()
		html_util.add_table_body_tr_start()
		for k in keys:
			html_util.add_table_body_td(td=two_tds[0])
			html_util.add_table_body_td(td=two_tds[1])
		html_util.add_table_body_td(td=last_td)
		html_util.add_table_body_tr_end()
		# 排序和计算均值
		groups_list = []
		aves_dic = {}
		for k in keys:
			group = self.stocks_group
			groups_list.append(group)
		# 内容行
		for line in range(len(self.stocks_group)):
			html_util.add_table_body_tr_start()
			for k in keys:
				idx = int(keys[0]) - int(k)
				group = groups_list[idx]
				stk = group[line]
				numkeypath = '%s[%s].%s' % (forms, k, prop)
				#
				is_target_color = StockUtil.color_of_is_target(stock=stk, target=self.target)
				html_util.add_table_body_td(td=stk.name, color=is_target_color)
				#
				html_util.add_table_body_td(td=StockUtil.strValueForKeyPath(stock=stk, keypath=numkeypath), color=is_target_color)
			html_util.add_table_body_td_empty()
			html_util.add_table_body_tr_end()
		# 表格结束
		html_util.add_table_body_end()
		html_util.add_table_end()

	def add_num_table(self, html_util, keys, caption, two_tds, last_td, forms, prop, compvals, func, units, decending):
		assert len(two_tds) == 2
		assert len(units) == len(two_tds)
		if func is None:
			func = lambda x:x
		html_util.add_table_start(caption=caption)
		# 标题行
		html_util.add_table_head_start()
		for k in keys:
			html_util.add_table_head_th(th=k, colspan=2)
		html_util.add_table_head_th_recommend()
		html_util.add_table_head_end()
		# 副标题行
		html_util.add_table_body_start()
		html_util.add_table_body_tr_start()
		for k in keys:
			html_util.add_table_body_td(td=two_tds[0])
			html_util.add_table_body_td(td=two_tds[1])
		html_util.add_table_body_td(td=last_td)
		html_util.add_table_body_tr_end()
		# 排序和计算均值
		groups_list = []
		aves_dic = {}
		for k in keys:
			numkeypath = '%s[%s].%s' % (forms, k, prop)
			group = sorted(self.stocks_group, key=lambda stk: func(StockUtil.numValueForKeyPath(stock=stk, keypath=numkeypath)), reverse=decending)
			groups_list.append(group)
			ave = StockUtil.get_ave_val(stocks=self.stocks_group, keypath=numkeypath)
			ave = func(ave)
			aves_dic[k] = ave
		# 内容行
		for line in range(len(self.stocks_group)):
			html_util.add_table_body_tr_start()
			for k in keys:
				idx = int(keys[0]) - int(k)
				group = groups_list[idx]
				stk = group[line]
				numkeypath = '%s[%s].%s' % (forms, k, prop)
				#
				is_target_color = StockUtil.color_of_is_target(stock=stk, target=self.target)
				html_util.add_table_body_td(td=stk.name, color=is_target_color)
				#
				val = StockUtil.numValueForKeyPath(stock=stk, keypath=numkeypath)
				if len(compvals) == 1 and compvals[0] == Cons._ave_:
					tmpcompval = aves_dic[k]
					color = StockUtil.color_of_margins(val=val, compval=tmpcompval, margin_up=self.margin_up, margin_down=self.margin_down, decending=decending)
				else:
					if len(compvals) == 0:
						color = Cons.COLOR_WHITE
					elif len(compvals) == 1:
						tmpcompval = compvals[0]
						if decending:
							if val >= tmpcompval:
								color = Cons.COLOR_GREEN
							else:
								color = Cons.COLOR_RED
						else:
							if val <= tmpcompval:
								color = Cons.COLOR_GREEN
							else:
								color = Cons.COLOR_RED
					elif len(compvals) >= 2:
						compvals = sorted(compvals, reverse=False)
						val0 = compvals[0]
						val1 = compvals[1]
						if decending:
							if val > val1:
								color = Cons.COLOR_GREEN
							elif val < val0:
								color = Cons.COLOR_RED
							else:
								color = Cons.COLOR_YELLOW
						else:
							if val < val0:
								color = Cons.COLOR_GREEN
							elif val > val1:
								color = Cons.COLOR_RED
							else:
								color = Cons.COLOR_YELLOW
				html_util.add_table_body_td_val(val=val, color=color, unit=units[1])
			html_util.add_table_body_td_empty()
			html_util.add_table_body_tr_end()
		# 均值行
		if len(compvals) == 1 and compvals[0] == Cons._ave_:
			html_util.add_table_body_tr_start()
			for k in keys:
				val = aves_dic[k]
				html_util.add_table_body_td_empty()
				html_util.add_table_body_td_val(val=val, color=Cons.COLOR_YELLOW, unit=units[1])
			html_util.add_table_body_tr_end()
		# 表格结束
		html_util.add_table_body_end()
		html_util.add_table_end()
	
	# 数额，年增长率，复合增长率
	def add_growth_tables(self, html_util, keys, topic, forms, prop, decending):
		if decending:
			rule = '从高到低排序；行业均值规则'
		else:
			rule = '从低到高排序；行业均值规则'

		# 数额
		# 行业均值规则
		caption0 = '%s数额' % topic
		self.add_num_table(
			html_util=html_util,
			keys=keys,
			caption=caption0,
			two_tds=['企业', caption0],
			last_td=rule,
			forms=forms,
			prop=prop,
			compvals=[Cons._ave_],
			func=None,
			units=[None, Cons.Yi],
			decending=True)

		# 年增长率
		# 行业均值规则
		caption1 = '%s年增长率' % topic
		self.add_growrate_table(
			html_util=html_util,
			keys=keys,
			caption=caption1,
			three_tds=['企业', caption0, '同比年增长率'],
			last_td=rule,
			forms=forms,
			prop=prop,
			func=None,
			units=[None, Cons.Yi, Cons.Percent],
			decending=True)

		# 复合增长率
		# 行业均值规则
		caption2 = '%s复合增长率' % topic
		self.add_comprate_table(
			html_util=html_util,
			keys=keys,
			caption=caption2,
			three_tds=['企业', caption0, '复合年增长率'],
			last_td=rule,
			forms=forms,
			prop=prop,
			func=None,
			units=[None, Cons.Yi, Cons.Percent],
			decending=True)

	def add_weightdave_dividedval_table(self, html_util, keys, caption, four_tds, last_td, num_forms, num_property, den_forms, den_property, func, units, decending):
		assert len(four_tds) == 4
		assert len(units) == len(four_tds)
		if func is None:
			func = lambda x:x
		html_util.add_table_start(caption=caption)
		# 标题行
		html_util.add_table_head_start()
		for k in keys:
			html_util.add_table_head_th(th=k, colspan=4)
		html_util.add_table_head_th_recommend()
		html_util.add_table_head_end()
		# 副标题行
		html_util.add_table_body_start()
		html_util.add_table_body_tr_start()
		for k in keys:
			html_util.add_table_body_td(td=four_tds[0])
			html_util.add_table_body_td(td=four_tds[1])
			html_util.add_table_body_td(td=four_tds[2])
			html_util.add_table_body_td(td=four_tds[3])
		html_util.add_table_body_td(td=last_td)
		html_util.add_table_body_tr_end()
		# 排序和计算均值
		groups_list = []
		aves_dic = {}
		for k in keys:
			group = sorted(self.stocks_group, key=lambda stk: func(StockUtil.get_weighted_dividedval(stock=stk, numforms=num_forms, numprop=num_property, denforms=den_forms, denprop=den_property, year=k)), reverse=decending)
			groups_list.append(group)
			ave = StockUtil.get_ave_weighted_dividedval(stocks=self.stocks_group, numforms=num_forms, numprop=num_property, denforms=den_forms, denprop=den_property, year=k)
			ave = func(ave)
			aves_dic[k] = ave
		# 内容行
		for line in range(len(self.stocks_group)):
			html_util.add_table_body_tr_start()
			for k in keys:
				idx = int(keys[0]) - int(k)
				group = groups_list[idx]
				stk = group[line]
				ave = aves_dic[k]
				numkeypath = '%s[%s].%s' % (num_forms, k, num_property)
				#
				is_target_color = StockUtil.color_of_is_target(stock=stk, target=self.target)
				html_util.add_table_body_td(td=stk.name, color=is_target_color)
				#
				html_util.add_table_body_td_val(val=StockUtil.numValueForKeyPath(stock=stk, keypath=numkeypath), color=is_target_color, unit=units[1])
				#
				den0keypath = '%s[%d].%s' % (den_forms, int(k) - 1, den_property)
				den1keypath = '%s[%s].%s' % (den_forms, k, den_property)
				den0 = StockUtil.numValueForKeyPath(stock=stk, keypath=den0keypath)
				den1 = StockUtil.numValueForKeyPath(stock=stk, keypath=den1keypath)
				if den0 == 0:
					denval = den1
				else:
					denval = (den0 + den1) / 2
				html_util.add_table_body_td_val(val=denval, color=is_target_color, unit=units[2])
				#
				val = StockUtil.get_weighted_dividedval(stock=stk, numforms=num_forms, numprop=num_property, denforms=den_forms, denprop=den_property, year=k)
				val = func(val)
				margins_color = StockUtil.color_of_margins(val=val, compval=ave, margin_up=self.margin_up, margin_down=self.margin_down, decending=decending)
				html_util.add_table_body_td_val(val=val, color=margins_color, unit=units[3])
			html_util.add_table_body_td_empty()
			html_util.add_table_body_tr_end()
		# 均值行
		html_util.add_table_body_tr_start()
		for k in keys:
			val = aves_dic[k]
			html_util.add_table_body_td_empty()
			html_util.add_table_body_td_empty()
			html_util.add_table_body_td_empty()
			html_util.add_table_body_td_val(val=val, color=Cons.COLOR_YELLOW, unit=units[3])
		html_util.add_table_body_tr_end()
		# 表格结束
		html_util.add_table_body_end()
		html_util.add_table_end()

	def add_thisdividedlast_table(self, html_util, keys, caption, four_tds, last_td, num_forms, num_property, den_forms, den_property, func, units, decending):
		assert len(four_tds) == 4
		assert len(units) == len(four_tds)
		if func is None:
			func = lambda x:x
		html_util.add_table_start(caption=caption)
		# 标题行
		html_util.add_table_head_start()
		for k in keys:
			html_util.add_table_head_th(th=k, colspan=4)
		html_util.add_table_head_th_recommend()
		html_util.add_table_head_end()
		# 副标题行
		html_util.add_table_body_start()
		html_util.add_table_body_tr_start()
		for k in keys:
			html_util.add_table_body_td(td=four_tds[0])
			html_util.add_table_body_td(td=four_tds[1])
			html_util.add_table_body_td(td=four_tds[2])
			html_util.add_table_body_td(td=four_tds[3])
		html_util.add_table_body_td(td=last_td)
		html_util.add_table_body_tr_end()
		# 排序和计算均值
		groups_list = []
		aves_dic = {}
		for k in keys:
			group = sorted(self.stocks_group, key=lambda stk: func(StockUtil.get_thisdividedlast(stock=stk, numforms=num_forms, numprop=num_property, denforms=den_forms, denprop=den_property, year=k)), reverse=decending)
			groups_list.append(group)
			ave = StockUtil.get_ave_thisdividedlast(stocks=self.stocks_group, numforms=num_forms, numprop=num_property, denforms=den_forms, denprop=den_property, year=k)
			ave = func(ave)
			aves_dic[k] = ave
		# 内容行
		for line in range(len(self.stocks_group)):
			html_util.add_table_body_tr_start()
			for k in keys:
				idx = int(keys[0]) - int(k)
				group = groups_list[idx]
				stk = group[line]
				ave = aves_dic[k]
				numkeypath = '%s[%s].%s' % (num_forms, k, num_property)
				#
				is_target_color = StockUtil.color_of_is_target(stock=stk, target=self.target)
				html_util.add_table_body_td(td=stk.name, color=is_target_color)
				#
				html_util.add_table_body_td_val(val=StockUtil.numValueForKeyPath(stock=stk, keypath=numkeypath), color=is_target_color, unit=units[1])
				#
				den0keypath = '%s[%d].%s' % (den_forms, int(k) - 1, den_property)
				den0 = StockUtil.numValueForKeyPath(stock=stk, keypath=den0keypath)
				html_util.add_table_body_td_val(val=den0, color=is_target_color, unit=units[2])
				#
				val = StockUtil.get_thisdividedlast(stock=stk, numforms=num_forms, numprop=num_property, denforms=den_forms, denprop=den_property, year=k)
				val = func(val)
				margins_color = StockUtil.color_of_margins(val=val, compval=ave, margin_up=self.margin_up, margin_down=self.margin_down, decending=decending)
				html_util.add_table_body_td_val(val=val, color=margins_color, unit=units[3])
			html_util.add_table_body_td_empty()
			html_util.add_table_body_tr_end()
		# 均值行
		html_util.add_table_body_tr_start()
		for k in keys:
			val = aves_dic[k]
			html_util.add_table_body_td_empty()
			html_util.add_table_body_td_empty()
			html_util.add_table_body_td_val(val=val, color=Cons.COLOR_YELLOW, unit=units[3])
		html_util.add_table_body_tr_end()
		# 表格结束
		html_util.add_table_body_end()
		html_util.add_table_end()

	# 一、货币资金质量
	def draw_curfds_quaility(self, html_util, keys):
		html_util.add_title(title='一、货币资金质量')

		# 货币资金数额
		# 行业均值规则
		self.add_num_table(
			html_util=html_util,
			keys=keys,
			caption='货币资金数额',
			two_tds=['企业', '货币资金数额'],
			last_td='从高到低排序；行业均值规则',
			forms='zcfzbs',
			prop='curfds',
			compvals=[Cons._ave_],
			func=None,
			units=[None, Cons.Yi],
			decending=True)

		# 货币资金数额，货币资金/总资产
		# 行业均值规则
		self.add_divideval_table(
			html_util=html_util,
			keys=keys,
			caption='货币资金占比',
			three_tds=['企业', '货币资金数额', '货币资金/总资产'],
			last_td='由高到低排序；行业均值规则',
			num_forms='zcfzbs',
			num_property='curfds',
			den_forms='zcfzbs',
			den_property='totasset',
			func=None,
			units=[None, Cons.Yi, Cons.Percent],
			decending=True)

		## 货币资金同比年增长率
		## 行业均值规则
		self.add_growrate_table(
			html_util=html_util,
			keys=keys,
			caption='货币资金年增长率',
			three_tds=['企业', '货币资金数额', '同比年增长率'],
			last_td='由高到低排序；行业均值规则',
			forms='zcfzbs',
			prop='curfds',
			func=None,
			units=[None, Cons.Yi, Cons.Percent],
			decending=True)

		## 货币资金复合年增长率
		## 行业均值规则
		self.add_comprate_table(
			html_util=html_util,
			keys=keys,
			caption='货币资金复合年增长率',
			three_tds=['企业', '货币资金数额', '复合年增长率'],
			last_td='由高到低排序；行业均值规则',
			forms='zcfzbs',
			prop='curfds',
			func=None,
			units=[None, Cons.Yi, Cons.Percent],
			decending=True)

	# 二、应收账款质量
	def draw_accorece_quality(self, html_util, keys):
		html_util.add_title(title='二、应收账款质量')

		# 应收款总和/总资产
		# 行业均值规则
		self.add_divideval_table(
			html_util=html_util,
			keys=keys,
			caption='应收款总和/总资产',
			three_tds=['企业', '应收款总和', '应收款总和/总资产'],
			last_td='从低到高排序；行业均值规则',
			num_forms='zcfzbs',
			num_property='rectot',
			den_forms='zcfzbs',
			den_property='totasset',
			func=None,
			units=[None, Cons.Yi, Cons.Percent],
			decending=False)

		# 应收款总和/营业收入 * 12
		# 行业均值规则
		self.add_divideval_table(
			html_util=html_util,
			keys=keys,
			caption='应收款总和/营业收入 * 12',
			three_tds=['企业', '应收款总和', '应收款总和/营业收入 * 12'],
			last_td='从低到高排序；行业均值规则',
			num_forms='zcfzbs',
			num_property='rectot',
			den_forms='gslrbs',
			den_property='bizinco',
			func=lambda x:x*12,
			units=[None, Cons.Yi, None],
			decending=False)

		# 应收账款增幅
		# 行业均值规则
		self.add_growrate_table(
			html_util=html_util,
			keys=keys,
			caption='应收账款同比年增长率',
			three_tds=['企业', '应收账款数额', '同比年增长率'],
			last_td='从低到高排序；行业均值规则',
			forms='zcfzbs',
			prop='accorece',
			func=None,
			units=[None, Cons.Yi, Cons.Percent],
			decending=False)

		# 应收账款/营业收入 * 12
		# 行业均值规则
		self.add_divideval_table(
			html_util=html_util,
			keys=keys,
			caption='应收账款/营业收入 * 12',
			three_tds=['企业', '应收账款', '应收账款/营业收入 * 12'],
			last_td='从低到高排序；行业均值规则',
			num_forms='zcfzbs',
			num_property='accorece',
			den_forms='gslrbs',
			den_property='bizinco',
			func=lambda x:x*12,
			units=[None, Cons.Yi, None],
			decending=False)

		# 坏账准备总和/应收账款
		# 行业均值规则
		self.add_divideval_table(
			html_util=html_util,
			keys=keys,
			caption='坏账准备总和/应收账款',
			three_tds=['企业', '坏账准备总和', '坏账准备总和/应收账款'],
			last_td='从低到高排序；行业均值规则；注意过低的也要小心风险',
			num_forms='fjsjs',
			num_property='accorece_bad_tot',
			den_forms='zcfzbs',
			den_property='accorece',
			func=None,
			units=[None, Cons.Yi, Cons.Percent],
			decending=False)

	# 三、存货质量
	def draw_inve_quality(self, html_util, keys):
		html_util.add_title(title='三、存货质量')

		# 存货的数额，存货/营业成本
		# 行业均值规则
		self.add_divideval_table(
			html_util=html_util,
			keys=keys,
			caption='存货/营业成本',
			three_tds=['企业', '存货总额', '存货/营业成本'],
			last_td='从低到高排序；行业均值规则',
			num_forms='zcfzbs',
			num_property='inve',
			den_forms='gslrbs',
			den_property='bizcost',
			func=None,
			units=[None, Cons.Yi, Cons.Percent],
			decending=False)

		# 净利润 / 存货
		self.add_divideval_table(
			html_util=html_util,
			keys=keys,
			caption='净利润 / 存货',
			three_tds=['企业', '存货总额', '净利润 / 存货'],
			last_td='从高到低排序；行业均值规则',
			num_forms='gslrbs',
			num_property='netprofit',
			den_forms='zcfzbs',
			den_property='inve',
			func=None,
			units=[None, Cons.Yi, None],
			decending=True)

		# 存货增幅/营业成本增幅
		# 超过行业均值 margin_up 和低于行业均值 margin_down 的都要标红色
		self.add_growrate_table(
			html_util=html_util,
			keys=keys,
			caption='存货同比年增长率',
			three_tds=['企业', '存货总额', '年增长率'],
			last_td='从低到高排序；行业均值规则',
			forms='zcfzbs',
			prop='inve',
			func=None,
			units=[None, Cons.Yi, Cons.Percent],
			decending=False)

		# 销产比
		# 行业均值规则
		tmp_stocks_info = {}
		for stk in self.stocks_group:
			inve_unit = StockUtil.get_inve_unit_from_stock(stk)
			if inve_unit and len(inve_unit) > 0:
				if not inve_unit in tmp_stocks_info:
					tmp_stocks_info[inve_unit] = 0
				else:
					tmp_stocks_info[inve_unit] += 1
		inve_unit = ''
		maxcount = 0
		for unit, cnt in tmp_stocks_info.iteritems():
			if cnt >= maxcount:
				inve_unit = unit
				maxcount = cnt
		self.add_divideval_table(
			html_util=html_util,
			keys=keys,
			caption='销产比',
			three_tds=['企业', '销量', '销产比'],
			last_td='从高到低排序；行业均值规则',
			num_forms='fjsjs',
			num_property='inve_sale',
			den_forms='fjsjs',
			den_property='inve_prod',
			func=None,
			units=[None, inve_unit, None],
			decending=True)

		# 销产存比
		# 行业均值规则
		self.add_divideval_table(
			html_util=html_util,
			keys=keys,
			caption='销产存比',
			three_tds=['企业', '销量', '销产存比'],
			last_td='从高到低排序；行业均值规则',
			num_forms='fjsjs',
			num_property='inve_sale',
			den_forms='fjsjs',
			den_property='inve_prodandsave',
			func=None,
			units=[None, inve_unit, None],
			decending=True)

		# 存货跌价计提准备政策
		# 不用标
		self.add_str_table(
			html_util=html_util,
			keys=keys,
			caption='存货跌价计提准备政策',
			two_tds=['企业', '存货跌价计提准备政策'],
			last_td='无排序',
			forms='fjsjs',
			prop='inverevvallossstandard',
			func=None)

		# 计提跌价准备比例
		# 超过行业均值 margin_up 和低于行业均值 margin_down 的都要标红色
		self.add_divideval_table(
			html_util=html_util,
			keys=keys,
			caption='计提跌价准备比例',
			three_tds=['企业', '计提跌价准备总和', '计提跌价准备总和/存货'],
			last_td='从低到高排序；行业均值规则；过高和过低的都要注意风险',
			num_forms='fjsjs',
			num_property='inverevvallosstot',
			den_forms='zcfzbs',
			den_property='inve',
			func=None,
			units=[None, Cons.Yi, Cons.Percent],
			decending=False)

	# 四、生产相关资产
	def draw_prodasset_quality(self, html_util, keys):
		html_util.add_title(title='四、生产相关资产')

		# 生产资产/总资产
		# 行业均值规则
		self.add_divideval_table(
			html_util=html_util,
			keys=keys,
			caption='生产资产/总资产',
			three_tds=['企业', '生产资产总和', '生产资产/总资产'],
			last_td='从低到高排序；行业均值规则',
			num_forms='zcfzbs',
			num_property='prodassetot',
			den_forms='zcfzbs',
			den_property='totasset',
			func=None,
			units=[None, Cons.Yi, Cons.Percent],
			decending=False)
		
		# 税前利润总额 / 生产资产（资产是轻是重）
		# 行业均值规则
		self.add_divideval_table(
			html_util=html_util,
			keys=keys,
			caption='税前利润总额 / 生产资产',
			three_tds=['企业', '生产资产总和', '税前利润总额 / 生产资产'],
			last_td='从高到低排序；行业均值规则；低于12%的要注意',
			num_forms='gslrbs',
			num_property='totprofit',
			den_forms='zcfzbs',
			den_property='prodassetot',
			func=None,
			units=[None, Cons.Yi, Cons.Percent],
			decending=True)

	# 五、投资相关资产
	def draw_inveasset_quality(self, html_util, keys):
		html_util.add_title(title='五、投资相关资产')

		# 投资相关资产/总资产
		# 行业均值规则
		self.add_divideval_table(
			html_util=html_util,
			keys=keys,
			caption='投资相关资产/总资产',
			three_tds=['企业', '投资资产总和', '投资相关资产/总资产'],
			last_td='从低到高排序；行业均值规则',
			num_forms='zcfzbs',
			num_property='inveassetot',
			den_forms='zcfzbs',
			den_property='totasset',
			func=None,
			units=[None, Cons.Yi, Cons.Percent],
			decending=False)

	# 六、营业收入质量
	def draw_inc_quality(self, html_util, keys):
		html_util.add_title(title='六、营业收入质量')

		# 经营现金流净额 / 净利润
		# 行业均值规则
		self.add_divideval_table(
			html_util=html_util,
			keys=keys,
			caption='经营现金流净额 / 净利润',
			three_tds=['企业', '经营现金流净额', '经营现金流净额 / 净利润'],
			last_td='从高到低排序；行业均值规则',
			num_forms='xjllbs',
			num_property='mananetr',
			den_forms='gslrbs',
			den_property='netprofit',
			func=None,
			units=[None, Cons.Yi, None],
			decending=True)

		# 销售商品、提供劳务收到的现金 / 营业收入
		# 行业均值规则
		self.add_divideval_table(
			html_util=html_util,
			keys=keys,
			caption='销售商品、提供劳务收到的现金 / 营业收入',
			three_tds=['企业', '销售商品、提供劳务收到的现金', '销售商品、提供劳务收到的现金 / 营业收入'],
			last_td='从高到低排序；行业均值规则',
			num_forms='xjllbs',
			num_property='laborgetcash',
			den_forms='gslrbs',
			den_property='bizinco',
			func=None,
			units=[None, Cons.Yi, None],
			decending=True)

		# 营业收入 / 营业总收入
		self.add_num_table(
			html_util=html_util,
			keys=keys,
			caption='营业收入 / 营业总收入',
			two_tds=['企业', '营业收入 / 营业总收入'],
			last_td='从高到低排序；小于0.99的标红色，否则表绿色',
			forms='gslrbs',
			prop='bizincorate',
			compvals=[0.99],
			func=None,
			units=[None, None],
			decending=True)

	# 七、现金流量质量
	def draw_cashflow_quality(self, html_util, keys):
		html_util.add_title(title='七、现金流量质量')

		# 期末现金及现金等价物余额
		# 行业均值规则
		self.add_num_table(
			html_util=html_util,
			keys=keys,
			caption='期末现金及现金等价物余额',
			two_tds=['企业', '期末现金及现金等价物余额'],
			last_td='从高到低排序；行业均值规则',
			forms='xjllbs',
			prop='finalcashbala',
			compvals=[Cons._ave_],
			func=None,
			units=[None, Cons.Yi],
			decending=True)

		# 投资活动产生的现金流量净额
		# 小于0的绿色，大于0的红色
		self.add_num_table(
			html_util=html_util,
			keys=keys,
			caption='投资活动产生的现金流量净额',
			two_tds=['企业', '投资活动产生的现金流量净额'],
			last_td='从低到高排序；大于0的绿色，小于0的红色',
			forms='xjllbs',
			prop='invnetcashflow',
			compvals=[0.0],
			func=None,
			units=[None, Cons.Yi],
			decending=False)

		# 现金及现金等价物净增加额
		# 行业均值规则
		self.add_num_table(
			html_util=html_util,
			keys=keys,
			caption='现金及现金等价物净增加额',
			two_tds=['企业', '现金及现金等价物净增加额'],
			last_td='从高到低排序；行业均值规则',
			forms='xjllbs',
			prop='cashnetr',
			compvals=[Cons._ave_],
			func=None,
			units=[None, Cons.Yi],
			decending=True)

		# 折旧摊销/经营活动现金流净额
		# 行业均值规则
		self.add_divideval_table(
			html_util=html_util,
			keys=keys,
			caption='折旧摊销/经营活动现金流净额',
			three_tds=['企业', '折旧摊销', '折旧摊销/经营活动现金流净额'],
			last_td='从低到高排序；行业均值规则',
			num_forms='xjllbs',
			num_property='depamortot',
			den_forms='xjllbs',
			den_property='biznetcflow',
			func=None,
			units=[None, Cons.Yi, None],
			decending=False)

		# 简化的自由现金流 = 经营现金流净额 - 投资活动现金流出净额
		# 行业均值规则
		self.add_num_table(
			html_util=html_util,
			keys=keys,
			caption='简化的自由现金流',
			two_tds=['企业', '简化的自由现金流'],
			last_td='从高到低排序；行业均值规则',
			forms='xjllbs',
			prop='simfreecashflow',
			compvals=[Cons._ave_],
			func=None,
			units=[None, Cons.Yi],
			decending=True)
	
	# 八、安全性
	def draw_safety_quality(self, html_util, keys):
		html_util.add_title(title='八、安全性')

		# 有息负债率
		# >60% 标红色，没有的标绿色
		self.add_num_table(
			html_util=html_util,
			keys=keys,
			caption='有息负债率',
			two_tds=['企业', '有息负债率'],
			last_td='从低到高排序；>60% 标红色，<1% 的标绿色，否则标黄色',
			forms='zcfzbs',
			prop='borrate',
			compvals=[0.01, 0.6],
			func=None,
			units=[None, Cons.Percent],
			decending=False)

		# 货币资金/有息负债
		# 行业均值规则
		self.add_divideval_table(
			html_util=html_util,
			keys=keys,
			caption='货币资金 / 有息负债',
			three_tds=['企业', '货币资金', '货币资金 / 有息负债'],
			last_td='从高到低排序；行业均值规则',
			num_forms='zcfzbs',
			num_property='curfds',
			den_forms='zcfzbs',
			den_property='borrtot',
			func=None,
			units=[None, Cons.Yi, None],
			decending=True)

		# 期末现金及现金等价物余额 / 有息负债
		# 行业均值规则
		self.add_divideval_table(
			html_util=html_util,
			keys=keys,
			caption='期末现金及现金等价物余额 / 有息负债',
			three_tds=['企业', '期末现金及现金等价物余额', '期末现金及现金等价物余额 / 有息负债'],
			last_td='从高到低排序；行业均值规则',
			num_forms='xjllbs',
			num_property='finalcashbala',
			den_forms='zcfzbs',
			den_property='borrtot',
			func=None,
			units=[None, Cons.Yi, None],
			decending=True)

	# 九、成长性
	def draw_growth_quality(self, html_util, keys):
		html_util.add_title(title='九、成长性')

		# 总资产
		self.add_growth_tables(
			html_util=html_util,
			keys=keys,
			topic='总资产',
			forms='zcfzbs',
			prop='totasset',
			decending=True)

		# 净资产
		self.add_growth_tables(
			html_util=html_util,
			keys=keys,
			topic='净资产',
			forms='zcfzbs',
			prop='righaggr',
			decending=True)

		# 总负债
		self.add_growth_tables(
			html_util=html_util,
			keys=keys,
			topic='净资产',
			forms='zcfzbs',
			prop='totliab',
			decending=True)

		# 营业收入
		self.add_growth_tables(
			html_util=html_util,
			keys=keys,
			topic='营业收入',
			forms='gslrbs',
			prop='perprofit',
			decending=True)

		# 毛利润
		self.add_growth_tables(
			html_util=html_util,
			keys=keys,
			topic='毛利润',
			forms='gslrbs',
			prop='grossprofit',
			decending=True)

		# 营业利润
		self.add_growth_tables(
			html_util=html_util,
			keys=keys,
			topic='营业利润',
			forms='gslrbs',
			prop='perprofit',
			decending=True)

		# 净利润
		self.add_growth_tables(
			html_util=html_util,
			keys=keys,
			topic='净利润',
			forms='gslrbs',
			prop='netprofit',
			decending=True)

	# 十、盈利能力
	def draw_earns_quality(self, html_util, keys):
		html_util.add_title(title='十、盈利能力')

		# 加权平均 ROE
		# 行业均值规则
		self.add_weightdave_dividedval_table(
			html_util=html_util,
			keys=keys,
			caption='加权平均 ROE',
			four_tds=['企业', '净利润', '加权平均净资产', '加权平均 ROE'],
			last_td='从高到低排序；行业均值规则',
			num_forms='gslrbs',
			num_property='netprofit',
			den_forms='zcfzbs',
			den_property='righaggr',
			func=None,
			units=[None, Cons.Yi, Cons.Yi, Cons.Percent],
			decending=True)

		# 加权平均 ROA
		# 行业均值规则
		self.add_weightdave_dividedval_table(
			html_util=html_util,
			keys=keys,
			caption='加权平均 ROA',
			four_tds=['企业', '净利润', '加权平均总资产', '加权平均 ROA'],
			last_td='从高到低排序；行业均值规则',
			num_forms='gslrbs',
			num_property='netprofit',
			den_forms='zcfzbs',
			den_property='totasset',
			func=None,
			units=[None, Cons.Yi, Cons.Yi, Cons.Percent],
			decending=True)

		# 加权平均净资产现金回收率
		# 行业均值规则
		self.add_weightdave_dividedval_table(
			html_util=html_util,
			keys=keys,
			caption='加权平均净资产现金回收率',
			four_tds=['企业', '经营现金流净额', '加权平均净资产', '加权平均净资产现金回收率'],
			last_td='从高到低排序；行业均值规则',
			num_forms='xjllbs',
			num_property='mananetr',
			den_forms='zcfzbs',
			den_property='righaggr',
			func=None,
			units=[None, Cons.Yi, Cons.Yi, Cons.Percent],
			decending=True)

		# 加权平均总资产现金回收率
		# 行业均值规则
		self.add_weightdave_dividedval_table(
			html_util=html_util,
			keys=keys,
			caption='加权平均总资产现金回收率',
			four_tds=['企业', '经营现金流净额', '加权平均总资产', '加权平均总资产现金回收率'],
			last_td='从高到低排序；行业均值规则',
			num_forms='xjllbs',
			num_property='mananetr',
			den_forms='zcfzbs',
			den_property='totasset',
			func=None,
			units=[None, Cons.Yi, Cons.Yi, Cons.Percent],
			decending=True)

		# 本期 ROE
		# 行业均值规则
		self.add_thisdividedlast_table(
			html_util=html_util,
			keys=keys,
			caption='本期 ROE',
			four_tds=['企业', '净利润', '期初净资产', '本期 ROE'],
			last_td='从高到低排序；行业均值规则',
			num_forms='gslrbs',
			num_property='netprofit',
			den_forms='zcfzbs',
			den_property='righaggr',
			func=None,
			units=[None, Cons.Yi, Cons.Yi, Cons.Percent],
			decending=True)

		# 本期 ROA
		# 行业均值规则
		self.add_thisdividedlast_table(
			html_util=html_util,
			keys=keys,
			caption='本期 ROA',
			four_tds=['企业', '净利润', '期初总资产', '本期 ROA'],
			last_td='从高到低排序；行业均值规则',
			num_forms='gslrbs',
			num_property='netprofit',
			den_forms='zcfzbs',
			den_property='totasset',
			func=None,
			units=[None, Cons.Yi, Cons.Yi, Cons.Percent],
			decending=True)

		# 本期净资产现金回收率
		# 行业均值规则
		self.add_thisdividedlast_table(
			html_util=html_util,
			keys=keys,
			caption='本期净资产现金回收率',
			four_tds=['企业', '经营现金流净额', '期初净资产', '本期净资产现金回收率'],
			last_td='从高到低排序；行业均值规则',
			num_forms='xjllbs',
			num_property='mananetr',
			den_forms='zcfzbs',
			den_property='righaggr',
			func=None,
			units=[None, Cons.Yi, Cons.Yi, Cons.Percent],
			decending=True)

		# 本期总资产现金回收率
		# 行业均值规则
		self.add_thisdividedlast_table(
			html_util=html_util,
			keys=keys,
			caption='本期总资产现金回收率',
			four_tds=['企业', '经营现金流净额', '期初总资产', '本期总资产现金回收率'],
			last_td='从高到低排序；行业均值规则',
			num_forms='xjllbs',
			num_property='mananetr',
			den_forms='zcfzbs',
			den_property='totasset',
			func=None,
			units=[None, Cons.Yi, Cons.Yi, Cons.Percent],
			decending=True)

		# 毛利率
		# 行业均值规则
		self.add_divideval_table(
			html_util=html_util,
			keys=keys,
			caption='毛利率',
			three_tds=['企业', '毛利润', '毛利率'],
			last_td='从高到低排序；行业均值规则；除以的是营业收入',
			num_forms='gslrbs',
			num_property='grossprofit',
			den_forms='gslrbs',
			den_property='bizinco',
			func=None,
			units=[None, Cons.Yi, Cons.Percent],
			decending=True)

		# 扣除非经常性损益营业利润率
		# 行业均值规则
		self.add_divideval_table(
			html_util=html_util,
			keys=keys,
			caption='扣除非经常性损益营业利润率',
			three_tds=['企业', '扣除非经常性损益营业利润', '扣除非经常性损益营业利润率'],
			last_td='从高到低排序；行业均值规则',
			num_forms='gslrbs',
			num_property='rmlosgainperprofit',
			den_forms='gslrbs',
			den_property='biztotinco',
			func=None,
			units=[None, Cons.Yi, Cons.Percent],
			decending=True)

		# 营业利润率
		# 行业均值规则
		self.add_divideval_table(
			html_util=html_util,
			keys=keys,
			caption='营业利润率',
			three_tds=['企业', '营业利润', '营业利润率'],
			last_td='从高到低排序；行业均值规则',
			num_forms='gslrbs',
			num_property='perprofit',
			den_forms='gslrbs',
			den_property='biztotinco',
			func=None,
			units=[None, Cons.Yi, Cons.Percent],
			decending=True)

		# 净利率
		# 行业均值规则
		self.add_divideval_table(
			html_util=html_util,
			keys=keys,
			caption='净利率',
			three_tds=['企业', '净利润', '净利率'],
			last_td='从高到低排序；行业均值规则',
			num_forms='gslrbs',
			num_property='netprofit',
			den_forms='gslrbs',
			den_property='biztotinco',
			func=None,
			units=[None, Cons.Yi, Cons.Percent],
			decending=True)

		# 营业成本率
		# 行业均值规则
		self.add_divideval_table(
			html_util=html_util,
			keys=keys,
			caption='营业成本率',
			three_tds=['企业', '营业成本', '营业成本率'],
			last_td='从低到高排序；行业均值规则；除以的是营业收入',
			num_forms='gslrbs',
			num_property='bizcost',
			den_forms='gslrbs',
			den_property='bizinco',
			func=None,
			units=[None, Cons.Yi, Cons.Percent],
			decending=False)

		# 三费 / 毛利润 = (销售费用 + 管理费用 + 正数的财务费用) / 毛利润
		# 行业均值规则
		self.add_divideval_table(
			html_util=html_util,
			keys=keys,
			caption='三费 / 毛利润',
			three_tds=['企业', '三费', '三费 / 毛利润'],
			last_td='从低到高排序；行业均值规则；三费 = 销售费用 + 管理费用 + 正数的财务费用',
			num_forms='gslrbs',
			num_property='salmanfinexpes',
			den_forms='gslrbs',
			den_property='grossprofit',
			func=None,
			units=[None, Cons.Yi, Cons.Percent],
			decending=False)
		# 超过 70% 的标红色，低于 70% 的标绿色
		self.add_num_table(
			html_util=html_util,
			keys=keys,
			caption='三费 / 毛利润',
			two_tds=['企业', '三费 / 毛利润'],
			last_td='从低到高排序；>70% 标红色，<70% 的标绿色',
			forms='gslrbs',
			prop='salmanfinexpes_gross_rate',
			compvals=[0.7],
			func=None,
			units=[None, Cons.Percent],
			decending=False)

		# 销售费用率
		# 行业均值规则
		self.add_divideval_table(
			html_util=html_util,
			keys=keys,
			caption='销售费用率',
			three_tds=['企业', '销售费用', '销售费用率'],
			last_td='从低到高排序；行业均值规则；除以的是营业收入',
			num_forms='gslrbs',
			num_property='salesexpe',
			den_forms='gslrbs',
			den_property='bizinco',
			func=None,
			units=[None, Cons.Yi, Cons.Percent],
			decending=False)

		# 管理费用率
		# 行业均值规则
		self.add_divideval_table(
			html_util=html_util,
			keys=keys,
			caption='管理费用率',
			three_tds=['企业', '管理费用', '管理费用率'],
			last_td='从低到高排序；行业均值规则；除以的是营业收入',
			num_forms='gslrbs',
			num_property='manaexpe',
			den_forms='gslrbs',
			den_property='bizinco',
			func=None,
			units=[None, Cons.Yi, Cons.Percent],
			decending=False)

		# 财务费用率
		# 行业均值规则
		self.add_divideval_table(
			html_util=html_util,
			keys=keys,
			caption='财务费用率',
			three_tds=['企业', '财务费用', '财务费用率'],
			last_td='从低到高排序；行业均值规则；除以的是营业收入',
			num_forms='gslrbs',
			num_property='finexpe',
			den_forms='gslrbs',
			den_property='bizinco',
			func=None,
			units=[None, Cons.Yi, Cons.Percent],
			decending=False)

		# 开发支出/营业成本
		# 行业均值规则
		self.add_divideval_table(
			html_util=html_util,
			keys=keys,
			caption='开发支出/营业成本',
			three_tds=['企业', '开发支出', '开发支出/营业成本'],
			last_td='从低到高排序；行业均值规则',
			num_forms='fjsjs',
			num_property='findevexp',
			den_forms='gslrbs',
			den_property='bizcost',
			func=None,
			units=[None, Cons.Yi, Cons.Percent],
			decending=False)

		# 资产减值损失 / 营业总收入
		# 行业均值规则
		self.add_divideval_table(
			html_util=html_util,
			keys=keys,
			caption='资产减值损失 / 营业总收入',
			three_tds=['企业', '资产减值损失', '资产减值损失 / 营业总收入'],
			last_td='从低到高排序；行业均值规则',
			num_forms='gslrbs',
			num_property='asseimpaloss',
			den_forms='gslrbs',
			den_property='biztotinco',
			func=None,
			units=[None, Cons.Yi, Cons.Percent],
			decending=False)

		# 公允价值变动收益 / 营业总收入
		# 行业均值规则
		self.add_divideval_table(
			html_util=html_util,
			keys=keys,
			caption='公允价值变动收益 / 营业总收入',
			three_tds=['企业', '公允价值变动收益', '公允价值变动收益 / 营业总收入'],
			last_td='从低到高排序；行业均值规则',
			num_forms='gslrbs',
			num_property='valuechgloss',
			den_forms='gslrbs',
			den_property='biztotinco',
			func=None,
			units=[None, Cons.Yi, Cons.Percent],
			decending=False)

		# 投资收益 / 营业总收入
		# 行业均值规则
		self.add_divideval_table(
			html_util=html_util,
			keys=keys,
			caption='投资收益 / 营业总收入',
			three_tds=['企业', '投资收益', '投资收益 / 营业总收入'],
			last_td='从低到高排序；行业均值规则',
			num_forms='gslrbs',
			num_property='inveinco',
			den_forms='gslrbs',
			den_property='biztotinco',
			func=None,
			units=[None, Cons.Yi, Cons.Percent],
			decending=False)

		# 汇兑收益 / 营业总收入
		# 行业均值规则
		self.add_divideval_table(
			html_util=html_util,
			keys=keys,
			caption='汇兑收益 / 营业总收入',
			three_tds=['企业', '汇兑收益', '汇兑收益 / 营业总收入'],
			last_td='从低到高排序；行业均值规则',
			num_forms='gslrbs',
			num_property='exchggain',
			den_forms='gslrbs',
			den_property='biztotinco',
			func=None,
			units=[None, Cons.Yi, Cons.Percent],
			decending=False)

		# 其他业务利润 / 营业总收入
		# 行业均值规则
		self.add_divideval_table(
			html_util=html_util,
			keys=keys,
			caption='其他业务利润 / 营业总收入',
			three_tds=['企业', '其他业务利润', '其他业务利润 / 营业总收入'],
			last_td='从低到高排序；行业均值规则',
			num_forms='gslrbs',
			num_property='otherbizprof',
			den_forms='gslrbs',
			den_property='biztotinco',
			func=None,
			units=[None, Cons.Yi, Cons.Percent],
			decending=False)

		# 非经常性损益净额 / 营业总收入
		# 行业均值规则
		self.add_divideval_table(
			html_util=html_util,
			keys=keys,
			caption='非经常性损益净额 / 营业总收入',
			three_tds=['企业', '非经常性损益净额', '非经常性损益净额 / 营业总收入'],
			last_td='从低到高排序；行业均值规则',
			num_forms='gslrbs',
			num_property='unoftenlosgain',
			den_forms='gslrbs',
			den_property='biztotinco',
			func=None,
			units=[None, Cons.Yi, Cons.Percent],
			decending=False)

		# 营业外收支净额 / 营业利润
		# 行业均值规则
		self.add_divideval_table(
			html_util=html_util,
			keys=keys,
			caption='营业外收支净额 / 营业利润',
			three_tds=['企业', '营业外收支净额', '营业外收支净额 / 营业利润'],
			last_td='从低到高排序；行业均值规则',
			num_forms='gslrbs',
			num_property='noninoutnet',
			den_forms='gslrbs',
			den_property='perprofit',
			func=None,
			units=[None, Cons.Yi, Cons.Percent],
			decending=False)

		# 非流动资产处置损失 / 营业利润
		# 行业均值规则
		self.add_divideval_table(
			html_util=html_util,
			keys=keys,
			caption='非流动资产处置损失 / 营业利润',
			three_tds=['企业', '非流动资产处置损失', '非流动资产处置损失 / 营业利润'],
			last_td='从低到高排序；行业均值规则',
			num_forms='gslrbs',
			num_property='noncassetsdisl',
			den_forms='gslrbs',
			den_property='perprofit',
			func=None,
			units=[None, Cons.Yi, Cons.Percent],
			decending=False)

		# 税率
		# 行业均值规则
		self.add_divideval_table(
			html_util=html_util,
			keys=keys,
			caption='税率',
			three_tds=['企业', '所得税总额', '税率'],
			last_td='从低到高排序；行业均值规则；除以利润总额',
			num_forms='gslrbs',
			num_property='incotaxexpe',
			den_forms='gslrbs',
			den_property='totprofit',
			func=None,
			units=[None, Cons.Yi, Cons.Percent],
			decending=False)

	# 十一、管理层运营能力
	def draw_managers_quality(self, html_util, keys):
		html_util.add_title(title='十一、管理层运营能力')

		# 应收账款周转率 = 营业收入 / 加权平均应收账款
		# 行业均值规则
		self.add_weightdave_dividedval_table(
			html_util=html_util,
			keys=keys,
			caption='应收账款周转率',
			four_tds=['企业', '营业收入', '加权平均应收账款', '应收账款周转率'],
			last_td='从高到低排序；行业均值规则；应收账款周转率 = 营业收入 / 加权平均应收账款',
			num_forms='gslrbs',
			num_property='bizinco',
			den_forms='zcfzbs',
			den_property='accorece',
			func=None,
			units=[None, Cons.Yi, Cons.Yi, None],
			decending=True)

		# 应收款总和周转率 = 营业收入 / 加权平均应收账款总和
		# 行业均值规则
		self.add_weightdave_dividedval_table(
			html_util=html_util,
			keys=keys,
			caption='应收款总和周转率',
			four_tds=['企业', '营业收入', '加权平均应收款总和', '应收款总和周转率'],
			last_td='从高到低排序；行业均值规则；应收款总和周转率 = 营业收入 / 加权平均应收款总和',
			num_forms='gslrbs',
			num_property='bizinco',
			den_forms='zcfzbs',
			den_property='rectot',
			func=None,
			units=[None, Cons.Yi, Cons.Yi, None],
			decending=True)

		# 存货周转率 = 营业成本 / 加权平均存货总额
		# 行业均值规则
		self.add_weightdave_dividedval_table(
			html_util=html_util,
			keys=keys,
			caption='存货周转率',
			four_tds=['企业', '营业成本', '加权存货总额', '存货周转率'],
			last_td='从高到低排序；行业均值规则；存货周转率 = 营业成本 / 加权平均存货总额',
			num_forms='gslrbs',
			num_property='bizcost',
			den_forms='zcfzbs',
			den_property='inve',
			func=None,
			units=[None, Cons.Yi, Cons.Yi, None],
			decending=True)

		# 固定资产周转率 = 营业收入 / 加权平均固定资产净额
		# 行业均值规则
		self.add_weightdave_dividedval_table(
			html_util=html_util,
			keys=keys,
			caption='固定资产周转率',
			four_tds=['企业', '营业收入', '加权平均固定资产净额', '固定资产周转率'],
			last_td='从高到低排序；行业均值规则；固定资产周转率 = 营业收入 / 加权平均固定资产净额',
			num_forms='gslrbs',
			num_property='bizinco',
			den_forms='zcfzbs',
			den_property='fixedassenet',
			func=None,
			units=[None, Cons.Yi, Cons.Yi, None],
			decending=True)

		# 生产相关资产周转率 = 营业收入 / 加权生产相关资产总额
		# 行业均值规则
		self.add_weightdave_dividedval_table(
			html_util=html_util,
			keys=keys,
			caption='生产相关资产周转率',
			four_tds=['企业', '营业收入', '加权生产相关资产总额', '生产相关资产周转率'],
			last_td='从高到低排序；行业均值规则；生产相关资产周转率 = 营业收入 / 加权生产相关资产总额',
			num_forms='gslrbs',
			num_property='bizinco',
			den_forms='zcfzbs',
			den_property='prodassetot',
			func=None,
			units=[None, Cons.Yi, Cons.Yi, None],
			decending=True)

		# 总资产周转率 = 营业收入 / 加权平均总资产，判断是否沃尔玛模式的关键指标
		# 行业均值规则
		self.add_weightdave_dividedval_table(
			html_util=html_util,
			keys=keys,
			caption='总资产运用能力',
			four_tds=['企业', '营业收入', '加权平均总资产', '总资产周转率'],
			last_td='从高到低排序；行业均值规则；总资产周转率 = 营业收入 / 加权平均总资产',
			num_forms='gslrbs',
			num_property='bizinco',
			den_forms='zcfzbs',
			den_property='totasset',
			func=None,
			units=[None, Cons.Yi, Cons.Yi, None],
			decending=True)

	# 十二、杜邦分析
	def draw_roe_quality(self, html_util, keys):
		html_util.add_title(title='十二、杜邦分析')

		# 茅台模式：净利率
		# 行业均值规则
		# 净利率
		# 行业均值规则
		self.add_divideval_table(
			html_util=html_util,
			keys=keys,
			caption='茅台模式：净利率',
			three_tds=['企业', '净利润', '净利率'],
			last_td='从高到低排序；行业均值规则',
			num_forms='gslrbs',
			num_property='netprofit',
			den_forms='gslrbs',
			den_property='biztotinco',
			func=None,
			units=[None, Cons.Yi, Cons.Percent],
			decending=True)

		# 管理层运营能力：总资产周转率
		# 行业均值规则
		self.add_weightdave_dividedval_table(
			html_util=html_util,
			keys=keys,
			caption='管理层运营能力：总资产周转率',
			four_tds=['企业', '营业收入', '加权平均总资产', '总资产周转率'],
			last_td='从高到低排序；行业均值规则；总资产周转率 = 营业收入 / 加权平均总资产',
			num_forms='gslrbs',
			num_property='bizinco',
			den_forms='zcfzbs',
			den_property='totasset',
			func=None,
			units=[None, Cons.Yi, Cons.Yi, None],
			decending=True)

		# 杠杆系数：加权平均总资产 / 净资产
		# 行业均值规则
		self.add_weightdave_dividedval_table(
			html_util=html_util,
			keys=keys,
			caption='杠杆系数：加权平均总资产 / 净资产',
			four_tds=['企业', '净资产', '加权平均总资产', '杠杆系数'],
			last_td='从低到高排序；行业均值规则；杠杆系数 = 加权平均总资产 / 净资产',
			num_forms='zcfzbs',
			num_property='righaggr',
			den_forms='zcfzbs',
			den_property='totasset',
			func=lambda x: 1/x,
			units=[None, Cons.Yi, Cons.Yi, None],
			decending=False)
