# -*- coding: utf-8 -*-

from models.zcfzb import ZCFZB
from models.gslrb import GSLRB
from models.xjllb import XJLLB
from models.fjsj import FJSJ
from models.quote import QUOTE
from models.stock import Stock
import utils.util_cons as Cons
from utils.util_stock import StockUtil
from utils.util_res import ResUtil
from utils.util_html import HTMLUtil
from utils.util_math import MathUtil

class QuoteDrawer(object):
	def __init__(self, stock):
		if stock is None:
			return
		self.stock = stock
		self.html_util = HTMLUtil()

		minyear = 0
		maxyear = 0
		for k in stock.zcfzbs.keys():
			k = int(k)
			if minyear > k:
				minyear = k
			if maxyear < k:
				maxyear = k
		self.min_report_year = minyear
		self.max_report_year = maxyear

		self.last_zcfzb = self.stock.zcfzbs[str(self.max_report_year)]
		self.last_gslrb = self.stock.gslrbs[str(self.max_report_year)]
		self.last_xjllb = self.stock.xjllbs[str(self.max_report_year)]
		if self.max_report_year in self.stock.fjsjs:
			self.last_fjsj = self.stock.fjsjs[str(self.max_report_year)]
		else:
			self.last_fjsj = FJSJ()

	def add_table_line(self, two_tds, color=Cons.COLOR_WHITE, last_td=''):
		assert len(two_tds) == 2
		html_util = self.html_util
		html_util.add_table_body_tr_start()
		html_util.add_table_body_td(td=two_tds[0], color=color)
		html_util.add_table_body_td(td=two_tds[1], color=color)
		html_util.add_table_body_td(td=last_td, color=color)
		html_util.add_table_body_tr_end()

	def draw(self):
		html_util = self.html_util

		title = '%s 市场数据' % self.stock.name
		caption = '市场数据 %s' % self.stock.quote.time
		html_util.add_start(title=title)

		# 标题部分
		html_util.add_title(title=title)
		html_util.add_table_start(caption=caption)
		# 标题行
		html_util.add_table_head_start()
		html_util.add_table_head_th(th='项目', colspan=1, color=Cons.COLOR_WHITE)
		html_util.add_table_head_th(th='数值', colspan=1, color=Cons.COLOR_WHITE)
		html_util.add_table_head_th_recommend()
		html_util.add_table_head_end()
		# 内容部分
		html_util.add_table_body_start()

		current = self.stock.quote.current
		totalShares = self.stock.quote.totalShares
		current_total = current * totalShares
		currency_unit = self.stock.quote.currency_unit

		td0 = '股价'
		td1 = '%.2f %s' % (current, currency_unit)
		self.add_table_line(two_tds=[td0, td1])

		td0 = '总股本'
		td1 = '%.4f 亿' % (self.stock.quote.totalShares / Cons.Yi)
		self.add_table_line(two_tds=[td0, td1])

		td0 = '流动股本'
		td1 = '%.4f 亿' % (self.stock.quote.float_shares / Cons.Yi)
		self.add_table_line(two_tds=[td0, td1])

		td0 = '流动比例'
		td1 = '%.2f%%' % StockUtil.getDivideVal(num=self.stock.quote.float_shares, den=self.stock.quote.totalShares, use_percent_format=True)
		self.add_table_line(two_tds=[td0, td1])

		td0 = '总市值'
		td1 = '%.2f 亿' % (current_total / Cons.Yi)
		self.add_table_line(two_tds=[td0, td1])

		td0 = '流动市值'
		td1 = '%.2f 亿' % (current * self.stock.quote.float_shares / Cons.Yi)
		self.add_table_line(two_tds=[td0, td1])

		td0 = 'NAV'
		nav = StockUtil.getDivideVal(num=self.last_zcfzb.righaggr, den=totalShares, use_percent_format=False)
		td1 = '%.2f %s' % (nav, currency_unit)
		last_td = '参照的数值是 %d 年终的数据；除以总股本；下同' % self.max_report_year
		self.add_table_line(two_tds=[td0, td1], last_td=last_td)

		td0 = '市净率 PB'
		pb = StockUtil.getDivideVal(num=current, den=nav, use_percent_format=False)
		td1 = '%.2f' % pb
		last_td = '购买 1 元净资产需要付出的价格'
		self.add_table_line(two_tds=[td0, td1], last_td=last_td)

		td0 = '每股经营现金流净额'
		td1 = '%.2f %s' % (StockUtil.getDivideVal(num=self.last_xjllb.mananetr, den=totalShares, use_percent_format=False), currency_unit)
		self.add_table_line(two_tds=[td0, td1])

		td0 = '每股现金流'
		td1 = '%.2f %s' % (StockUtil.getDivideVal(num=self.last_xjllb.cashfinalbala, den=totalShares, use_percent_format=False), currency_unit)
		self.add_table_line(two_tds=[td0, td1])

		td0 = 'EPS'
		eps = StockUtil.getDivideVal(num=self.last_gslrb.parenetp, den=totalShares, use_percent_format=False)
		td1 = '%.2f %s' % (eps, currency_unit)
		last_td = 'EPS = 归属于母公司的净利润 / 总股本'
		self.add_table_line(two_tds=[td0, td1], last_td=last_td)

		td0 = '市盈率 PE'
		pe = StockUtil.getDivideVal(num=current, den=eps, use_percent_format=False)
		td1 = '%.2f' % pe
		last_td = '购买这家企业回本需要多少年'
		self.add_table_line(two_tds=[td0, td1], last_td=last_td)

		td0 = '盈利率'
		ep = StockUtil.getDivideVal(num=1, den=pe, use_percent_format=False)
		td1 = '%.2f%%' % (ep * 100)
		if ep >= 0.0432 * 2:
			color = Cons.COLOR_GREEN
		else:
			color = Cons.COLOR_RED
		last_td = '格雷厄姆标准：盈利率至少为长期 AAA 级债券收益率的 2 倍，假设 AAA 级债券利率为 4.32%，下同'
		self.add_table_line(two_tds=[td0, td1], color=color, last_td=last_td)

		td0 = '每股销售额'
		sps = StockUtil.getDivideVal(num=self.last_gslrb.bizinco, den=totalShares, use_percent_format=False)
		td1 = '%.2f %s' % (sps, currency_unit)
		last_td = '每股销售额 = 营业收入 / 总股本'
		self.add_table_line(two_tds=[td0, td1], last_td=last_td)

		td0 = '市销率'
		td1 = '%.2f' % StockUtil.getDivideVal(num=current, den=sps, use_percent_format=False)
		self.add_table_line(two_tds=[td0, td1])

		td0 = '每股股息'
		td1 = '%.2f %s' % (self.stock.quote.dividend, currency_unit)
		self.add_table_line(two_tds=[td0, td1])

		td0 = '股息率'
		divyield = StockUtil.getDivideVal(num=self.stock.quote.dividend, den=current, use_percent_format=False)
		td1 = '%.2f%%' % (divyield * 100)
		if divyield >= 0.0432 * 2/3:
			color = Cons.COLOR_GREEN
		else:
			color = Cons.COLOR_WHITE
		last_td = '格雷厄姆标准：股息收益率至少为长期 AAA 级债券收益率的 2/3'
		self.add_table_line(two_tds=[td0, td1], color=color, last_td=last_td)

		td0 = '资本结构'
		capstruct = StockUtil.getDivideVal(num=current_total, den=(current_total + self.last_zcfzb.totliab), use_percent_format=False)
		td1 = '%.2f%%' % (capstruct * 100)
		if capstruct < 1./3:
			color = Cons.COLOR_RED
		elif capstruct > 2./3:
			color = Cons.COLOR_GREEN
		else:
			color = Cons.COLOR_YELLOW
		last_td = '资本结构 = 股票市值 / 资本总市值，其中：资本总市值 = 股票市值 + 总负债 + 优先股市值（如果有优先股），格雷厄姆标准：比例很高的是保守型，很低的是投机型，适中的是最优型'
		self.add_table_line(two_tds=[td0, td1], color=color, last_td=last_td)

		html_util.add_table_body_end()
		html_util.add_table_end()

		html_util.add_end()
		html_util.save_to_stock_file(stock=self.stock, fname='市场数据')
