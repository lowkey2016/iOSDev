# -*- coding: utf-8 -*-

from models.zcfzb import ZCFZB
from models.fjsj import FJSJ
from models.stock import Stock
from utils.util_res import ResUtil
import utils.util_cons as Cons

class LiabsDrawer(object):
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

		html_str += '<body>\n<h4>资产负债表</h4>\n\n<table class="table table-bordered">\n\t<caption>负债部分</caption>\n<thead><tr>\n\t<th>项目</th>\n\t<th>所属分类</th>'

		keys = [k for k in sorted(self.stock.zcfzbs)]
		keys.reverse()

		# 表头
		for k in keys:
			tmpstr = '\t<th colspan="2">%s</th>\n' % k
			html_str += tmpstr
		html_str += '\t<th>备注</th>\n</tr></thead>\n<tbody>'

		# 一、融资性负债
		# 短期借款
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">短期借款</td>\n\t<td style="background: %s; color: #FFFFFF">融资性负债</td>\n' % (Cons.COLOR_RED, Cons.COLOR_RED)
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if zb.shorttermborr:
				val = zb.shorttermborr
			else:
				val = 0.0
			zb.shorttermborr = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / zb.totliab * 100)
		html_str += '</tr>\n'

		# 长期借款
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">长期借款</td>\n\t<td style="background: %s; color: #FFFFFF">融资性负债</td>\n' % (Cons.COLOR_RED, Cons.COLOR_RED)
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if zb.longborr:
				val = zb.longborr
			else:
				val = 0.0
			zb.longborr = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / zb.totliab * 100)
		html_str += '</tr>\n'

		# 应付短期债券
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">应付短期债券</td>\n\t<td style="background: %s; color: #FFFFFF">融资性负债</td>\n' % (Cons.COLOR_RED, Cons.COLOR_RED)
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if zb.shorttermbdspaya:
				val = zb.shorttermbdspaya
			else:
				val = 0.0
			zb.shorttermbdspaya = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / zb.totliab * 100)
		html_str += '</tr>\n'

		# 应付债券
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">应付债券</td>\n\t<td style="background: %s; color: #FFFFFF">融资性负债</td>\n' % (Cons.COLOR_RED, Cons.COLOR_RED)
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if zb.bdspaya:
				val = zb.bdspaya
			else:
				val = 0.0
			zb.bdspaya = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / zb.totliab * 100)
		html_str += '</tr>\n'

		# 合计
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">融资性负债合计</td>\n\t<td></td>\n' % Cons.COLOR_RED
		for k in keys:
			zb = self.stock.zcfzbs[k]
			val = 0.0
			val += zb.shorttermborr
			val += zb.longborr
			val += zb.shorttermbdspaya
			val += zb.bdspaya
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / zb.totliab * 100)
		html_str += '</tr>\n'

		# 二、经营性负债
		# 应付票据
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">应付票据</td>\n\t<td style="background: %s; color: #FFFFFF">经营性负债</td>\n' % (Cons.COLOR_PINK, Cons.COLOR_PINK)
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if zb.notespaya:
				val = zb.notespaya
			else:
				val = 0.0
			zb.notespaya = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / zb.totliab * 100)
		html_str += '</tr>\n'

		# 应付账款
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">应付账款</td>\n\t<td style="background: %s; color: #FFFFFF">经营性负债</td>\n' % (Cons.COLOR_PINK, Cons.COLOR_PINK)
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if zb.accopaya:
				val = zb.accopaya
			else:
				val = 0.0
			zb.accopaya = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / zb.totliab * 100)
		html_str += '</tr>\n'

		# 预收款项
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">预收款项</td>\n\t<td style="background: %s; color: #FFFFFF">经营性负债</td>\n' % (Cons.COLOR_PINK, Cons.COLOR_PINK)
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if zb.advapaym:
				val = zb.advapaym
			else:
				val = 0.0
			zb.advapaym = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / zb.totliab * 100)
		html_str += '</tr>\n'

		# 应付职工薪酬
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">应付职工薪酬</td>\n\t<td style="background: %s; color: #FFFFFF">经营性负债</td>\n' % (Cons.COLOR_PINK, Cons.COLOR_PINK)
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if zb.copeworkersal:
				val = zb.copeworkersal
			else:
				val = 0.0
			zb.copeworkersal = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / zb.totliab * 100)
		html_str += '</tr>\n'

		# 员工本年度薪酬总额
		html_str += '<tr bgcolor="white">\n\t<td>员工本年度薪酬</td>\n\t<td>经营性负债</td>\n'
		for k in keys:
			k1 = '%s' % (int(k) - 1)
			if k1 in self.stock.zcfzbs:
				zb_lst = self.stock.zcfzbs[k1]
			else:
				zb_lst = ZCFZB()
			zb_cur = self.stock.zcfzbs[k]
			xb = self.stock.xjllbs[k]
			if not k in self.stock.fjsjs:
				fj = FJSJ()
			else:
				fj = self.stock.fjsjs[k]

			if zb_lst.copeworkersal == 0 or fj.emplyescnt == 0:
				val = 0
				ave = 0
			else:
				val = zb_cur.copeworkersal - zb_lst.copeworkersal + xb.payworkcash
				ave = val / fj.emplyescnt
			html_str += '\t<td>%.2f亿</td>\n\t<td>平均%.2f</td>\n' % (val / Cons.Yi, ave)
		html_str += '<td>先总额，后平均</td></tr>\n'

		# 员工总数
		html_str += '<tr bgcolor="white">\n\t<td>员工总数</td>\n\t<td>经营性负债</td>\n'
		for k in keys:
			if not k in self.stock.fjsjs:
				fj = FJSJ()
			else:
				fj = self.stock.fjsjs[k]

			if fj.emplyescnt:
				val = fj.emplyescnt
			else:
				val = 0.0
			fj.emplyescnt = val
			html_str += '\t<td>%d人</td>\n\t<td></td>\n' % (val)
		html_str += '</tr>\n'

		# 应付利息
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">应付利息</td>\n\t<td style="background: %s; color: #FFFFFF">经营性负债</td>\n' % (Cons.COLOR_PINK, Cons.COLOR_PINK)
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if zb.intepaya:
				val = zb.intepaya
			else:
				val = 0.0
			zb.intepaya = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / zb.totliab * 100)
		html_str += '</tr>\n'

		# 其他应付款
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">其他应付款</td>\n\t<td style="background: %s; color: #FFFFFF">经营性负债</td>\n' % (Cons.COLOR_PINK, Cons.COLOR_PINK)
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if zb.otherpay:
				val = zb.otherpay
			else:
				val = 0.0
			zb.otherpay = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / zb.totliab * 100)
		html_str += '</tr>\n'

		# 长期应付款
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">长期应付款</td>\n\t<td style="background: %s; color: #FFFFFF">经营性负债</td>\n' % (Cons.COLOR_PINK, Cons.COLOR_PINK)
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if zb.longpaya:
				val = zb.longpaya
			else:
				val = 0.0
			zb.longpaya = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / zb.totliab * 100)
		html_str += '</tr>\n'

		# 专项应付款
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">专项应付款</td>\n\t<td style="background: %s; color: #FFFFFF">经营性负债</td>\n' % (Cons.COLOR_PINK, Cons.COLOR_PINK)
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if zb.specpaya:
				val = zb.specpaya
			else:
				val = 0.0
			zb.specpaya = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / zb.totliab * 100)
		html_str += '</tr>\n'

		# 合计
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">经营性负债合计</td>\n\t<td></td>\n' % Cons.COLOR_PINK
		for k in keys:
			zb = self.stock.zcfzbs[k]
			val = 0.0
			val += zb.notespaya
			val += zb.accopaya
			val += zb.advapaym
			val += zb.copeworkersal
			val += zb.intepaya
			val += zb.otherpay
			val += zb.longpaya
			val += zb.specpaya
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / zb.totliab * 100)
		html_str += '</tr>\n'

		# 应交税费
		html_str += '<tr">\n\t<td style="background: %s; color: #FFFFFF">应交税费</td>\n\t<td style="background: %s; color: #FFFFFF">分配性负债</td>\n' % (Cons.COLOR_GREEN, Cons.COLOR_GREEN)
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if zb.taxespaya:
				val = zb.taxespaya
			else:
				val = 0.0
			zb.taxespaya = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / zb.totliab * 100)
		html_str += '</tr>\n'

		# 应付股利
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">应付股利</td>\n\t<td style="background: %s; color: #FFFFFF">分配性负债</td>\n' % (Cons.COLOR_GREEN, Cons.COLOR_GREEN)
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if zb.divipaya:
				val = zb.divipaya
			else:
				val = 0.0
			zb.divipaya = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / zb.totliab * 100)
		html_str += '</tr>\n'

		# 合计
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">分配性负债合计</td>\n\t<td></td>\n' % Cons.COLOR_GREEN
		for k in keys:
			zb = self.stock.zcfzbs[k]
			val = 0.0
			val += zb.taxespaya
			val += zb.divipaya
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / zb.totliab * 100)
		html_str += '</tr>\n'

		# 交易性金融负债
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">交易性金融负债</td>\n\t<td style="background: %s; color: #FFFFFF">其它负债</td>\n' % (Cons.COLOR_BLUE, Cons.COLOR_BLUE)
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if zb.tradfinliab:
				val = zb.tradfinliab
			else:
				val = 0.0
			zb.tradfinliab = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / zb.totliab * 100)
		html_str += '</tr>\n'

		# 一年内到期的非流动负债
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">一年内到期的非流动负债</td>\n\t<td style="background: %s; color: #FFFFFF">其它负债</td>\n' % (Cons.COLOR_BLUE, Cons.COLOR_BLUE)
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if zb.duenoncliab:
				val = zb.duenoncliab
			else:
				val = 0.0
			zb.duenoncliab = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / zb.totliab * 100)
		html_str += '</tr>\n'

		# 长期递延收益
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">长期递延收益</td>\n\t<td style="background: %s; color: #FFFFFF">其它负债</td>\n' % (Cons.COLOR_BLUE, Cons.COLOR_BLUE)
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if zb.longdefeinco:
				val = zb.longdefeinco
			else:
				val = 0.0
			zb.longdefeinco = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / zb.totliab * 100)
		html_str += '</tr>\n'

		# 递延所得税负债
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">递延所得税负债</td>\n\t<td style="background: %s; color: #FFFFFF">其它负债</td>\n' % (Cons.COLOR_BLUE, Cons.COLOR_BLUE)
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if zb.defeincotaxliab:
				val = zb.defeincotaxliab
			else:
				val = 0.0
			zb.defeincotaxliab = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / zb.totliab * 100)
		html_str += '</tr>\n'

		# 其他流动负债
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">其他流动负债</td>\n\t<td style="background: %s; color: #FFFFFF">其它负债</td>\n' % (Cons.COLOR_BLUE, Cons.COLOR_BLUE)
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if zb.othercurreliabi:
				val = zb.othercurreliabi
			else:
				val = 0.0
			zb.othercurreliabi = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / zb.totliab * 100)
		html_str += '</tr>\n'

		# 其他非流动负债
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">其他非流动负债</td>\n\t<td style="background: %s; color: #FFFFFF">其它负债</td>\n' % (Cons.COLOR_BLUE, Cons.COLOR_BLUE)
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if zb.othernoncliabi:
				val = zb.othernoncliabi
			else:
				val = 0.0
			zb.othernoncliabi = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / zb.totliab * 100)
		html_str += '</tr>\n'

		# 合计
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">其它负债合计</td>\n\t<td></td>\n' % Cons.COLOR_BLUE
		for k in keys:
			zb = self.stock.zcfzbs[k]
			val = 0.0
			val += zb.tradfinliab
			val += zb.duenoncliab
			val += zb.longdefeinco
			val += zb.defeincotaxliab
			val += zb.othercurreliabi
			val += zb.othernoncliabi
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / zb.totliab * 100)
		html_str += '</tr>\n'

		# 负债合计
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">负债合计</td>\n\t<td></td>\n' % Cons.COLOR_PURPLE
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if zb.totliab:
				val = zb.totliab
			else:
				val = 0.0
			zb.totliab = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / zb.totliab * 100)
		html_str += '</tr>\n'

		# 资产合计
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">资产合计</td>\n\t<td></td>\n' % Cons.COLOR_PURPLE
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if zb.totasset:
				val = zb.totasset
			else:
				val = 0.0
			zb.totasset = val
			html_str += '\t<td>%.2f亿</td>\n\t<td></td>\n' % (val / Cons.Yi)
		html_str += '</tr>\n'

		# 所有者权益(或股东权益)合计
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">股东权益合计</td>\n\t<td></td>\n' % Cons.COLOR_PURPLE
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if zb.righaggr:
				val = zb.righaggr
			else:
				val = 0.0
			zb.righaggr = val
			html_str += '\t<td>%.2f亿</td>\n\t<td></td>\n' % (val / Cons.Yi)
		html_str += '</tr>\n'

		# 现金净流量与到期债务之比 = 经营现金净流量 / 本期到期的债务
		html_str += '<tr bgcolor="white">\n\t<td>现金净流量与到期债务之比</td><td></td>\n'
		for k in keys:
			zb = self.stock.zcfzbs[k]
			xb = self.stock.xjllbs[k]
			if zb.duenoncliab == 0:
				val = 0
			else:
				val = xb.mananetr / zb.duenoncliab
			html_str += '\t<td>%.2f</td><td></td>\n' % val
		html_str += '<td>经营现金净流量 / 一年内到期的非流动负债</td></tr>\n'

		# 现金净流量与流动负债之比 = 经营现金净流量 / 流动负债
		html_str += '<tr bgcolor="white">\n\t<td>现金净流量与流动负债之比</td><td></td>\n'
		for k in keys:
			zb = self.stock.zcfzbs[k]
			xb = self.stock.xjllbs[k]
			if zb.totalcurrliab == 0:
				val = 0
			else:
				val = xb.mananetr / zb.totalcurrliab
			html_str += '\t<td>%.2f</td><td></td>\n' % val
		html_str += '<td>经营现金净流量 / 流动负债</td></tr>\n'

		# 现金净流量与债务总额之比 = 经营现金净流量 / 债务总额
		html_str += '<tr bgcolor="white">\n\t<td>现金净流量与债务总额之比</td><td></td>\n'
		for k in keys:
			zb = self.stock.zcfzbs[k]
			xb = self.stock.xjllbs[k]
			if zb.totliab == 0:
				val = 0
			else:
				val = xb.mananetr / zb.totliab
			html_str += '\t<td>%.2f</td><td></td>\n' % val
		html_str += '<td>经营现金净流量 / 债务总额</td></tr>\n'

		# 表尾
		html_str += '</table>\n\n'


		### 有息负债明细 ###
		html_str += """
		<head>
		<link rel="stylesheet" href="https://cdn.bootcss.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">

		<!-- 最新的 Bootstrap 核心 JavaScript 文件 -->
		<script src="https://cdn.bootcss.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>
		<style>tbody tr:first-child td:nth-child(1), tbody tr:first-child td:nth-child(2) { white-space: nowrap; } thead tr:first-child th:last-child { white-space: nowrap; padding: 5px 50px; }</style>
		</head>
		"""

		html_str += '<p></p>\n\n<table class="table table-bordered">\n\t<caption>有息负债</caption>\n<thead><tr>\n\t<th>项目</th>\n\t'

		# 表头
		for k in keys:
			tmpstr = '\t<th>%s</th>\n' % k
			html_str += tmpstr
		html_str += '\t<th>备注</th>\n</tr></thead>\n<tbody>\n'

		# 短期借款明细
		html_str += '<tr bgcolor="white">\n\t<td>短期借款明细</td>\n'
		for k in keys:
			if not k in self.stock.fjsjs:
				fj = FJSJ()
			else:
				fj = self.stock.fjsjs[k]
			if fj.shorttermborrdetail:
				val = fj.shorttermborrdetail
			else:
				val = ""
			fj.shorttermborrdetail = ""
			html_str += '\t<td>%s</td>\n' % val
		html_str += '</tr>\n'

		# 长期借款明细
		html_str += '<tr bgcolor="white">\n\t<td>长期借款明细</td>\n'
		for k in keys:
			if not k in self.stock.fjsjs:
				fj = FJSJ()
			else:
				fj = self.stock.fjsjs[k]
			if fj.longborrdetail:
				val = fj.longborrdetail
			else:
				val = ""
			fj.longborrdetail = ""
			html_str += '\t<td>%s</td>\n' % val
		html_str += '</tr>\n'

		# 有息负债率 = 有息负债 / 总资产
		html_str += '<tr bgcolor="white">\n\t<td>有息负债率</td>\n'
		for k in keys:
			zb = self.stock.zcfzbs[k]
			rate = (zb.shorttermborr + zb.longborr) / zb.totasset * 100
			html_str += '\t<td>%.2f%%</td>\n' % rate
		html_str += '<td>有息负债 / 总资产</td></tr>\n'

		# 现金有息负债比率 = 现金及现金等价物余额 / 有息负债，现金及现金等价物余额指货币资金中使用不受限的钱
		html_str += '<tr bgcolor="white">\n\t<td>现金有息负债比率</td>\n'
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if not k in self.stock.fjsjs:
				fj = FJSJ()
			else:
				fj = self.stock.fjsjs[k]
			borr = zb.shorttermborr + zb.longborr
			if borr == 0:
				rate = 0
			else:	
				rate = (zb.curfds - fj.curfds_limit) / borr
			html_str += '\t<td>%.2f</td>\n' % rate
		html_str += '<td>现金及现金等价物余额 / 有息负债</td></tr>\n'
		
		# 表尾
		html_str += '</tbody></table>\n\n</body>\n</html>'

		# print html_str
		fname = 'db/%s_%s/资产负债表负债部分.html' % (self.stock.symbol, self.stock.name)
		ResUtil.save_html_content(html_str, fname)
