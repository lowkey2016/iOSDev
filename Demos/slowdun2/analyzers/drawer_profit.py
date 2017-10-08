# -*- coding: utf-8 -*-

from models.gslrb import GSLRB
from models.fjsj import FJSJ
from models.stock import Stock
from utils.util_res import ResUtil
from utils.util_math import MathUtil
import utils.util_cons as Cons

class ProfitDrawer(object):
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

		html_str += '<body>\n<h4>利润表</h4>\n\n<table class="table table-bordered">\n\t<caption>利润变化过程</caption>\n<thead><tr>\n\t<th>项目</th>\n\t<th>加/减</th>'

		keys = [k for k in sorted(self.stock.gslrbs)]
		keys.reverse()

		# 表头
		for k in keys:
			tmpstr = '\t<th colspan="2">%s</th>\n' % k
			html_str += tmpstr
		html_str += '\t<th>备注</th>\n</tr>\n</thead>\n<tbody>\n'

		# 一、营业总收入部分

		# 营业收入
		html_str += '<tr style="background: %s; color: #FFFFFF">\n\t<td>营业收入</td>\n\t<td style="background: %s; color: #FFFFFF">+</td>\n' % (Cons.COLOR_GREEN, Cons.COLOR_GREEN)
		for k in keys:
			lb = self.stock.gslrbs[k]
			if lb.bizinco:
				val = lb.bizinco
			else:
				val = 0.0
			lb.bizinco = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / lb.biztotinco * 100)
		html_str += '<td>默认都是除以营业总收入</td></tr>\n'

		# 营业收入年增长率
		html_str += '<tr bgcolor="white">\n\t<td>营业收入年增长率</td>\n\t<td></td>\n'
		for k in keys:
			k1 = '%s' % (int(k) - 1)
			if k1 in self.stock.gslrbs:
				lb_lst = self.stock.gslrbs[k1]
			else:
				lb_lst = GSLRB()
			lb_cur = self.stock.gslrbs[k]

			if lb_lst.bizinco == 0:
				val = 0.0
			else:
				val = (lb_cur.bizinco / lb_lst.bizinco - 1) * 100
			html_str += '\t<td>%.2f%%</td>\n\t<td></td>\n' % (val)
		html_str += '<td>(本年/去年 - 1) * 100%</td></tr>\n'

		# 营业收入复合年增长率
		html_str += '<tr bgcolor="white">\n\t<td>复合年增长率</td>\n\t<td></td>\n'
		for k in keys:
			k1 = keys[-1]
			lb_lst = self.stock.gslrbs[k1]
			lb_cur = self.stock.gslrbs[k]
			val = MathUtil.comprateper(lb_cur.bizinco / lb_lst.bizinco, int(k) - int(k1))
			html_str += '\t<td>%.2f%%</td>\n\t<td></td>\n' % (val)
		html_str += '<td>以最初的年份为基数</td></tr>\n'

		# 利息收入
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">利息收入</td>\n\t<td style="background: %s; color: #FFFFFF">+</td>\n' % (Cons.COLOR_GREEN, Cons.COLOR_GREEN)
		for k in keys:
			lb = self.stock.gslrbs[k]
			if lb.inteinco:
				val = lb.inteinco
			else:
				val = 0.0
			lb.inteinco = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / lb.biztotinco * 100)
		html_str += '</tr>\n'

		# 房地产销售收入
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">房地产销售收入</td>\n\t<td style="background: %s; color: #FFFFFF">+</td>\n' % (Cons.COLOR_GREEN, Cons.COLOR_GREEN)
		for k in keys:
			lb = self.stock.gslrbs[k]
			if lb.realsale:
				val = lb.realsale
			else:
				val = 0.0
			lb.realsale = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / lb.biztotinco * 100)
		html_str += '</tr>\n'

		# 其他业务收入
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">其他业务收入</td>\n\t<td style="background: %s; color: #FFFFFF">+</td>\n' % (Cons.COLOR_GREEN, Cons.COLOR_GREEN)
		for k in keys:
			lb = self.stock.gslrbs[k]
			if lb.otherbizinco:
				val = lb.otherbizinco
			else:
				val = 0.0
			lb.otherbizinco = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / lb.biztotinco * 100)
		html_str += '</tr>\n'

		# 营业总收入
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">营业总收入</td>\n\t<td style="background: %s; color: #FFFFFF">共</td>\n' % (Cons.COLOR_GREEN, Cons.COLOR_GREEN)
		for k in keys:
			lb = self.stock.gslrbs[k]
			if lb.biztotinco:
				val = lb.biztotinco
			else:
				val = 0.0
			lb.biztotinco = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>100%%</td>\n' % (val / Cons.Yi)
		html_str += '</tr>\n'

		# 营业总收入年增长率
		html_str += '<tr bgcolor="white">\n\t<td>营业总收入年增长率</td>\n\t<td></td>\n'
		for k in keys:
			k1 = '%s' % (int(k) - 1)
			if k1 in self.stock.gslrbs:
				lb_lst = self.stock.gslrbs[k1]
			else:
				lb_lst = GSLRB()
			lb_cur = self.stock.gslrbs[k]

			if lb_lst.biztotinco == 0:
				val = 0.0
			else:
				val = (lb_cur.biztotinco / lb_lst.biztotinco - 1) * 100
			html_str += '\t<td>%.2f%%</td>\n\t<td></td>\n' % (val)
		html_str += '<td>(本年/去年 - 1) * 100%</td></tr>\n'

		# 二、营业总成本部分

		# 营业成本
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">营业成本</td>\n\t<td style="background: %s; color: #FFFFFF">-</td>\n' % (Cons.COLOR_RED, Cons.COLOR_RED)
		for k in keys:
			lb = self.stock.gslrbs[k]
			if lb.bizcost:
				val = lb.bizcost
			else:
				val = 0.0
			lb.bizcost = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / lb.biztotcost * 100)
		html_str += '<td>除以营业总成本，本部分默认都是</td></tr>\n'

		# 营业成本年增长率
		html_str += '<tr bgcolor="white">\n\t<td>营业成本年增长率</td>\n\t<td></td>\n'
		for k in keys:
			k1 = '%s' % (int(k) - 1)
			if k1 in self.stock.gslrbs:
				lb_lst = self.stock.gslrbs[k1]
			else:
				lb_lst = GSLRB()
			lb_cur = self.stock.gslrbs[k]

			if lb_lst.bizcost == 0:
				val = 0.0
			else:
				val = (lb_cur.bizcost / lb_lst.bizcost - 1) * 100
			html_str += '\t<td>%.2f%%</td>\n\t<td></td>\n' % (val)
		html_str += '<td>(本年/去年 - 1) * 100%</td></tr>\n'

		# 利息支出
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">利息支出</td>\n\t<td style="background: %s; color: #FFFFFF">-</td>\n' % (Cons.COLOR_RED, Cons.COLOR_RED)
		for k in keys:
			lb = self.stock.gslrbs[k]
			if lb.inteexpe:
				val = lb.inteexpe
			else:
				val = 0.0
			lb.inteexpe = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / lb.biztotcost * 100)
		html_str += '</tr>\n'

		# 房地产销售成本
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">房地产销售成本</td>\n\t<td style="background: %s; color: #FFFFFF">-</td>\n' % (Cons.COLOR_RED, Cons.COLOR_RED)
		for k in keys:
			lb = self.stock.gslrbs[k]
			if lb.realsalecost:
				val = lb.realsalecost
			else:
				val = 0.0
			lb.realsalecost = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / lb.biztotcost * 100)
		html_str += '</tr>\n'

		# 其他业务成本
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">其他业务成本</td>\n\t<td style="background: %s; color: #FFFFFF">-</td>\n' % (Cons.COLOR_RED, Cons.COLOR_RED)
		for k in keys:
			lb = self.stock.gslrbs[k]
			if lb.otherbizcost:
				val = lb.otherbizcost
			else:
				val = 0.0
			lb.otherbizcost = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / lb.biztotcost * 100)
		html_str += '</tr>\n'

		# 营业税金及附加
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">营业税金及附加</td>\n\t<td style="background: %s; color: #FFFFFF">-</td>\n' % (Cons.COLOR_RED, Cons.COLOR_RED)
		for k in keys:
			lb = self.stock.gslrbs[k]
			if lb.biztax:
				val = lb.biztax
			else:
				val = 0.0
			lb.biztax = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / lb.biztotcost * 100)
		html_str += '</tr>\n'

		# 研发费用
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">研发费用</td>\n\t<td style="background: %s; color: #FFFFFF">-</td>\n' % (Cons.COLOR_RED, Cons.COLOR_RED)
		for k in keys:
			lb = self.stock.gslrbs[k]
			if lb.deveexpe:
				val = lb.deveexpe
			else:
				val = 0.0
			lb.deveexpe = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / lb.biztotcost * 100)
		html_str += '</tr>\n'

		# 财报中记录的开发支出
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">财报中记录的开发支出</td>\n\t<td style="background: %s; color: #FFFFFF">-</td>\n' % (Cons.COLOR_RED, Cons.COLOR_RED)
		for k in keys:
			lb = self.stock.gslrbs[k]
			if k in self.stock.fjsjs:
				fj = self.stock.fjsjs[k]
			else:
				fj = FJSJ()

			if fj.findevexp:
				val = fj.findevexp
			else:
				val = 0.0
			fj.findevexp = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / lb.biztotcost * 100)
		html_str += '</tr>\n'

		# 销售费用
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">销售费用</td>\n\t<td style="background: %s; color: #FFFFFF">-</td>\n' % (Cons.COLOR_RED, Cons.COLOR_RED)
		for k in keys:
			lb = self.stock.gslrbs[k]
			if lb.salesexpe:
				val = lb.salesexpe
			else:
				val = 0.0
			lb.salesexpe = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / lb.biztotcost * 100)
		html_str += '</tr>\n'

		# 管理费用
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">管理费用</td>\n\t<td style="background: %s; color: #FFFFFF">-</td>\n' % (Cons.COLOR_RED, Cons.COLOR_RED)
		for k in keys:
			lb = self.stock.gslrbs[k]
			if lb.manaexpe:
				val = lb.manaexpe
			else:
				val = 0.0
			lb.manaexpe = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / lb.biztotcost * 100)
		html_str += '</tr>\n'

		# 财务费用
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">财务费用</td>\n\t<td style="background: %s; color: #FFFFFF">-</td>\n' % (Cons.COLOR_RED, Cons.COLOR_RED)
		for k in keys:
			lb = self.stock.gslrbs[k]
			if lb.finexpe:
				val = lb.finexpe
			else:
				val = 0.0
			lb.finexpe = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / lb.biztotcost * 100)
		html_str += '</tr>\n'

		# 费用 / 毛利润 = (销售费用 + 管理费用 + 正数的财务费用) / 毛利润
		html_str += '<tr bgcolor="white">\n\t<td>费用</td>\n\t<td></td>\n'
		for k in keys:
			lb = self.stock.gslrbs[k]
			val = lb.salesexpe + lb.manaexpe
			if lb.finexpe > 0:
				val += lb.finexpe
			grospro = lb.bizinco - lb.bizcost
			rate = val / grospro * 100
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, rate)
		html_str += '<td>费用 = 销售费用 + 管理费用 + 正数的财务费用，除以毛利润</td></tr>\n'

		# 销售费用和管理费用总和的年增长率
		html_str += '<tr bgcolor="white">\n\t<td>销售费用和管理费用总和的年增长率</td>\n\t<td></td>\n'
		for k in keys:
			k1 = '%s' % (int(k) - 1)
			if k1 in self.stock.gslrbs:
				lb_lst = self.stock.gslrbs[k1]
			else:
				lb_lst = GSLRB()
			lb_cur = self.stock.gslrbs[k]

			val_cur = lb_cur.salesexpe + lb_cur.manaexpe
			val_lst = lb_lst.salesexpe + lb_lst.manaexpe
			if val_lst == 0:
				rate = 0.0
			else:
				rate = (val_cur / val_lst - 1) * 100
			html_str += '\t<td>%.2f%%</td>\n\t<td></td>\n' % (rate)
		html_str += '<td>(本年/去年 - 1) * 100%</td></tr>\n'

		# 营业成本率 = 营业成本 / 营业收入
		html_str += '<tr bgcolor="white">\n\t<td>营业成本率</td>\n\t<td></td>\n'
		for k in keys:
			lb = self.stock.gslrbs[k]
			val = lb.bizcost / lb.bizinco * 100
			html_str += '\t<td>%.2f%%</td>\n\t<td></td>\n' % (val)
		html_str += '<td>营业成本 / 营业收入</td></tr>\n'

		# 销售费用率 = 销售费用 / 营业收入
		html_str += '<tr bgcolor="white">\n\t<td>销售费用率</td>\n\t<td></td>\n'
		for k in keys:
			lb = self.stock.gslrbs[k]
			val = lb.salesexpe / lb.bizinco * 100
			html_str += '\t<td>%.2f%%</td>\n\t<td></td>\n' % (val)
		html_str += '<td>销售费用 / 营业收入</td></tr>\n'

		# 管理费用率 = 管理费用 / 营业收入
		html_str += '<tr bgcolor="white">\n\t<td>管理费用率</td>\n\t<td></td>\n'
		for k in keys:
			lb = self.stock.gslrbs[k]
			val = lb.manaexpe / lb.bizinco * 100
			html_str += '\t<td>%.2f%%</td>\n\t<td></td>\n' % (val)
		html_str += '<td>管理费用 / 营业收入</td></tr>\n'

		# 息税前利润率 = (利息支出 + 营业利润) / 营业收入
		html_str += '<tr bgcolor="white">\n\t<td>息税前利润率</td>\n\t<td></td>\n'
		for k in keys:
			lb = self.stock.gslrbs[k]
			val = (lb.biztotinco - lb.biztotcost + lb.inteexpe) / lb.bizinco * 100
			html_str += '\t<td>%.2f%%</td>\n\t<td></td>\n' % (val)
		html_str += '<td>(利息支出 + 营业利润) / 营业收入</td></tr>\n'

		# 营业总成本
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">营业总成本</td>\n\t<td style="background: %s; color: #FFFFFF">共</td>\n' % (Cons.COLOR_RED, Cons.COLOR_RED)
		for k in keys:
			lb = self.stock.gslrbs[k]
			if lb.biztotcost:
				val = lb.biztotcost
			else:
				val = 0.0
			lb.biztotcost = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>100%%</td>\n' % (val / Cons.Yi)
		html_str += '</tr>\n'

		# 营业总成本年增长率
		html_str += '<tr bgcolor="white">\n\t<td>营业总成本年增长率</td>\n\t<td></td>\n'
		for k in keys:
			k1 = '%s' % (int(k) - 1)
			if k1 in self.stock.gslrbs:
				lb_lst = self.stock.gslrbs[k1]
			else:
				lb_lst = GSLRB()
			lb_cur = self.stock.gslrbs[k]

			if lb_lst.biztotcost == 0:
				val = 0.0
			else:
				val = (lb_cur.biztotcost / lb_lst.biztotcost - 1) * 100
			html_str += '\t<td>%.2f%%</td>\n\t<td></td>\n' % (val)
		html_str += '<td>(本年/去年 - 1) * 100%</td></tr>\n'

		# 毛利润和毛利率
		html_str += '<tr bgcolor="white">\n\t<td style="background: %s; color: #FFFFFF">毛利润</td>\n\t<td></td>\n' % Cons.COLOR_PURPLE
		for k in keys:
			lb = self.stock.gslrbs[k]
			val = lb.bizinco - lb.bizcost
			rate = val / lb.bizinco * 100
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, rate)
		html_str += '<td>毛利率在后面</td></tr>\n'

		# 扣除经常性损益营业利润
		html_str += '<tr bgcolor="white">\n\t<td style="background: %s; color: #FFFFFF">扣除经常性损益营业利润</td>\n\t<td></td>\n' % Cons.COLOR_PURPLE
		for k in keys:
			lb = self.stock.gslrbs[k]
			val = lb.biztotinco - lb.biztotcost
			rate = val / lb.biztotinco * 100
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, rate)
		html_str += '</tr>\n'

		# 三、非经常性损益部分

		# 资产减值损失
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">资产减值损失</td>\n\t<td style="background: %s; color: #FFFFFF">-</td>\n' % (Cons.COLOR_RED, Cons.COLOR_RED)
		for k in keys:
			lb = self.stock.gslrbs[k]
			if lb.asseimpaloss:
				val = lb.asseimpaloss
			else:
				val = 0.0
			lb.asseimpaloss = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / lb.biztotinco * 100)
		html_str += '</tr>\n'

		# 公允价值变动收益
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">公允价值变动收益</td>\n\t<td style="background: %s; color: #FFFFFF">+</td>\n' % (Cons.COLOR_GREEN, Cons.COLOR_GREEN)
		for k in keys:
			lb = self.stock.gslrbs[k]
			if lb.valuechgloss:
				val = lb.valuechgloss
			else:
				val = 0.0
			lb.valuechgloss = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / lb.biztotinco * 100)
		html_str += '</tr>\n'

		# 投资收益
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">投资收益</td>\n\t<td style="background: %s; color: #FFFFFF">+</td>\n' % (Cons.COLOR_GREEN, Cons.COLOR_GREEN)
		for k in keys:
			lb = self.stock.gslrbs[k]
			if lb.inveinco:
				val = lb.inveinco
			else:
				val = 0.0
			lb.inveinco = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / lb.biztotinco * 100)
		html_str += '</tr>\n'

		# 其中:对联营企业和合营企业的投资收益
		html_str += '<tr bgcolor="white">\n\t<td>其中:对联营企业和合营企业的投资收益</td>\n\t<td>+</td>\n'
		for k in keys:
			lb = self.stock.gslrbs[k]
			if lb.assoinveprof:
				val = lb.assoinveprof
			else:
				val = 0.0
			lb.assoinveprof = val

			if lb.inveinco == 0:
				rate = 0
			else:
				rate = val / lb.inveinco * 100
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, rate)
		html_str += '<td>除以投资收益</td></tr>\n'

		# 汇兑收益
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">汇兑收益</td>\n\t<td style="background: %s; color: #FFFFFF">+</td>\n' % (Cons.COLOR_GREEN, Cons.COLOR_GREEN)
		for k in keys:
			lb = self.stock.gslrbs[k]
			if lb.exchggain:
				val = lb.exchggain
			else:
				val = 0.0
			lb.exchggain = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / lb.biztotinco * 100)
		html_str += '</tr>\n'

		# 其他业务利润
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">其他业务利润</td>\n\t<td style="background: %s; color: #FFFFFF">+</td>\n' % (Cons.COLOR_GREEN, Cons.COLOR_GREEN)
		for k in keys:
			lb = self.stock.gslrbs[k]
			if lb.otherbizprof:
				val = lb.otherbizprof
			else:
				val = 0.0
			lb.otherbizprof = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / lb.biztotinco * 100)
		html_str += '</tr>\n'

		# 四、营业利润部分

		# 营业利润
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">营业利润</td>\n\t<td></td>\n' % Cons.COLOR_PURPLE
		for k in keys:
			lb = self.stock.gslrbs[k]
			if lb.perprofit:
				val = lb.perprofit
			else:
				val = 0.0
			lb.perprofit = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / lb.biztotinco * 100)
		html_str += '<td>营业利润率在后面</td></tr>\n'

		# 营业利润年增长率
		html_str += '<tr bgcolor="white">\n\t<td>营业利润年增长率</td>\n\t<td></td>\n'
		for k in keys:
			k1 = '%s' % (int(k) - 1)
			if k1 in self.stock.gslrbs:
				lb_lst = self.stock.gslrbs[k1]
			else:
				lb_lst = GSLRB()
			lb_cur = self.stock.gslrbs[k]

			if lb_lst.perprofit == 0:
				val = 0.0
			else:
				val = (lb_cur.perprofit / lb_lst.perprofit - 1) * 100
			html_str += '\t<td>%.2f%%</td>\n\t<td></td>\n' % (val)
		html_str += '<td>(本年/去年 - 1) * 100%</td></tr>\n'

		# 营业利润复合年增长率
		html_str += '<tr bgcolor="white">\n\t<td>复合年增长率</td>\n\t<td></td>\n'
		for k in keys:
			k1 = keys[-1]
			lb_lst = self.stock.gslrbs[k1]
			lb_cur = self.stock.gslrbs[k]
			val = MathUtil.comprateper(lb_cur.perprofit / lb_lst.perprofit, int(k) - int(k1))
			html_str += '\t<td>%.2f%%</td>\n\t<td></td>\n' % (val)
		html_str += '<td>以最初的年份为基数</td></tr>\n'

		# 营业外收入
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">营业外收入</td>\n\t<td style="background: %s; color: #FFFFFF">+</td>\n' % (Cons.COLOR_GREEN, Cons.COLOR_GREEN)
		for k in keys:
			lb = self.stock.gslrbs[k]
			if lb.nonoreve:
				val = lb.nonoreve
			else:
				val = 0.0
			lb.nonoreve = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / lb.perprofit * 100)
		html_str += '<td>除以营业利润，本部分默认都是</td></tr>\n'

		# 营业外支出
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">营业外支出</td>\n\t<td style="background: %s; color: #FFFFFF">-</td>\n' % (Cons.COLOR_RED, Cons.COLOR_RED)
		for k in keys:
			lb = self.stock.gslrbs[k]
			if lb.nonoexpe:
				val = lb.nonoexpe
			else:
				val = 0.0
			lb.nonoexpe = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / lb.perprofit * 100)
		html_str += '</tr>\n'

		# 营业外收支净额
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">营业外收支净额</td>\n\t<td style="background: %s; color: #FFFFFF">-</td>\n' % (Cons.COLOR_PURPLE, Cons.COLOR_PURPLE)
		for k in keys:
			lb = self.stock.gslrbs[k]
			val = lb.nonoreve - lb.nonoexpe
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / lb.perprofit * 100)
		html_str += '</tr>\n'

		# 非流动资产处置损失
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">非流动资产处置损失</td>\n\t<td style="background: %s; color: #FFFFFF">-</td>\n' % (Cons.COLOR_RED, Cons.COLOR_RED)
		for k in keys:
			lb = self.stock.gslrbs[k]
			if lb.noncassetsdisl:
				val = lb.noncassetsdisl
			else:
				val = 0.0
			lb.noncassetsdisl = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / lb.perprofit * 100)
		html_str += '</tr>\n'

		# 五、净利润部分

		# 利润总额
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">利润总额</td>\n\t<td></td>\n' % Cons.COLOR_PURPLE
		for k in keys:
			lb = self.stock.gslrbs[k]
			if lb.totprofit:
				val = lb.totprofit
			else:
				val = 0.0
			lb.totprofit = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / lb.biztotinco * 100)
		html_str += '</tr>\n'

		# 所得税费用
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">所得税费用</td>\n\t<td style="background: %s; color: #FFFFFF">-</td>\n' % (Cons.COLOR_RED, Cons.COLOR_RED)
		for k in keys:
			lb = self.stock.gslrbs[k]
			if lb.incotaxexpe:
				val = lb.incotaxexpe
			else:
				val = 0.0
			lb.incotaxexpe = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / lb.totprofit * 100)
		html_str += '<td>后面的是所得税率</td></tr>\n'

		# 净利润
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">净利润</td>\n\t<td></td>\n' % Cons.COLOR_PURPLE
		for k in keys:
			lb = self.stock.gslrbs[k]
			if lb.netprofit:
				val = lb.netprofit
			else:
				val = 0.0
			lb.netprofit = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / lb.biztotinco * 100)
		html_str += '<td>后面的是净利率</td></tr>\n'

		# 归属于母公司所有者的净利润
		html_str += '<tr bgcolor="white">\n\t<td>归属于母公司所有者的净利润</td>\n\t<td></td>\n'
		for k in keys:
			lb = self.stock.gslrbs[k]
			if lb.parenetp:
				val = lb.parenetp
			else:
				val = 0.0
			lb.parenetp = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / lb.netprofit * 100)
		html_str += '<td>除以净利润</td></tr>\n'

		# 少数股东损益
		html_str += '<tr bgcolor="white">\n\t<td>少数股东损益</td>\n\t<td></td>\n'
		for k in keys:
			lb = self.stock.gslrbs[k]
			if lb.minysharrigh:
				val = lb.minysharrigh
			else:
				val = 0.0
			lb.minysharrigh = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / lb.netprofit * 100)
		html_str += '<td>除以净利润</td></tr>\n'

		# 经营现金流净额 / 净利润
		html_str += '<tr bgcolor="white">\n\t<td>经营现金流净额 / 净利润</td>\n\t<td></td>\n'
		for k in keys:
			lb = self.stock.gslrbs[k]
			xb = self.stock.xjllbs[k]
			val = xb.mananetr / lb.netprofit
			if val >= 1:
				color = Cons.COLOR_GREEN
			else:
				color = Cons.COLOR_RED
			html_str += '\t<td style="background: %s; color: #FFFFFF">%.2f</td>\n\t<td></td>\n' % (color, val)
		html_str += '</tr>\n'

		# 六、每股收益部分

		# 基本每股收益
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">基本每股收益</td>\n\t<td></td>\n' % Cons.COLOR_PINK
		for k in keys:
			lb = self.stock.gslrbs[k]
			if lb.basiceps:
				val = lb.basiceps
			else:
				val = 0.0
			lb.basiceps = val
			html_str += '\t<td>%.2f</td>\n\t<td></td>\n' % (val)
		html_str += '</tr>\n'

		# 稀释每股收益
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">基稀释每股收益</td>\n\t<td></td>\n' % Cons.COLOR_PINK
		for k in keys:
			lb = self.stock.gslrbs[k]
			if lb.dilutedeps:
				val = lb.dilutedeps
			else:
				val = 0.0
			lb.dilutedeps = val
			html_str += '\t<td>%.2f</td>\n\t<td></td>\n' % (val)
		html_str += '</tr>\n'

		# 七、综合收益部分

		# 其他综合收益
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">其他综合收益</td>\n\t<td style="background: %s; color: #FFFFFF">+</td>\n' % (Cons.COLOR_GREEN, Cons.COLOR_GREEN)
		for k in keys:
			lb = self.stock.gslrbs[k]
			if lb.othercompinco:
				val = lb.othercompinco
			else:
				val = 0.0
			lb.othercompinco = val

			if lb.compincoamt:
				rate = val / lb.compincoamt * 100
			else:
				rate = 0
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, rate)
		html_str += '<td>除以综合收益总额</td></tr>\n'

		# 归属于母公司所有者的其他综合收益
		html_str += '<tr>\n\t<td>归属于母公司所有者的其他综合收益</td>\n\t<td></td>\n'
		for k in keys:
			lb = self.stock.gslrbs[k]
			if lb.parecompinco:
				val = lb.parecompinco
			else:
				val = 0.0
			lb.parecompinco = val

			if lb.othercompinco == 0:
				rate = 0
			else:
				rate = val / lb.othercompinco * 100
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, rate)
		html_str += '<td>除以其他综合收益</td></tr>\n'

		# 归属于少数股东的其他综合收益
		html_str += '<tr>\n\t<td>归属于少数股东的其他综合收益</td>\n\t<td></td>\n'
		for k in keys:
			lb = self.stock.gslrbs[k]
			if lb.minysharinco:
				val = lb.minysharinco
			else:
				val = 0.0
			lb.minysharinco = val

			if lb.othercompinco == 0:
				rate = 0
			else:
				rate = val / lb.othercompinco * 100
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, rate)
		html_str += '<td>除以其他综合收益</td></tr>\n'

		# 综合收益总额
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">综合收益总额</td>\n\t<td></td>\n' % Cons.COLOR_PURPLE
		for k in keys:
			lb = self.stock.gslrbs[k]
			if lb.compincoamt:
				val = lb.compincoamt
			else:
				val = 0.0
			lb.compincoamt = val
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, val / lb.biztotinco * 100)
		html_str += '</tr>\n'

		# 归属于母公司所有者的综合收益总额
		html_str += '<tr>\n\t<td>归属于母公司所有者的综合收益总额</td>\n\t<td></td>\n'
		for k in keys:
			lb = self.stock.gslrbs[k]
			if lb.parecompincoamt:
				val = lb.parecompincoamt
			else:
				val = 0.0
			lb.parecompincoamt = val

			if lb.compincoamt:
				rate = val / lb.compincoamt * 100
			else:
				rate = 0
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, rate)
		html_str += '<td>除以综合收益总额</td></tr>\n'

		# 归属于少数股东的综合收益总额
		html_str += '<tr>\n\t<td>归属于少数股东的综合收益总额</td>\n\t<td></td>\n'
		for k in keys:
			lb = self.stock.gslrbs[k]
			if lb.minysharincoamt:
				val = lb.minysharincoamt
			else:
				val = 0.0
			lb.minysharincoamt = val

			if lb.compincoamt:
				rate = val / lb.compincoamt * 100
			else:
				rate = 0
			html_str += '\t<td>%.2f亿</td>\n\t<td>%.2f%%</td>\n' % (val / Cons.Yi, rate)
		html_str += '<td>除以综合收益总额</td></tr>\n'

		# 加权平均净资产收益率 ROE = 净利润 / 平均净资产
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">加权平均 ROE</td>\n\t<td></td>\n' % Cons.COLOR_PURPLE
		for k in keys:
			lb = self.stock.gslrbs[k]

			zb_cur = self.stock.zcfzbs[k]
			k1 = '%s' % (int(k) - 1)
			if k1 in self.stock.zcfzbs:
				zb_lst = self.stock.zcfzbs[k1]
				righaggr = (zb_cur.righaggr + zb_lst.righaggr) / 2
			else:
				righaggr = zb_cur.righaggr

			val = lb.netprofit / righaggr * 100
			if val > 15:
				color = Cons.COLOR_GREEN
			else:
				color = Cons.COLOR_RED
			html_str += '\t<td style="background: %s; color: #FFFFFF">%.2f%%</td>\n\t<td></td>\n' % (color, val)
		html_str += '<td>净利润 / 平均净资产</td></tr>\n'

		# 加权平均总资产收益率 ROA = 净利润 / 平均总资产
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">加权平均 ROA</td>\n\t<td></td>\n' % Cons.COLOR_PURPLE
		for k in keys:
			lb = self.stock.gslrbs[k]

			zb_cur = self.stock.zcfzbs[k]
			k1 = '%s' % (int(k) - 1)
			if k1 in self.stock.zcfzbs:
				zb_lst = self.stock.zcfzbs[k1]
				totassetave = (zb_cur.totasset + zb_lst.totasset) / 2
			else:
				totassetave = zb_cur.totasset

			val = lb.netprofit / totassetave * 100
			if val > 7.5:
				color = Cons.COLOR_GREEN
			else:
				color = Cons.COLOR_RED
			html_str += '\t<td style="background: %s; color: #FFFFFF">%.2f%%</td>\n\t<td></td>\n' % (color, val)
		html_str += '<td>净利润 / 平均总资产</td></tr>\n'

		# 本期 ROE = 净利润 / 上期净资产
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">本期 ROE</td>\n\t<td></td>\n' % Cons.COLOR_PURPLE
		for k in keys:
			lb = self.stock.gslrbs[k]

			zb_cur = self.stock.zcfzbs[k]
			k1 = '%s' % (int(k) - 1)
			if k1 in self.stock.zcfzbs:
				zb_lst = self.stock.zcfzbs[k1]
				righaggr = zb_lst.righaggr
				val = lb.netprofit / righaggr * 100
			else:
				val = 0

			if val > 15:
				color = Cons.COLOR_GREEN
			else:
				color = Cons.COLOR_RED
			html_str += '\t<td style="background: %s; color: #FFFFFF">%.2f%%</td>\n\t<td></td>\n' % (color, val)
		html_str += '<td>净利润 / 上期净资产</td></tr>\n'

		# 本期 ROA = 净利润 / 上期总资产
		html_str += '<tr>\n\t<td style="background: %s; color: #FFFFFF">本期 ROA</td>\n\t<td></td>\n' % Cons.COLOR_PURPLE
		for k in keys:
			lb = self.stock.gslrbs[k]

			zb_cur = self.stock.zcfzbs[k]
			k1 = '%s' % (int(k) - 1)
			if k1 in self.stock.zcfzbs:
				zb_lst = self.stock.zcfzbs[k1]
				totasset = zb_lst.totasset
				val = lb.netprofit / totasset * 100
			else:
				val = 0
			
			if val > 7.5:
				color = Cons.COLOR_GREEN
			else:
				color = Cons.COLOR_RED
			html_str += '\t<td style="background: %s; color: #FFFFFF">%.2f%%</td>\n\t<td></td>\n' % (color, val)
		html_str += '<td>净利润 / 上期总资产</td></tr><tbody>\n'

		# 表尾
		html_str += '</table>\n\n'

		# 表尾
		html_str += '</body>\n</html>'

		print html_str
		fname = 'db/%s_%s/利润表.html' % (self.stock.symbol, self.stock.name)
		ResUtil.save_html_content(html_str, fname)
