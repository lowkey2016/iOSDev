# -*- coding: utf-8 -*-

from models.zcfzb import ZCFZB
from models.gslrb import GSLRB
from models.xjllb import XJLLB
from models.fjsj import FJSJ
from models.stock import Stock
from filters.filter_margins import MarginsFilter
from filters.filter_comp import CompFilter
from utils.util_res import ResUtil
from utils.util_stock import StockUtil
from utils.util_html import HTMLUtil
import utils.util_cons as Cons

class GroupDrawer(object):
	def __init__(self, stocks_group, target):
		if stocks_group is None or len(stocks_group) == 0:
			return
		self.stocks_group = stocks_group
		self.target = target
		self.margin_up = 0.5
		self.margin_down = 0.5

	def draw(self):
		years = len(self.stocks_group[0].zcfzbs)

		keys = [k for k in sorted(self.stocks_group[0].zcfzbs)]
		keys.reverse()

		html_util = HTMLUtil()
		html_util.add_start()
		self.draw_curfds_quaility(html_util, keys)
		self.draw_accorece_quality(html_util, keys)
		self.draw_inve_quality(html_util, keys)
		html_util.add_end()
		html_util.save_to_file('厨电行业综合对比')

	def add_divideval_table(self, html_util, keys, caption, three_tds, last_td, num_forms, num_property, den_forms, den_property, func, use_percent_format, decending=True):
		assert len(three_tds) == 3
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
				html_util.add_table_body_td_val(val=StockUtil.numValueForKeyPath(stock=stk, keypath=numkeypath), color=is_target_color, yi=True)
				#
				val = StockUtil.getDivideVal(num=StockUtil.numValueForKeyPath(stock=stk, keypath=numkeypath), den=StockUtil.numValueForKeyPath(stock=stk, keypath=denkeypath), use_percent_format=False)
				val = func(val)
				margins_color = StockUtil.color_of_margins(val=val, compval=ave, margin_up=self.margin_up, margin_down=self.margin_down, decending=decending)
				html_util.add_table_body_td_val(val=val, color=margins_color, percent=use_percent_format)
			html_util.add_table_body_td_empty()
			html_util.add_table_body_tr_end()
		# 均值行
		html_util.add_table_body_tr_start()
		for k in keys:
			val = aves_dic[k]
			html_util.add_table_body_td_empty()
			html_util.add_table_body_td_empty()
			html_util.add_table_body_td_val(val=val, color=Cons.COLOR_YELLOW, percent=use_percent_format)
		html_util.add_table_body_tr_end()
		# 表格结束
		html_util.add_table_body_end()
		html_util.add_table_end()

	def add_growrate_table(self, html_util, keys, caption, three_tds, last_td, forms, prop, func, use_percent_format, decending=True):
		assert len(three_tds) == 3
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
				html_util.add_table_body_td_val(val=StockUtil.numValueForKeyPath(stock=stk, keypath=numkeypath), color=is_target_color, yi=True)
				#
				val = StockUtil.getGrowRate(val_cur=StockUtil.numValueForKeyPath(stock=stk, keypath=numkeypath), val_lst=StockUtil.numValueForKeyPath(stock=stk, keypath=denkeypath), use_percent_format=False)
				val = func(val)
				margins_color = StockUtil.color_of_margins(val=val, compval=ave, margin_up=self.margin_up, margin_down=self.margin_down, decending=decending)
				html_util.add_table_body_td_val(val=val, color=margins_color, percent=use_percent_format)
			html_util.add_table_body_td_empty()
			html_util.add_table_body_tr_end()
		# 均值行
		html_util.add_table_body_tr_start()
		for k in keys:
			val = aves_dic[k]
			html_util.add_table_body_td_empty()
			html_util.add_table_body_td_empty()
			html_util.add_table_body_td_val(val=val, color=Cons.COLOR_YELLOW, percent=use_percent_format)
		html_util.add_table_body_tr_end()
		# 表格结束
		html_util.add_table_body_end()
		html_util.add_table_end()

	def add_comprate_table(self, html_util, keys, caption, three_tds, last_td, forms, prop, func, use_percent_format, decending=True):
		assert len(three_tds) == 3
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
				html_util.add_table_body_td_val(val=StockUtil.numValueForKeyPath(stock=stk, keypath=numkeypath), color=is_target_color, yi=True)
				#
				val = StockUtil.getCompRate(val_cur=StockUtil.numValueForKeyPath(stock=stk, keypath=numkeypath), val_lst=StockUtil.numValueForKeyPath(stock=stk, keypath=denkeypath), years=years, use_percent_format=False)
				val = func(val)
				margins_color = StockUtil.color_of_margins(val=val, compval=ave, margin_up=self.margin_up, margin_down=self.margin_down, decending=decending)
				html_util.add_table_body_td_val(val=val, color=margins_color, percent=use_percent_format)
			html_util.add_table_body_td_empty()
			html_util.add_table_body_tr_end()
		# 均值行
		html_util.add_table_body_tr_start()
		for k in keys:
			val = aves_dic[k]
			html_util.add_table_body_td_empty()
			html_util.add_table_body_td_empty()
			html_util.add_table_body_td_val(val=val, color=Cons.COLOR_YELLOW, percent=use_percent_format)
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

	# 一、货币资金质量
	def draw_curfds_quaility(self, html_util, keys):
		html_util.add_title(title='一、货币资金质量')

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
			use_percent_format=True,
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
			use_percent_format=True,
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
			use_percent_format=True,
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
			use_percent_format=True,
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
			use_percent_format=False,
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
			use_percent_format=True,
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
			use_percent_format=True,
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
			use_percent_format=True,
			decending=False)

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
			use_percent_format=True,
			decending=False)

		# 销产比
		# 行业均值规则
		inve_unit = ''
		if '2016' in self.stocks_group[0].fjsjs.keys() and inve_unit == '':
			inve_unit = self.stocks_group[0].fjsjs['2016'].inve_unit
		recom = '从高到低排序；行业均值规则；单位从亿改成%s' % inve_unit
		self.add_divideval_table(
			html_util=html_util,
			keys=keys,
			caption='销产比',
			three_tds=['企业', '销量', '销产比'],
			last_td=recom,
			num_forms='fjsjs',
			num_property='inve_sale',
			den_forms='fjsjs',
			den_property='inve_prod',
			func=None,
			use_percent_format=True,
			decending=True)

		# 销产存比
		# 行业均值规则
		self.add_divideval_table(
			html_util=html_util,
			keys=keys,
			caption='销产存比',
			three_tds=['企业', '销量', '销产存比'],
			last_td=recom,
			num_forms='fjsjs',
			num_property='inve_sale',
			den_forms='fjsjs',
			den_property='inve_prodandsave',
			func=None,
			use_percent_format=True,
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
			use_percent_format=True,
			decending=False)


		# 四、生产相关资产

		html_util.add_title(title='四、生产相关资产')

		# 生产资产/总资产
		# 分两行：第一行是比值，第二行是趋势
		# 行业均值规则: 计算行业的均值（行业历史生产资产总额 / 行业历史总资产总额），超过均值 margin_up 的标绿色，低于均值 margin_down 的标红色，下同
		# 比值对比去年，上升了标黄色，下降了标绿色

		# 税前利润总额 / 生产资产（资产是轻是重）
		# <12% 标黄色
		# 行业均值规则


		# 五、投资相关资产

		html_util.add_title(title='五、投资相关资产')

		# 投资相关资产/总资产
		# 超过行业均值的标黄色


		# 六、营业收入质量

		html_util.add_title(title='六、营业收入质量')

		# 经营现金流净额 / 净利润，大于1的年份数/总年份数
		# 大于1绿色，小于1红色

		# 销售商品、提供劳务收到的现金 / 营业收入
		# 大于1绿色，小于1红色


		# 七、现金流量质量

		html_util.add_title(title='七、现金流量质量')

		# 投资活动产生的现金流量净额
		# 小于0绿色，大于0红色

		# 现金及现金等价物净增加额
		# 大于0绿色，小于0红色

		# 折旧摊销/经营活动现金流净额
		# 行业均值规则


		# 八、安全性

		html_util.add_title(title='八、安全性')

		# 有息负债率
		# >60% 标红色，没有的标绿色

		# 货币资金/有息负债
		# 大于1绿色，小于1红色

		# 期末现金及现金等价物余额 / 有息负债
		# 大于1绿色，小于1红色


		# 九、成长性

		html_util.add_title(title='九、成长性')

		# 总资产数额，增长率
		# 增长的标绿色，减少的标红色

		# 总资产复合增长率
		# 行业均值规则

		# 净资产数额，增长率
		# 增长的标绿色，减少的标红色

		# 净资产复合增长率
		# 行业均值规则

		# 营业收入数额，增长率
		# 增长的标绿色，减少的标红色

		# 营业收入复合增长率
		# 行业均值规则

		# 营业利润数额，增长率
		# 增长的标绿色，减少的标红色

		# 营业利润复合增长率
		# 行业均值规则

		# 净利润数额，增长率
		# 增长的标绿色，减少的标红色

		# 净利润复合增长率
		# 行业均值规则


		# 十、盈利能力

		html_util.add_title(title='十、盈利能力')

		# 加权平均 ROE
		# 行业均值规则

		# 加权平均 ROA
		# 行业均值规则

		# 本期 ROE
		# 行业均值规则

		# 本期 ROA
		# 行业均值规则

		# 毛利率
		# 行业均值规则

		# 扣除非经常性损益营业利润率
		# 行业均值规则

		# 营业利润率
		# 行业均值规则

		# 净利率
		# 行业均值规则

		# 营业成本率
		# 行业均值规则

		# 费用率
		# 行业均值规则

		# 销售费用率
		# 行业均值规则

		# 管理费用率
		# 行业均值规则

		# 财务费用率
		# 行业均值规则

		# 开发支出/营业成本
		# 行业均值规则

		# 资产减值损失比例
		# 行业均值规则

		# 营业外收支净额/营业利润
		# 行业均值规则

		# 税率
		# 行业均值规则

		# 净资产现金回收率
		# 行业均值规则

		# 总资产现金回收率
		# 行业均值规则
		

		# 十一、管理层运营能力

		html_util.add_title(title='十一、管理层运营能力')

		# 应收账款周转率
		# 行业均值规则

		# 存货周转率
		# 行业均值规则

		# 固定资产周转率
		# 行业均值规则

		# 总资产周转率
		# 行业均值规则


		# 十二、杜邦分析

		html_util.add_title(title='十二、杜邦分析')

		# 茅台模式：净利率
		# 行业均值规则

		# 管理层运营能力：总资产周转率
		# 行业均值规则

		# 杠杆系数：平均总资产 / 净资产
		# 行业均值规则

