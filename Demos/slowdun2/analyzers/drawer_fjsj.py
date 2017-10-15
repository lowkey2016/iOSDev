# -*- coding: utf-8 -*-

from models.stock import Stock
from utils.util_stock import StockUtil
import utils.util_cons as Cons
from drawer_common import CommonDrawer

class FJSJDrawer(object):
	def __init__(self, stock):
		if stock is None:
			return
		self.stock = stock

		keys = [k for k in sorted(self.stock.zcfzbs)]
		keys.reverse()

		self.comdrawer = CommonDrawer(stock=stock, keys=keys)

	def draw(self):
		self.comdrawer.add_start(title='附加数据')

		# 标题部分
		self.comdrawer.html_util.add_title(title='附加数据')
		self.comdrawer.html_util.add_table_start(caption='附加')
		# 标题行
		self.comdrawer.html_util.add_table_head_start()
		self.comdrawer.html_util.add_table_head_th(th='项目', colspan=1, color=Cons.COLOR_WHITE)
		for k in self.comdrawer.keys:
			self.comdrawer.html_util.add_table_head_th(th=k, colspan=1)
		self.comdrawer.html_util.add_table_head_th_recommend()
		self.comdrawer.html_util.add_table_head_end()
		# 内容部分
		self.comdrawer.html_util.add_table_body_start()
		self.comdrawer.html_util.add_table_body_tr_start()

		# 财报意见
		self.comdrawer.html_util.add_table_body_td(td='财报意见', color=Cons.COLOR_WHITE)
		for k in self.comdrawer.keys:
			keypath = 'fjsjs[%s].finstmtcomments' % k
			val = StockUtil.strValueForKeyPath(stock=self.comdrawer.stock, keypath=keypath)
			self.comdrawer.html_util.add_table_body_td(td=val, color=Cons.COLOR_WHITE)
		self.comdrawer.html_util.add_table_body_td(td='', color=Cons.COLOR_WHITE)
		self.comdrawer.html_util.add_table_body_tr_end()

		# 董事会在财报中提出的注意事项
		self.comdrawer.html_util.add_table_body_td(td='董事会在财报中提出的注意事项', color=Cons.COLOR_WHITE)
		for k in self.comdrawer.keys:
			keypath = 'fjsjs[%s].finstmtspecials' % k
			val = StockUtil.strValueForKeyPath(stock=self.comdrawer.stock, keypath=keypath)
			self.comdrawer.html_util.add_table_body_td(td=val, color=Cons.COLOR_WHITE)
		self.comdrawer.html_util.add_table_body_td(td='', color=Cons.COLOR_WHITE)
		self.comdrawer.html_util.add_table_body_tr_end()

		# 股份总数
		self.comdrawer.html_util.add_table_body_td(td='股份总数', color=Cons.COLOR_WHITE)
		for k in self.comdrawer.keys:
			keypath = 'fjsjs[%s].sharecount' % k
			val = StockUtil.numValueForKeyPath(stock=self.comdrawer.stock, keypath=keypath) / 10000
			td = '%.4f 万股' % val
			self.comdrawer.html_util.add_table_body_td(td=td, color=Cons.COLOR_WHITE)
		self.comdrawer.html_util.add_table_body_td(td='', color=Cons.COLOR_WHITE)
		self.comdrawer.html_util.add_table_body_tr_end()
		
		self.comdrawer.add_table_end()
		self.comdrawer.add_end_and_save_to_stock_file(fname='附加数据')
