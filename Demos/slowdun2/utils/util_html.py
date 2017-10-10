# -*- coding: utf-8 -*-

from utils.util_res import ResUtil
import utils.util_cons as Cons

class HTMLUtil(object):
	def __init__(self):
		self.html_str = ''

	def add_start(self):
		self.html_str += """
		<html>
		<head>
		<link rel="stylesheet" href="https://cdn.bootcss.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">

		<!-- 最新的 Bootstrap 核心 JavaScript 文件 -->
		<script src="https://cdn.bootcss.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>
		<style>tbody tr:first-child td:nth-child(1), tbody tr:first-child td:nth-child(2) { white-space: nowrap; } thead tr:first-child th:last-child { white-space: nowrap; padding: 5px 50px; }</style>
		</head>

		<body>
		"""

	def add_title(self, title):
		self.html_str += '<h4>%s</h4>' % title

	def add_table_start(self, caption):
		self.html_str += '<table class="table table-bordered">\n<caption>%s</caption>' % caption

	def add_table_head_start(self):
		self.html_str += '<thead><tr>'

	def add_table_head_th(self, th, colspan=1, color=Cons.COLOR_WHITE):
		if color == Cons.COLOR_WHITE:
			font_color = Cons.COLOR_BLACK
		else:
			font_color = Cons.COLOR_WHITE
		self.html_str += '<th colspan="%d" style="background: %s; color: %s">%s</th>' % (colspan, color, font_color, th)

	def add_table_head_th_recommend(self):
		self.add_table_head_th('备注')

	def add_table_head_end(self):
		self.html_str += '</tr></thead>'
	
	def add_table_body_start(self):
		self.html_str += '<tbody>'

	def add_table_body_tr_start(self):
		self.html_str += '<tr>'

	def add_table_body_td(self, td, color=Cons.COLOR_WHITE):
		if color == Cons.COLOR_WHITE:
			font_color = Cons.COLOR_BLACK
		else:
			font_color = Cons.COLOR_WHITE
		self.html_str += '<td style="background: %s; color: %s">%s</td>' % (color, font_color, td)

	def add_table_body_td_val(self, val, color=Cons.COLOR_WHITE, unit=None):
		assert isinstance(val, (int, float))
		val = float(val)
		if unit == Cons.Yi:
			s = '%.2f亿' % (val / Cons.Yi)
		elif unit == Cons.Percent:
			s = '%.2f%%' % (val * 100)
		elif unit:
			s = '%.2f%s' % (val, unit)
		else:
			s = '%.2f' % val
		self.add_table_body_td(td=s, color=color)

	def add_table_body_td_empty(self):
		self.add_table_body_td(' ')

	def add_table_body_tr_end(self):
		self.html_str += '</tr>'

	def add_table_body_end(self):
		self.html_str += '</tbody>'

	def add_table_end(self):
		self.html_str += '</table>'

	def add_end(self):
		self.html_str += '</body></html>'

	def save_to_stock_file(self, stock, fname):
		fname = 'db/%s_%s/%s.html' % (stock.symbol, stock.name, fname)
		ResUtil.save_html_content(self.html_str, fname)

	def save_to_file(self, fname):
		fname = 'db/%s.html' % fname
		ResUtil.save_html_content(self.html_str, fname)
