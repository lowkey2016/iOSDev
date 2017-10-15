# -*- coding: utf-8 -*-

from models.gslrb import GSLRB
from models.fjsj import FJSJ
from models.stock import Stock
import utils.util_cons as Cons
from drawer_common import CommonDrawer

class ProfitDrawer(object):
	def __init__(self, stock):
		if stock is None:
			return
		self.stock = stock

		keys = [k for k in sorted(self.stock.zcfzbs)]
		keys.reverse()
		
		self.comdrawer = CommonDrawer(stock=stock, keys=keys)

	def draw(self):
		self.comdrawer.add_start(title='利润表')

		# 标题部分
		self.comdrawer.add_title_and_table_head(
			title='利润表',
			caption='利润变化过程',
			two_ths=['项目', '+/-'])

		# 一、营业总收入部分

		# 营业收入
		self.comdrawer.add_val_growrate_comprate_table_lines(
			two_tds=['营业收入', '+'],
			td_colors=[Cons.COLOR_GREEN, Cons.COLOR_GREEN],
			num_forms='gslrbs',
			num_prop='bizinco',
			den_forms='gslrbs',
			den_prop='biztotinco',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以营业总收入')

		# 利息收入
		self.comdrawer.add_dividedval_table_line(
			two_tds=['利息收入', '+'],
			td_colors=[Cons.COLOR_GREEN, Cons.COLOR_GREEN],
			num_forms='gslrbs',
			num_prop='inteinco',
			den_forms='gslrbs',
			den_prop='biztotinco',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以营业总收入')

		# 房地产销售收入
		self.comdrawer.add_dividedval_table_line(
			two_tds=['房地产销售收入', '+'],
			td_colors=[Cons.COLOR_GREEN, Cons.COLOR_GREEN],
			num_forms='gslrbs',
			num_prop='realsale',
			den_forms='gslrbs',
			den_prop='biztotinco',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以营业总收入')

		# 其他业务收入
		self.comdrawer.add_dividedval_table_line(
			two_tds=['其他业务收入', '+'],
			td_colors=[Cons.COLOR_GREEN, Cons.COLOR_GREEN],
			num_forms='gslrbs',
			num_prop='otherbizinco',
			den_forms='gslrbs',
			den_prop='biztotinco',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以营业总收入')

		# 营业总收入
		self.comdrawer.add_val_growrate_comprate_table_lines(
			two_tds=['营业总收入', '='],
			td_colors=[Cons.COLOR_PURPLE, Cons.COLOR_PURPLE],
			num_forms='gslrbs',
			num_prop='biztotinco',
			den_forms='gslrbs',
			den_prop='biztotinco',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以营业总收入')

		# 二、营业总成本部分

		# 营业成本
		self.comdrawer.add_val_growrate_comprate_table_lines(
			two_tds=['营业成本', '-'],
			td_colors=[Cons.COLOR_RED, Cons.COLOR_RED],
			num_forms='gslrbs',
			num_prop='bizcost',
			den_forms='gslrbs',
			den_prop='biztotcost',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以营业总成本')
		# 营业成本率 = 营业成本 / 营业收入
		self.comdrawer.add_dividedval_table_line(
			two_tds=['营业成本率', '-'],
			td_colors=[Cons.COLOR_RED, Cons.COLOR_RED],
			num_forms='gslrbs',
			num_prop='bizcost',
			den_forms='gslrbs',
			den_prop='bizinco',
			two_units=[Cons.Percent, None],
			last_td='营业成本率 = 营业成本 / 营业收入',
			only_dividedval_column=True)

		# 利息支出
		self.comdrawer.add_dividedval_table_line(
			two_tds=['利息支出', '-'],
			td_colors=[Cons.COLOR_RED, Cons.COLOR_RED],
			num_forms='gslrbs',
			num_prop='inteexpe',
			den_forms='gslrbs',
			den_prop='biztotcost',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以营业总成本')

		# 房地产销售成本
		self.comdrawer.add_dividedval_table_line(
			two_tds=['房地产销售成本', '-'],
			td_colors=[Cons.COLOR_RED, Cons.COLOR_RED],
			num_forms='gslrbs',
			num_prop='realsalecost',
			den_forms='gslrbs',
			den_prop='biztotcost',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以营业总成本')

		# 其他业务成本
		self.comdrawer.add_dividedval_table_line(
			two_tds=['其他业务成本', '-'],
			td_colors=[Cons.COLOR_RED, Cons.COLOR_RED],
			num_forms='gslrbs',
			num_prop='otherbizcost',
			den_forms='gslrbs',
			den_prop='biztotcost',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以营业总成本')

		# 营业税金及附加
		self.comdrawer.add_dividedval_table_line(
			two_tds=['营业税金及附加', '-'],
			td_colors=[Cons.COLOR_RED, Cons.COLOR_RED],
			num_forms='gslrbs',
			num_prop='biztax',
			den_forms='gslrbs',
			den_prop='biztotcost',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以营业总成本')

		# 研发费用
		self.comdrawer.add_val_growrate_comprate_table_lines(
			two_tds=['研发费用', '-'],
			td_colors=[Cons.COLOR_RED, Cons.COLOR_RED],
			num_forms='gslrbs',
			num_prop='deveexpe',
			den_forms='gslrbs',
			den_prop='biztotcost',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以营业总成本')

		# 财报中记录的开发支出
		self.comdrawer.add_val_growrate_comprate_table_lines(
			two_tds=['财报中记录的开发支出', '-'],
			td_colors=[Cons.COLOR_RED, Cons.COLOR_RED],
			num_forms='fjsjs',
			num_prop='findevexp',
			den_forms='gslrbs',
			den_prop='biztotcost',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以营业总成本')

		# 销售费用
		self.comdrawer.add_val_growrate_comprate_table_lines(
			two_tds=['销售费用', '-'],
			td_colors=[Cons.COLOR_RED, Cons.COLOR_RED],
			num_forms='gslrbs',
			num_prop='salesexpe',
			den_forms='gslrbs',
			den_prop='biztotcost',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以营业总成本')
		# 销售费用率 = 销售费用 / 营业收入
		self.comdrawer.add_dividedval_table_line(
			two_tds=['销售费用率', ''],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			num_forms='gslrbs',
			num_prop='salesexpe',
			den_forms='gslrbs',
			den_prop='bizinco',
			two_units=[Cons.Percent, None],
			last_td='销售费用率 = 销售费用 / 营业收入',
			only_dividedval_column=True)

		# 管理费用
		self.comdrawer.add_val_growrate_comprate_table_lines(
			two_tds=['管理费用', '-'],
			td_colors=[Cons.COLOR_RED, Cons.COLOR_RED],
			num_forms='gslrbs',
			num_prop='manaexpe',
			den_forms='gslrbs',
			den_prop='biztotcost',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以营业总成本')
		# 管理费用率 = 管理费用 / 营业收入
		self.comdrawer.add_dividedval_table_line(
			two_tds=['管理费用率', ''],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			num_forms='gslrbs',
			num_prop='manaexpe',
			den_forms='gslrbs',
			den_prop='bizinco',
			two_units=[Cons.Percent, None],
			last_td='管理费用率 = 管理费用 / 营业收入',
			only_dividedval_column=True)

		# 财务费用
		self.comdrawer.add_val_growrate_comprate_table_lines(
			two_tds=['财务费用', '-'],
			td_colors=[Cons.COLOR_RED, Cons.COLOR_RED],
			num_forms='gslrbs',
			num_prop='finexpe',
			den_forms='gslrbs',
			den_prop='biztotcost',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以营业总成本')

		# 销售费用和管理费用总和
		self.comdrawer.add_val_growrate_comprate_table_lines(
			two_tds=['销售费用和管理费用总和', ''],
			td_colors=[Cons.COLOR_RED, Cons.COLOR_WHITE],
			num_forms='gslrbs',
			num_prop='salmanexpes',
			den_forms='gslrbs',
			den_prop='biztotcost',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以营业总成本')

		# 三费 = 销售费用 + 管理费用 + 正数的财务费用
		self.comdrawer.add_val_growrate_comprate_table_lines(
			two_tds=['三费', ''],
			td_colors=[Cons.COLOR_RED, Cons.COLOR_WHITE],
			num_forms='gslrbs',
			num_prop='salmanfinexpes',
			den_forms='gslrbs',
			den_prop='grossprofit',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='三费 = 销售费用 + 管理费用 + 正数的财务费用；除以毛利润')

		# 营业总成本
		self.comdrawer.add_val_growrate_comprate_table_lines(
			two_tds=['营业总成本', '='],
			td_colors=[Cons.COLOR_PURPLE, Cons.COLOR_PURPLE],
			num_forms='gslrbs',
			num_prop='biztotcost',
			den_forms='gslrbs',
			den_prop='biztotinco',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以营业总收入')

		# 毛利润和毛利率
		self.comdrawer.add_dividedval_table_line(
			two_tds=['毛利润', ''],
			td_colors=[Cons.COLOR_PURPLE, Cons.COLOR_PURPLE],
			num_forms='gslrbs',
			num_prop='grossprofit',
			den_forms='gslrbs',
			den_prop='bizinco',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以营业收入；后面的是毛利率')

		# 息税前利润率 = (利息支出 + 营业利润) / 营业总收入
		self.comdrawer.add_dividedval_table_line(
			two_tds=['息税前利润', ''],
			td_colors=[Cons.COLOR_PURPLE, Cons.COLOR_PURPLE],
			num_forms='gslrbs',
			num_prop='rmtaxinteprofit',
			den_forms='gslrbs',
			den_prop='biztotinco',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='息税前利润率 = (利息支出 + 营业利润) / 营业总收入')

		# 扣除经常性损益营业利润
		self.comdrawer.add_dividedval_table_line(
			two_tds=['扣除经常性损益营业利润', ''],
			td_colors=[Cons.COLOR_PURPLE, Cons.COLOR_PURPLE],
			num_forms='gslrbs',
			num_prop='rmtaxinteprofit',
			den_forms='gslrbs',
			den_prop='biztotinco',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以营业总收入')

		# 三、非经常性损益部分

		# 资产减值损失
		self.comdrawer.add_dividedval_table_line(
			two_tds=['资产减值损失', '-'],
			td_colors=[Cons.COLOR_RED, Cons.COLOR_RED],
			num_forms='gslrbs',
			num_prop='asseimpaloss',
			den_forms='gslrbs',
			den_prop='biztotinco',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以营业总收入')

		# 公允价值变动收益
		self.comdrawer.add_dividedval_table_line(
			two_tds=['公允价值变动收益', '+'],
			td_colors=[Cons.COLOR_GREEN, Cons.COLOR_GREEN],
			num_forms='gslrbs',
			num_prop='valuechgloss',
			den_forms='gslrbs',
			den_prop='biztotinco',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以营业总收入')

		# 投资收益
		self.comdrawer.add_dividedval_table_line(
			two_tds=['投资收益', '+'],
			td_colors=[Cons.COLOR_GREEN, Cons.COLOR_GREEN],
			num_forms='gslrbs',
			num_prop='inveinco',
			den_forms='gslrbs',
			den_prop='biztotinco',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以营业总收入')

		# 其中:对联营企业和合营企业的投资收益
		self.comdrawer.add_dividedval_table_line(
			two_tds=['其中:对联营企业和合营企业的投资收益', ''],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			num_forms='gslrbs',
			num_prop='assoinveprof',
			den_forms='gslrbs',
			den_prop='inveinco',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以投资收益')

		# 汇兑收益
		self.comdrawer.add_dividedval_table_line(
			two_tds=['汇兑收益', '+'],
			td_colors=[Cons.COLOR_GREEN, Cons.COLOR_GREEN],
			num_forms='gslrbs',
			num_prop='exchggain',
			den_forms='gslrbs',
			den_prop='biztotinco',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以营业总收入')

		# 其他业务利润
		self.comdrawer.add_dividedval_table_line(
			two_tds=['其他业务利润', '+'],
			td_colors=[Cons.COLOR_GREEN, Cons.COLOR_GREEN],
			num_forms='gslrbs',
			num_prop='otherbizprof',
			den_forms='gslrbs',
			den_prop='biztotinco',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以营业总收入')

		# 四、营业利润部分

		# 营业利润
		self.comdrawer.add_val_growrate_comprate_table_lines(
			two_tds=['营业利润', '='],
			td_colors=[Cons.COLOR_PURPLE, Cons.COLOR_PURPLE],
			num_forms='gslrbs',
			num_prop='perprofit',
			den_forms='gslrbs',
			den_prop='biztotinco',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以营业总收入；营业利润率在后面')

		# 营业外收入
		self.comdrawer.add_dividedval_table_line(
			two_tds=['营业外收入', '+'],
			td_colors=[Cons.COLOR_GREEN, Cons.COLOR_GREEN],
			num_forms='gslrbs',
			num_prop='nonoreve',
			den_forms='gslrbs',
			den_prop='perprofit',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以营业利润')

		# 营业外支出
		self.comdrawer.add_dividedval_table_line(
			two_tds=['营业外支出', '-'],
			td_colors=[Cons.COLOR_RED, Cons.COLOR_RED],
			num_forms='gslrbs',
			num_prop='nonoexpe',
			den_forms='gslrbs',
			den_prop='perprofit',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以营业利润')

		# 营业外收支净额
		self.comdrawer.add_dividedval_table_line(
			two_tds=['营业外收支净额', '='],
			td_colors=[Cons.COLOR_PURPLE, Cons.COLOR_PURPLE],
			num_forms='gslrbs',
			num_prop='noninoutnet',
			den_forms='gslrbs',
			den_prop='perprofit',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以营业利润')

		# 非流动资产处置损失
		self.comdrawer.add_dividedval_table_line(
			two_tds=['非流动资产处置损失', '-'],
			td_colors=[Cons.COLOR_RED, Cons.COLOR_RED],
			num_forms='gslrbs',
			num_prop='noncassetsdisl',
			den_forms='gslrbs',
			den_prop='perprofit',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以营业利润')

		# 五、净利润部分

		# 利润总额
		self.comdrawer.add_val_growrate_comprate_table_lines(
			two_tds=['利润总额', '='],
			td_colors=[Cons.COLOR_PURPLE, Cons.COLOR_PURPLE],
			num_forms='gslrbs',
			num_prop='totprofit',
			den_forms='gslrbs',
			den_prop='biztotinco',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以营业总收入；后面的是税前利润率')

		# 所得税费用
		self.comdrawer.add_dividedval_table_line(
			two_tds=['所得税费用', '-'],
			td_colors=[Cons.COLOR_RED, Cons.COLOR_RED],
			num_forms='gslrbs',
			num_prop='incotaxexpe',
			den_forms='gslrbs',
			den_prop='totprofit',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以利润总额；后面的是所得税率')

		# 净利润
		self.comdrawer.add_val_growrate_comprate_table_lines(
			two_tds=['净利润', '='],
			td_colors=[Cons.COLOR_PURPLE, Cons.COLOR_PURPLE],
			num_forms='gslrbs',
			num_prop='netprofit',
			den_forms='gslrbs',
			den_prop='biztotinco',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以营业总收入；后面的是净利率')

		# 归属于母公司所有者的净利润
		self.comdrawer.add_dividedval_table_line(
			two_tds=['归属于母公司所有者的净利润', ''],
			td_colors=[Cons.COLOR_PURPLE, Cons.COLOR_WHITE],
			num_forms='gslrbs',
			num_prop='parenetp',
			den_forms='gslrbs',
			den_prop='netprofit',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以净利润')

		# 少数股东损益
		self.comdrawer.add_dividedval_table_line(
			two_tds=['少数股东损益', ''],
			td_colors=[Cons.COLOR_PURPLE, Cons.COLOR_WHITE],
			num_forms='gslrbs',
			num_prop='minysharrigh',
			den_forms='gslrbs',
			den_prop='netprofit',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以净利润')

		# 经营现金流净额 / 净利润
		self.comdrawer.add_dividedval_table_line(
			two_tds=['经营现金流净额 / 净利润', ''],
			td_colors=[Cons.COLOR_PINK, Cons.COLOR_WHITE],
			num_forms='xjllbs',
			num_prop='mananetr',
			den_forms='gslrbs',
			den_prop='netprofit',
			two_units=[None, None],
			last_td='',
			only_dividedval_column=True)

		# 六、每股收益部分

		# 基本每股收益
		self.comdrawer.add_num_table_line(
			two_tds=['基本每股收益', ''],
			td_colors=[Cons.COLOR_PINK, Cons.COLOR_WHITE],
			forms='gslrbs',
			prop='basiceps',
			unit=None,
			last_td='')

		# 稀释每股收益
		self.comdrawer.add_num_table_line(
			two_tds=['稀释每股收益', ''],
			td_colors=[Cons.COLOR_PINK, Cons.COLOR_WHITE],
			forms='gslrbs',
			prop='dilutedeps',
			unit=None,
			last_td='')

		# 七、综合收益部分

		# 其他综合收益
		self.comdrawer.add_dividedval_table_line(
			two_tds=['其他综合收益', '+'],
			td_colors=[Cons.COLOR_GREEN, Cons.COLOR_GREEN],
			num_forms='gslrbs',
			num_prop='othercompinco',
			den_forms='gslrbs',
			den_prop='compincoamt',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以综合收益总额')

		# 归属于母公司所有者的其他综合收益
		self.comdrawer.add_dividedval_table_line(
			two_tds=['归属于母公司所有者的其他综合收益', ''],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			num_forms='gslrbs',
			num_prop='parecompinco',
			den_forms='gslrbs',
			den_prop='othercompinco',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以其他综合收益')

		# 归属于少数股东的其他综合收益
		self.comdrawer.add_dividedval_table_line(
			two_tds=['归属于少数股东的其他综合收益', ''],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			num_forms='gslrbs',
			num_prop='minysharinco',
			den_forms='gslrbs',
			den_prop='othercompinco',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以其他综合收益')

		# 综合收益总额
		self.comdrawer.add_dividedval_table_line(
			two_tds=['其他综合收益', '='],
			td_colors=[Cons.COLOR_PURPLE, Cons.COLOR_PURPLE],
			num_forms='gslrbs',
			num_prop='compincoamt',
			den_forms='gslrbs',
			den_prop='biztotinco',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以营业总收入')

		# 归属于母公司所有者的综合收益总额
		self.comdrawer.add_dividedval_table_line(
			two_tds=['归属于母公司所有者的综合收益总额', ''],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			num_forms='gslrbs',
			num_prop='parecompincoamt',
			den_forms='gslrbs',
			den_prop='compincoamt',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以综合收益总额')

		# 归属于少数股东的综合收益总额
		self.comdrawer.add_dividedval_table_line(
			two_tds=['归属于少数股东的综合收益总额', ''],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			num_forms='gslrbs',
			num_prop='minysharincoamt',
			den_forms='gslrbs',
			den_prop='compincoamt',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以综合收益总额')

		# 加权平均净资产收益率 ROE = 净利润 / 平均净资产
		self.comdrawer.add_weightedave_dividedval_table_line(
			two_tds=['加权平均 ROE', ''],
			td_colors=[Cons.COLOR_PINK, Cons.COLOR_WHITE],
			num_forms='gslrbs',
			num_prop='netprofit',
			den_forms='zcfzbs',
			den_prop='righaggr',
			two_units=[Cons.Percent, None],
			last_td='净利润 / 平均净资产',
			func=None,
			color_map_func=Cons.roe_color_map_func)

		# 加权平均总资产收益率 ROA = 净利润 / 平均总资产
		self.comdrawer.add_weightedave_dividedval_table_line(
			two_tds=['加权平均 ROA', ''],
			td_colors=[Cons.COLOR_PINK, Cons.COLOR_WHITE],
			num_forms='gslrbs',
			num_prop='netprofit',
			den_forms='zcfzbs',
			den_prop='totasset',
			two_units=[Cons.Percent, None],
			last_td='净利润 / 平均总资产',
			func=None,
			color_map_func=Cons.roa_color_map_func)

		# 本期 ROE = 净利润 / 上期净资产
		self.comdrawer.add_dividedval_table_line(
			two_tds=['本期 ROE', ''],
			td_colors=[Cons.COLOR_PINK, Cons.COLOR_WHITE],
			num_forms='gslrbs',
			num_prop='netprofit',
			den_forms='zcfzbs',
			den_prop='righaggr',
			two_units=[Cons.Percent, None],
			last_td='本期 ROE = 净利润 / 上期净资产',
			only_dividedval_column=True,
			dividedval_color_map_func=Cons.roe_color_map_func)

		# 本期 ROA = 净利润 / 上期总资产
		self.comdrawer.add_dividedval_table_line(
			two_tds=['本期 ROE', ''],
			td_colors=[Cons.COLOR_PINK, Cons.COLOR_WHITE],
			num_forms='gslrbs',
			num_prop='netprofit',
			den_forms='zcfzbs',
			den_prop='totasset',
			two_units=[Cons.Percent, None],
			last_td='本期 ROA = 净利润 / 上期总资产',
			only_dividedval_column=True,
			dividedval_color_map_func=Cons.roa_color_map_func)

		self.comdrawer.add_table_end()
		self.comdrawer.add_end_and_save_to_stock_file(fname='利润表')
