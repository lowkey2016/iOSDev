# -*- coding: utf-8 -*-

from models.stock import Stock
from utils.util_res import ResUtil

class FJSJDrawer(object):
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

		html_str += '<body>\n<h4>附加数据</h4>\n\n<table class="table table-bordered">\n\t<caption>附加</caption>\n<thead><tr>\n\t<th>项目</th>\n'

		keys = [k for k in sorted(self.stock.fjsjs)]
		keys.reverse()

		# 表头
		for k in keys:
			tmpstr = '\t<th>%s</th>\n' % k
			html_str += tmpstr
		html_str += '\t<th>备注</th>\n</tr>\n</thead>\n<tbody>\n'

		# 财报意见
		html_str += '<tr bgcolor="white">\n\t<td>财报意见</td>\n'
		for k in keys:
			fj = self.stock.fjsjs[k]
			if fj.finstmtcomments:
				val = fj.finstmtcomments
			else:
				val = ""
			fj.finstmtcomments = ""
			html_str += '\t<td>%s</td>\n' % (val)
		html_str += '</tr>\n'

		# 董事会在财报中提出的注意事项
		html_str += '<tr bgcolor="white">\n\t<td>董事会在财报中提出的注意事项</td>\n'
		for k in keys:
			fj = self.stock.fjsjs[k]
			if fj.finstmtspecials:
				val = fj.finstmtspecials
			else:
				val = ""
			fj.finstmtspecials = ""
			html_str += '\t<td>%s</td>\n' % (val)
		html_str += '</tr>\n'

		# 股份总数
		html_str += '<tr bgcolor="white">\n\t<td>股份总数</td>\n'
		for k in keys:
			fj = self.stock.fjsjs[k]
			if fj.sharecount:
				val = fj.sharecount
			else:
				val = 0
			fj.sharecount = val
			html_str += '\t<td>%.4f万股</td>\n' % (val / 10000)
		html_str += '</tr>\n</tbody>\n'

		# 表尾
		html_str += '</table>\n\n</body>\n</html>'

		print html_str
		fname = 'db/%s_%s/附加数据.html' % (self.stock.symbol, self.stock.name)
		ResUtil.save_html_content(html_str, fname)
