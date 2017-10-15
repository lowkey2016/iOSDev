# -*- coding: utf-8 -*-

from models.xjllb import XJLLB
from models.fjsj import FJSJ
from models.stock import Stock
from utils.util_stock import StockUtil
import utils.util_cons as Cons
from drawer_common import CommonDrawer

class CashDrawer(object):
	def __init__(self, stock):
		if stock is None:
			return
		self.stock = stock

		keys = [k for k in sorted(self.stock.zcfzbs)]
		keys.reverse()
		
		self.comdrawer = CommonDrawer(stock=stock, keys=keys)

	def draw(self):
		self.comdrawer.add_start(title='现金流量表')

		# 标题部分
		self.comdrawer.add_title_and_table_head(
			title='现金流量表',
			caption='直接法编制',
			two_ths=['项目', '所属分类'])

		# 一、经营活动现金流

		# 销售商品、提供劳务收到的现金
		self.comdrawer.add_dividedval_table_line(
			two_tds=['销售商品、提供劳务收到的现金', '经营活动 +'],
			td_colors=[Cons.COLOR_GREEN, Cons.COLOR_GREEN],
			num_forms='xjllbs',
			num_prop='laborgetcash',
			den_forms='xjllbs',
			den_prop='bizcashinfl',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以经营活动现金流入小计')

		# 销售商品、提供劳务收到的现金 / 营业收入
		self.comdrawer.add_dividedval_table_line(
			two_tds=['销售商品、提供劳务收到的现金 / 营业收入', ''],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			num_forms='xjllbs',
			num_prop='laborgetcash',
			den_forms='gslrbs',
			den_prop='bizinco',
			two_units=[None, None],
			last_td='',
			only_dividedval_column=True)

		# 收到的其他与经营活动有关的现金
		self.comdrawer.add_dividedval_table_line(
			two_tds=['收到的其他与经营活动有关的现金', '经营活动 +'],
			td_colors=[Cons.COLOR_GREEN, Cons.COLOR_GREEN],
			num_forms='xjllbs',
			num_prop='receotherbizcash',
			den_forms='xjllbs',
			den_prop='bizcashinfl',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以经营活动现金流入小计')

		# 经营活动现金流入小计
		self.comdrawer.add_dividedval_table_line(
			two_tds=['经营活动现金流入小计', '经营活动 + ='],
			td_colors=[Cons.COLOR_GREEN, Cons.COLOR_GREEN],
			num_forms='xjllbs',
			num_prop='bizcashinfl',
			den_forms='xjllbs',
			den_prop='bizcashinfl',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以经营活动现金流入小计')

		# 购买商品、接受劳务支付的现金
		self.comdrawer.add_dividedval_table_line(
			two_tds=['购买商品、接受劳务支付的现金', '经营活动 -'],
			td_colors=[Cons.COLOR_RED, Cons.COLOR_RED],
			num_forms='xjllbs',
			num_prop='labopayc',
			den_forms='xjllbs',
			den_prop='bizcashoutf',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以经营活动现金流出小计')

		# 支付给职工以及为职工支付的现金
		self.comdrawer.add_dividedval_table_line(
			two_tds=['支付给职工以及为职工支付的现金', '经营活动 -'],
			td_colors=[Cons.COLOR_RED, Cons.COLOR_RED],
			num_forms='xjllbs',
			num_prop='payworkcash',
			den_forms='xjllbs',
			den_prop='bizcashoutf',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以经营活动现金流出小计')

		# 支付的各项税费
		self.comdrawer.add_dividedval_table_line(
			two_tds=['支付的各项税费', '经营活动 -'],
			td_colors=[Cons.COLOR_RED, Cons.COLOR_RED],
			num_forms='xjllbs',
			num_prop='paytax',
			den_forms='xjllbs',
			den_prop='bizcashoutf',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以经营活动现金流出小计')

		# 支付的其他与经营活动有关的现金
		self.comdrawer.add_dividedval_table_line(
			two_tds=['支付的其他与经营活动有关的现金', '经营活动 -'],
			td_colors=[Cons.COLOR_RED, Cons.COLOR_RED],
			num_forms='xjllbs',
			num_prop='payacticash',
			den_forms='xjllbs',
			den_prop='bizcashoutf',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以经营活动现金流出小计')

		# 经营活动现金流出小计
		self.comdrawer.add_dividedval_table_line(
			two_tds=['经营活动现金流出小计', '经营活动 - ='],
			td_colors=[Cons.COLOR_RED, Cons.COLOR_RED],
			num_forms='xjllbs',
			num_prop='bizcashoutf',
			den_forms='xjllbs',
			den_prop='bizcashoutf',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以经营活动现金流出小计')

		# 经营活动产生的现金流量净额
		self.comdrawer.add_dividedval_table_line(
			two_tds=['经营活动产生的现金流量净额', '经营活动 ='],
			td_colors=[Cons.COLOR_PURPLE, Cons.COLOR_PURPLE],
			num_forms='xjllbs',
			num_prop='mananetr',
			den_forms='xjllbs',
			den_prop='cashnetr',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以现金及现金等价物净增加额')

		# 经营现金流净额 / 应收款总和
		self.comdrawer.add_dividedval_table_line(
			two_tds=['经营现金流净额 / 应收款总和', ''],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			num_forms='xjllbs',
			num_prop='mananetr',
			den_forms='zcfzbs',
			den_prop='rectot',
			two_units=[None, None],
			last_td='',
			only_dividedval_column=True)

		# 二、投资活动现金流

		# 收回投资所收到的现金
		self.comdrawer.add_dividedval_table_line(
			two_tds=['收回投资所收到的现金', '投资活动 +'],
			td_colors=[Cons.COLOR_GREEN, Cons.COLOR_GREEN],
			num_forms='xjllbs',
			num_prop='withinvgetcash',
			den_forms='xjllbs',
			den_prop='invcashinfl',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以投资活动现金流入小计')

		# 取得投资收益收到的现金
		self.comdrawer.add_dividedval_table_line(
			two_tds=['取得投资收益收到的现金', '投资活动 +'],
			td_colors=[Cons.COLOR_GREEN, Cons.COLOR_GREEN],
			num_forms='xjllbs',
			num_prop='inveretugetcash',
			den_forms='xjllbs',
			den_prop='invcashinfl',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以投资活动现金流入小计')

		# 处置固定资产、无形资产和其他长期资产所回收的现金净额
		self.comdrawer.add_dividedval_table_line(
			two_tds=['处置固定资产、无形资产和其他长期资产所回收的现金净额', '投资活动 +'],
			td_colors=[Cons.COLOR_GREEN, Cons.COLOR_GREEN],
			num_forms='xjllbs',
			num_prop='fixedassetnetc',
			den_forms='xjllbs',
			den_prop='invcashinfl',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以投资活动现金流入小计')

		# 处置子公司及其他营业单位收到的现金净额
		self.comdrawer.add_dividedval_table_line(
			two_tds=['处置子公司及其他营业单位收到的现金净额', '投资活动 +'],
			td_colors=[Cons.COLOR_GREEN, Cons.COLOR_GREEN],
			num_forms='xjllbs',
			num_prop='subsnetc',
			den_forms='xjllbs',
			den_prop='invcashinfl',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以投资活动现金流入小计')

		# 收到的其他与投资活动有关的现金
		self.comdrawer.add_dividedval_table_line(
			two_tds=['收到的其他与投资活动有关的现金', '投资活动 +'],
			td_colors=[Cons.COLOR_GREEN, Cons.COLOR_GREEN],
			num_forms='xjllbs',
			num_prop='receinvcash',
			den_forms='xjllbs',
			den_prop='invcashinfl',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以投资活动现金流入小计')

		# 减少质押和定期存款所收到的现金
		self.comdrawer.add_dividedval_table_line(
			two_tds=['减少质押和定期存款所收到的现金', '投资活动 +'],
			td_colors=[Cons.COLOR_GREEN, Cons.COLOR_GREEN],
			num_forms='xjllbs',
			num_prop='reducashpled',
			den_forms='xjllbs',
			den_prop='invcashinfl',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以投资活动现金流入小计')

		# 投资活动现金流入小计
		self.comdrawer.add_dividedval_table_line(
			two_tds=['投资活动现金流入小计', '投资活动 + ='],
			td_colors=[Cons.COLOR_GREEN, Cons.COLOR_GREEN],
			num_forms='xjllbs',
			num_prop='invcashinfl',
			den_forms='xjllbs',
			den_prop='invcashinfl',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以投资活动现金流入小计')

		# 购建固定资产、无形资产和其他长期资产所支付的现金
		self.comdrawer.add_dividedval_table_line(
			two_tds=['购建固定资产、无形资产和其他长期资产所支付的现金', '投资活动 -'],
			td_colors=[Cons.COLOR_RED, Cons.COLOR_RED],
			num_forms='xjllbs',
			num_prop='acquassetcash',
			den_forms='xjllbs',
			den_prop='invcashoutf',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以投资活动现金流出小计')

		# 购买固定资产、无形资产等支出 / 经营现金流净额
		self.comdrawer.add_dividedval_table_line(
			two_tds=['购买固定资产、无形资产等支出 / 经营现金流净额', ''],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			num_forms='xjllbs',
			num_prop='acquassetcash',
			den_forms='xjllbs',
			den_prop='mananetr',
			two_units=[None, None],
			last_td='',
			only_dividedval_column=True)

		# 投资所支付的现金
		self.comdrawer.add_dividedval_table_line(
			two_tds=['投资所支付的现金', '投资活动 -'],
			td_colors=[Cons.COLOR_RED, Cons.COLOR_RED],
			num_forms='xjllbs',
			num_prop='invpayc',
			den_forms='xjllbs',
			den_prop='invcashoutf',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以投资活动现金流出小计')

		# 质押贷款净增加额
		self.comdrawer.add_dividedval_table_line(
			two_tds=['质押贷款净增加额', '投资活动 -'],
			td_colors=[Cons.COLOR_RED, Cons.COLOR_RED],
			num_forms='xjllbs',
			num_prop='loannetr',
			den_forms='xjllbs',
			den_prop='invcashoutf',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以投资活动现金流出小计')

		# 取得子公司及其他营业单位支付的现金净额
		self.comdrawer.add_dividedval_table_line(
			two_tds=['取得子公司及其他营业单位支付的现金净额', '投资活动 -'],
			td_colors=[Cons.COLOR_RED, Cons.COLOR_RED],
			num_forms='xjllbs',
			num_prop='subspaynetcash',
			den_forms='xjllbs',
			den_prop='invcashoutf',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以投资活动现金流出小计')

		# 支付的其他与投资活动有关的现金
		self.comdrawer.add_dividedval_table_line(
			two_tds=['支付的其他与投资活动有关的现金', '投资活动 -'],
			td_colors=[Cons.COLOR_RED, Cons.COLOR_RED],
			num_forms='xjllbs',
			num_prop='payinvecash',
			den_forms='xjllbs',
			den_prop='invcashoutf',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以投资活动现金流出小计')

		# 增加质押和定期存款所支付的现金
		self.comdrawer.add_dividedval_table_line(
			two_tds=['增加质押和定期存款所支付的现金', '投资活动 -'],
			td_colors=[Cons.COLOR_RED, Cons.COLOR_RED],
			num_forms='xjllbs',
			num_prop='incrcashpled',
			den_forms='xjllbs',
			den_prop='invcashoutf',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以投资活动现金流出小计')

		# 投资活动现金流出小计
		self.comdrawer.add_dividedval_table_line(
			two_tds=['投资活动现金流出小计', '投资活动 - ='],
			td_colors=[Cons.COLOR_RED, Cons.COLOR_RED],
			num_forms='xjllbs',
			num_prop='invcashoutf',
			den_forms='xjllbs',
			den_prop='invcashoutf',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以投资活动现金流出小计')

		# 投资活动产生的现金流量净额
		self.comdrawer.add_dividedval_table_line(
			two_tds=['投资活动产生的现金流量净额', '投资活动 ='],
			td_colors=[Cons.COLOR_PURPLE, Cons.COLOR_PURPLE],
			num_forms='xjllbs',
			num_prop='invnetcashflow',
			den_forms='xjllbs',
			den_prop='cashnetr',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以现金及现金等价物净增加额')

		# 三、筹资活动现金流

		# 吸收投资收到的现金
		self.comdrawer.add_dividedval_table_line(
			two_tds=['吸收投资收到的现金', '筹资活动 +'],
			td_colors=[Cons.COLOR_GREEN, Cons.COLOR_GREEN],
			num_forms='xjllbs',
			num_prop='invrececash',
			den_forms='xjllbs',
			den_prop='fincashinfl',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以筹资活动现金流入小计')

		# 其中：子公司吸收少数股东投资收到的现金
		self.comdrawer.add_dividedval_table_line(
			two_tds=['其中：子公司吸收少数股东投资收到的现金', ''],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			num_forms='xjllbs',
			num_prop='subsrececash',
			den_forms='xjllbs',
			den_prop='invrececash',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以吸收投资收到的现金')

		# 取得借款收到的现金
		self.comdrawer.add_dividedval_table_line(
			two_tds=['取得借款收到的现金', '筹资活动 +'],
			td_colors=[Cons.COLOR_GREEN, Cons.COLOR_GREEN],
			num_forms='xjllbs',
			num_prop='recefromloan',
			den_forms='xjllbs',
			den_prop='fincashinfl',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以筹资活动现金流入小计')

		# 发行债券收到的现金
		self.comdrawer.add_dividedval_table_line(
			two_tds=['发行债券收到的现金', '筹资活动 +'],
			td_colors=[Cons.COLOR_GREEN, Cons.COLOR_GREEN],
			num_forms='xjllbs',
			num_prop='issbdrececash',
			den_forms='xjllbs',
			den_prop='fincashinfl',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以筹资活动现金流入小计')

		# 收到其他与筹资活动有关的现金
		self.comdrawer.add_dividedval_table_line(
			two_tds=['收到其他与筹资活动有关的现金', '筹资活动 +'],
			td_colors=[Cons.COLOR_GREEN, Cons.COLOR_GREEN],
			num_forms='xjllbs',
			num_prop='recefincash',
			den_forms='xjllbs',
			den_prop='fincashinfl',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以筹资活动现金流入小计')

		# 筹资活动现金流入小计
		self.comdrawer.add_dividedval_table_line(
			two_tds=['筹资活动现金流入小计', '筹资活动 + ='],
			td_colors=[Cons.COLOR_GREEN, Cons.COLOR_GREEN],
			num_forms='xjllbs',
			num_prop='fincashinfl',
			den_forms='xjllbs',
			den_prop='fincashinfl',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以筹资活动现金流入小计')

		# 偿还债务支付的现金
		self.comdrawer.add_dividedval_table_line(
			two_tds=['偿还债务支付的现金', '筹资活动 -'],
			td_colors=[Cons.COLOR_RED, Cons.COLOR_RED],
			num_forms='xjllbs',
			num_prop='debtpaycash',
			den_forms='xjllbs',
			den_prop='fincashoutf',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以筹资活动现金流出小计')

		# 分配股利、利润或偿付利息所支付的现金
		self.comdrawer.add_dividedval_table_line(
			two_tds=['分配股利、利润或偿付利息所支付的现金', '筹资活动 -'],
			td_colors=[Cons.COLOR_RED, Cons.COLOR_RED],
			num_forms='xjllbs',
			num_prop='diviprofpaycash',
			den_forms='xjllbs',
			den_prop='fincashoutf',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以筹资活动现金流出小计')

		# 其中：子公司支付给少数股东的股利，利润
		self.comdrawer.add_dividedval_table_line(
			two_tds=['其中：子公司支付给少数股东的股利，利润', ''],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			num_forms='xjllbs',
			num_prop='subspaydivid',
			den_forms='xjllbs',
			den_prop='diviprofpaycash',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以分配股利、利润或偿付利息所支付的现金')

		# 支付其他与筹资活动有关的现金
		self.comdrawer.add_dividedval_table_line(
			two_tds=['支付其他与筹资活动有关的现金', '筹资活动 -'],
			td_colors=[Cons.COLOR_RED, Cons.COLOR_RED],
			num_forms='xjllbs',
			num_prop='finrelacash',
			den_forms='xjllbs',
			den_prop='fincashoutf',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以筹资活动现金流出小计')

		# 筹资活动现金流出小计
		self.comdrawer.add_dividedval_table_line(
			two_tds=['筹资活动现金流出小计', '筹资活动 - ='],
			td_colors=[Cons.COLOR_RED, Cons.COLOR_RED],
			num_forms='xjllbs',
			num_prop='fincashoutf',
			den_forms='xjllbs',
			den_prop='fincashoutf',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以筹资活动现金流出小计')

		# 筹资活动产生的现金流量净额
		self.comdrawer.add_dividedval_table_line(
			two_tds=['筹资活动产生的现金流量净额', '筹资活动 ='],
			td_colors=[Cons.COLOR_PURPLE, Cons.COLOR_PURPLE],
			num_forms='xjllbs',
			num_prop='finnetcflow',
			den_forms='xjllbs',
			den_prop='cashnetr',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以现金及现金等价物净增加额')

		# 权益性筹资的发行价
		self.comdrawer.add_num_table_line(
			two_tds=['权益性筹资的发行价', ''],
			td_colors=[Cons.COLOR_PINK, Cons.COLOR_WHITE],
			forms='fjsjs',
			prop='equfinpubpri',
			unit='元',
			last_td='')

		# 债务性筹资的利率
		self.comdrawer.add_num_table_line(
			two_tds=['债务性筹资的利率', ''],
			td_colors=[Cons.COLOR_PINK, Cons.COLOR_WHITE],
			forms='fjsjs',
			prop='debtfininrate',
			unit=Cons.Percent,
			last_td='')

		# 四、汇总

		# 汇率变动对现金及现金等价物的影响
		self.comdrawer.add_dividedval_table_line(
			two_tds=['汇率变动对现金及现金等价物的影响', ''],
			td_colors=[Cons.COLOR_PURPLE, Cons.COLOR_WHITE],
			num_forms='xjllbs',
			num_prop='chgexchgchgs',
			den_forms='xjllbs',
			den_prop='cashnetr',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以现金及现金等价物净增加额')

		# 现金及现金等价物净增加额
		self.comdrawer.add_dividedval_table_line(
			two_tds=['现金及现金等价物净增加额', '+'],
			td_colors=[Cons.COLOR_PURPLE, Cons.COLOR_PURPLE],
			num_forms='xjllbs',
			num_prop='cashnetr',
			den_forms='xjllbs',
			den_prop='finalcashbala',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以期末现金及现金等价物余额',
			dividedval_color_map_func=Cons.rateover0_color_map_func)

		# 期初现金及现金等价物余额
		self.comdrawer.add_dividedval_table_line(
			two_tds=['期初现金及现金等价物余额', '='],
			td_colors=[Cons.COLOR_PURPLE, Cons.COLOR_PURPLE],
			num_forms='xjllbs',
			num_prop='inicashbala',
			den_forms='xjllbs',
			den_prop='finalcashbala',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以期末现金及现金等价物余额')

		# 期末现金及现金等价物余额
		self.comdrawer.add_dividedval_table_line(
			two_tds=['期末现金及现金等价物余额', '='],
			td_colors=[Cons.COLOR_PURPLE, Cons.COLOR_PURPLE],
			num_forms='xjllbs',
			num_prop='finalcashbala',
			den_forms='xjllbs',
			den_prop='finalcashbala',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以期末现金及现金等价物余额')

		# 期末现金及现金等价物余额 / 有息负债
		self.comdrawer.add_dividedval_table_line(
			two_tds=['期末现金及现金等价物余额 / 有息负债', ''],
			td_colors=[Cons.COLOR_PINK, Cons.COLOR_WHITE],
			num_forms='xjllbs',
			num_prop='finalcashbala',
			den_forms='zcfzbs',
			den_prop='borrtot',
			two_units=[None, None],
			last_td='',
			only_dividedval_column=True,
			dividedval_color_map_func=Cons.valover1_oris0_color_map_func)

		# 期末现金及现金等价物余额 + 应收票据中的银行承兑汇票 > 有息负债
		self.comdrawer.html_util.add_table_body_td(td='(期末现金及现金等价物余额 + 应收票据中的银行承兑汇票) / 有息负债', color=Cons.COLOR_PINK)
		self.comdrawer.html_util.add_table_body_td(td='', color=Cons.COLOR_WHITE)
		for k in self.comdrawer.keys:
			keypath1 = 'xjllbs[%s].finalcashbala' % k
			keypath2 = 'fjsjs[%s].notesrece_bank' % k
			keypath3 = 'zcfzbs[%s].borrtot' % k
			val1 = StockUtil.numValueForKeyPath(stock=self.comdrawer.stock, keypath=keypath1)
			val2 = StockUtil.numValueForKeyPath(stock=self.comdrawer.stock, keypath=keypath2)
			val3 = StockUtil.numValueForKeyPath(stock=self.comdrawer.stock, keypath=keypath3)
			numval = val1 + val2
			denval = val3
			rate = StockUtil.getDivideVal(num=numval, den=denval, use_percent_format=False)
			if numval >= denval:
				color = Cons.COLOR_GREEN
			else:
				color = Cons.COLOR_RED
			self.comdrawer.html_util.add_table_body_td_val(val=rate, color=color, unit=Cons.Percent)
			self.comdrawer.html_util.add_table_body_td_empty()
		self.comdrawer.html_util.add_table_body_td(td='', color=Cons.COLOR_WHITE)
		self.comdrawer.html_util.add_table_body_tr_end()

		# 加权平均净资产现金回收率 = 经营现金流净额 / 平均净资产
		self.comdrawer.add_weightedave_dividedval_table_line(
			two_tds=['加权平均净资产现金回收率', ''],
			td_colors=[Cons.COLOR_PINK, Cons.COLOR_WHITE],
			num_forms='xjllbs',
			num_prop='mananetr',
			den_forms='zcfzbs',
			den_prop='righaggr',
			two_units=[Cons.Percent, None],
			last_td='加权平均净资产现金回收率 = 经营现金流净额 / 平均净资产',
			func=None,
			color_map_func=None)

		# 加权平均总资产现金回收率 = 经营现金流净额 / 平均总资产
		self.comdrawer.add_weightedave_dividedval_table_line(
			two_tds=['加权平均总资产现金回收率', ''],
			td_colors=[Cons.COLOR_PINK, Cons.COLOR_WHITE],
			num_forms='xjllbs',
			num_prop='mananetr',
			den_forms='zcfzbs',
			den_prop='totasset',
			two_units=[Cons.Percent, None],
			last_td='加权平均总资产现金回收率 = 经营现金流净额 / 平均总资产',
			func=None,
			color_map_func=None)

		# 简化的自由现金流 = 经营现金流净额 - 投资活动现金流出净额
		self.comdrawer.add_num_table_line(
			two_tds=['简化的自由现金流', ''],
			td_colors=[Cons.COLOR_PINK, Cons.COLOR_WHITE],
			forms='xjllbs',
			prop='simfreecashflow',
			unit=Cons.Yi,
			last_td='简化的自由现金流 = 经营现金流净额 - 投资活动现金流出净额',
			val_color_map_func=Cons.valover0_map_func)

		# 所属类型(奶牛/母鸡/蛮牛等)
		self.comdrawer.html_util.add_table_body_td(td='所属类型(奶牛/母鸡/蛮牛等)', color=Cons.COLOR_PURPLE)
		self.comdrawer.html_util.add_table_body_td(td='', color=Cons.COLOR_WHITE)
		for k in self.comdrawer.keys:
			xb = self.comdrawer.stock.xjllbs[k]

			A = xb.mananetr > 0
			B = xb.invnetcashflow > 0
			C = xb.finnetcflow > 0

			if A and B and C:
				val = '妖精型'
				color = Cons.COLOR_RED
			elif A and B and not C:
				val = '老母鸡型'
				color = Cons.COLOR_GREEN
			elif A and not B and C:
				val = '蛮牛型'
				color = Cons.COLOR_YELLOW
			elif A and not B and not C:
				val = '奶牛型'
				color = Cons.COLOR_GREEN
			elif not A and B and C:
				val = '骗吃骗喝型'
				color = Cons.COLOR_RED
			elif not A and B and not C:
				val = '混吃等死型'
				color = Cons.COLOR_RED
			elif not A and not B and C:
				val = '赌徒型'
				color = Cons.COLOR_RED
			elif not A and not B and not C:
				val = '大出血型'
				color = Cons.COLOR_RED
			
			self.comdrawer.html_util.add_table_body_td(td=val, color=color)
			self.comdrawer.html_util.add_table_body_td_empty()
		self.comdrawer.html_util.add_table_body_td(td='', color=Cons.COLOR_WHITE)
		self.comdrawer.html_util.add_table_body_tr_end()

		self.comdrawer.add_table_end()
		self.comdrawer.add_end_and_save_to_stock_file(fname='现金流量表')
