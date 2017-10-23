# -*- coding: utf-8 -*-

import os
from models.zcfzb import ZCFZB
from models.gslrb import GSLRB
from models.xjllb import XJLLB
from models.fjsj import FJSJ
from models.stock import Stock
from utils.util_res import ResUtil
import utils.util_cons as Cons
from drawer_assets import AssetsDrawer
from drawer_liabs import LiabsDrawer
from drawer_profit import ProfitDrawer
from drawer_cash import CashDrawer
from drawer_cash_in import CashInDrawer
from drawer_fjsj import FJSJDrawer
from drawer_group import GroupDrawer

class AnlzMgr(object):
	def __init__(self, stock):
		if stock is None:
			return
		self.stock = stock

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

		self.assetsDrawer = AssetsDrawer(stock=stock)
		self.liabsDrawer = LiabsDrawer(stock=stock)
		self.profitDrawer = ProfitDrawer(stock=stock)
		self.cashDrawer = CashDrawer(stock=stock)
		self.cashinDrawer = CashInDrawer(stock=stock)
		self.fjsjDrawer = FJSJDrawer(stock=stock)

	def draw(self):
		self.assetsDrawer.draw()
		self.liabsDrawer.draw()
		self.profitDrawer.draw()
		self.cashDrawer.draw()
		self.cashinDrawer.draw()
		self.fjsjDrawer.draw()

	@classmethod
	def draw_jiadian_chudians(self):
		group = []

		stk = Stock(symbol='SZ002032', name='苏泊尔', year_from = 2010)
		anlz_mgr = AnlzMgr(stock=stk)
		anlz_mgr.draw()
		group.append(stk)

		stk = Stock(symbol='SZ002035', name='华帝股份', year_from = 2010)
		anlz_mgr = AnlzMgr(stock=stk)
		anlz_mgr.draw()
		group.append(stk)

		stk = Stock(symbol='SZ002242', name='九阳股份', year_from = 2010)
		anlz_mgr = AnlzMgr(stock=stk)
		anlz_mgr.draw()
		group.append(stk)

		stk = Stock(symbol='SZ002403', name='爱仕达', year_from = 2010)
		anlz_mgr = AnlzMgr(stock=stk)
		anlz_mgr.draw()
		group.append(stk)

		stk = Stock(symbol='SZ002508', name='老板电器', year_from = 2010)
		anlz_mgr = AnlzMgr(stock=stk)
		anlz_mgr.draw()
		group.append(stk)
		target = stk

		stk = Stock(symbol='SZ002543', name='万和电气', year_from = 2010)
		anlz_mgr = AnlzMgr(stock=stk)
		anlz_mgr.draw()
		group.append(stk)

		stk = Stock(symbol='SZ002677', name='浙江美大', year_from = 2010)
		anlz_mgr = AnlzMgr(stock=stk)
		anlz_mgr.draw()
		group.append(stk)

		gdrawer = GroupDrawer(industry=Cons.INDUSTRY_ELETRIC_KITCHEN, stocks_group=group, target=target)
		gdrawer.draw()

	@classmethod
	def draw_fangdichan_ppp(self):
		group = []
		
		stk = Stock(symbol='SH600340', name='华夏幸福', year_from = 2011)
		anlz_mgr = AnlzMgr(stock=stk)
		anlz_mgr.draw()
		group.append(stk)

	@classmethod
	def draw_others(self):
		group = []
		
		stk = Stock(symbol='SH600298', name='安琪酵母', year_from = 2007)
		anlz_mgr = AnlzMgr(stock=stk)
		anlz_mgr.draw()
		group.append(stk)
	