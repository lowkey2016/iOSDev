# -*- coding: utf-8 -*-

from models.zcfzb import ZCFZB
from models.fjsj import FJSJ
from models.stock import Stock
from utils.util_stock import StockUtil
import utils.util_cons as Cons
from drawer_common import CommonDrawer

class AssetsDrawer(object):
	def __init__(self, stock):
		if stock is None:
			return
		self.stock = stock

		keys = [k for k in sorted(self.stock.zcfzbs)]
		keys.reverse()
		
		self.comdrawer = CommonDrawer(stock=stock, keys=keys)

	def draw(self):
		self.comdrawer.add_start(title='资产部分')

		# 标题部分
		self.comdrawer.add_title_and_table_head(
			title='资产负债表',
			caption='资产部分',
			two_ths=['项目', '所属分类'])

		## 一、货币资金类资产
		# 货币资金
		self.comdrawer.add_val_growrate_comprate_table_lines(
			two_tds=['货币资金', '货币资金'],
			td_colors=[Cons.COLOR_GREEN, Cons.COLOR_GREEN],
			num_forms='zcfzbs',
			num_prop='curfds',
			den_forms='zcfzbs',
			den_prop='totasset',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='')

		# 货币资金中的库存现金
		self.comdrawer.add_dividedval_table_line(
			two_tds=['其中：库存现金', ''],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			num_forms='fjsjs',
			num_prop='curfds_cash',
			den_forms='zcfzbs',
			den_prop='curfds',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以货币资金')

		# 货币资金中的银行存款
		self.comdrawer.add_dividedval_table_line(
			two_tds=['其中：银行存款', ''],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			num_forms='fjsjs',
			num_prop='curfds_bank',
			den_forms='zcfzbs',
			den_prop='curfds',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以货币资金')

		# 货币资金中的其他货币资金
		self.comdrawer.add_dividedval_table_line(
			two_tds=['其中：其他货币资金', ''],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			num_forms='fjsjs',
			num_prop='curfds_other',
			den_forms='zcfzbs',
			den_prop='curfds',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以货币资金')

		# 货币资金中的使用受限资金
		self.comdrawer.add_dividedval_table_line(
			two_tds=['其中：使用受限资金', ''],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			num_forms='fjsjs',
			num_prop='curfds_limit',
			den_forms='zcfzbs',
			den_prop='curfds',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以货币资金')

		# 合计
		self.comdrawer.add_dividedval_table_line(
			two_tds=['货币资金合计', ''],
			td_colors=[Cons.COLOR_GREEN, Cons.COLOR_WHITE],
			num_forms='zcfzbs',
			num_prop='curfds',
			den_forms='zcfzbs',
			den_prop='totasset',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='')

		## 二、经营相关资产
		# 应收票据
		self.comdrawer.add_val_growrate_comprate_table_lines(
			two_tds=['应收票据', '经营相关资产'],
			td_colors=[Cons.COLOR_RED, Cons.COLOR_RED],
			num_forms='zcfzbs',
			num_prop='notesrece',
			den_forms='zcfzbs',
			den_prop='totasset',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='')

		# 应收票据中的银行承兑汇票
		self.comdrawer.add_dividedval_table_line(
			two_tds=['其中：银行承兑汇票', ''],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			num_forms='fjsjs',
			num_prop='notesrece_bank',
			den_forms='zcfzbs',
			den_prop='notesrece',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以应收票据')

		# 应收票据中的商业承兑汇票
		self.comdrawer.add_dividedval_table_line(
			two_tds=['其中：商业承兑汇票', ''],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			num_forms='fjsjs',
			num_prop='notesrece_business',
			den_forms='zcfzbs',
			den_prop='notesrece',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以应收票据')

		# 应收票据中的其它部分
		self.comdrawer.add_dividedval_table_line(
			two_tds=['其中：其它部分', ''],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			num_forms='fjsjs',
			num_prop='notesrece_other',
			den_forms='zcfzbs',
			den_prop='notesrece',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以应收票据')

		# 应收账款
		self.comdrawer.add_val_growrate_comprate_table_lines(
			two_tds=['应收账款', '经营相关资产'],
			td_colors=[Cons.COLOR_RED, Cons.COLOR_RED],
			num_forms='zcfzbs',
			num_prop='accorece',
			den_forms='zcfzbs',
			den_prop='totasset',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='')

		# 应收账款周转率 = 营业收入 / 平均应收账款，其中：平均应收账款 = (期初应收账款总额 + 期末应收账款总额) / 2
		self.comdrawer.add_weightedave_dividedval_table_line(
			two_tds=['应收账款周转率', ''],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			num_forms='gslrbs',
			num_prop='bizinco',
			den_forms='zcfzbs',
			den_prop='accorece',
			two_units=[None, None],
			last_td='应收账款周转率 = 营业收入 / 平均应收账款，其中：平均应收账款 = (期初应收账款总额 + 期末应收账款总额) / 2')

		# 相当于多少个月的营业收入
		self.comdrawer.add_dividedval_table_line(
			two_tds=['相当于多少个月的营业收入', ''],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			num_forms='zcfzbs',
			num_prop='accorece',
			den_forms='gslrbs',
			den_prop='bizincopermonth',
			two_units=[None, None],
			last_td='',
			only_dividedval_column=True)

		# 按信用风险特征组合计坏账准备的应收账款
		self.comdrawer.add_dividedval_table_line(
			two_tds=['其中：按信用风险特征组合计坏账准备的', ''],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			num_forms='fjsjs',
			num_prop='accorece_credit_tot',
			den_forms='fjsjs',
			den_prop='accorecetot',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='')
		# 按信用风险特征组合计坏账准备的应收账款坏账准备
		self.comdrawer.add_dividedval_table_line(
			two_tds=['坏账准备', ''],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			num_forms='fjsjs',
			num_prop='accorece_credit_bad',
			den_forms='fjsjs',
			den_prop='accorece_credit_tot',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以按信用风险特征组合计坏账准备的应收账款')

		# 单项金额不重大但单独计坏账准备的应收账款
		self.comdrawer.add_dividedval_table_line(
			two_tds=['其中：单项金额不重大但单独计坏账准备的', ''],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			num_forms='fjsjs',
			num_prop='accorece_single_tot',
			den_forms='fjsjs',
			den_prop='accorecetot',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='')
		# 单项金额不重大但单独计坏账准备的应收账款坏账准备
		self.comdrawer.add_dividedval_table_line(
			two_tds=['坏账准备', ''],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			num_forms='fjsjs',
			num_prop='accorece_single_bad',
			den_forms='fjsjs',
			den_prop='accorece_single_tot',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以单项金额不重大但单独计坏账准备的应收账款')

		# 单项金额重大并单项计坏账准备的应收账款
		self.comdrawer.add_dividedval_table_line(
			two_tds=['其中：单项金额重大并单项计坏账准备的', ''],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			num_forms='fjsjs',
			num_prop='accorece_single_imp_tot',
			den_forms='fjsjs',
			den_prop='accorecetot',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='')
		# 单项金额重大并单项计坏账准备的应收账款坏账准备
		self.comdrawer.add_dividedval_table_line(
			two_tds=['坏账准备', ''],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			num_forms='fjsjs',
			num_prop='accorece_single_imp_bad',
			den_forms='fjsjs',
			den_prop='accorece_single_imp_tot',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以单项金额重大并单项计坏账准备的应收账款')

		# 账龄小于1年的应收账款
		self.comdrawer.add_dividedval_table_line(
			two_tds=['其中：账龄小于1年的', ''],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			num_forms='fjsjs',
			num_prop='accorece_0_1_tot',
			den_forms='fjsjs',
			den_prop='accorece_credit_tot',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='')
		# 账龄小于1年的应收账款坏账准备
		self.comdrawer.add_dividedval_table_line(
			two_tds=['坏账准备', ''],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			num_forms='fjsjs',
			num_prop='accorece_0_1_bad',
			den_forms='fjsjs',
			den_prop='accorece_0_1_tot',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以账龄小于1年的应收账款')

		# 账龄1-2年的应收账款
		self.comdrawer.add_dividedval_table_line(
			two_tds=['其中：账龄1-2年的', ''],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			num_forms='fjsjs',
			num_prop='accorece_1_2_tot',
			den_forms='fjsjs',
			den_prop='accorece_credit_tot',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='')
		# 账龄1-2年的应收账款坏账准备
		self.comdrawer.add_dividedval_table_line(
			two_tds=['坏账准备', ''],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			num_forms='fjsjs',
			num_prop='accorece_1_2_bad',
			den_forms='fjsjs',
			den_prop='accorece_1_2_tot',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以账龄1-2年的应收账款')

		# 账龄2-3年的应收账款
		self.comdrawer.add_dividedval_table_line(
			two_tds=['其中：账龄2-3年的', ''],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			num_forms='fjsjs',
			num_prop='accorece_2_3_tot',
			den_forms='fjsjs',
			den_prop='accorece_credit_tot',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='')
		# 账龄2-3年的应收账款坏账准备
		self.comdrawer.add_dividedval_table_line(
			two_tds=['坏账准备', ''],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			num_forms='fjsjs',
			num_prop='accorece_2_3_bad',
			den_forms='fjsjs',
			den_prop='accorece_2_3_tot',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以账龄2-3年的应收账款')

		# 账龄3-4年的应收账款
		self.comdrawer.add_dividedval_table_line(
			two_tds=['其中：账龄3-4年的', ''],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			num_forms='fjsjs',
			num_prop='accorece_3_4_tot',
			den_forms='fjsjs',
			den_prop='accorece_credit_tot',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='')
		# 账龄3-4年的应收账款坏账准备
		self.comdrawer.add_dividedval_table_line(
			two_tds=['坏账准备', ''],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			num_forms='fjsjs',
			num_prop='accorece_3_4_bad',
			den_forms='fjsjs',
			den_prop='accorece_3_4_tot',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以账龄3-4年的应收账款')

		# 账龄4-5年的应收账款
		self.comdrawer.add_dividedval_table_line(
			two_tds=['其中：账龄4-5年的', ''],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			num_forms='fjsjs',
			num_prop='accorece_4_5_tot',
			den_forms='fjsjs',
			den_prop='accorece_credit_tot',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='')
		# 账龄4-5年的应收账款坏账准备
		self.comdrawer.add_dividedval_table_line(
			two_tds=['坏账准备', ''],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			num_forms='fjsjs',
			num_prop='accorece_4_5_bad',
			den_forms='fjsjs',
			den_prop='accorece_4_5_tot',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以账龄4-5年的应收账款')

		# 账龄大于5年的应收账款
		self.comdrawer.add_dividedval_table_line(
			two_tds=['其中：账龄大于5年的', ''],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			num_forms='fjsjs',
			num_prop='accorece_5_n_tot',
			den_forms='fjsjs',
			den_prop='accorece_credit_tot',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='')
		# 账龄大于5年的应收账款坏账准备
		self.comdrawer.add_dividedval_table_line(
			two_tds=['坏账准备', ''],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			num_forms='fjsjs',
			num_prop='accorece_5_n_bad',
			den_forms='fjsjs',
			den_prop='accorece_5_n_tot',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以账龄大于5年的应收账款')

		# 应收账款的坏账计提标准
		self.comdrawer.add_str_table_line(
			two_tds=['坏账计提标准', ''],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			forms='fjsjs',
			prop='accorece_bad_standard',
			last_td='')

		# 预付款项
		self.comdrawer.add_val_growrate_comprate_table_lines(
			two_tds=['预付款项', '经营相关资产'],
			td_colors=[Cons.COLOR_RED, Cons.COLOR_RED],
			num_forms='zcfzbs',
			num_prop='prep',
			den_forms='zcfzbs',
			den_prop='totasset',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='')

    	# 1年内的预付款项
		self.comdrawer.add_dividedval_table_line(
    		two_tds=['其中：1年内的', ''],
    		td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
    		num_forms='fjsjs',
    		num_prop='prep_0_1',
    		den_forms='zcfzbs',
    		den_prop='prep',
    		two_units=[Cons.Yi, Cons.Percent],
    		last_td='除以预付款项')
		# 1年以上的预付款项
		self.comdrawer.add_dividedval_table_line(
			two_tds=['其中：1年以上的', ''],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			num_forms='fjsjs',
			num_prop='prep_1_n',
			den_forms='zcfzbs',
			den_prop='prep',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以预付款项')

		# 预付款项 / 营业收入
		self.comdrawer.add_dividedval_table_line(
			two_tds=['预付款项 / 营业收入', ''],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			num_forms='zcfzbs',
			num_prop='prep',
			den_forms='gslrbs',
			den_prop='bizinco',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以营业收入')

		# 预付款项 / 营业成本
		self.comdrawer.add_dividedval_table_line(
			two_tds=['预付款项 / 营业成本', ''],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			num_forms='zcfzbs',
			num_prop='prep',
			den_forms='gslrbs',
			den_prop='bizcost',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以营业成本')

		# 应收利息
		self.comdrawer.add_dividedval_table_line(
			two_tds=['应收利息', '经营相关资产'],
			td_colors=[Cons.COLOR_RED, Cons.COLOR_RED],
			num_forms='zcfzbs',
			num_prop='interece',
			den_forms='zcfzbs',
			den_prop='totasset',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='')

		# 应收股利
		self.comdrawer.add_dividedval_table_line(
			two_tds=['应收股利', '经营相关资产'],
			td_colors=[Cons.COLOR_RED, Cons.COLOR_RED],
			num_forms='zcfzbs',
			num_prop='dividrece',
			den_forms='zcfzbs',
			den_prop='totasset',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='')

		# 长期应收款
		self.comdrawer.add_dividedval_table_line(
			two_tds=['长期应收款', '经营相关资产'],
			td_colors=[Cons.COLOR_RED, Cons.COLOR_RED],
			num_forms='zcfzbs',
			num_prop='longrece',
			den_forms='zcfzbs',
			den_prop='totasset',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='')

		# 其他应收款
		self.comdrawer.add_dividedval_table_line(
			two_tds=['其他应收款', '经营相关资产'],
			td_colors=[Cons.COLOR_RED, Cons.COLOR_RED],
			num_forms='zcfzbs',
			num_prop='otherrece',
			den_forms='zcfzbs',
			den_prop='totasset',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='')

		# 存货
		self.comdrawer.add_val_growrate_comprate_table_lines(
			two_tds=['存货', '经营相关资产'],
			td_colors=[Cons.COLOR_RED, Cons.COLOR_RED],
			num_forms='zcfzbs',
			num_prop='inve',
			den_forms='zcfzbs',
			den_prop='totasset',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='')

		# 存货周转率 = 营业成本 / 存货平均余额，其中：存货平均余额 = (期初存货总额 + 期末存货总额) / 2
		self.comdrawer.add_weightedave_dividedval_table_line(
			two_tds=['存货周转率', ''],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			num_forms='gslrbs',
			num_prop='bizcost',
			den_forms='zcfzbs',
			den_prop='inve',
			two_units=[None, None],
			last_td='存货周转率 = 营业成本 / 存货平均余额，其中：存货平均余额 = (期初存货总额 + 期末存货总额) / 2')

		# 存货 / 营业成本
		self.comdrawer.add_dividedval_table_line(
			two_tds=['存货 / 营业成本', ''],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			num_forms='zcfzbs',
			num_prop='inve',
			den_forms='gslrbs',
			den_prop='bizcost',
			two_units=[Cons.Percent, None],
			last_td='除以营业成本',
			only_dividedval_column=True)

		# 净利润 / 存货
		self.comdrawer.add_dividedval_table_line(
			two_tds=['净利润 / 存货', ''],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			num_forms='gslrbs',
			num_prop='netprofit',
			den_forms='zcfzbs',
			den_prop='inve',
			two_units=[None, None],
			last_td='',
			only_dividedval_column=True,
			dividedval_color_map_func=Cons.valover1_color_map_func)

		# 存货跌价计提标准
		self.comdrawer.add_str_table_line(
			two_tds=['存货跌价计提标准', ''],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			forms='fjsjs',
			prop='inverevvallossstandard',
			last_td='')

		# 存货跌价计提总额
		self.comdrawer.add_dividedval_table_line(
			two_tds=['存货跌价计提总额', ''],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			num_forms='fjsjs',
			num_prop='inverevvallosstot',
			den_forms='zcfzbs',
			den_prop='inve',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以存货')

		# 存货的成本计价方法
		self.comdrawer.add_str_table_line(
			two_tds=['存货的成本计价方法', ''],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			forms='fjsjs',
			prop='inveincal',
			last_td='')

		# 存货的发出计价方法
		self.comdrawer.add_str_table_line(
			two_tds=['存货的发出计价方法', ''],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			forms='fjsjs',
			prop='inveoutcal',
			last_td='')

		# 存货产量
		inve_unit = StockUtil.get_inve_unit_from_stock(stock=self.comdrawer.stock)
		self.comdrawer.add_val_growrate_comprate_table_lines(
			two_tds=['存货产量', '经营相关资产'],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			num_forms='fjsjs',
			num_prop='inve_prod',
			den_forms='fjsjs',
			den_prop='inve_prodsalesave',
			two_units=[inve_unit, Cons.Percent],
			last_td='除以产销存之和')

		# 存货销量
		self.comdrawer.add_val_growrate_comprate_table_lines(
			two_tds=['存货销量', '经营相关资产'],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			num_forms='fjsjs',
			num_prop='inve_sale',
			den_forms='fjsjs',
			den_prop='inve_prodsalesave',
			two_units=[inve_unit, Cons.Percent],
			last_td='除以产销存之和')

		# 销产比
		self.comdrawer.add_dividedval_table_line(
			two_tds=['销产比', ''],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			num_forms='fjsjs',
			num_prop='inve_sale',
			den_forms='fjsjs',
			den_prop='inve_prod',
			two_units=[None, None],
			last_td='除以存货产量',
			only_dividedval_column=True)

		# 销产存比
		self.comdrawer.add_dividedval_table_line(
			two_tds=['销产存比', ''],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			num_forms='fjsjs',
			num_prop='inve_sale',
			den_forms='fjsjs',
			den_prop='inve_prodandsave',
			two_units=[None, None],
			last_td='除以存货产量和存量之和',
			only_dividedval_column=True)

		# 存货存量
		self.comdrawer.add_val_growrate_comprate_table_lines(
			two_tds=['存货存量', '经营相关资产'],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			num_forms='fjsjs',
			num_prop='inve_save',
			den_forms='fjsjs',
			den_prop='inve_prodsalesave',
			two_units=[inve_unit, Cons.Percent],
			last_td='除以产销存之和')

		# 应收款合计
		self.comdrawer.add_val_growrate_comprate_table_lines(
			two_tds=['应收款合计', '经营相关资产'],
			td_colors=[Cons.COLOR_RED, Cons.COLOR_RED],
			num_forms='zcfzbs',
			num_prop='rectot',
			den_forms='zcfzbs',
			den_prop='totasset',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='')
		# 相当于多少个月的营业收入
		self.comdrawer.add_dividedval_table_line(
			two_tds=['相当于多少个月的营业收入', ''],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			num_forms='zcfzbs',
			num_prop='rectot',
			den_forms='gslrbs',
			den_prop='bizincopermonth',
			two_units=[None, None],
			last_td='',
			only_dividedval_column=True)

		# 合计
		self.comdrawer.add_dividedval_table_line(
			two_tds=['经营相关资产合计', ''],
			td_colors=[Cons.COLOR_RED, Cons.COLOR_WHITE],
			num_forms='zcfzbs',
			num_prop='manageassetot',
			den_forms='zcfzbs',
			den_prop='totasset',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='')

		# 三、投资相关资产
		# 交易性金融资产
		self.comdrawer.add_dividedval_table_line(
			two_tds=['交易性金融资产', '投资相关资产'],
			td_colors=[Cons.COLOR_PINK, Cons.COLOR_PINK],
			num_forms='zcfzbs',
			num_prop='tradfinasset',
			den_forms='zcfzbs',
			den_prop='totasset',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='')

		# 可供出售金融资产
		self.comdrawer.add_dividedval_table_line(
			two_tds=['可供出售金融资产', '投资相关资产'],
			td_colors=[Cons.COLOR_PINK, Cons.COLOR_PINK],
			num_forms='zcfzbs',
			num_prop='avaisellasse',
			den_forms='zcfzbs',
			den_prop='totasset',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='')

		# 可供出售金融资产的期末账面余额和买入成本
		self.comdrawer.add_2nums_table_line(
			two_tds=['期末账面余额和买入成本', ''],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			two_forms=['fjsjs', 'fjsjs'],
			two_props=['avaisellassecur', 'avaisellassecost'],
			two_units=[Cons.Yi, None],
			last_td='先账面余额，后买入成本')

		# 持有至到期投资
		self.comdrawer.add_dividedval_table_line(
			two_tds=['持有至到期投资', '投资相关资产'],
			td_colors=[Cons.COLOR_PINK, Cons.COLOR_PINK],
			num_forms='zcfzbs',
			num_prop='holdinvedue',
			den_forms='zcfzbs',
			den_prop='totasset',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='')

		# 持有至到期投资的实际利率
		self.comdrawer.add_num_table_line(
			two_tds=['持有至到期投资的实际利率', ''],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			forms='fjsjs',
			prop='holdinvedue_inrate',
			unit=Cons.Percent,
			last_td='')

		# 持有至到期投资的减值数额
		self.comdrawer.add_dividedval_table_line(
			two_tds=['持有至到期投资的减值数额', ''],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			num_forms='fjsjs',
			num_prop='holdinvedue_losscur',
			den_forms='zcfzbs',
			den_prop='totasset',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='')

		# 持有至到期投资的减值转回数额
		self.comdrawer.add_dividedval_table_line(
			two_tds=['持有至到期投资的减值转回数额', ''],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			num_forms='fjsjs',
			num_prop='holdinvedue_lossback',
			den_forms='gslrbs',
			den_prop='biztotinco',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以营业总收入')

		# 长期股权投资
		self.comdrawer.add_dividedval_table_line(
			two_tds=['长期股权投资', '投资相关资产'],
			td_colors=[Cons.COLOR_PINK, Cons.COLOR_PINK],
			num_forms='zcfzbs',
			num_prop='equiinve',
			den_forms='zcfzbs',
			den_prop='totasset',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='')

		# 其他长期投资
		self.comdrawer.add_dividedval_table_line(
			two_tds=['其他长期投资', '投资相关资产'],
			td_colors=[Cons.COLOR_PINK, Cons.COLOR_PINK],
			num_forms='zcfzbs',
			num_prop='otherlonginve',
			den_forms='zcfzbs',
			den_prop='totasset',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='')

		# 投资性房地产
		self.comdrawer.add_dividedval_table_line(
			two_tds=['投资性房地产', '投资相关资产'],
			td_colors=[Cons.COLOR_PINK, Cons.COLOR_PINK],
			num_forms='zcfzbs',
			num_prop='inveprop',
			den_forms='zcfzbs',
			den_prop='totasset',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='')

		# 投资性房地产的计量模式
		self.comdrawer.add_str_table_line(
			two_tds=['投资性房地产的计量模式', ''],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			forms='fjsjs',
			prop='invepropcal',
			last_td='')

		# 合计
		self.comdrawer.add_dividedval_table_line(
			two_tds=['投资性房地产合计', ''],
			td_colors=[Cons.COLOR_PINK, Cons.COLOR_WHITE],
			num_forms='zcfzbs',
			num_prop='inveassetot',
			den_forms='zcfzbs',
			den_prop='totasset',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='')

		# 四、生产相关资产
		# 固定资产原值
		self.comdrawer.add_dividedval_table_line(
			two_tds=['固定资产原值', '生产相关资产'],
			td_colors=[Cons.COLOR_YELLOW, Cons.COLOR_YELLOW],
			num_forms='zcfzbs',
			num_prop='fixedasseimmo',
			den_forms='zcfzbs',
			den_prop='totasset',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='')

		# 累计折旧
		self.comdrawer.add_dividedval_table_line(
			two_tds=['累计折旧', ''],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			num_forms='zcfzbs',
			num_prop='accudepr',
			den_forms='zcfzbs',
			den_prop='fixedasseimmo',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以固定资产原值')

		# 固定资产净值
		self.comdrawer.add_dividedval_table_line(
			two_tds=['固定资产净值', '生产相关资产'],
			td_colors=[Cons.COLOR_YELLOW, Cons.COLOR_YELLOW],
			num_forms='zcfzbs',
			num_prop='fixedassenetw',
			den_forms='zcfzbs',
			den_prop='totasset',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='')

		# 固定资产减值准备
		self.comdrawer.add_dividedval_table_line(
			two_tds=['固定资产减值准备', ''],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			num_forms='zcfzbs',
			num_prop='fixedasseimpa',
			den_forms='zcfzbs',
			den_prop='fixedasseimmo',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以固定资产原值')

		# 固定资产净额
		self.comdrawer.add_dividedval_table_line(
			two_tds=['固定资产净额', '生产相关资产'],
			td_colors=[Cons.COLOR_YELLOW, Cons.COLOR_YELLOW],
			num_forms='zcfzbs',
			num_prop='fixedassenet',
			den_forms='zcfzbs',
			den_prop='totasset',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='')

		# 固定资产周转率 = 营业收入 / 平均固定资产净额
		self.comdrawer.add_weightedave_dividedval_table_line(
			two_tds=['固定资产周转率', ''],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			num_forms='gslrbs',
			num_prop='bizinco',
			den_forms='zcfzbs',
			den_prop='fixedassenet',
			two_units=[None, None],
			last_td='固定资产周转率 = 营业收入 / 平均固定资产净额')

		# 固定资产的折旧政策
		self.comdrawer.add_str_table_line(
			two_tds=['固定资产的折旧政策', ''],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			forms='fjsjs',
			prop='fixedassedepolicy',
			last_td='')

		# 在建工程
		self.comdrawer.add_dividedval_table_line(
			two_tds=['在建工程', '生产相关资产'],
			td_colors=[Cons.COLOR_YELLOW, Cons.COLOR_YELLOW],
			num_forms='zcfzbs',
			num_prop='consprog',
			den_forms='zcfzbs',
			den_prop='totasset',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='')

		# 工程物资
		self.comdrawer.add_dividedval_table_line(
			two_tds=['工程物资', '生产相关资产'],
			td_colors=[Cons.COLOR_YELLOW, Cons.COLOR_YELLOW],
			num_forms='zcfzbs',
			num_prop='engimate',
			den_forms='zcfzbs',
			den_prop='totasset',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='')

		# 生产性生物资产
		self.comdrawer.add_dividedval_table_line(
			two_tds=['生产性生物资产', '生产相关资产'],
			td_colors=[Cons.COLOR_YELLOW, Cons.COLOR_YELLOW],
			num_forms='zcfzbs',
			num_prop='prodasse',
			den_forms='zcfzbs',
			den_prop='totasset',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='')

		# 公益性生物资产
		self.comdrawer.add_dividedval_table_line(
			two_tds=['公益性生物资产', '生产相关资产'],
			td_colors=[Cons.COLOR_YELLOW, Cons.COLOR_YELLOW],
			num_forms='zcfzbs',
			num_prop='comasse',
			den_forms='zcfzbs',
			den_prop='totasset',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='')

		# 油气资产
		self.comdrawer.add_dividedval_table_line(
			two_tds=['油气资产', '生产相关资产'],
			td_colors=[Cons.COLOR_YELLOW, Cons.COLOR_YELLOW],
			num_forms='zcfzbs',
			num_prop='hydrasset',
			den_forms='zcfzbs',
			den_prop='totasset',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='')

		# 无形资产
		self.comdrawer.add_dividedval_table_line(
			two_tds=['无形资产', '生产相关资产'],
			td_colors=[Cons.COLOR_YELLOW, Cons.COLOR_YELLOW],
			num_forms='zcfzbs',
			num_prop='intaasset',
			den_forms='zcfzbs',
			den_prop='totasset',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='')

		# 无形资产的摊销政策
		self.comdrawer.add_str_table_line(
			two_tds=['无形资产的摊销政策', ''],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			forms='fjsjs',
			prop='intaassetdmopolicy',
			last_td='')

		# 开发支出
		self.comdrawer.add_dividedval_table_line(
			two_tds=['开发支出', '生产相关资产'],
			td_colors=[Cons.COLOR_YELLOW, Cons.COLOR_YELLOW],
			num_forms='zcfzbs',
			num_prop='deveexpe',
			den_forms='zcfzbs',
			den_prop='totasset',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='')

		# 商誉
		self.comdrawer.add_dividedval_table_line(
			two_tds=['商誉', '生产相关资产'],
			td_colors=[Cons.COLOR_YELLOW, Cons.COLOR_YELLOW],
			num_forms='zcfzbs',
			num_prop='goodwill',
			den_forms='zcfzbs',
			den_prop='totasset',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='')

		# 待摊费用
		self.comdrawer.add_val_growrate_comprate_table_lines(
			two_tds=['待摊费用', '生产相关资产'],
			td_colors=[Cons.COLOR_YELLOW, Cons.COLOR_YELLOW],
			num_forms='zcfzbs',
			num_prop='prepexpe',
			den_forms='zcfzbs',
			den_prop='totasset',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='')

		# 长期待摊费用
		self.comdrawer.add_val_growrate_comprate_table_lines(
			two_tds=['长期待摊费用', '生产相关资产'],
			td_colors=[Cons.COLOR_YELLOW, Cons.COLOR_YELLOW],
			num_forms='zcfzbs',
			num_prop='logprepexpe',
			den_forms='zcfzbs',
			den_prop='totasset',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='')

		# 递延所得税资产
		self.comdrawer.add_dividedval_table_line(
			two_tds=['递延所得税资产', '生产相关资产'],
			td_colors=[Cons.COLOR_YELLOW, Cons.COLOR_YELLOW],
			num_forms='zcfzbs',
			num_prop='defetaxasset',
			den_forms='zcfzbs',
			den_prop='totasset',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='')

		# 合计
		self.comdrawer.add_dividedval_table_line(
			two_tds=['生产相关资产合计', ''],
			td_colors=[Cons.COLOR_YELLOW, Cons.COLOR_WHITE],
			num_forms='zcfzbs',
			num_prop='prodassetot',
			den_forms='zcfzbs',
			den_prop='totasset',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='')

		# 税前利润总额 / 生产资产
		self.comdrawer.add_dividedval_table_line(
			two_tds=['税前利润总额 / 生产资产', ''],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			num_forms='gslrbs',
			num_prop='totprofit',
			den_forms='zcfzbs',
			den_prop='prodassetot',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='',
			only_dividedval_column=True)

		# 五、其它资产
		# 其他流动资产
		self.comdrawer.add_dividedval_table_line(
			two_tds=['其他流动资产', '其它资产'],
			td_colors=[Cons.COLOR_BLUE, Cons.COLOR_BLUE],
			num_forms='zcfzbs',
			num_prop='othercurrasse',
			den_forms='zcfzbs',
			den_prop='totasset',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='')

		# 其他非流动资产
		self.comdrawer.add_dividedval_table_line(
			two_tds=['其他非流动资产', '其它资产'],
			td_colors=[Cons.COLOR_BLUE, Cons.COLOR_BLUE],
			num_forms='zcfzbs',
			num_prop='othernoncasse',
			den_forms='zcfzbs',
			den_prop='totasset',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='')

		# 合计
		self.comdrawer.add_dividedval_table_line(
			two_tds=['其它资产合计', ''],
			td_colors=[Cons.COLOR_BLUE, Cons.COLOR_WHITE],
			num_forms='zcfzbs',
			num_prop='otherasettot',
			den_forms='zcfzbs',
			den_prop='totasset',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='')

		# 六、总结
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

		# 总资产周转率 = 营业收入 / 平均总资产，判断是否沃尔玛模式的关键指标
		self.comdrawer.add_weightedave_dividedval_table_line(
			two_tds=['总资产周转率', ''],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			num_forms='gslrbs',
			num_prop='bizinco',
			den_forms='zcfzbs',
			den_prop='totasset',
			two_units=[None, None],
			last_td='总资产周转率 = 营业收入 / 平均总资产，判断是否沃尔玛模式的关键指标')

		# 杠杆系数 = 平均总资产 / 净资产，判断是否银行模式的关键指标
		self.comdrawer.add_weightedave_dividedval_table_line(
			two_tds=['杠杆系数', ''],
			td_colors=[Cons.COLOR_BLUE, Cons.COLOR_WHITE],
			num_forms='zcfzbs',
			num_prop='righaggr',
			den_forms='zcfzbs',
			den_prop='totasset',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='杠杆系数 = 平均总资产 / 净资产，判断是否银行模式的关键指标；',
			func=lambda x: 1/x)

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

		# 流动比率 = 流动资产 / 流动负债
		self.comdrawer.add_dividedval_table_line(
			two_tds=['流动比率', ''],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			num_forms='zcfzbs',
			num_prop='totcurrasset',
			den_forms='zcfzbs',
			den_prop='totalcurrliab',
			two_units=[None, None],
			last_td='流动比率 = 流动资产 / 流动负债',
			only_dividedval_column=True)

		# 速动比率 = 速动资产 / 流动负债，其中速动资产  = 流动资产 - 存货
		self.comdrawer.add_dividedval_table_line(
			two_tds=['速动比率', ''],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			num_forms='zcfzbs',
			num_prop='liquidaset',
			den_forms='zcfzbs',
			den_prop='totalcurrliab',
			two_units=[None, None],
			last_td='速动比率 = 速动资产 / 流动负债，其中速动资产  = 流动资产 - 存货',
			only_dividedval_column=True)

		# 资产负债比率 = 资产总额 / 负债总额
		self.comdrawer.add_dividedval_table_line(
			two_tds=['资产负债比率', ''],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			num_forms='zcfzbs',
			num_prop='totasset',
			den_forms='zcfzbs',
			den_prop='totliab',
			two_units=[None, None],
			last_td='资产负债比率 = 资产总额 / 负债总额',
			only_dividedval_column=True)

		self.comdrawer.add_table_end()
		self.comdrawer.add_end_and_save_to_stock_file(fname='资产负债表资产部分')
