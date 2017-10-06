# -*- coding: utf-8 -*-

from models.xjllb import XJLLB
from models.fjsj import FJSJ
from models.stock import Stock
from utils.util_res import ResUtil
import utils.util_cons as Cons

class CashDrawer(object):
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

		html_str += '<body>\n<h4>现金流量表</h4>\n\n<table class="table table-bordered">\n\t<caption>直接法编制</caption>\n<thead><tr>\n\t<th>项目</th>\n\t<th>所属分类</th>'

		keys = [k for k in sorted(self.stock.xjllbs)]
		keys.reverse()

		# 表头
		for k in keys:
			tmpstr = '\t<th colspan="2">%s</th>\n' % k
			html_str += tmpstr
		html_str += '\t<th>备注</th>\n</tr>\n</thead>\n<tbody>\n'

		# 一、经营活动现金流

		# 销售商品、提供劳务收到的现金
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">销售商品、提供劳务收到的现金</td>\n\t<td style="background: %s; color: #FFFFFF">经营活动 +</td>\n' % (Cons.COLOR_PINK, Cons.COLOR_PINK)
		for k in keys:
			xb = self.stock.xjllbs[k]
			if xb.laborgetcash:
				val = xb.laborgetcash
			else:
				val = 0.0
			xb.laborgetcash = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, 0)
		html_str += '</tr>\n'

		# 销售商品、提供劳务收到的现金 / 营业收入
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">销售商品、提供劳务收到的现金 / 营业收入</td>\n\t<td style="background: %s; color: #FFFFFF">经营活动 +</td>\n' % (Cons.COLOR_PINK, Cons.COLOR_PINK)
		for k in keys:
			gb = self.stock.gslrbs[k]
			xb = self.stock.xjllbs[k]
			val = xb.laborgetcash / gb.bizinco
			html_str += '\t<td>%.2f</td>\n\t<td></td>\n' % (val)
		html_str += '</tr>\n'

		# 收到的其他与经营活动有关的现金
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">收到的其他与经营活动有关的现金</td>\n\t<td style="background: %s; color: #FFFFFF">经营活动 +</td>\n' % (Cons.COLOR_PINK, Cons.COLOR_PINK)
		for k in keys:
			xb = self.stock.xjllbs[k]
			if xb.receotherbizcash:
				val = xb.receotherbizcash
			else:
				val = 0.0
			xb.receotherbizcash = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, 0)
		html_str += '</tr>\n'

		# 经营活动现金流入小计
		html_str += '<tr bgcolor="white">\n\t<td>经营活动现金流入小计</td>\n\t<td>经营活动 +</td>\n'
		for k in keys:
			xb = self.stock.xjllbs[k]
			if xb.bizcashinfl:
				val = xb.bizcashinfl
			else:
				val = 0.0
			xb.bizcashinfl = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, 0)
		html_str += '</tr>\n'

		# 购买商品、接受劳务支付的现金
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">购买商品、接受劳务支付的现金</td>\n\t<td style="background: %s; color: #FFFFFF">经营活动 -</td>\n' % (Cons.COLOR_PINK, Cons.COLOR_PINK)
		for k in keys:
			xb = self.stock.xjllbs[k]
			if xb.labopayc:
				val = xb.labopayc
			else:
				val = 0.0
			xb.labopayc = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, 0)
		html_str += '</tr>\n'

		# 支付给职工以及为职工支付的现金
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">支付给职工以及为职工支付的现金</td>\n\t<td style="background: %s; color: #FFFFFF">经营活动 -</td>\n' % (Cons.COLOR_PINK, Cons.COLOR_PINK)
		for k in keys:
			xb = self.stock.xjllbs[k]
			if xb.payworkcash:
				val = xb.payworkcash
			else:
				val = 0.0
			xb.payworkcash = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, 0)
		html_str += '</tr>\n'

		# 支付的各项税费
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">支付的各项税费</td>\n\t<td style="background: %s; color: #FFFFFF">经营活动 -</td>\n' % (Cons.COLOR_PINK, Cons.COLOR_PINK)
		for k in keys:
			xb = self.stock.xjllbs[k]
			if xb.paytax:
				val = xb.paytax
			else:
				val = 0.0
			xb.paytax = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, 0)
		html_str += '</tr>\n'

		# 支付的其他与经营活动有关的现金
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">支付的其他与经营活动有关的现金</td>\n\t<td style="background: %s; color: #FFFFFF">经营活动 -</td>\n' % (Cons.COLOR_PINK, Cons.COLOR_PINK)
		for k in keys:
			xb = self.stock.xjllbs[k]
			if xb.payacticash:
				val = xb.payacticash
			else:
				val = 0.0
			xb.payacticash = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, 0)
		html_str += '</tr>\n'

		# 经营活动现金流出小计
		html_str += '<tr bgcolor="white">\n\t<td>经营活动现金流出小计</td>\n\t<td>经营活动 -</td>\n'
		for k in keys:
			xb = self.stock.xjllbs[k]
			if xb.bizcashoutf:
				val = xb.bizcashoutf
			else:
				val = 0.0
			xb.bizcashoutf = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, 0)
		html_str += '</tr>\n'

		# 经营活动产生的现金流量净额
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">经营活动产生的现金流量净额</td>\n\t<td style="background: %s; color: #FFFFFF">经营活动</td>\n' % (Cons.COLOR_YELLOW, Cons.COLOR_YELLOW)
		for k in keys:
			xb = self.stock.xjllbs[k]
			if xb.mananetr:
				val = xb.mananetr
			else:
				val = 0.0
			xb.mananetr = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, 0)
		html_str += '</tr>\n'

		# 经营现金流净额 / 应收款
		html_str += '<tr>\n\t<td bgcolor="white">经营现金流净额 / 应收款</td>\n\t<td></td>\n'
		for k in keys:
			zb = self.stock.zcfzbs[k]
			xb = self.stock.xjllbs[k]

			val = 0.0
			val += zb.notesrece
			val += zb.accorece
			val += zb.interece
			val += zb.dividrece
			val += zb.otherrece
			val += zb.longrece
			rectot = val

			val = xb.mananetr / rectot

			html_str += '\t<td>%.2f</td>\n\t<td></td>\n' % (val)
		html_str += '</tr>\n'

		# 二、投资活动现金流

		# 收回投资所收到的现金
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">收回投资所收到的现金</td>\n\t<td style="background: %s; color: #FFFFFF">投资活动 +</td>\n' % (Cons.COLOR_GREEN, Cons.COLOR_GREEN)
		for k in keys:
			xb = self.stock.xjllbs[k]
			if xb.withinvgetcash:
				val = xb.withinvgetcash
			else:
				val = 0.0
			xb.withinvgetcash = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, 0)
		html_str += '</tr>\n'

		# 取得投资收益收到的现金
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">取得投资收益收到的现金</td>\n\t<td style="background: %s; color: #FFFFFF">投资活动 +</td>\n' % (Cons.COLOR_GREEN, Cons.COLOR_GREEN)
		for k in keys:
			xb = self.stock.xjllbs[k]
			if xb.inveretugetcash:
				val = xb.inveretugetcash
			else:
				val = 0.0
			xb.inveretugetcash = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, 0)
		html_str += '</tr>\n'

		# 处置固定资产、无形资产和其他长期资产所回收的现金净额
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">处置固定资产、无形资产和其他长期资产所回收的现金净额</td>\n\t<td style="background: %s; color: #FFFFFF">投资活动 +</td>\n' % (Cons.COLOR_GREEN, Cons.COLOR_GREEN)
		for k in keys:
			xb = self.stock.xjllbs[k]
			if xb.fixedassetnetc:
				val = xb.fixedassetnetc
			else:
				val = 0.0
			xb.fixedassetnetc = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, 0)
		html_str += '</tr>\n'

		# 处置子公司及其他营业单位收到的现金净额
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">处置子公司及其他营业单位收到的现金净额</td>\n\t<td style="background: %s; color: #FFFFFF">投资活动 +</td>\n' % (Cons.COLOR_GREEN, Cons.COLOR_GREEN)
		for k in keys:
			xb = self.stock.xjllbs[k]
			if xb.subsnetc:
				val = xb.subsnetc
			else:
				val = 0.0
			xb.subsnetc = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, 0)
		html_str += '</tr>\n'

		# 收到的其他与投资活动有关的现金
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">收到的其他与投资活动有关的现金</td>\n\t<td style="background: %s; color: #FFFFFF">投资活动 +</td>\n' % (Cons.COLOR_GREEN, Cons.COLOR_GREEN)
		for k in keys:
			xb = self.stock.xjllbs[k]
			if xb.receinvcash:
				val = xb.receinvcash
			else:
				val = 0.0
			xb.receinvcash = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, 0)
		html_str += '</tr>\n'

		# 减少质押和定期存款所收到的现金
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">减少质押和定期存款所收到的现金</td>\n\t<td style="background: %s; color: #FFFFFF">投资活动 +</td>\n' % (Cons.COLOR_GREEN, Cons.COLOR_GREEN)
		for k in keys:
			xb = self.stock.xjllbs[k]
			if xb.reducashpled:
				val = xb.reducashpled
			else:
				val = 0.0
			xb.reducashpled = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, 0)
		html_str += '</tr>\n'

		# 投资活动现金流入小计
		html_str += '<tr bgcolor="white">\n\t<td>投资活动现金流入小计</td>\n\t<td>投资活动 +</td>\n'
		for k in keys:
			xb = self.stock.xjllbs[k]
			if xb.invcashinfl:
				val = xb.invcashinfl
			else:
				val = 0.0
			xb.invcashinfl = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, 0)
		html_str += '</tr>\n'

		# 购建固定资产、无形资产和其他长期资产所支付的现金
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">购建固定资产、无形资产和其他长期资产所支付的现金</td>\n\t<td style="background: %s; color: #FFFFFF">投资活动 -</td>\n' % (Cons.COLOR_GREEN, Cons.COLOR_GREEN)
		for k in keys:
			xb = self.stock.xjllbs[k]
			if xb.acquassetcash:
				val = xb.acquassetcash
			else:
				val = 0.0
			xb.acquassetcash = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, 0)
		html_str += '</tr>\n'

		# 购买固定资产、无形资产等支出 / 经营现金流净额
		html_str += '<tr>\n\t<td>购买固定资产、无形资产等支出 / 经营现金流净额</td>\n\t<td>投资活动 -</td>\n'
		for k in keys:
			xb = self.stock.xjllbs[k]
			val = xb.acquassetcash / xb.mananetr
			html_str += '\t<td>%.2f</td>\n\t<td></td>\n' % (val)
		html_str += '</tr>\n'

		# 投资所支付的现金
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">投资所支付的现金</td>\n\t<td style="background: %s; color: #FFFFFF">投资活动 -</td>\n' % (Cons.COLOR_GREEN, Cons.COLOR_GREEN)
		for k in keys:
			xb = self.stock.xjllbs[k]
			if xb.invpayc:
				val = xb.invpayc
			else:
				val = 0.0
			xb.invpayc = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, 0)
		html_str += '</tr>\n'

		# 质押贷款净增加额
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">质押贷款净增加额</td>\n\t<td style="background: %s; color: #FFFFFF">投资活动 -</td>\n' % (Cons.COLOR_GREEN, Cons.COLOR_GREEN)
		for k in keys:
			xb = self.stock.xjllbs[k]
			if xb.loannetr:
				val = xb.loannetr
			else:
				val = 0.0
			xb.loannetr = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, 0)
		html_str += '</tr>\n'

		# 取得子公司及其他营业单位支付的现金净额
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">取得子公司及其他营业单位支付的现金净额</td>\n\t<td style="background: %s; color: #FFFFFF">投资活动 -</td>\n' % (Cons.COLOR_GREEN, Cons.COLOR_GREEN)
		for k in keys:
			xb = self.stock.xjllbs[k]
			if xb.subspaynetcash:
				val = xb.subspaynetcash
			else:
				val = 0.0
			xb.subspaynetcash = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, 0)
		html_str += '</tr>\n'

		# 支付的其他与投资活动有关的现金
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">支付的其他与投资活动有关的现金</td>\n\t<td style="background: %s; color: #FFFFFF">投资活动 -</td>\n' % (Cons.COLOR_GREEN, Cons.COLOR_GREEN)
		for k in keys:
			xb = self.stock.xjllbs[k]
			if xb.payinvecash:
				val = xb.payinvecash
			else:
				val = 0.0
			xb.payinvecash = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, 0)
		html_str += '</tr>\n'

		# 增加质押和定期存款所支付的现金
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">增加质押和定期存款所支付的现金</td>\n\t<td style="background: %s; color: #FFFFFF">投资活动 -</td>\n' % (Cons.COLOR_GREEN, Cons.COLOR_GREEN)
		for k in keys:
			xb = self.stock.xjllbs[k]
			if xb.incrcashpled:
				val = xb.incrcashpled
			else:
				val = 0.0
			xb.incrcashpled = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, 0)
		html_str += '</tr>\n'

		# 投资活动现金流出小计
		html_str += '<tr bgcolor="white">\n\t<td>投资活动现金流出小计</td>\n\t<td>投资活动 -</td>\n'
		for k in keys:
			xb = self.stock.xjllbs[k]
			if xb.invcashoutf:
				val = xb.invcashoutf
			else:
				val = 0.0
			xb.invcashoutf = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, 0)
		html_str += '</tr>\n'

		# 投资活动产生的现金流量净额
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">投资活动产生的现金流量净额</td>\n\t<td style="background: %s; color: #FFFFFF">投资活动</td>\n' % (Cons.COLOR_YELLOW, Cons.COLOR_YELLOW)
		for k in keys:
			xb = self.stock.xjllbs[k]
			if xb.invnetcashflow:
				val = xb.invnetcashflow
			else:
				val = 0.0
			xb.invnetcashflow = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, 0)
		html_str += '</tr>\n'

		# 三、筹资活动现金流

		# 吸收投资收到的现金
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">吸收投资收到的现金</td>\n\t<td style="background: %s; color: #FFFFFF">筹资活动 +</td>\n' % (Cons.COLOR_RED, Cons.COLOR_RED)
		for k in keys:
			xb = self.stock.xjllbs[k]
			if xb.invrececash:
				val = xb.invrececash
			else:
				val = 0.0
			xb.invrececash = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, 0)
		html_str += '</tr>\n'

		# 其中：子公司吸收少数股东投资收到的现金
		html_str += '<tr>\n\t<td>其中：子公司吸收少数股东投资收到的现金</td>\n\t<td>筹资活动 +</td>\n'
		for k in keys:
			xb = self.stock.xjllbs[k]
			if xb.subsrececash:
				val = xb.subsrececash
			else:
				val = 0.0
			xb.subsrececash = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, 0)
		html_str += '</tr>\n'

		# 取得借款收到的现金
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">取得借款收到的现金</td>\n\t<td style="background: %s; color: #FFFFFF">筹资活动 +</td>\n' % (Cons.COLOR_RED, Cons.COLOR_RED)
		for k in keys:
			xb = self.stock.xjllbs[k]
			if xb.recefromloan:
				val = xb.recefromloan
			else:
				val = 0.0
			xb.recefromloan = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, 0)
		html_str += '</tr>\n'

		# 发行债券收到的现金
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">发行债券收到的现金</td>\n\t<td style="background: %s; color: #FFFFFF">筹资活动 +</td>\n' % (Cons.COLOR_RED, Cons.COLOR_RED)
		for k in keys:
			xb = self.stock.xjllbs[k]
			if xb.issbdrececash:
				val = xb.issbdrececash
			else:
				val = 0.0
			xb.issbdrececash = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, 0)
		html_str += '</tr>\n'

		# 收到其他与筹资活动有关的现金
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">收到其他与筹资活动有关的现金</td>\n\t<td style="background: %s; color: #FFFFFF">筹资活动 +</td>\n' % (Cons.COLOR_RED, Cons.COLOR_RED)
		for k in keys:
			xb = self.stock.xjllbs[k]
			if xb.recefincash:
				val = xb.recefincash
			else:
				val = 0.0
			xb.recefincash = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, 0)
		html_str += '</tr>\n'

		# 筹资活动现金流入小计
		html_str += '<tr bgcolor="white">\n\t<td>筹资活动现金流入小计</td>\n\t<td>筹资活动 +</td>\n'
		for k in keys:
			xb = self.stock.xjllbs[k]
			if xb.fincashinfl:
				val = xb.fincashinfl
			else:
				val = 0.0
			xb.fincashinfl = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, 0)
		html_str += '</tr>\n'

		# 偿还债务支付的现金
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">偿还债务支付的现金</td>\n\t<td style="background: %s; color: #FFFFFF">筹资活动 -</td>\n' % (Cons.COLOR_RED, Cons.COLOR_RED)
		for k in keys:
			xb = self.stock.xjllbs[k]
			if xb.debtpaycash:
				val = xb.debtpaycash
			else:
				val = 0.0
			xb.debtpaycash = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, 0)
		html_str += '</tr>\n'

		# 分配股利、利润或偿付利息所支付的现金
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">分配股利、利润或偿付利息所支付的现金</td>\n\t<td style="background: %s; color: #FFFFFF">筹资活动 -</td>\n' % (Cons.COLOR_RED, Cons.COLOR_RED)
		for k in keys:
			xb = self.stock.xjllbs[k]
			if xb.diviprofpaycash:
				val = xb.diviprofpaycash
			else:
				val = 0.0
			xb.diviprofpaycash = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, 0)
		html_str += '</tr>\n'

		# 其中：子公司支付给少数股东的股利，利润
		html_str += '<tr>\n\t<td>其中：子公司支付给少数股东的股利，利润</td>\n\t<td>筹资活动 -</td>\n'
		for k in keys:
			xb = self.stock.xjllbs[k]
			if xb.subspaydivid:
				val = xb.subspaydivid
			else:
				val = 0.0
			xb.subspaydivid = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, 0)
		html_str += '</tr>\n'

		# 支付其他与筹资活动有关的现金
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">支付其他与筹资活动有关的现金</td>\n\t<td style="background: %s; color: #FFFFFF">筹资活动 -</td>\n' % (Cons.COLOR_RED, Cons.COLOR_RED)
		for k in keys:
			xb = self.stock.xjllbs[k]
			if xb.finrelacash:
				val = xb.finrelacash
			else:
				val = 0.0
			xb.finrelacash = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, 0)
		html_str += '</tr>\n'

		# 筹资活动现金流出小计
		html_str += '<tr bgcolor="white">\n\t<td>筹资活动现金流出小计</td>\n\t<td>筹资活动 -</td>\n'
		for k in keys:
			xb = self.stock.xjllbs[k]
			if xb.fincashoutf:
				val = xb.fincashoutf
			else:
				val = 0.0
			xb.fincashoutf = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, 0)
		html_str += '</tr>\n'

		# 筹资活动产生的现金流量净额
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">筹资活动产生的现金流量净额</td>\n\t<td style="background: %s; color: #FFFFFF">筹资活动</td>\n' % (Cons.COLOR_YELLOW, Cons.COLOR_YELLOW)
		for k in keys:
			xb = self.stock.xjllbs[k]
			if xb.finnetcflow:
				val = xb.finnetcflow
			else:
				val = 0.0
			xb.finnetcflow = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, 0)
		html_str += '</tr>\n'

		# 权益性筹资的发行价
		html_str += '<tr bgcolor="white">\n\t<td>权益性筹资的发行价</td>\n\t<td>筹资活动</td>\n'
		for k in keys:
			if not k in self.stock.fjsjs:
				fj = FJSJ()
			else:
				fj = self.stock.fjsjs[k]

			if fj.equfinpubpri:
				val = fj.equfinpubpri
			else:
				val = 0.0
			fj.equfinpubpri = val
			html_str += '\t<td>%.2f</td>\n\t<td></td>\n' % (val)
		html_str += '</tr>\n'

		# 债务性筹资的利率
		html_str += '<tr bgcolor="white">\n\t<td>债务性筹资的利率</td>\n\t<td>筹资活动</td>\n'
		for k in keys:
			if not k in self.stock.fjsjs:
				fj = FJSJ()
			else:
				fj = self.stock.fjsjs[k]

			if fj.debtfininrate:
				val = fj.debtfininrate
			else:
				val = 0.0
			fj.debtfininrate = val
			html_str += '\t<td>%.2f%%</td>\n\t<td></td>\n' % (val)
		html_str += '</tr>\n'

		# 四、汇总

		# 汇率变动对现金及现金等价物的影响
		html_str += '<tr bgcolor="white">\n\t<td>汇率变动对现金及现金等价物的影响</td>\n\t<td></td>\n'
		for k in keys:
			xb = self.stock.xjllbs[k]
			if xb.chgexchgchgs:
				val = xb.chgexchgchgs
			else:
				val = 0.0
			xb.chgexchgchgs = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, 0)
		html_str += '</tr>\n'

		# 现金及现金等价物净增加额
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">现金及现金等价物净增加额</td>\n\t<td></td>\n' % Cons.COLOR_PURPLE
		for k in keys:
			xb = self.stock.xjllbs[k]
			if xb.cashnetr:
				val = xb.cashnetr
			else:
				val = 0.0
			xb.cashnetr = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, 0)
		html_str += '</tr>\n'

		# 期初现金及现金等价物余额
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">期初现金及现金等价物余额</td>\n\t<td></td>\n' % Cons.COLOR_PURPLE
		for k in keys:
			xb = self.stock.xjllbs[k]
			if xb.inicashbala:
				val = xb.inicashbala
			else:
				val = 0.0
			xb.inicashbala = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, 0)
		html_str += '</tr>\n'

		# 期末现金及现金等价物余额
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">期末现金及现金等价物余额</td>\n\t<td></td>\n' % Cons.COLOR_PURPLE
		for k in keys:
			xb = self.stock.xjllbs[k]
			if xb.finalcashbala:
				val = xb.finalcashbala
			else:
				val = 0.0
			xb.finalcashbala = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, 0)
		html_str += '</tr>\n'

		# 期末现金及现金等价物余额 / 有息负债
		html_str += '<tr bgcolor="white">\n\t<td>期末现金及现金等价物余额 / 有息负债</td>\n\t<td></td>\n'
		for k in keys:
			zb = self.stock.zcfzbs[k]
			xb = self.stock.xjllbs[k]

			borr = zb.shorttermborr + zb.longborr
			if borr == 0:
				val = 0
			else:
				val = xb.finalcashbala / borr
			html_str += '\t<td>%.2f</td>\n\t<td></td>\n' % (val)
		html_str += '</tr>\n'

		# 期末现金及现金等价物余额 + 应收票据中的银行承兑汇票 > 有息负债
		html_str += '<tr bgcolor="white">\n\t<td>期末现金及现金等价物余额 + 应收票据中的银行承兑汇票 / 有息负债</td>\n\t<td></td>\n'
		for k in keys:
			zb = self.stock.zcfzbs[k]
			xb = self.stock.xjllbs[k]
			if not k in self.stock.fjsjs:
				fj = FJSJ()
			else:
				fj = self.stock.fjsjs[k]

			borr = zb.shorttermborr + zb.longborr
			if borr == 0:
				val = 0
			else:
				val = (xb.finalcashbala + fj.notesrece_bank) / borr
			html_str += '\t<td>%.2f</td>\n\t<td></td>\n' % (val)
		html_str += '</tr>\n'

		# 加权平均净资产现金回收率 = 经营现金流净额 / 平均净资产
		html_str += '<tr bgcolor="white">\n\t<td>加权平均净资产现金回收率</td>\n\t<td></td>\n'
		for k in keys:
			xb = self.stock.xjllbs[k]

			zb_cur = self.stock.zcfzbs[k]
			k1 = '%s' % (int(k) - 1)
			if k1 in self.stock.zcfzbs:
				zb_lst = self.stock.zcfzbs[k1]
				righaggr = (zb_cur.righaggr + zb_lst.righaggr) / 2
			else:
				righaggr = zb_cur.righaggr

			val = xb.mananetr / righaggr * 100
			html_str += '\t<td>%.2f%%</td>\n\t<td></td>\n' % (val)
		html_str += '<td>经营现金流净额 / 平均净资产</td></tr>\n'

		# 加权平均总资产现金回收率 = 经营现金流净额 / 平均总资产
		html_str += '<tr bgcolor="white">\n\t<td>加权平均总资产现金回收率</td>\n\t<td></td>\n'
		for k in keys:
			xb = self.stock.xjllbs[k]

			zb_cur = self.stock.zcfzbs[k]
			k1 = '%s' % (int(k) - 1)
			if k1 in self.stock.zcfzbs:
				zb_lst = self.stock.zcfzbs[k1]
				totassetave = (zb_cur.totasset + zb_lst.totasset) / 2
			else:
				totassetave = zb_cur.totasset

			val = xb.mananetr / totassetave * 100
			html_str += '\t<td>%.2f%%</td>\n\t<td></td>\n' % (val)
		html_str += '<td>经营现金流净额 / 平均总资产</td></tr>\n'

		# 简化的自由现金流 = 经营现金流净额 - 投资活动现金流出净额
		html_str += '<tr>\n\t<td>简化的自由现金流</td>\n\t<td></td>\n'
		for k in keys:
			xb = self.stock.xjllbs[k]
			if xb.invnetcashflow < 0:
				outflow = -xb.invnetcashflow
			else:
				outflow = 0
			val = xb.mananetr - outflow
			if val > 0:
				color = Cons.COLOR_GREEN
			else:
				color = Cons.COLOR_RED
			html_str += '\t<td style="background: %s; color: #FFFFFF">%.2f亿</td>\n\t<td></td>\n' % (color, val / Cons.Yi)
		html_str += '<td>经营现金流净额 - 投资活动现金流出净额</td></tr>\n'

		# 所属类型(奶牛/母鸡/蛮牛等)
		html_str += '<tr>\n\t<td>所属类型</td>\n\t<td></td>\n'
		for k in keys:
			xb = self.stock.xjllbs[k]

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
			html_str += '\t<td style="background: %s; color: #FFFFFF">%s</td>\n\t<td></td>\n' % (color, val)
		html_str += '</tr>\n'
		
		# 表尾
		html_str += '</tbody>\n</table>\n\n</body>\n</html>'

		print html_str
		fname = 'db/%s_%s/现金流量表.html' % (self.stock.symbol, self.stock.name)
		ResUtil.save_html_content(html_str, fname)
