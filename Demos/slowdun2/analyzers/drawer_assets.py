# -*- coding: utf-8 -*-

from models.zcfzb import ZCFZB
from models.fjsj import FJSJ
from models.stock import Stock
from utils.util_res import ResUtil
import utils.util_cons as Cons

class AssetsDrawer(object):
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

		html_str += '<body>\n<h4>资产负债表</h4>\n\n<table class="table table-bordered">\n\t<caption>资产部分</caption>\n<thead><tr>\n\t<th>项目</th>\n\t<th>所属分类</th>'

		keys = [k for k in sorted(self.stock.zcfzbs)]
		keys.reverse()

		# 表头
		for k in keys:
			tmpstr = '\t<th colspan="2">%s</th>\n' % k
			html_str += tmpstr
		html_str += '\t<th>备注</th>\n</tr></thead>\n<tbody>\n'

		## 一、货币资金类资产
		# 货币资金
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">货币资金</td>\n\t<td style="background: %s; color: #FFFFFF">货币资金</td>\n' % (Cons.COLOR_GREEN, Cons.COLOR_GREEN)
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if zb.curfds:
				val = zb.curfds
			else:
				val = 0.0
			zb.curfds = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / zb.totasset * 100)
		html_str += '</tr>\n'

		# 货币资金同比年增长率
		html_str += '<tr bgcolor="white">\n\t<td>同比年增长率</td>\n\t<td>货币资金</td>\n'
		for k in keys:
			k1 = '%s' % (int(k) - 1)
			if k1 in self.stock.zcfzbs:
				zb_lst = self.stock.zcfzbs[k1]
			else:
				zb_lst = ZCFZB()
			zb_cur = self.stock.zcfzbs[k]

			if zb_lst.accorece == 0:
				val = 0.0
			else:
				val = (zb_cur.curfds / zb_lst.curfds - 1) * 100
			html_str += '\t<td>%.2f%%</td>\n\t<td></td>\n' % (val)
		html_str += '<td>(本年/去年 - 1) * 100%</td></tr>\n'

		# 货币资金中的库存现金
		html_str += '<tr>\n\t<td bgcolor="white">其中：库存现金</td>\n\t<td></td>\n'
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if not k in self.stock.fjsjs:
				fj = FJSJ()
			else:
				fj = self.stock.fjsjs[k]
			val = fj.curfds_cash
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / zb.curfds * 100)
		html_str += '<td>除以货币资金</td></tr>\n'

		# 货币资金中的银行存款
		html_str += '<tr>\n\t<td bgcolor="white">其中：银行存款</td>\n\t<td></td>\n'
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if not k in self.stock.fjsjs:
				fj = FJSJ()
			else:
				fj = self.stock.fjsjs[k]
			val = fj.curfds_bank
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / zb.curfds * 100)
		html_str += '<td>除以货币资金</td></tr>\n'

		# 货币资金中的其他货币资金
		html_str += '<tr>\n\t<td bgcolor="white">其中：其他货币资金</td>\n\t<td></td>\n'
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if not k in self.stock.fjsjs:
				fj = FJSJ()
			else:
				fj = self.stock.fjsjs[k]
			val = fj.curfds_other
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / zb.curfds * 100)
		html_str += '<td>除以货币资金</td></tr>\n'

		# 货币资金中的使用受限资金
		html_str += '<tr>\n\t<td bgcolor="white">其中：使用受限资金</td>\n\t<td></td>\n'
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if not k in self.stock.fjsjs:
				fj = FJSJ()
			else:
				fj = self.stock.fjsjs[k]
			val = fj.curfds_limit
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / zb.curfds * 100)
		html_str += '<td>除以货币资金</td></tr>\n'

		# 合计
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">货币资金合计</td>\n\t<td></td>\n' % Cons.COLOR_GREEN
		for k in keys:
			zb = self.stock.zcfzbs[k]
			val = zb.curfds
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / zb.totasset * 100)
		html_str += '</tr>\n'

		## 二、经营相关资产
		# 应收票据
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">应收票据</td>\n\t<td style="background: %s; color: #FFFFFF">经营相关资产</td>\n' % (Cons.COLOR_RED, Cons.COLOR_RED)
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if zb.notesrece:
				val = zb.notesrece
			else:
				val = 0.0
			zb.notesrece = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / zb.totasset * 100)
		html_str += '</tr>\n'

		# 应收票据中的银行承兑汇票
		html_str += '<tr>\n\t<td bgcolor="white">其中：银行承兑汇票</td>\n\t<td></td>\n'
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if not k in self.stock.fjsjs:
				fj = FJSJ()
			else:
				fj = self.stock.fjsjs[k]
			val = fj.notesrece_bank

			if zb.notesrece == 0:
				rate = 0
			else:
				rate = val / zb.notesrece * 100
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, rate)
		html_str += '<td>除以应收票据</td></tr>\n'

		# 应收票据中的商业承兑汇票
		html_str += '<tr>\n\t<td bgcolor="white">其中：商业承兑汇票</td>\n\t<td></td>\n'
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if not k in self.stock.fjsjs:
				fj = FJSJ()
			else:
				fj = self.stock.fjsjs[k]
			val = fj.notesrece_business

			if zb.notesrece == 0:
				rate = 0
			else:
				rate = val / zb.notesrece * 100
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, rate)
		html_str += '<td>除以应收票据</td></tr>\n'

		# 应收票据中的其它部分
		html_str += '<tr>\n\t<td bgcolor="white">其中：其它部分</td>\n\t<td></td>\n'
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if not k in self.stock.fjsjs:
				fj = FJSJ()
			else:
				fj = self.stock.fjsjs[k]
			val = fj.notesrece_other

			if zb.notesrece == 0:
				rate = 0
			else:
				rate = val / zb.notesrece * 100
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, rate)
		html_str += '<td>除以应收票据</td></tr>\n'

		# 应收账款
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">应收账款</td>\n\t<td style="background: %s; color: #FFFFFF">经营相关资产</td>\n' % (Cons.COLOR_RED, Cons.COLOR_RED)
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if zb.accorece:
				val = zb.accorece
			else:
				val = 0.0
			zb.accorece = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / zb.totasset * 100)
		html_str += '</tr>\n'

		# 应收账款同比年增长率
		html_str += '<tr bgcolor="white">\n\t<td>同比年增长率</td>\n\t<td>经营相关资产</td>\n'
		for k in keys:
			k1 = '%s' % (int(k) - 1)
			if k1 in self.stock.zcfzbs:
				zb_lst = self.stock.zcfzbs[k1]
			else:
				zb_lst = ZCFZB()
			zb_cur = self.stock.zcfzbs[k]

			if zb_lst.accorece == 0:
				val = 0.0
			else:
				val = (zb_cur.accorece / zb_lst.accorece - 1) * 100
			html_str += '\t<td>%.2f%%</td>\n\t<td></td>\n' % (val)
		html_str += '<td>(本年/去年 - 1) * 100%</td></tr>\n'

		# 应收账款周转率 = 营业收入 / 平均应收账款，其中：平均应收账款 = (期初应收账款总额 + 期末应收账款总额) / 2
		html_str += '<tr bgcolor="white">\n\t<td>应收账款周转率</td>\n\t<td>经营相关资产</td>\n'
		for k in keys:
			lb = self.stock.gslrbs[k]
			zb_cur = self.stock.zcfzbs[k]
			k1 = '%s' % (int(k) - 1)
			if k1 in self.stock.zcfzbs:
				zb_lst = self.stock.zcfzbs[k1]
				val = lb.bizinco / (zb_cur.accorece + zb_lst.accorece) * 2
			else:
				val = lb.bizinco / zb_cur.accorece
			html_str += '\t<td>%.2f</td>\n\t<td></td>\n' % (val)
		html_str += '<td>营业收入 / 平均应收账款</td></tr>\n'

		# 按信用风险特征组合计坏账准备的应收账款
		html_str += '<tr bgcolor="white">\n\t<td>其中：按信用风险特征组合计坏账准备的</td>\n\t<td>经营相关资产</td>\n'
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if not k in self.stock.fjsjs:
				fj = FJSJ()
			else:
				fj = self.stock.fjsjs[k]

			if fj.accorece_credit_tot:
				val = fj.accorece_credit_tot
			else:
				val = 0.0
			fj.accorece_credit_tot = val
			tot = fj.accorece_credit_tot + fj.accorece_single_tot + fj.accorece_single_imp_tot

			if tot == 0:
				rate = 0
			else:
				rate = val / tot * 100
			html_str += '\t<td>%.2f</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, rate)
		html_str += '</tr>\n'

		# 按信用风险特征组合计坏账准备的应收账款坏账准备
		html_str += '<tr bgcolor="white">\n\t<td>坏账准备</td>\n\t<td>经营相关资产</td>\n'
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if not k in self.stock.fjsjs:
				fj = FJSJ()
			else:
				fj = self.stock.fjsjs[k]

			if fj.accorece_credit_bad:
				val = fj.accorece_credit_bad
			else:
				val = 0.0
			fj.accorece_credit_bad = val

			if fj.accorece_credit_tot == 0:
				rate = 0
			else:
				rate = val / fj.accorece_credit_tot * 100
			html_str += '\t<td>%.2f</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, rate)
		html_str += '</tr>\n'

		# 单项金额不重大但单独计坏账准备的应收账款
		html_str += '<tr bgcolor="white">\n\t<td>其中：单项金额不重大但单独计坏账准备的</td>\n\t<td>经营相关资产</td>\n'
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if not k in self.stock.fjsjs:
				fj = FJSJ()
			else:
				fj = self.stock.fjsjs[k]

			if fj.accorece_single_tot:
				val = fj.accorece_single_tot
			else:
				val = 0.0
			fj.accorece_single_tot = val
			tot = fj.accorece_credit_tot + fj.accorece_single_tot + fj.accorece_single_imp_tot

			if tot == 0:
				rate = 0
			else:
				rate = val / tot * 100
			html_str += '\t<td>%.2f</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, rate)
		html_str += '</tr>\n'

		# 单项金额不重大但单独计坏账准备的应收账款坏账准备
		html_str += '<tr bgcolor="white">\n\t<td>坏账准备</td>\n\t<td>经营相关资产</td>\n'
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if not k in self.stock.fjsjs:
				fj = FJSJ()
			else:
				fj = self.stock.fjsjs[k]

			if fj.accorece_single_bad:
				val = fj.accorece_single_bad
			else:
				val = 0.0
			fj.accorece_single_bad = val

			if fj.accorece_single_tot == 0:
				rate = 0
			else:
				rate = fj.accorece_single_bad / fj.accorece_single_tot * 100
			html_str += '\t<td>%.2f</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, rate)
		html_str += '</tr>\n'

		# 期末单项金额重大并单项计坏账准备的应收账款
		html_str += '<tr bgcolor="white">\n\t<td>其中：期末单项金额重大并单项计坏账准备的</td>\n\t<td>经营相关资产</td>\n'
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if not k in self.stock.fjsjs:
				fj = FJSJ()
			else:
				fj = self.stock.fjsjs[k]

			if fj.accorece_single_imp_tot:
				val = fj.accorece_single_imp_tot
			else:
				val = 0.0
			fj.accorece_single_imp_tot = val
			tot = fj.accorece_credit_tot + fj.accorece_single_tot + fj.accorece_single_imp_tot

			if tot == 0:
				rate = 0
			else:
				rate = val / tot * 100
			html_str += '\t<td>%.2f</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, rate)
		html_str += '</tr>\n'

		# 期末单项金额重大并单项计坏账准备的应收账款坏账准备
		html_str += '<tr bgcolor="white">\n\t<td>坏账准备</td>\n\t<td>经营相关资产</td>\n'
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if not k in self.stock.fjsjs:
				fj = FJSJ()
			else:
				fj = self.stock.fjsjs[k]

			if fj.accorece_single_imp_bad:
				val = fj.accorece_single_imp_bad
			else:
				val = 0.0
			fj.accorece_single_imp_bad = val

			if fj.accorece_single_imp_tot == 0:
				rate = 0
			else:
				rate = fj.accorece_single_imp_bad / fj.accorece_single_imp_tot * 100
			html_str += '\t<td>%.2f</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, rate)
		html_str += '</tr>\n'

		# 账龄小于1年的应收账款
		html_str += '<tr bgcolor="white">\n\t<td>其中：账龄小于1年的</td>\n\t<td>经营相关资产</td>\n'
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if not k in self.stock.fjsjs:
				fj = FJSJ()
			else:
				fj = self.stock.fjsjs[k]

			if fj.accorece_0_1_tot:
				val = fj.accorece_0_1_tot
			else:
				val = 0.0
			fj.accorece_0_1_tot = val
			tot = fj.accorece_0_1_tot + fj.accorece_1_2_tot + fj.accorece_2_3_tot + fj.accorece_3_4_tot + fj.accorece_4_5_tot + fj.accorece_5_n_tot
			
			if tot == 0:
				rate = 0
			else:
				rate = val / tot * 100
			html_str += '\t<td>%.2f</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, rate)
		html_str += '</tr>\n'

		# 账龄小于1年的应收账款坏账准备
		html_str += '<tr bgcolor="white">\n\t<td>坏账准备</td>\n\t<td>经营相关资产</td>\n'
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if not k in self.stock.fjsjs:
				fj = FJSJ()
			else:
				fj = self.stock.fjsjs[k]

			if fj.accorece_0_1_bad:
				val = fj.accorece_0_1_bad
			else:
				val = 0.0
			fj.accorece_0_1_bad = val

			if fj.accorece_0_1_tot == 0:
				rate = 0
			else:
				rate = fj.accorece_0_1_bad / fj.accorece_0_1_tot * 100
			html_str += '\t<td>%.2f</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, rate)
		html_str += '</tr>\n'

		# 账龄1-2年的应收账款
		html_str += '<tr bgcolor="white">\n\t<td>其中：账龄1-2年的</td>\n\t<td>经营相关资产</td>\n'
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if not k in self.stock.fjsjs:
				fj = FJSJ()
			else:
				fj = self.stock.fjsjs[k]

			if fj.accorece_1_2_tot:
				val = fj.accorece_1_2_tot
			else:
				val = 0.0
			fj.accorece_1_2_tot = val
			tot = fj.accorece_0_1_tot + fj.accorece_1_2_tot + fj.accorece_2_3_tot + fj.accorece_3_4_tot + fj.accorece_4_5_tot + fj.accorece_5_n_tot
			
			if tot == 0:
				rate = 0
			else:
				rate = val / tot * 100
			html_str += '\t<td>%.2f</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, rate)
		html_str += '</tr>\n'

		# 账龄1-2年的应收账款坏账准备
		html_str += '<tr bgcolor="white">\n\t<td>坏账准备</td>\n\t<td>经营相关资产</td>\n'
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if not k in self.stock.fjsjs:
				fj = FJSJ()
			else:
				fj = self.stock.fjsjs[k]

			if fj.accorece_1_2_bad:
				val = fj.accorece_1_2_bad
			else:
				val = 0.0
			fj.accorece_1_2_bad = val

			if fj.accorece_1_2_tot == 0:
				rate = 0
			else:
				rate = fj.accorece_1_2_bad / fj.accorece_1_2_tot * 100
			html_str += '\t<td>%.2f</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, rate)
		html_str += '</tr>\n'

		# 账龄2-3年的应收账款
		html_str += '<tr bgcolor="white">\n\t<td>其中：账龄2-3年的</td>\n\t<td>经营相关资产</td>\n'
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if not k in self.stock.fjsjs:
				fj = FJSJ()
			else:
				fj = self.stock.fjsjs[k]

			if fj.accorece_2_3_tot:
				val = fj.accorece_2_3_tot
			else:
				val = 0.0
			fj.accorece_2_3_tot = val
			tot = fj.accorece_0_1_tot + fj.accorece_1_2_tot + fj.accorece_2_3_tot + fj.accorece_3_4_tot + fj.accorece_4_5_tot + fj.accorece_5_n_tot
			
			if tot == 0:
				rate = 0
			else:
				rate = val / tot * 100
			html_str += '\t<td>%.2f</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, rate)
		html_str += '</tr>\n'

		# 账龄2-3年的应收账款坏账准备
		html_str += '<tr bgcolor="white">\n\t<td>坏账准备</td>\n\t<td>经营相关资产</td>\n'
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if not k in self.stock.fjsjs:
				fj = FJSJ()
			else:
				fj = self.stock.fjsjs[k]

			if fj.accorece_2_3_bad:
				val = fj.accorece_2_3_bad
			else:
				val = 0.0
			fj.accorece_2_3_bad = val

			if fj.accorece_2_3_tot == 0:
				rate = 0
			else:
				rate = fj.accorece_2_3_bad / fj.accorece_2_3_tot * 100
			html_str += '\t<td>%.2f</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, rate)
		html_str += '</tr>\n'

		# 账龄3-4年的应收账款
		html_str += '<tr bgcolor="white">\n\t<td>其中：账龄3-4年的</td>\n\t<td>经营相关资产</td>\n'
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if not k in self.stock.fjsjs:
				fj = FJSJ()
			else:
				fj = self.stock.fjsjs[k]

			if fj.accorece_3_4_tot:
				val = fj.accorece_3_4_tot
			else:
				val = 0.0
			fj.accorece_3_4_tot = val
			tot = fj.accorece_0_1_tot + fj.accorece_1_2_tot + fj.accorece_2_3_tot + fj.accorece_3_4_tot + fj.accorece_4_5_tot + fj.accorece_5_n_tot
			
			if tot == 0:
				rate = 0
			else:
				rate = val / tot * 100
			html_str += '\t<td>%.2f</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, rate)
		html_str += '</tr>\n'

		# 账龄3-4年的应收账款坏账准备
		html_str += '<tr bgcolor="white">\n\t<td>坏账准备</td>\n\t<td>经营相关资产</td>\n'
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if not k in self.stock.fjsjs:
				fj = FJSJ()
			else:
				fj = self.stock.fjsjs[k]

			if fj.accorece_3_4_bad:
				val = fj.accorece_3_4_bad
			else:
				val = 0.0
			fj.accorece_3_4_bad = val

			if fj.accorece_3_4_tot == 0:
				rate = 0
			else:
				rate = fj.accorece_3_4_bad / fj.accorece_3_4_tot * 100
			html_str += '\t<td>%.2f</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, rate)
		html_str += '</tr>\n'

		# 账龄4-5年的应收账款
		html_str += '<tr bgcolor="white">\n\t<td>其中：账龄4-5年的</td>\n\t<td>经营相关资产</td>\n'
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if not k in self.stock.fjsjs:
				fj = FJSJ()
			else:
				fj = self.stock.fjsjs[k]

			if fj.accorece_4_5_tot:
				val = fj.accorece_4_5_tot
			else:
				val = 0.0
			fj.accorece_4_5_tot = val
			tot = fj.accorece_0_1_tot + fj.accorece_1_2_tot + fj.accorece_2_3_tot + fj.accorece_3_4_tot + fj.accorece_4_5_tot + fj.accorece_5_n_tot
			
			if tot == 0:
				rate = 0
			else:
				rate = val / tot * 100
			html_str += '\t<td>%.2f</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, rate)
		html_str += '</tr>\n'

		# 账龄4-5年的应收账款坏账准备
		html_str += '<tr bgcolor="white">\n\t<td>坏账准备</td>\n\t<td>经营相关资产</td>\n'
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if not k in self.stock.fjsjs:
				fj = FJSJ()
			else:
				fj = self.stock.fjsjs[k]

			if fj.accorece_4_5_bad:
				val = fj.accorece_4_5_bad
			else:
				val = 0.0
			fj.accorece_4_5_bad = val

			if fj.accorece_4_5_tot == 0:
				rate = 0
			else:
				rate = fj.accorece_4_5_bad / fj.accorece_4_5_tot * 100
			html_str += '\t<td>%.2f</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, rate)
		html_str += '</tr>\n'

		# 账龄大于5年的应收账款
		html_str += '<tr bgcolor="white">\n\t<td>其中：账龄大于5年的</td>\n\t<td>经营相关资产</td>\n'
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if not k in self.stock.fjsjs:
				fj = FJSJ()
			else:
				fj = self.stock.fjsjs[k]

			if fj.accorece_5_n_tot:
				val = fj.accorece_5_n_tot
			else:
				val = 0.0
			fj.accorece_5_n_tot = val
			tot = fj.accorece_0_1_tot + fj.accorece_1_2_tot + fj.accorece_2_3_tot + fj.accorece_3_4_tot + fj.accorece_4_5_tot + fj.accorece_5_n_tot
			
			if tot == 0:
				rate = 0
			else:
				rate = val / tot * 100
			html_str += '\t<td>%.2f</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, rate)
		html_str += '</tr>\n'

		# 账龄大于5年的应收账款坏账准备
		html_str += '<tr bgcolor="white">\n\t<td>坏账准备</td>\n\t<td>经营相关资产</td>\n'
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if not k in self.stock.fjsjs:
				fj = FJSJ()
			else:
				fj = self.stock.fjsjs[k]

			if fj.accorece_5_n_bad:
				val = fj.accorece_5_n_bad
			else:
				val = 0.0
			fj.accorece_5_n_bad = val

			if fj.accorece_5_n_tot == 0:
				rate = 0
			else:
				rate = fj.accorece_5_n_bad / fj.accorece_5_n_tot * 100
			html_str += '\t<td>%.2f</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, rate)
		html_str += '</tr>\n'

		# 应收账款的坏账计提标准
		html_str += '<tr bgcolor="white">\n\t<td>应收账款的坏账计提标准</td>\n\t<td>经营相关资产</td>\n'
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if not k in self.stock.fjsjs:
				fj = FJSJ()
			else:
				fj = self.stock.fjsjs[k]

			if fj.accorece_bad_standard:
				val = fj.accorece_bad_standard
			else:
				val = ""
			fj.accorece_bad_standard = val
			html_str += '\t<td>%s</td>\n\t<td></td>\n' % (val)
		html_str += '</tr>\n'

		# 预付款项
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">预付款项</td>\n\t<td style="background: %s; color: #FFFFFF">经营相关资产</td>\n' % (Cons.COLOR_RED, Cons.COLOR_RED)
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if zb.prep:
				val = zb.prep
			else:
				val = 0.0
			zb.prep = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / zb.totasset * 100)
		html_str += '</tr>\n'

		# 预付款项同比年增长率
		html_str += '<tr bgcolor="white">\n\t<td>预付款项同比年增长率</td>\n\t<td>经营相关资产</td>\n'
		for k in keys:
			k1 = '%s' % (int(k) - 1)
			if k1 in self.stock.zcfzbs:
				zb_lst = self.stock.zcfzbs[k1]
			else:
				zb_lst = ZCFZB()
			zb_cur = self.stock.zcfzbs[k]

			if zb_lst.prep == 0:
				val = 0.0
			else:
				val = (zb_cur.prep / zb_lst.prep - 1) * 100
			html_str += '\t<td>%.2f%%</td>\n\t<td></td>\n' % (val)
		html_str += '<td>(本年/去年 - 1) * 100%</td></tr>\n'

    	# 1年内的预付款项
		html_str += '<tr bgcolor="white">\n\t<td>其中：1年内的</td>\n\t<td>经营相关资产</td>\n'
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if not k in self.stock.fjsjs:
				fj = FJSJ()
			else:
				fj = self.stock.fjsjs[k]

			if fj.prep_0_1:
				val = fj.prep_0_1
			else:
				val = 0.0
			fj.prep_0_1 = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / zb.prep * 100)
		html_str += '<td>除以预付款项</td></tr>\n'

		# 1年以上的预付款项
		html_str += '<tr bgcolor="white">\n\t<td>其中：1年以上的</td>\n\t<td>经营相关资产</td>\n'
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if not k in self.stock.fjsjs:
				fj = FJSJ()
			else:
				fj = self.stock.fjsjs[k]

			if fj.prep_1_n:
				val = fj.prep_1_n
			else:
				val = 0.0
			fj.prep_1_n = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / zb.prep * 100)
		html_str += '<td>除以预付款项</td></tr>\n'

		# 预付款项 / 营业收入
		html_str += '<tr bgcolor="white">\n\t<td>预付款项 / 营业收入</td>\n\t<td>经营相关资产</td>\n'
		for k in keys:
			zb = self.stock.zcfzbs[k]
			lb = self.stock.gslrbs[k]
			if lb.bizinco == 0:
				rate = 0
			else:
				rate = zb.prep / lb.bizinco * 100
			html_str += '\t<td>%.2f%%</td>\n\t<td></td>\n' % (rate)
		html_str += '</tr>\n'

		# 预付款项 / 营业成本
		html_str += '<tr bgcolor="white">\n\t<td>预付款项 / 营业成本</td>\n\t<td>经营相关资产</td>\n'
		for k in keys:
			zb = self.stock.zcfzbs[k]
			lb = self.stock.gslrbs[k]
			if lb.bizcost == 0:
				rate = 0
			else:
				rate = zb.prep / lb.bizcost * 100
			html_str += '\t<td>%.2f%%</td>\n\t<td></td>\n' % (rate)
		html_str += '</tr>\n'

		# 应收利息
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">应收利息</td>\n\t<td style="background: %s; color: #FFFFFF">经营相关资产</td>\n' % (Cons.COLOR_RED, Cons.COLOR_RED)
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if zb.interece:
				val = zb.interece
			else:
				val = 0.0
			zb.interece = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / zb.totasset * 100)
		html_str += '</tr>\n'

		# 应收股利
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">应收股利</td>\n\t<td style="background: %s; color: #FFFFFF">经营相关资产</td>\n' % (Cons.COLOR_RED, Cons.COLOR_RED)
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if zb.dividrece:
				val = zb.dividrece
			else:
				val = 0.0
			zb.dividrece = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / zb.totasset * 100)
		html_str += '</tr>\n'

		# 长期应收款
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">长期应收款</td>\n\t<td style="background: %s; color: #FFFFFF">经营相关资产</td>\n' % (Cons.COLOR_RED, Cons.COLOR_RED)
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if zb.longrece:
				val = zb.longrece
			else:
				val = 0.0
			zb.longrece = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / zb.totasset * 100)
		html_str += '</tr>\n'

		# 其他应收款
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">其他应收款</td>\n\t<td style="background: %s; color: #FFFFFF">经营相关资产</td>\n' % (Cons.COLOR_RED, Cons.COLOR_RED)
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if zb.otherrece:
				val = zb.otherrece
			else:
				val = 0.0
			zb.otherrece = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / zb.totasset * 100)
		html_str += '</tr>\n'

		# 存货
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">存货</td>\n\t<td style="background: %s; color: #FFFFFF">经营相关资产</td>\n' % (Cons.COLOR_RED, Cons.COLOR_RED)
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if zb.inve:
				val = zb.inve
			else:
				val = 0.0
			zb.inve = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / zb.totasset * 100)
		html_str += '</tr>\n'

		# 存货的同比年增长率
		html_str += '<tr bgcolor="white">\n\t<td>存货的同比年增长率</td>\n\t<td>经营相关资产</td>\n'
		for k in keys:
			k1 = '%s' % (int(k) - 1)
			if k1 in self.stock.zcfzbs:
				zb_lst = self.stock.zcfzbs[k1]
			else:
				zb_lst = ZCFZB()
			zb_cur = self.stock.zcfzbs[k]

			if zb_lst.inve == 0:
				val = 0.0
			else:
				val = (zb_cur.inve / zb_lst.inve - 1) * 100
			html_str += '\t<td>%.2f%%</td>\n\t<td></td>\n' % (val)
		html_str += '<td>(本年/去年 - 1) * 100%</td></tr>\n'

		# 存货周转率 = 营业成本 / 存货平均余额，其中：存货平均余额 = (期初存货总额 + 期末存货总额) / 2
		html_str += '<tr bgcolor="white">\n\t<td>存货周转率</td>\n\t<td>经营相关资产</td>\n'
		for k in keys:
			lb = self.stock.gslrbs[k]
			zb_cur = self.stock.zcfzbs[k]
			k1 = '%s' % (int(k) - 1)
			if k1 in self.stock.zcfzbs:
				zb_lst = self.stock.zcfzbs[k1]
				val = lb.bizcost / (zb_cur.inve + zb_lst.inve) * 2
			else:
				val = lb.bizcost / zb_cur.inve
			html_str += '\t<td>%.2f</td>\n\t<td></td>\n' % (val)
		html_str += '<td>营业成本 / 存货平均总额</td></tr>\n'

		# 存货 / 营业成本
		html_str += '<tr bgcolor="white">\n\t<td>存货 / 营业成本</td>\n\t<td>经营相关资产</td>\n'
		for k in keys:
			zb = self.stock.zcfzbs[k]
			lb = self.stock.gslrbs[k]
			if lb.bizcost == 0:
				rate = 0
			else:
				rate = zb.inve / lb.bizcost * 100
			html_str += '\t<td>%.2f%%</td>\n\t<td></td>\n' % (rate)
		html_str += '</tr>\n'

		# 存货跌价计提标准
		html_str += '<tr bgcolor="white">\n\t<td>存货跌价计提标准</td>\n\t<td>经营相关资产</td>\n'
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if not k in self.stock.fjsjs:
				fj = FJSJ()
			else:
				fj = self.stock.fjsjs[k]

			if fj.inverevvallossstandard:
				val = fj.inverevvallossstandard
			else:
				val = ""
			fj.inverevvallossstandard = val
			html_str += '\t<td>%s</td>\n\t<td></td>\n' % (val)
		html_str += '</tr>\n'

		# 存货跌价计提总额
		html_str += '<tr bgcolor="white">\n\t<td>存货跌价计提总额</td>\n\t<td>经营相关资产</td>\n'
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if not k in self.stock.fjsjs:
				fj = FJSJ()
			else:
				fj = self.stock.fjsjs[k]

			if fj.inverevvallosstot:
				val = fj.inverevvallosstot
			else:
				val = 0.0
			fj.inverevvallosstot = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / zb.inve * 100)
		html_str += '<td>除以存货</td></tr>\n'

		# 存货的成本计价方法
		html_str += '<tr bgcolor="white">\n\t<td>存货的成本计价方法</td>\n\t<td>经营相关资产</td>\n'
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if not k in self.stock.fjsjs:
				fj = FJSJ()
			else:
				fj = self.stock.fjsjs[k]

			if fj.inveincal:
				val = fj.inveincal
			else:
				val = ""
			fj.inveincal = val
			html_str += '\t<td>%s</td>\n\t<td></td>\n' % (val)
		html_str += '</tr>\n'

		# 存货的发出计价方法
		html_str += '<tr bgcolor="white">\n\t<td>存货的发出计价方法</td>\n\t<td>经营相关资产</td>\n'
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if not k in self.stock.fjsjs:
				fj = FJSJ()
			else:
				fj = self.stock.fjsjs[k]

			if fj.inveoutcal:
				val = fj.inveoutcal
			else:
				val = ""
			fj.inveoutcal = val
			html_str += '\t<td>%s</td>\n\t<td></td>\n' % (val)
		html_str += '</tr>\n'

		# 应收款合计
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">应收款合计</td>\n\t<td></td>\n' % Cons.COLOR_RED
		for k in keys:
			zb = self.stock.zcfzbs[k]
			lb = self.stock.gslrbs[k]
			val = 0.0
			val += zb.notesrece
			val += zb.accorece
			val += zb.interece
			val += zb.dividrece
			val += zb.otherrece
			val += zb.longrece
			rectot = val

			ave = val / lb.bizinco * 12
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%% =%.2f个月营业收入</td>\n' % (val / Cons.Yi, val / zb.totasset * 100, ave)
		html_str += '</tr>\n'

		# 合计
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">经营相关资产合计</td>\n\t<td></td>\n' % Cons.COLOR_RED
		for k in keys:
			zb = self.stock.zcfzbs[k]
			val = 0.0
			val += zb.notesrece
			val += zb.accorece
			val += zb.prep
			val += zb.interece
			val += zb.dividrece
			val += zb.longrece
			val += zb.otherrece
			val += zb.inve
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / zb.totasset * 100)
		html_str += '</tr>\n'

		# 三、投资相关资产
		# 交易性金融资产
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">交易性金融资产</td>\n\t<td style="background: %s; color: #FFFFFF">投资相关资产</td>\n' % (Cons.COLOR_PINK, Cons.COLOR_PINK)
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if zb.tradfinasset:
				val = zb.tradfinasset
			else:
				val = 0.0
			zb.tradfinasset = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / zb.totasset * 100)
		html_str += '</tr>\n'

		# 可供出售金融资产
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">可供出售金融资产</td>\n\t<td style="background: %s; color: #FFFFFF">投资相关资产</td>\n' % (Cons.COLOR_PINK, Cons.COLOR_PINK)
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if zb.avaisellasse:
				val = zb.avaisellasse
			else:
				val = 0.0
			zb.avaisellasse = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / zb.totasset * 100)
		html_str += '</tr>\n'

		# 可供出售金融资产的期末账面余额和买入成本
		html_str += '<tr bgcolor="white">\n\t<td>期末账面余额和买入成本</td>\n\t<td>投资相关资产</td>\n'
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if not k in self.stock.fjsjs:
				fj = FJSJ()
			else:
				fj = self.stock.fjsjs[k]

			if fj.avaisellassecur:
				val = fj.avaisellassecur
			else:
				val = 0.0
			fj.avaisellassecur = val

			if fj.avaisellassecost:
				val = fj.avaisellassecost
			else:
				val = 0.0
			fj.avaisellassecost = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f</td>\n' % (fj.avaisellassecur / Cons.Yi, fj.avaisellassecost)
		html_str += '<td>先账面余额，后买入成本</td></tr>\n'

		# 持有至到期投资
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">持有至到期投资</td>\n\t<td style="background: %s; color: #FFFFFF">投资相关资产</td>\n' % (Cons.COLOR_PINK, Cons.COLOR_PINK)
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if zb.holdinvedue:
				val = zb.holdinvedue
			else:
				val = 0.0
			zb.holdinvedue = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / zb.totasset * 100)
		html_str += '</tr>\n'

		# 持有至到期投资的实际利率
		html_str += '<tr bgcolor="white">\n\t<td>持有至到期投资的实际利率</td>\n\t<td>投资相关资产</td>\n'
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if not k in self.stock.fjsjs:
				fj = FJSJ()
			else:
				fj = self.stock.fjsjs[k]

			if fj.holdinvedue_inrate:
				val = fj.holdinvedue_inrate
			else:
				val = 0.0
			fj.holdinvedue_inrate = val
			html_str += '\t<td>%.2f%%</td>\n\t<td></td>\n' % (val * 100)
		html_str += '<td>除以存货</td></tr>\n'

		# 持有至到期投资的减值数额
		html_str += '<tr bgcolor="white">\n\t<td>持有至到期投资的减值数额</td>\n\t<td>投资相关资产</td>\n'
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if not k in self.stock.fjsjs:
				fj = FJSJ()
			else:
				fj = self.stock.fjsjs[k]

			if fj.holdinvedue_losscur:
				val = fj.holdinvedue_losscur
			else:
				val = 0.0
			fj.holdinvedue_losscur = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / zb.totasset * 100)
		html_str += '</tr>\n'

		# 持有至到期投资的减值转回数额
		html_str += '<tr bgcolor="white">\n\t<td>持有至到期投资的减值转回数额</td>\n\t<td>投资相关资产</td>\n'
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if not k in self.stock.fjsjs:
				fj = FJSJ()
			else:
				fj = self.stock.fjsjs[k]

			if fj.holdinvedue_lossback:
				val = fj.holdinvedue_lossback
			else:
				val = 0.0
			fj.holdinvedue_lossback = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / zb.totasset * 100)
		html_str += '</tr>\n'

		# 长期股权投资
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">长期股权投资</td>\n\t<td style="background: %s; color: #FFFFFF">投资相关资产</td>\n' % (Cons.COLOR_PINK, Cons.COLOR_PINK)
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if zb.equiinve:
				val = zb.equiinve
			else:
				val = 0.0
			zb.equiinve = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / zb.totasset * 100)
		html_str += '</tr>\n'

		# 其他长期投资
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">其他长期投资</td>\n\t<td style="background: %s; color: #FFFFFF">投资相关资产</td>\n' % (Cons.COLOR_PINK, Cons.COLOR_PINK)
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if zb.otherlonginve:
				val = zb.otherlonginve
			else:
				val = 0.0
			zb.otherlonginve = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / zb.totasset * 100)
		html_str += '</tr>\n'

		# 投资性房地产
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">投资性房地产</td>\n\t<td style="background: %s; color: #FFFFFF">投资相关资产</td>\n' % (Cons.COLOR_PINK, Cons.COLOR_PINK)
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if zb.inveprop:
				val = zb.inveprop
			else:
				val = 0.0
			zb.inveprop = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / zb.totasset * 100)
		html_str += '</tr>\n'

		# 投资性房地产的计量模式
		html_str += '<tr bgcolor="white">\n\t<td>投资性房地产的计量模式</td>\n\t<td>投资相关资产</td>\n'
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if not k in self.stock.fjsjs:
				fj = FJSJ()
			else:
				fj = self.stock.fjsjs[k]

			if fj.invepropcal:
				val = fj.invepropcal
			else:
				val = ""
			fj.invepropcal = val
			html_str += '\t<td>%s</td>\n\t<td></td>\n' % (val)
		html_str += '</tr>\n'

		# 合计
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">投资相关资产合计</td>\n\t<td></td>\n' % Cons.COLOR_PINK
		for k in keys:
			zb = self.stock.zcfzbs[k]
			val = 0.0
			val += zb.tradfinasset
			val += zb.avaisellasse
			val += zb.holdinvedue
			val += zb.equiinve
			val += zb.otherlonginve
			val += zb.inveprop
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / zb.totasset * 100)
		html_str += '</tr>\n'

		# 固定资产原值
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">固定资产原值</td>\n\t<td style="background: %s; color: #FFFFFF">生产相关资产</td>\n' % (Cons.COLOR_YELLOW, Cons.COLOR_YELLOW)
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if zb.fixedasseimmo:
				val = zb.fixedasseimmo
			else:
				val = 0.0
			zb.fixedasseimmo = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / zb.totasset * 100)
		html_str += '</tr>\n'

		# 累计折旧
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">累计折旧</td>\n\t<td style="background: %s; color: #FFFFFF">生产相关资产</td>\n' % (Cons.COLOR_YELLOW, Cons.COLOR_YELLOW)
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if zb.accudepr:
				val = zb.accudepr
			else:
				val = 0.0
			zb.accudepr = val

			if zb.fixedasseimmo == 0:
				rate = 0.0
			else:
				rate = val / zb.fixedasseimmo * 100
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, rate)
		html_str += '<td>除以固定资产原值</td></tr>\n'

		# 固定资产净值
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">固定资产净值</td>\n\t<td style="background: %s; color: #FFFFFF">生产相关资产</td>\n' % (Cons.COLOR_YELLOW, Cons.COLOR_YELLOW)
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if zb.fixedassenetw:
				val = zb.fixedassenetw
			else:
				val = 0.0
			zb.fixedassenetw = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / zb.totasset * 100)
		html_str += '</tr>\n'

		# 固定资产减值准备
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">固定资产减值准备</td>\n\t<td style="background: %s; color: #FFFFFF">生产相关资产</td>\n' % (Cons.COLOR_YELLOW, Cons.COLOR_YELLOW)
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if zb.fixedasseimpa:
				val = zb.fixedasseimpa
			else:
				val = 0.0
			zb.fixedasseimpa = val

			if zb.fixedasseimmo == 0:
				rate = 0
			else:
				rate = val / zb.fixedasseimmo * 100
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, rate)
		html_str += '<td>除以固定资产原值</td></tr>\n'

		# 固定资产净额
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">固定资产净额</td>\n\t<td style="background: %s; color: #FFFFFF">生产相关资产</td>\n' % (Cons.COLOR_YELLOW, Cons.COLOR_YELLOW)
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if zb.fixedassenet:
				val = zb.fixedassenet
			else:
				val = 0.0
			zb.fixedassenet = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / zb.totasset * 100)
		html_str += '</tr>\n'

		# 固定资产周转率 = 营业收入 / 平均固定资产净额
		html_str += '<tr bgcolor="white">\n\t<td>固定资产周转率</td>\n\t<td>生产相关资产</td>\n'
		for k in keys:
			lb = self.stock.gslrbs[k]
			zb_cur = self.stock.zcfzbs[k]
			k1 = '%s' % (int(k) - 1)
			if k1 in self.stock.zcfzbs:
				zb_lst = self.stock.zcfzbs[k1]
				fixedassenet = (zb_cur.fixedassenet + zb_lst.fixedassenet) / 2
			else:
				fixedassenet = zb_cur.fixedassenet

			if fixedassenet == 0:
				val = 0
			else:
				val = lb.bizinco /  fixedassenet
			html_str += '\t<td>%.2f</td>\n\t<td></td>\n' % (val)
		html_str += '<td>营业收入 / 平均固定资产净额</td></tr>\n'

		# 固定资产的折旧政策
		html_str += '<tr bgcolor="white">\n\t<td>固定资产的折旧政策</td>\n\t<td>生产相关资产</td>\n'
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if not k in self.stock.fjsjs:
				fj = FJSJ()
			else:
				fj = self.stock.fjsjs[k]

			if fj.fixedassedepolicy:
				val = fj.fixedassedepolicy
			else:
				val = ""
			fj.fixedassedepolicy = val
			html_str += '\t<td>%s</td>\n\t<td></td>\n' % (val)
		html_str += '</tr>\n'

		# 在建工程
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">在建工程</td>\n\t<td style="background: %s; color: #FFFFFF">生产相关资产</td>\n' % (Cons.COLOR_YELLOW, Cons.COLOR_YELLOW)
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if zb.consprog:
				val = zb.consprog
			else:
				val = 0.0
			zb.consprog = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / zb.totasset * 100)
		html_str += '</tr>\n'

		# 工程物资
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">工程物资</td>\n\t<td style="background: %s; color: #FFFFFF">生产相关资产</td>\n' % (Cons.COLOR_YELLOW, Cons.COLOR_YELLOW)
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if zb.engimate:
				val = zb.engimate
			else:
				val = 0.0
			zb.engimate = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / zb.totasset * 100)
		html_str += '</tr>\n'

		# 生产性生物资产
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">生产性生物资产</td>\n\t<td style="background: %s; color: #FFFFFF">生产相关资产</td>\n' % (Cons.COLOR_YELLOW, Cons.COLOR_YELLOW)
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if zb.prodasse:
				val = zb.prodasse
			else:
				val = 0.0
			zb.prodasse = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / zb.totasset * 100)
		html_str += '</tr>\n'

		# 公益性生物资产
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">公益性生物资产</td>\n\t<td style="background: %s; color: #FFFFFF">生产相关资产</td>\n' % (Cons.COLOR_YELLOW, Cons.COLOR_YELLOW)
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if zb.comasse:
				val = zb.comasse
			else:
				val = 0.0
			zb.comasse = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / zb.totasset * 100)
		html_str += '</tr>\n'

		# 油气资产
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">油气资产</td>\n\t<td style="background: %s; color: #FFFFFF">生产相关资产</td>\n' % (Cons.COLOR_YELLOW, Cons.COLOR_YELLOW)
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if zb.hydrasset:
				val = zb.hydrasset
			else:
				val = 0.0
			zb.hydrasset = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / zb.totasset * 100)
		html_str += '</tr>\n'

		# 无形资产
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">无形资产</td>\n\t<td style="background: %s; color: #FFFFFF">生产相关资产</td>\n' % (Cons.COLOR_YELLOW, Cons.COLOR_YELLOW)
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if zb.intaasset:
				val = zb.intaasset
			else:
				val = 0.0
			zb.intaasset = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / zb.totasset * 100)
		html_str += '</tr>\n'

		# 无形资产的摊销政策
		html_str += '<tr bgcolor="white">\n\t<td>无形资产的摊销政策</td>\n\t<td>生产相关资产</td>\n'
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if not k in self.stock.fjsjs:
				fj = FJSJ()
			else:
				fj = self.stock.fjsjs[k]

			if fj.intaassetdmopolicy:
				val = fj.intaassetdmopolicy
			else:
				val = ""
			fj.intaassetdmopolicy = val
			html_str += '\t<td>%s</td>\n\t<td></td>\n' % (val)
		html_str += '</tr>\n'

		# 开发支出
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">开发支出</td>\n\t<td style="background: %s; color: #FFFFFF">生产相关资产</td>\n' % (Cons.COLOR_YELLOW, Cons.COLOR_YELLOW)
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if zb.deveexpe:
				val = zb.deveexpe
			else:
				val = 0.0
			zb.deveexpe = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / zb.totasset * 100)
		html_str += '</tr>\n'

		# 商誉
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">商誉</td>\n\t<td style="background: %s; color: #FFFFFF">生产相关资产</td>\n' % (Cons.COLOR_YELLOW, Cons.COLOR_YELLOW)
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if zb.goodwill:
				val = zb.goodwill
			else:
				val = 0.0
			zb.goodwill = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / zb.totasset * 100)
		html_str += '</tr>\n'

		# 待摊费用
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">待摊费用</td>\n\t<td style="background: %s; color: #FFFFFF">生产相关资产</td>\n' % (Cons.COLOR_YELLOW, Cons.COLOR_YELLOW)
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if zb.prepexpe:
				val = zb.prepexpe
			else:
				val = 0.0
			zb.prepexpe = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / zb.totasset * 100)
		html_str += '</tr>\n'

		# 待摊费用同比年增长率
		html_str += '<tr bgcolor="white">\n\t<td>同比年增长率</td>\n\t<td>生产相关资产</td>\n'
		for k in keys:
			k1 = '%s' % (int(k) - 1)
			if k1 in self.stock.zcfzbs:
				zb_lst = self.stock.zcfzbs[k1]
			else:
				zb_lst = ZCFZB()
			zb_cur = self.stock.zcfzbs[k]

			if zb_lst.prepexpe == 0:
				val = 0.0
			else:
				val = (zb_cur.prepexpe / zb_lst.prepexpe - 1) * 100
			html_str += '\t<td>%.2f%%</td>\n\t<td></td>\n' % (val)
		html_str += '<td>(本年/去年 - 1) * 100%</td></tr>\n'

		# 长期待摊费用
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">长期待摊费用</td>\n\t<td style="background: %s; color: #FFFFFF">生产相关资产</td>\n' % (Cons.COLOR_YELLOW, Cons.COLOR_YELLOW)
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if zb.logprepexpe:
				val = zb.logprepexpe
			else:
				val = 0.0
			zb.logprepexpe = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / zb.totasset * 100)
		html_str += '</tr>\n'

		# 长期待摊费用同比年增长率
		html_str += '<tr bgcolor="white">\n\t<td>同比年增长率</td>\n\t<td>生产相关资产</td>\n'
		for k in keys:
			k1 = '%s' % (int(k) - 1)
			if k1 in self.stock.zcfzbs:
				zb_lst = self.stock.zcfzbs[k1]
			else:
				zb_lst = ZCFZB()
			zb_cur = self.stock.zcfzbs[k]

			if zb_lst.logprepexpe == 0:
				val = 0.0
			else:
				val = (zb_cur.logprepexpe / zb_lst.logprepexpe - 1) * 100
			html_str += '\t<td>%.2f%%</td>\n\t<td></td>\n' % (val)
		html_str += '<td>(本年/去年 - 1) * 100%</td></tr>\n'

		# 递延所得税资产
		html_str += '<tr\>\n\t<td style="background: %s; color: #FFFFFF">递延所得税资产</td>\n\t<td style="background: %s; color: #FFFFFF">生产相关资产</td>\n' % (Cons.COLOR_YELLOW, Cons.COLOR_YELLOW)
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if zb.defetaxasset:
				val = zb.defetaxasset
			else:
				val = 0.0
			zb.defetaxasset = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / zb.totasset * 100)
		html_str += '</tr>\n'

		# 合计
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">生产相关资产合计</td>\n\t<td></td>\n' % Cons.COLOR_YELLOW
		prodasset = {}
		for k in keys:
			zb = self.stock.zcfzbs[k]
			val = 0.0
			val += zb.fixedassenet
			val += zb.consprog
			val += zb.engimate
			val += zb.prodasse
			val += zb.comasse
			val += zb.hydrasset
			val += zb.intaasset
			val += zb.deveexpe
			val += zb.goodwill
			val += zb.prepexpe
			val += zb.logprepexpe
			val += zb.defetaxasset
			prodasset[k] = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / zb.totasset * 100)
		html_str += '</tr>\n'

		# 税前利润总额 / 生产资产
		html_str += '<tr>\n\t<td bgcolor="white">税前利润总额 / 生产资产</td>\n\t<td></td>\n'
		for k in keys:
			lb = self.stock.gslrbs[k]
			val = prodasset[k]
			html_str += '\t<td>%.2f%%</td>\n\t<td></td>\n' % (lb.totprofit / val * 100)
		html_str += '</tr>\n'

		# 其他流动资产
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">其他流动资产</td>\n\t<td style="background: %s; color: #FFFFFF">其它资产</td>\n' % (Cons.COLOR_BLUE, Cons.COLOR_BLUE)
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if zb.othercurrasse:
				val = zb.othercurrasse
			else:
				val = 0.0
			zb.othercurrasse = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / zb.totasset * 100)
		html_str += '</tr>\n'

		# 其他非流动资产
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">其他非流动资产</td>\n\t<td style="background: %s; color: #FFFFFF">其它资产</td>\n' % (Cons.COLOR_BLUE, Cons.COLOR_BLUE)
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if zb.othernoncasse:
				val = zb.othernoncasse
			else:
				val = 0.0
			zb.othernoncasse = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / zb.totasset * 100)
		html_str += '</tr>\n'

		# 合计
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">其它相关资产合计</td>\n\t<td></td>\n' % Cons.COLOR_BLUE
		for k in keys:
			zb = self.stock.zcfzbs[k]
			val = 0.0
			val += zb.othercurrasse
			val += zb.othernoncasse
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / zb.totasset * 100)
		html_str += '</tr>\n'

		# 资产合计
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">资产合计</td>\n\t<td></td>\n' % Cons.COLOR_YELLOW
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if zb.totasset:
				val = zb.totasset
			else:
				val = 0.0
			zb.totasset = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / zb.totasset * 100)
		html_str += '</tr>\n'

		# 总资产增长率
		html_str += '<tr bgcolor="white">\n\t<td>总资产增长率</td>\n\t<td></td>\n'
		for k in keys:
			k1 = '%s' % (int(k) - 1)
			if k1 in self.stock.zcfzbs:
				zb_lst = self.stock.zcfzbs[k1]
			else:
				zb_lst = ZCFZB()
			zb_cur = self.stock.zcfzbs[k]

			if zb_lst.totasset == 0:
				val = 0.0
			else:
				val = (zb_cur.totasset / zb_lst.totasset - 1) * 100
			html_str += '\t<td>%.2f%%</td>\n\t<td></td>\n' % (val)
		html_str += '<td>(本年/去年 - 1) * 100%</td></tr>\n'

		# 总资产周转率 = 营业收入 / 平均总资产，判断是否沃尔玛模式的关键指标
		html_str += '<tr bgcolor="white">\n\t<td>总资产周转率</td>\n\t<td></td>\n'
		for k in keys:
			lb = self.stock.gslrbs[k]
			zb_cur = self.stock.zcfzbs[k]
			k1 = '%s' % (int(k) - 1)
			if k1 in self.stock.zcfzbs:
				zb_lst = self.stock.zcfzbs[k1]
				totasset = (zb_cur.totasset + zb_lst.totasset) / 2
			else:
				totasset = zb_cur.totasset

			if totasset == 0:
				val = 0
			else:
				val = lb.bizinco /  totasset
			html_str += '\t<td>%.2f</td>\n\t<td></td>\n' % (val)
		html_str += '<td>营业收入 / 平均总资产</td></tr>\n'

		# 杠杆系数 = 平均总资产 / 净资产，判断是否银行模式的关键指标
		html_str += '<tr bgcolor="white">\n\t<td>杠杆系数</td>\n\t<td></td>\n'
		for k in keys:
			lb = self.stock.gslrbs[k]
			zb_cur = self.stock.zcfzbs[k]
			k1 = '%s' % (int(k) - 1)
			if k1 in self.stock.zcfzbs:
				zb_lst = self.stock.zcfzbs[k1]
				totasset = (zb_cur.totasset + zb_lst.totasset) / 2
			else:
				totasset = zb_cur.totasset

			val = totasset / zb_cur.righaggr
			html_str += '\t<td>%.2f</td>\n\t<td></td>\n' % (val)
		html_str += '<td>平均总资产 / 净资产</td></tr>\n'

		# 负债合计
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">负债合计</td>\n\t<td></td>\n' % Cons.COLOR_RED
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if zb.totliab:
				val = zb.totliab
			else:
				val = 0.0
			zb.totliab = val
			html_str += '\t<td>%.2f亿</td>\n\t<td></td>\n' % (val / Cons.Yi)
		html_str += '</tr>\n'

		# 所有者权益(或股东权益)合计
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">股东权益合计</td>\n\t<td></td>\n' % Cons.COLOR_GREEN
		for k in keys:
			zb = self.stock.zcfzbs[k]
			if zb.righaggr:
				val = zb.righaggr
			else:
				val = 0.0
			zb.righaggr = val
			html_str += '\t<td>%.2f亿</td>\n\t<td></td>\n' % (val / Cons.Yi)
		html_str += '</tr>\n'

		# 净资产增长率
		html_str += '<tr bgcolor="white">\n\t<td>净资产增长率</td>\n\t<td></td>\n'
		for k in keys:
			k1 = '%s' % (int(k) - 1)
			if k1 in self.stock.zcfzbs:
				zb_lst = self.stock.zcfzbs[k1]
			else:
				zb_lst = ZCFZB()
			zb_cur = self.stock.zcfzbs[k]

			if zb_lst.righaggr == 0:
				val = 0.0
			else:
				val = (zb_cur.righaggr / zb_lst.righaggr - 1) * 100
			html_str += '\t<td>%.2f%%</td>\n\t<td></td>\n' % (val)
		html_str += '<td>(本年/去年 - 1) * 100%</td></tr>\n'

		# 流动比率 = 流动资产 / 流动负债
		html_str += '<tr bgcolor="white">\n\t<td>流动比率</td>\n\t<td></td>\n'
		for k in keys:
			zb = self.stock.zcfzbs[k]
			val = zb.totcurrasset / zb.totalcurrliab
			html_str += '\t<td>%.2f</td>\n\t<td></td>\n' % (val)
		html_str += '<td>流动资产 / 流动负债</td></tr>\n'

		# 速动比率 = 速动资产 / 流动负债，其中速动资产  = 流动资产 - 存货
		html_str += '<tr bgcolor="white">\n\t<td>速动比率</td>\n\t<td></td>\n'
		for k in keys:
			zb = self.stock.zcfzbs[k]
			val = (zb.totcurrasset - zb.inve) / zb.totalcurrliab
			html_str += '\t<td>%.2f</td>\n\t<td></td>\n' % (val)
		html_str += '<td>速动资产 / 流动负债，其中速动资产  = 流动资产 - 存货</td></tr>\n'

		# 资产负债比率 = 资产总额 / 负债总额
		html_str += '<tr bgcolor="white">\n\t<td>资产负债比率</td>\n\t<td></td>\n'
		for k in keys:
			zb = self.stock.zcfzbs[k]
			val = zb.totasset / zb.totliab
			html_str += '\t<td>%.2f</td>\n\t<td></td>\n' % (val)
		html_str += '<td>资产总额 / 负债总额</td></tr>\n'

		# 表尾
		html_str += '</tbody></table>\n\n'

		### 其他应收款明细 ###
		html_str += '<p></p>\n\n<table border="2">\n<caption>其他应收款明细</caption>\n<thead>\n<tr>\n\t'

		# 表头
		for k in keys:
			tmpstr = '\t<th>%s</th>\n' % k
			html_str += tmpstr
		html_str += '</tr>\n</thead>\n<tbody>'

		for k in keys:
			if not k in self.stock.fjsjs:
				fj = FJSJ()
			else:
				fj = self.stock.fjsjs[k]

			if fj.otherrecedetail:
				val = fj.otherrecedetail
			else:
				val = ""
			fj.otherrecedetail = ""
			html_str += '\t<td>%s</td>\n' % val
		html_str += '</tr><tbody>\n'

		# 表尾
		html_str += '</table>\n\n</body>\n</html>'

		print html_str
		fname = 'db/%s_%s/资产负债表资产部分.html' % (self.stock.symbol, self.stock.name)
		ResUtil.save_html_content(html_str, fname)
