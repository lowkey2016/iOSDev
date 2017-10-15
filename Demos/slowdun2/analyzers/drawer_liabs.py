# -*- coding: utf-8 -*-

from models.zcfzb import ZCFZB
from models.fjsj import FJSJ
from models.stock import Stock
from utils.util_stock import StockUtil
import utils.util_cons as Cons
from drawer_common import CommonDrawer

class LiabsDrawer(object):
	def __init__(self, stock):
		if stock is None:
			return
		self.stock = stock

		keys = [k for k in sorted(self.stock.zcfzbs)]
		keys.reverse()
		
		self.comdrawer = CommonDrawer(stock=stock, keys=keys)

	def draw(self):
		self.comdrawer.add_start(title='负债部分')

		# 标题部分
		self.comdrawer.add_title_and_table_head(
			title='资产负债表',
			caption='负债部分',
			two_ths=['项目', '所属分类'])

		# 一、融资性负债
		# 短期借款
		self.comdrawer.add_dividedval_table_line(
			two_tds=['短期借款', '融资性负债'],
			td_colors=[Cons.COLOR_RED, Cons.COLOR_RED],
			num_forms='zcfzbs',
			num_prop='shorttermborr',
			den_forms='zcfzbs',
			den_prop='totliab',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='',
			only_dividedval_column=False)

		# 长期借款
		self.comdrawer.add_dividedval_table_line(
			two_tds=['长期借款', '融资性负债'],
			td_colors=[Cons.COLOR_RED, Cons.COLOR_RED],
			num_forms='zcfzbs',
			num_prop='longborr',
			den_forms='zcfzbs',
			den_prop='totliab',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='',
			only_dividedval_column=False)

		# 应付短期债券
		self.comdrawer.add_dividedval_table_line(
			two_tds=['应付短期债券', '融资性负债'],
			td_colors=[Cons.COLOR_RED, Cons.COLOR_RED],
			num_forms='zcfzbs',
			num_prop='shorttermbdspaya',
			den_forms='zcfzbs',
			den_prop='totliab',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='',
			only_dividedval_column=False)

		# 应付债券
		self.comdrawer.add_dividedval_table_line(
			two_tds=['应付债券', '融资性负债'],
			td_colors=[Cons.COLOR_RED, Cons.COLOR_RED],
			num_forms='zcfzbs',
			num_prop='bdspaya',
			den_forms='zcfzbs',
			den_prop='totliab',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='',
			only_dividedval_column=False)

		# 合计
		self.comdrawer.add_dividedval_table_line(
			two_tds=['融资性负债合计', ''],
			td_colors=[Cons.COLOR_RED, Cons.COLOR_WHITE],
			num_forms='zcfzbs',
			num_prop='finliabtot',
			den_forms='zcfzbs',
			den_prop='totliab',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='',
			only_dividedval_column=False)

		# 二、经营性负债
		# 应付票据
		self.comdrawer.add_dividedval_table_line(
			two_tds=['应付票据', '经营性负债'],
			td_colors=[Cons.COLOR_PINK, Cons.COLOR_PINK],
			num_forms='zcfzbs',
			num_prop='notespaya',
			den_forms='zcfzbs',
			den_prop='totliab',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='',
			only_dividedval_column=False)

		# 应付账款
		self.comdrawer.add_dividedval_table_line(
			two_tds=['应付账款', '经营性负债'],
			td_colors=[Cons.COLOR_PINK, Cons.COLOR_PINK],
			num_forms='zcfzbs',
			num_prop='accopaya',
			den_forms='zcfzbs',
			den_prop='totliab',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='',
			only_dividedval_column=False)

		# 预收款项
		self.comdrawer.add_dividedval_table_line(
			two_tds=['预收款项', '经营性负债'],
			td_colors=[Cons.COLOR_PINK, Cons.COLOR_PINK],
			num_forms='zcfzbs',
			num_prop='advapaym',
			den_forms='zcfzbs',
			den_prop='totliab',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='',
			only_dividedval_column=False)

		# 应付职工薪酬
		self.comdrawer.add_dividedval_table_line(
			two_tds=['应付职工薪酬', '经营性负债'],
			td_colors=[Cons.COLOR_PINK, Cons.COLOR_PINK],
			num_forms='zcfzbs',
			num_prop='copeworkersal',
			den_forms='zcfzbs',
			den_prop='totliab',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='',
			only_dividedval_column=False)

		# 员工本年度薪酬总额
		self.comdrawer.html_util.add_table_body_td(td='员工本年度薪酬', color=Cons.COLOR_WHITE)
		self.comdrawer.html_util.add_table_body_td(td='', color=Cons.COLOR_WHITE)
		for k in self.comdrawer.keys:
			keypath = 'zcfzbs[%s].copeworkersal' % k
			copeworkersal_cur = StockUtil.numValueForKeyPath(stock=self.comdrawer.stock, keypath=keypath)
			#
			keypath = 'zcfzbs[%d].copeworkersal' % (int(k) - 1)
			copeworkersal_lst = StockUtil.numValueForKeyPath(stock=self.comdrawer.stock, keypath=keypath)
			#
			keypath = 'xjllbs[%s].payworkcash' % k
			payworkcash = StockUtil.numValueForKeyPath(stock=self.comdrawer.stock, keypath=keypath)
			#
			keypath = 'fjsjs[%s].emplyescnt' % k
			emplyescnt = StockUtil.numValueForKeyPath(stock=self.comdrawer.stock, keypath=keypath)
			#
			workersaltot = copeworkersal_cur - copeworkersal_lst + payworkcash
			#
			aveval = StockUtil.getDivideVal(num=workersaltot, den=emplyescnt, use_percent_format=False)
			#
			self.comdrawer.html_util.add_table_body_td_val(val=workersaltot, color=Cons.COLOR_WHITE, unit=Cons.Yi)
			self.comdrawer.html_util.add_table_body_td_val(val=aveval, color=Cons.COLOR_WHITE, unit='¥')
		self.comdrawer.html_util.add_table_body_td(td='先总额，后平均', color=Cons.COLOR_WHITE)
		self.comdrawer.html_util.add_table_body_tr_end()

		# 员工总数
		self.comdrawer.add_num_table_line(
			two_tds=['员工总数', ''],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			forms='fjsjs',
			prop='emplyescnt',
			unit='人',
			last_td='')

		# 应付利息
		self.comdrawer.add_dividedval_table_line(
			two_tds=['应付利息', '经营性负债'],
			td_colors=[Cons.COLOR_PINK, Cons.COLOR_PINK],
			num_forms='zcfzbs',
			num_prop='intepaya',
			den_forms='zcfzbs',
			den_prop='totliab',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='',
			only_dividedval_column=False)

		# 其他应付款
		self.comdrawer.add_dividedval_table_line(
			two_tds=['其他应付款', '经营性负债'],
			td_colors=[Cons.COLOR_PINK, Cons.COLOR_PINK],
			num_forms='zcfzbs',
			num_prop='otherpay',
			den_forms='zcfzbs',
			den_prop='totliab',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='',
			only_dividedval_column=False)

		# 长期应付款
		self.comdrawer.add_dividedval_table_line(
			two_tds=['长期应付款', '经营性负债'],
			td_colors=[Cons.COLOR_PINK, Cons.COLOR_PINK],
			num_forms='zcfzbs',
			num_prop='longpaya',
			den_forms='zcfzbs',
			den_prop='totliab',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='',
			only_dividedval_column=False)

		# 专项应付款
		self.comdrawer.add_dividedval_table_line(
			two_tds=['专项应付款', '经营性负债'],
			td_colors=[Cons.COLOR_PINK, Cons.COLOR_PINK],
			num_forms='zcfzbs',
			num_prop='specpaya',
			den_forms='zcfzbs',
			den_prop='totliab',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='',
			only_dividedval_column=False)

		# 合计
		self.comdrawer.add_dividedval_table_line(
			two_tds=['经营性负债合计', ''],
			td_colors=[Cons.COLOR_PINK, Cons.COLOR_WHITE],
			num_forms='zcfzbs',
			num_prop='manageliabtot',
			den_forms='zcfzbs',
			den_prop='totliab',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='',
			only_dividedval_column=False)

		# 应交税费
		self.comdrawer.add_dividedval_table_line(
			two_tds=['应交税费', '分配性负债'],
			td_colors=[Cons.COLOR_GREEN, Cons.COLOR_GREEN],
			num_forms='zcfzbs',
			num_prop='taxespaya',
			den_forms='zcfzbs',
			den_prop='totliab',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='',
			only_dividedval_column=False)

		# 应付股利
		self.comdrawer.add_dividedval_table_line(
			two_tds=['应付股利', '分配性负债'],
			td_colors=[Cons.COLOR_GREEN, Cons.COLOR_GREEN],
			num_forms='zcfzbs',
			num_prop='divipaya',
			den_forms='zcfzbs',
			den_prop='totliab',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='',
			only_dividedval_column=False)

		# 合计
		self.comdrawer.add_dividedval_table_line(
			two_tds=['分配性负债合计', ''],
			td_colors=[Cons.COLOR_GREEN, Cons.COLOR_WHITE],
			num_forms='zcfzbs',
			num_prop='payliabtot',
			den_forms='zcfzbs',
			den_prop='totliab',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='',
			only_dividedval_column=False)

		# 交易性金融负债
		self.comdrawer.add_dividedval_table_line(
			two_tds=['交易性金融负债', '其它负债'],
			td_colors=[Cons.COLOR_BLUE, Cons.COLOR_BLUE],
			num_forms='zcfzbs',
			num_prop='tradfinliab',
			den_forms='zcfzbs',
			den_prop='totliab',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='',
			only_dividedval_column=False)

		# 一年内到期的非流动负债
		self.comdrawer.add_dividedval_table_line(
			two_tds=['一年内到期的非流动负债', '其它负债'],
			td_colors=[Cons.COLOR_BLUE, Cons.COLOR_BLUE],
			num_forms='zcfzbs',
			num_prop='duenoncliab',
			den_forms='zcfzbs',
			den_prop='totliab',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='',
			only_dividedval_column=False)

		# 长期递延收益
		self.comdrawer.add_dividedval_table_line(
			two_tds=['长期递延收益', '其它负债'],
			td_colors=[Cons.COLOR_BLUE, Cons.COLOR_BLUE],
			num_forms='zcfzbs',
			num_prop='longdefeinco',
			den_forms='zcfzbs',
			den_prop='totliab',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='',
			only_dividedval_column=False)

		# 递延所得税负债
		self.comdrawer.add_dividedval_table_line(
			two_tds=['递延所得税负债', '其它负债'],
			td_colors=[Cons.COLOR_BLUE, Cons.COLOR_BLUE],
			num_forms='zcfzbs',
			num_prop='defeincotaxliab',
			den_forms='zcfzbs',
			den_prop='totliab',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='',
			only_dividedval_column=False)

		# 其他流动负债
		self.comdrawer.add_dividedval_table_line(
			two_tds=['其他流动负债', '其它负债'],
			td_colors=[Cons.COLOR_BLUE, Cons.COLOR_BLUE],
			num_forms='zcfzbs',
			num_prop='othercurreliabi',
			den_forms='zcfzbs',
			den_prop='totliab',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='',
			only_dividedval_column=False)

		# 其他非流动负债
		self.comdrawer.add_dividedval_table_line(
			two_tds=['其他非流动负债', '其它负债'],
			td_colors=[Cons.COLOR_BLUE, Cons.COLOR_BLUE],
			num_forms='zcfzbs',
			num_prop='othernoncliabi',
			den_forms='zcfzbs',
			den_prop='totliab',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='',
			only_dividedval_column=False)

		# 合计
		self.comdrawer.add_dividedval_table_line(
			two_tds=['其它负债合计', ''],
			td_colors=[Cons.COLOR_BLUE, Cons.COLOR_WHITE],
			num_forms='zcfzbs',
			num_prop='otherliabtot',
			den_forms='zcfzbs',
			den_prop='totliab',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='',
			only_dividedval_column=False)

		# 负债合计
		self.comdrawer.add_val_growrate_comprate_table_lines(
			two_tds=['总负债', ''],
			td_colors=[Cons.COLOR_PURPLE, Cons.COLOR_WHITE],
			num_forms='zcfzbs',
			num_prop='totliab',
			den_forms='zcfzbs',
			den_prop='totasset',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='')

		# 资产合计
		self.comdrawer.add_val_growrate_comprate_table_lines(
			two_tds=['总资产', ''],
			td_colors=[Cons.COLOR_PURPLE, Cons.COLOR_WHITE],
			num_forms='zcfzbs',
			num_prop='totasset',
			den_forms='zcfzbs',
			den_prop='totasset',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='')

		# 所有者权益(或股东权益)合计
		self.comdrawer.add_val_growrate_comprate_table_lines(
			two_tds=['所有者权益(或股东权益)合计', ''],
			td_colors=[Cons.COLOR_PURPLE, Cons.COLOR_WHITE],
			num_forms='zcfzbs',
			num_prop='righaggr',
			den_forms='zcfzbs',
			den_prop='totasset',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='')

		# 现金净流量与到期债务之比 = 经营现金净流量 / 本期到期的债务
		self.comdrawer.add_dividedval_table_line(
			two_tds=['现金净流量与到期债务之比', ''],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			num_forms='xjllbs',
			num_prop='mananetr',
			den_forms='zcfzbs',
			den_prop='duenoncliab',
			two_units=[None, None],
			last_td='现金净流量与到期债务之比 = 经营现金净流量 / 本期到期的债务',
			only_dividedval_column=True)

		# 现金净流量与流动负债之比 = 经营现金净流量 / 流动负债
		self.comdrawer.add_dividedval_table_line(
			two_tds=['现金净流量与流动负债之比', ''],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			num_forms='xjllbs',
			num_prop='mananetr',
			den_forms='zcfzbs',
			den_prop='totalcurrliab',
			two_units=[None, None],
			last_td='现金净流量与流动负债之比 = 经营现金净流量 / 流动负债',
			only_dividedval_column=True)

		# 现金净流量与债务总额之比 = 经营现金净流量 / 债务总额
		self.comdrawer.add_dividedval_table_line(
			two_tds=['现金净流量与债务总额之比', ''],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			num_forms='xjllbs',
			num_prop='mananetr',
			den_forms='zcfzbs',
			den_prop='totliab',
			two_units=[None, None],
			last_td='现金净流量与债务总额之比 = 经营现金净流量 / 债务总额',
			only_dividedval_column=True)

		self.comdrawer.add_table_end()

		### 有息负债明细 ###

		# 标题部分
		self.comdrawer.add_title_and_table_head(
			title='有息负债明细',
			caption='有息负债',
			two_ths=['项目', ''])

		# 短期借款明细
		self.comdrawer.add_str_table_line(
			two_tds=['短期借款明细', ''],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			forms='fjsjs',
			prop='shorttermborrdetail',
			last_td='')

		# 长期借款明细
		self.comdrawer.add_str_table_line(
			two_tds=['长期借款明细', ''],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			forms='fjsjs',
			prop='longborrdetail',
			last_td='')

		# 有息负债率 = 有息负债 / 总资产
		self.comdrawer.add_dividedval_table_line(
			two_tds=['有息负债率', ''],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			num_forms='zcfzbs',
			num_prop='borrtot',
			den_forms='zcfzbs',
			den_prop='totasset',
			two_units=[None, None],
			last_td='有息负债率 = 有息负债 / 总资产',
			only_dividedval_column=True)

		# 现金有息负债比率 = 现金及现金等价物余额 / 有息负债，现金及现金等价物余额指货币资金中使用不受限的钱
		self.comdrawer.html_util.add_table_body_td(td='现金有息负债比率', color=Cons.COLOR_WHITE)
		self.comdrawer.html_util.add_table_body_td(td='', color=Cons.COLOR_WHITE)
		for k in self.comdrawer.keys:
			keypath = 'zcfzbs[%s].curfds' % k
			curfds = StockUtil.numValueForKeyPath(stock=self.comdrawer.stock, keypath=keypath)
			#
			keypath = 'zcfzbs[%s].borrtot' % k
			borrtot = StockUtil.numValueForKeyPath(stock=self.comdrawer.stock, keypath=keypath)
			#
			keypath = 'fjsjs[%s].curfds_limit' % k
			curfds_limit = StockUtil.numValueForKeyPath(stock=self.comdrawer.stock, keypath=keypath)
			#
			rate = StockUtil.getDivideVal(num=(curfds - curfds_limit), den=borrtot, use_percent_format=False)
			#
			self.comdrawer.html_util.add_table_body_td_val(val=rate, color=Cons.COLOR_WHITE, unit=None)
			self.comdrawer.html_util.add_table_body_td_empty()
		self.comdrawer.html_util.add_table_body_td(td='现金有息负债比率 = 现金及现金等价物余额 / 有息负债，现金及现金等价物余额指货币资金中使用不受限的钱', color=Cons.COLOR_WHITE)
		self.comdrawer.html_util.add_table_body_tr_end()
		
		self.comdrawer.add_end_and_save_to_stock_file(fname='资产负债表负债部分')
