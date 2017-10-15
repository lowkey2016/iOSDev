# -*- coding: utf-8 -*-

from models.xjllb import XJLLB
from models.stock import Stock
from utils.util_stock import StockUtil
import utils.util_cons as Cons
from drawer_common import CommonDrawer

class CashInDrawer(object):
	def __init__(self, stock):
		if stock is None:
			return
		self.stock = stock

		keys = [k for k in sorted(self.stock.zcfzbs)]
		keys.reverse()
		
		self.comdrawer = CommonDrawer(stock=stock, keys=keys)

	def draw(self):
		self.comdrawer.add_start(title='现金流量表间接法')

		# 标题部分
		self.comdrawer.add_title_and_table_head(
			title='现金流量表',
			caption='间接法编制',
			two_ths=['项目', '所属分类'])

		# 净利润
		self.comdrawer.add_dividedval_table_line(
			two_tds=['净利润', '='],
			td_colors=[Cons.COLOR_PURPLE, Cons.COLOR_PURPLE],
			num_forms='xjllbs',
			num_prop='netprofit',
			den_forms='xjllbs',
			den_prop='netprofit',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以净利润')
		
		# # 少数股东权益
		# html_str += '<tr bgcolor="red">\n\t<td>少数股东权益</td>\n\t<td>-</td>\n'
		# for k in keys:
		# 	xb = self.stock.xjllbs[k]
		# 	if xb.minysharrigh:
		# 		val = xb.minysharrigh
		# 	else:
		# 		val = 0.0
		# 	xb.minysharrigh = val
		# 	html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, 0)
		# html_str += '</tr>\n'

		# 未确认的投资损失
		self.comdrawer.add_dividedval_table_line(
			two_tds=['未确认的投资损失', '+'],
			td_colors=[Cons.COLOR_GREEN, Cons.COLOR_GREEN],
			num_forms='xjllbs',
			num_prop='unreinveloss',
			den_forms='xjllbs',
			den_prop='netprofit',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以净利润')

		# 资产减值准备
		self.comdrawer.add_dividedval_table_line(
			two_tds=['资产减值准备', '+'],
			td_colors=[Cons.COLOR_GREEN, Cons.COLOR_GREEN],
			num_forms='xjllbs',
			num_prop='asseimpa',
			den_forms='xjllbs',
			den_prop='netprofit',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以净利润')

		# 固定资产折旧、油气资产折耗、生产性物资折旧
		self.comdrawer.add_dividedval_table_line(
			two_tds=['固定资产折旧、油气资产折耗、生产性物资折旧', '+'],
			td_colors=[Cons.COLOR_GREEN, Cons.COLOR_GREEN],
			num_forms='xjllbs',
			num_prop='assedepr',
			den_forms='xjllbs',
			den_prop='netprofit',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以净利润')

		# 无形资产摊销
		self.comdrawer.add_dividedval_table_line(
			two_tds=['无形资产摊销', '+'],
			td_colors=[Cons.COLOR_GREEN, Cons.COLOR_GREEN],
			num_forms='xjllbs',
			num_prop='intaasseamor',
			den_forms='xjllbs',
			den_prop='netprofit',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以净利润')

		# 间接法现金流量表中的折旧摊销，折旧摊销 / 经营活动现金流净额
		self.comdrawer.add_dividedval_table_line(
			two_tds=['折旧摊销 / 经营活动现金流净额', ''],
			td_colors=[Cons.COLOR_WHITE, Cons.COLOR_WHITE],
			num_forms='xjllbs',
			num_prop='depamortot',
			den_forms='xjllbs',
			den_prop='biznetcflow',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='折旧摊销 = 固定资产折旧、油气资产折耗、生产性物资折旧 + 无形资产摊销；除以经营活动现金流净额')

		# 投资性房地产折旧、摊销
		self.comdrawer.add_dividedval_table_line(
			two_tds=['投资性房地产折旧、摊销', '+'],
			td_colors=[Cons.COLOR_GREEN, Cons.COLOR_GREEN],
			num_forms='xjllbs',
			num_prop='realestadep',
			den_forms='xjllbs',
			den_prop='netprofit',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以净利润')

		# 长期待摊费用摊销
		self.comdrawer.add_dividedval_table_line(
			two_tds=['长期待摊费用摊销', '+'],
			td_colors=[Cons.COLOR_GREEN, Cons.COLOR_GREEN],
			num_forms='xjllbs',
			num_prop='longdefeexpenamor',
			den_forms='xjllbs',
			den_prop='netprofit',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以净利润')

		# 待摊费用的减少
		self.comdrawer.add_dividedval_table_line(
			two_tds=['待摊费用的减少', '+'],
			td_colors=[Cons.COLOR_GREEN, Cons.COLOR_GREEN],
			num_forms='xjllbs',
			num_prop='prepexpedecr',
			den_forms='xjllbs',
			den_prop='netprofit',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以净利润')

		# 预提费用的增加
		self.comdrawer.add_dividedval_table_line(
			two_tds=['预提费用的增加', '+'],
			td_colors=[Cons.COLOR_GREEN, Cons.COLOR_GREEN],
			num_forms='xjllbs',
			num_prop='accrexpeincr',
			den_forms='xjllbs',
			den_prop='netprofit',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以净利润')

		# 处置固定资产、无形资产和其他长期资产的损失
		self.comdrawer.add_dividedval_table_line(
			two_tds=['处置固定资产、无形资产和其他长期资产的损失', '+'],
			td_colors=[Cons.COLOR_GREEN, Cons.COLOR_GREEN],
			num_forms='xjllbs',
			num_prop='dispfixedassetloss',
			den_forms='xjllbs',
			den_prop='netprofit',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以净利润')

		# 固定资产报废损失
		self.comdrawer.add_dividedval_table_line(
			two_tds=['固定资产报废损失', '+'],
			td_colors=[Cons.COLOR_GREEN, Cons.COLOR_GREEN],
			num_forms='xjllbs',
			num_prop='fixedassescraloss',
			den_forms='xjllbs',
			den_prop='netprofit',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以净利润')

		# 公允价值变动损失
		self.comdrawer.add_dividedval_table_line(
			two_tds=['公允价值变动损失', '+'],
			td_colors=[Cons.COLOR_GREEN, Cons.COLOR_GREEN],
			num_forms='xjllbs',
			num_prop='valuechgloss',
			den_forms='xjllbs',
			den_prop='netprofit',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以净利润')

		# 递延收益增加（减：减少）
		self.comdrawer.add_dividedval_table_line(
			two_tds=['递延收益增加（减：减少）', '+'],
			td_colors=[Cons.COLOR_GREEN, Cons.COLOR_GREEN],
			num_forms='xjllbs',
			num_prop='defeincoincr',
			den_forms='xjllbs',
			den_prop='netprofit',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以净利润')

		# 预计负债
		self.comdrawer.add_dividedval_table_line(
			two_tds=['预计负债', '+'],
			td_colors=[Cons.COLOR_GREEN, Cons.COLOR_GREEN],
			num_forms='xjllbs',
			num_prop='estidebts',
			den_forms='xjllbs',
			den_prop='netprofit',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以净利润')

		# 财务费用
		self.comdrawer.add_dividedval_table_line(
			two_tds=['财务费用', '+'],
			td_colors=[Cons.COLOR_GREEN, Cons.COLOR_GREEN],
			num_forms='xjllbs',
			num_prop='finexpe',
			den_forms='xjllbs',
			den_prop='netprofit',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以净利润')

		# 投资损失
		self.comdrawer.add_dividedval_table_line(
			two_tds=['投资损失', '+'],
			td_colors=[Cons.COLOR_GREEN, Cons.COLOR_GREEN],
			num_forms='xjllbs',
			num_prop='inveloss',
			den_forms='xjllbs',
			den_prop='netprofit',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以净利润')

		# 递延所得税资产减少
		self.comdrawer.add_dividedval_table_line(
			two_tds=['递延所得税资产减少', '+'],
			td_colors=[Cons.COLOR_GREEN, Cons.COLOR_GREEN],
			num_forms='xjllbs',
			num_prop='defetaxassetdecr',
			den_forms='xjllbs',
			den_prop='netprofit',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以净利润')

		# 递延所得税负债增加
		self.comdrawer.add_dividedval_table_line(
			two_tds=['递延所得税负债增加', '+'],
			td_colors=[Cons.COLOR_GREEN, Cons.COLOR_GREEN],
			num_forms='xjllbs',
			num_prop='defetaxliabincr',
			den_forms='xjllbs',
			den_prop='netprofit',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以净利润')

		# 存货的减少
		self.comdrawer.add_dividedval_table_line(
			two_tds=['存货的减少', '+'],
			td_colors=[Cons.COLOR_GREEN, Cons.COLOR_GREEN],
			num_forms='xjllbs',
			num_prop='inveredu',
			den_forms='xjllbs',
			den_prop='netprofit',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以净利润')

		# 经营性应收项目的减少
		self.comdrawer.add_dividedval_table_line(
			two_tds=['经营性应收项目的减少', '+'],
			td_colors=[Cons.COLOR_GREEN, Cons.COLOR_GREEN],
			num_forms='xjllbs',
			num_prop='receredu',
			den_forms='xjllbs',
			den_prop='netprofit',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以净利润')

		# 经营性应付项目的增加
		self.comdrawer.add_dividedval_table_line(
			two_tds=['经营性应付项目的增加', '+'],
			td_colors=[Cons.COLOR_GREEN, Cons.COLOR_GREEN],
			num_forms='xjllbs',
			num_prop='payaincr',
			den_forms='xjllbs',
			den_prop='netprofit',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以净利润')

		# 已完工尚未结算款的减少(减:增加)
		self.comdrawer.add_dividedval_table_line(
			two_tds=['已完工尚未结算款的减少(减:增加)', '+'],
			td_colors=[Cons.COLOR_GREEN, Cons.COLOR_GREEN],
			num_forms='xjllbs',
			num_prop='unseparachg',
			den_forms='xjllbs',
			den_prop='netprofit',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以净利润')

		# 已结算尚未完工款的增加(减:减少)
		self.comdrawer.add_dividedval_table_line(
			two_tds=['已结算尚未完工款的增加(减:减少)', '+'],
			td_colors=[Cons.COLOR_GREEN, Cons.COLOR_GREEN],
			num_forms='xjllbs',
			num_prop='unfiparachg',
			den_forms='xjllbs',
			den_prop='netprofit',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以净利润')

		# 其他
		self.comdrawer.add_dividedval_table_line(
			two_tds=['已结算尚未完工款的增加(减:减少)', '+'],
			td_colors=[Cons.COLOR_GREEN, Cons.COLOR_GREEN],
			num_forms='xjllbs',
			num_prop='other',
			den_forms='xjllbs',
			den_prop='netprofit',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以净利润')

		# 经营活动产生现金流量净额
		self.comdrawer.add_dividedval_table_line(
			two_tds=['经营活动产生现金流量净额', '='],
			td_colors=[Cons.COLOR_PURPLE, Cons.COLOR_PURPLE],
			num_forms='xjllbs',
			num_prop='biznetcflow',
			den_forms='xjllbs',
			den_prop='cashfinalbala',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以现金的期末余额')

		# 债务转为资本
		self.comdrawer.add_dividedval_table_line(
			two_tds=['债务转为资本', '+'],
			td_colors=[Cons.COLOR_GREEN, Cons.COLOR_GREEN],
			num_forms='xjllbs',
			num_prop='debtintocapi',
			den_forms='xjllbs',
			den_prop='cashfinalbala',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以现金的期末余额')

		# 一年内到期的可转换公司债券
		self.comdrawer.add_dividedval_table_line(
			two_tds=['一年内到期的可转换公司债券', '+'],
			td_colors=[Cons.COLOR_GREEN, Cons.COLOR_GREEN],
			num_forms='xjllbs',
			num_prop='expiconvbd',
			den_forms='xjllbs',
			den_prop='cashfinalbala',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以现金的期末余额')

		# 融资租入固定资产
		self.comdrawer.add_dividedval_table_line(
			two_tds=['融资租入固定资产', '+'],
			td_colors=[Cons.COLOR_GREEN, Cons.COLOR_GREEN],
			num_forms='xjllbs',
			num_prop='finfixedasset',
			den_forms='xjllbs',
			den_prop='cashfinalbala',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以现金的期末余额')

		# 投资活动产生现金流量净额
		self.comdrawer.add_dividedval_table_line(
			two_tds=['投资活动产生现金流量净额', '+'],
			td_colors=[Cons.COLOR_GREEN, Cons.COLOR_GREEN],
			num_forms='xjllbs',
			num_prop='invnetcashflow',
			den_forms='xjllbs',
			den_prop='cashfinalbala',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以现金的期末余额')

		# 融资活动产生现金流量净额
		self.comdrawer.add_dividedval_table_line(
			two_tds=['融资活动产生现金流量净额', '+'],
			td_colors=[Cons.COLOR_GREEN, Cons.COLOR_GREEN],
			num_forms='xjllbs',
			num_prop='finnetcflow',
			den_forms='xjllbs',
			den_prop='cashfinalbala',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以现金的期末余额')

		# 现金及现金等价物的净增加额
		self.comdrawer.add_dividedval_table_line(
			two_tds=['现金及现金等价物的净增加额', '='],
			td_colors=[Cons.COLOR_PURPLE, Cons.COLOR_PURPLE],
			num_forms='xjllbs',
			num_prop='cashneti',
			den_forms='xjllbs',
			den_prop='cashfinalbala',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以现金的期末余额')

		# # 现金等价物的期初余额
		# self.comdrawer.add_dividedval_table_line(
		# 	two_tds=['现金等价物的期初余额', '='],
		# 	td_colors=[Cons.COLOR_PURPLE, Cons.COLOR_PURPLE],
		# 	num_forms='xjllbs',
		# 	num_prop='equopenbala',
		# 	den_forms='xjllbs',
		# 	den_prop='equfinalbala',
		# 	two_units=[Cons.Yi, Cons.Percent],
		# 	last_td='除以现金等价物的期末余额')
		
		# # 现金等价物的期末余额
		# self.comdrawer.add_dividedval_table_line(
		# 	two_tds=['现金等价物的期末余额', '='],
		# 	td_colors=[Cons.COLOR_PURPLE, Cons.COLOR_PURPLE],
		# 	num_forms='xjllbs',
		# 	num_prop='equfinalbala',
		# 	den_forms='xjllbs',
		# 	den_prop='equfinalbala',
		# 	two_units=[Cons.Yi, Cons.Percent],
		# 	last_td='除以现金等价物的期末余额')

		# 现金的期初余额
		self.comdrawer.add_dividedval_table_line(
			two_tds=['现金的期初余额', '='],
			td_colors=[Cons.COLOR_PURPLE, Cons.COLOR_PURPLE],
			num_forms='xjllbs',
			num_prop='cashopenbala',
			den_forms='xjllbs',
			den_prop='cashfinalbala',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以现金的期末余额')

		# 现金的期末余额
		self.comdrawer.add_dividedval_table_line(
			two_tds=['现金的期末余额', '='],
			td_colors=[Cons.COLOR_PURPLE, Cons.COLOR_PURPLE],
			num_forms='xjllbs',
			num_prop='cashfinalbala',
			den_forms='xjllbs',
			den_prop='cashfinalbala',
			two_units=[Cons.Yi, Cons.Percent],
			last_td='除以现金的期末余额')
		
		self.comdrawer.add_table_end()
		self.comdrawer.add_end_and_save_to_stock_file(fname='现金流量表间接法')
