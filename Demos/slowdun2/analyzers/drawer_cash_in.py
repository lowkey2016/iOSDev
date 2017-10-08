# -*- coding: utf-8 -*-

from models.xjllb import XJLLB
from models.stock import Stock
from utils.util_res import ResUtil
import utils.util_cons as Cons

class CashInDrawer(object):
	def __init__(self, stock):
		if stock is None:
			return
		self.stock = stock

	def draw(self):
		html_str = '<html>'
		html_str += """
		<head>
		<link rel="stylesheet" href="https://cdn.bootcss.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">

		<!-- 最新的 Bootstrap 核心 JavaScript 文件 -->
		<script src="https://cdn.bootcss.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>
		<style>tbody tr:first-child td:nth-child(1), tbody tr:first-child td:nth-child(2) { white-space: nowrap; } thead tr:first-child th:last-child { white-space: nowrap; padding: 5px 50px; }</style>
		</head>
		"""

		html_str += '<body>\n<h4>现金流量表</h4>\n\n<table class="table table-bordered">\n\t<caption>间接法编制</caption>\n<thead><tr>\n\t<th>项目</th>\n\t<th>所属分类</th>'

		keys = [k for k in sorted(self.stock.xjllbs)]
		keys.reverse()

		# 表头
		for k in keys:
			tmpstr = '\t<th colspan="2">%s</th>\n' % k
			html_str += tmpstr
		html_str += '\t<th>备注</th>\n</tr>\n</thead>\n<tbody>\n'

		# 净利润
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">净利润</td>\n\t<td style="background: %s; color: #FFFFFF">=</td>\n' % (Cons.COLOR_PURPLE, Cons.COLOR_PURPLE)
		for k in keys:
			xb = self.stock.xjllbs[k]
			if xb.netprofit:
				val = xb.netprofit
			else:
				val = 0.0
			xb.netprofit = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, 0)
		html_str += '</tr>\n'
		
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
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">未确认的投资损失</td>\n\t<td style="background: %s; color: #FFFFFF">+</td>\n' % (Cons.COLOR_GREEN, Cons.COLOR_GREEN)
		for k in keys:
			xb = self.stock.xjllbs[k]
			if xb.unreinveloss:
				val = xb.unreinveloss
			else:
				val = 0.0
			xb.unreinveloss = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, 0)
		html_str += '</tr>\n'

		# 资产减值准备
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">资产减值准备</td>\n\t<td style="background: %s; color: #FFFFFF">+</td>\n' % (Cons.COLOR_GREEN, Cons.COLOR_GREEN)
		for k in keys:
			xb = self.stock.xjllbs[k]
			if xb.asseimpa:
				val = xb.asseimpa
			else:
				val = 0.0
			xb.asseimpa = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, 0)
		html_str += '</tr>\n'

		# 固定资产折旧、油气资产折耗、生产性物资折旧
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">固定资产折旧、油气资产折耗、生产性物资折旧</td>\n\t<td style="background: %s; color: #FFFFFF">+</td>\n' % (Cons.COLOR_GREEN, Cons.COLOR_GREEN)
		for k in keys:
			xb = self.stock.xjllbs[k]
			if xb.assedepr:
				val = xb.assedepr
			else:
				val = 0.0
			xb.assedepr = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, 0)
		html_str += '</tr>\n'

		# 投资性房地产折旧、摊销
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">投资性房地产折旧、摊销</td>\n\t<td style="background: %s; color: #FFFFFF">+</td>\n' % (Cons.COLOR_GREEN, Cons.COLOR_GREEN)
		for k in keys:
			xb = self.stock.xjllbs[k]
			if xb.realestadep:
				val = xb.realestadep
			else:
				val = 0.0
			xb.realestadep = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, 0)
		html_str += '</tr>\n'

		# 无形资产摊销
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">无形资产摊销</td>\n\t<td style="background: %s; color: #FFFFFF">+</td>\n' % (Cons.COLOR_GREEN, Cons.COLOR_GREEN)
		for k in keys:
			xb = self.stock.xjllbs[k]
			if xb.intaasseamor:
				val = xb.intaasseamor
			else:
				val = 0.0
			xb.intaasseamor = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, 0)
		html_str += '</tr>\n'

		# 长期待摊费用摊销 
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">长期待摊费用摊销</td>\n\t<td style="background: %s; color: #FFFFFF">+</td>\n' % (Cons.COLOR_GREEN, Cons.COLOR_GREEN)
		for k in keys:
			xb = self.stock.xjllbs[k]
			if xb.longdefeexpenamor:
				val = xb.longdefeexpenamor
			else:
				val = 0.0
			xb.longdefeexpenamor = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, 0)
		html_str += '</tr>\n'

		# 间接法现金流量表中的折旧摊销，折旧摊销 / 经营活动现金流净额
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">折旧摊销总和</td>\n\t<td style="background: %s; color: #FFFFFF">=</td>\n' % (Cons.COLOR_PURPLE, Cons.COLOR_PURPLE)
		for k in keys:
			xb = self.stock.xjllbs[k]
			val = xb.assedepr + xb.realestadep + xb.intaasseamor + xb.longdefeexpenamor
			rate = val / xb.biznetcflow * 100
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, rate)
		html_str += '<td>除以经营活动现金流净额</td></tr>\n'

		# 待摊费用的减少
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">待摊费用的减少</td>\n\t<td style="background: %s; color: #FFFFFF">+</td>\n' % (Cons.COLOR_GREEN, Cons.COLOR_GREEN)
		for k in keys:
			xb = self.stock.xjllbs[k]
			if xb.prepexpedecr:
				val = xb.prepexpedecr
			else:
				val = 0.0
			xb.prepexpedecr = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, 0)
		html_str += '</tr>\n'

		# 预提费用的增加
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">预提费用的增加</td>\n\t<td style="background: %s; color: #FFFFFF">+</td>\n' % (Cons.COLOR_GREEN, Cons.COLOR_GREEN)
		for k in keys:
			xb = self.stock.xjllbs[k]
			if xb.accrexpeincr:
				val = xb.accrexpeincr
			else:
				val = 0.0
			xb.accrexpeincr = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, 0)
		html_str += '</tr>\n'

		# 处置固定资产、无形资产和其他长期资产的损失
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">处置固定资产、无形资产和其他长期资产的损失</td>\n\t<td style="background: %s; color: #FFFFFF">+</td>\n' % (Cons.COLOR_GREEN, Cons.COLOR_GREEN)
		for k in keys:
			xb = self.stock.xjllbs[k]
			if xb.dispfixedassetloss:
				val = xb.dispfixedassetloss
			else:
				val = 0.0
			xb.dispfixedassetloss = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, 0)
		html_str += '</tr>\n'

		# 固定资产报废损失
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">固定资产报废损失</td>\n\t<td style="background: %s; color: #FFFFFF">+</td>\n' % (Cons.COLOR_GREEN, Cons.COLOR_GREEN)
		for k in keys:
			xb = self.stock.xjllbs[k]
			if xb.fixedassescraloss:
				val = xb.fixedassescraloss
			else:
				val = 0.0
			xb.fixedassescraloss = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, 0)
		html_str += '</tr>\n'

		# 公允价值变动损失
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">公允价值变动损失</td>\n\t<td style="background: %s; color: #FFFFFF">+</td>\n' % (Cons.COLOR_GREEN, Cons.COLOR_GREEN)
		for k in keys:
			xb = self.stock.xjllbs[k]
			if xb.valuechgloss:
				val = xb.valuechgloss
			else:
				val = 0.0
			xb.valuechgloss = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, 0)
		html_str += '</tr>\n'

		# 递延收益增加（减：减少）
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">递延收益增加（减：减少）</td>\n\t<td style="background: %s; color: #FFFFFF">+</td>\n' % (Cons.COLOR_GREEN, Cons.COLOR_GREEN)
		for k in keys:
			xb = self.stock.xjllbs[k]
			if xb.defeincoincr:
				val = xb.defeincoincr
			else:
				val = 0.0
			xb.defeincoincr = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, 0)
		html_str += '</tr>\n'

		# 预计负债
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">预计负债</td>\n\t<td style="background: %s; color: #FFFFFF">+</td>\n' % (Cons.COLOR_GREEN, Cons.COLOR_GREEN)
		for k in keys:
			xb = self.stock.xjllbs[k]
			if xb.estidebts:
				val = xb.estidebts
			else:
				val = 0.0
			xb.estidebts = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, 0)
		html_str += '</tr>\n'

		# 财务费用
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">财务费用</td>\n\t<td style="background: %s; color: #FFFFFF">-</td>\n' % (Cons.COLOR_RED, Cons.COLOR_RED)
		for k in keys:
			xb = self.stock.xjllbs[k]
			if xb.finexpe:
				val = xb.finexpe
			else:
				val = 0.0
			xb.finexpe = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, 0)
		html_str += '</tr>\n'

		# 投资损失
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">投资损失</td>\n\t<td style="background: %s; color: #FFFFFF">-</td>\n' % (Cons.COLOR_RED, Cons.COLOR_RED)
		for k in keys:
			xb = self.stock.xjllbs[k]
			if xb.inveloss:
				val = xb.inveloss
			else:
				val = 0.0
			xb.inveloss = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, 0)
		html_str += '</tr>\n'

		# 递延所得税资产减少
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">递延所得税资产减少</td>\n\t<td style="background: %s; color: #FFFFFF">+</td>\n' % (Cons.COLOR_GREEN, Cons.COLOR_GREEN)
		for k in keys:
			xb = self.stock.xjllbs[k]
			if xb.defetaxassetdecr:
				val = xb.defetaxassetdecr
			else:
				val = 0.0
			xb.defetaxassetdecr = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, 0)
		html_str += '</tr>\n'

		# 递延所得税负债增加
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">递延所得税负债增加</td>\n\t<td style="background: %s; color: #FFFFFF">+</td>\n' % (Cons.COLOR_GREEN, Cons.COLOR_GREEN)
		for k in keys:
			xb = self.stock.xjllbs[k]
			if xb.defetaxliabincr:
				val = xb.defetaxliabincr
			else:
				val = 0.0
			xb.defetaxliabincr = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, 0)
		html_str += '</tr>\n'

		# 存货的减少
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">存货的减少</td>\n\t<td style="background: %s; color: #FFFFFF">+</td>\n' % (Cons.COLOR_GREEN, Cons.COLOR_GREEN)
		for k in keys:
			xb = self.stock.xjllbs[k]
			if xb.inveredu:
				val = xb.inveredu
			else:
				val = 0.0
			xb.inveredu = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, 0)
		html_str += '</tr>\n'

		# 经营性应收项目的减少
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">经营性应收项目的减少</td>\n\t<td style="background: %s; color: #FFFFFF">+</td>\n' % (Cons.COLOR_GREEN, Cons.COLOR_GREEN)
		for k in keys:
			xb = self.stock.xjllbs[k]
			if xb.receredu:
				val = xb.receredu
			else:
				val = 0.0
			xb.receredu = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, 0)
		html_str += '</tr>\n'

		# 经营性应付项目的增加
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">经营性应付项目的增加</td>\n\t<td style="background: %s; color: #FFFFFF">+</td>\n' % (Cons.COLOR_GREEN, Cons.COLOR_GREEN)
		for k in keys:
			xb = self.stock.xjllbs[k]
			if xb.payaincr:
				val = xb.payaincr
			else:
				val = 0.0
			xb.payaincr = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, 0)
		html_str += '</tr>\n'

		# 已完工尚未结算款的减少(减:增加)
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">已完工尚未结算款的减少(减:增加)</td>\n\t<td style="background: %s; color: #FFFFFF">-</td>\n' % (Cons.COLOR_RED, Cons.COLOR_RED)
		for k in keys:
			xb = self.stock.xjllbs[k]
			if xb.unseparachg:
				val = xb.unseparachg
			else:
				val = 0.0
			xb.unseparachg = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, 0)
		html_str += '</tr>\n'

		# 已结算尚未完工款的增加(减:减少)
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">已结算尚未完工款的增加(减:减少)</td>\n\t<td style="background: %s; color: #FFFFFF">-</td>\n' % (Cons.COLOR_RED, Cons.COLOR_RED)
		for k in keys:
			xb = self.stock.xjllbs[k]
			if xb.unfiparachg:
				val = xb.unfiparachg
			else:
				val = 0.0
			xb.unfiparachg = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, 0)
		html_str += '</tr>\n'

		# 其他
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">其他</td>\n\t<td style="background: %s; color: #FFFFFF">+</td>\n' % (Cons.COLOR_GREEN, Cons.COLOR_GREEN)
		for k in keys:
			xb = self.stock.xjllbs[k]
			if xb.other:
				val = xb.other
			else:
				val = 0.0
			xb.other = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, 0)
		html_str += '</tr>\n'

		# 经营活动产生现金流量净额
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">经营活动产生现金流量净额</td>\n\t<td style="background: %s; color: #FFFFFF">=</td>\n' % (Cons.COLOR_PURPLE, Cons.COLOR_PURPLE)
		for k in keys:
			xb = self.stock.xjllbs[k]
			if xb.biznetcflow:
				val = xb.biznetcflow
			else:
				val = 0.0
			xb.biznetcflow = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, 0)
		html_str += '</tr>\n'

		# 债务转为资本
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">债务转为资本</td>\n\t<td style="background: %s; color: #FFFFFF">+</td>\n' % (Cons.COLOR_GREEN, Cons.COLOR_GREEN)
		for k in keys:
			xb = self.stock.xjllbs[k]
			if xb.debtintocapi:
				val = xb.debtintocapi
			else:
				val = 0.0
			xb.debtintocapi = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, 0)
		html_str += '</tr>\n'

		# 一年内到期的可转换公司债券
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">一年内到期的可转换公司债券</td>\n\t<td style="background: %s; color: #FFFFFF">-</td>\n' % (Cons.COLOR_RED, Cons.COLOR_RED)
		for k in keys:
			xb = self.stock.xjllbs[k]
			if xb.expiconvbd:
				val = xb.expiconvbd
			else:
				val = 0.0
			xb.expiconvbd = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, 0)
		html_str += '</tr>\n'

		# 融资租入固定资产
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">融资租入固定资产</td>\n\t<td style="background: %s; color: #FFFFFF">-</td>\n' % (Cons.COLOR_RED, Cons.COLOR_RED)
		for k in keys:
			xb = self.stock.xjllbs[k]
			if xb.finfixedasset:
				val = xb.finfixedasset
			else:
				val = 0.0
			xb.finfixedasset = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, 0)
		html_str += '</tr>\n'

		# 现金的期末余额
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">现金的期末余额</td>\n\t<td style="background: %s; color: #FFFFFF">=</td>\n' % (Cons.COLOR_PURPLE, Cons.COLOR_PURPLE)
		for k in keys:
			xb = self.stock.xjllbs[k]
			if xb.cashfinalbala:
				val = xb.cashfinalbala
			else:
				val = 0.0
			xb.cashfinalbala = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, 0)
		html_str += '</tr>\n'

		# 现金的期初余额
		html_str += '<tr>\n\t<td>现金的期初余额</td>\n\t<td></td>\n'
		for k in keys:
			xb = self.stock.xjllbs[k]
			if xb.cashopenbala:
				val = xb.cashopenbala
			else:
				val = 0.0
			xb.cashopenbala = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, 0)
		html_str += '</tr>\n'

		# 现金等价物的期末余额
		html_str += '<tr>\n\t<td>现金等价物的期末余额</td>\n\t<td></td>\n'
		for k in keys:
			xb = self.stock.xjllbs[k]
			if xb.equfinalbala:
				val = xb.equfinalbala
			else:
				val = 0.0
			xb.equfinalbala = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, 0)
		html_str += '</tr>\n'

		# 现金等价物的期初余额
		html_str += '<tr>\n\t<td>现金等价物的期初余额</td>\n\t<td></td>\n'
		for k in keys:
			xb = self.stock.xjllbs[k]
			if xb.equopenbala:
				val = xb.equopenbala
			else:
				val = 0.0
			xb.equopenbala = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, 0)
		html_str += '</tr>\n'

		# 现金及现金等价物的净增加额
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">现金及现金等价物的净增加额</td>\n\t<td style="background: %s; color: #FFFFFF">=</td>\n' % (Cons.COLOR_PURPLE, Cons.COLOR_PURPLE)
		for k in keys:
			xb = self.stock.xjllbs[k]
			if xb.cashneti:
				val = xb.cashneti
			else:
				val = 0.0
			xb.cashneti = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, 0)
		html_str += '</tr>\n'
		
		# 表尾
		html_str += '</tbody>\n</table>\n\n</body>\n</html>'

		print html_str
		fname = 'db/%s_%s/现金流量表间接法.html' % (self.stock.symbol, self.stock.name)
		ResUtil.save_html_content(html_str, fname)
