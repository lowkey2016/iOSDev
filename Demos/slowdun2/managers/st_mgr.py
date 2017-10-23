# -*- coding: utf-8 -*-

import os
import sys
import re
from utils.util_res import ResUtil
from utils.util_req import ReqUtil
from utils.util_re import RegUtil
import json

class StMgr(object):
	def fetch_finforms_data_from_network(self, st_symbol):
		req = ReqUtil(st_symbol)
		html_content = req.prepare()
		if html_content is not None:
			desc = '<title>(.*?)\(%s\)' % st_symbol
			st_name = RegUtil.match_one_from_re(desc, html_content)
		else:
			st_name = ''
		# fname = 'test_html_%s' % st_name
		# file_path = ResUtil.get_file_path(fname)
		# with open(file_path, 'w') as outfile:
		# 	outfile.write(html_content)
		dirname = 'db/%s_%s' % (st_symbol, st_name)

		# 资产负债表
		content = req.fetch(ReqUtil.REP_TYPE_ASSETS)
		json_data = json.loads(content)
		file_path = ResUtil.get_zcfzb_file_path(dirname)
		with open(file_path, 'w') as outfile:
			json.dump(json_data, outfile)
		print content

		# 利润表
		content = req.fetch(ReqUtil.REP_TYPE_PROFIT)
		json_data = json.loads(content)
		file_path = ResUtil.get_gslrb_file_path(dirname)
		with open(file_path, 'w') as outfile:
			json.dump(json_data, outfile)
		print content

		# 现金流量表
		content = req.fetch(ReqUtil.REP_TYPE_CASH)
		json_data = json.loads(content)
		file_path = ResUtil.get_xjllb_file_path(dirname)
		with open(file_path, 'w') as outfile:
			json.dump(json_data, outfile)
		print content

	def fetch_curdata_from_network(self, st_symbol):
		req = ReqUtil(st_symbol)
		html_content = req.prepare()
		if html_content is not None:
			desc = '<title>(.*?)\(%s\)' % st_symbol
			st_name = RegUtil.match_one_from_re(desc, html_content)
		else:
			st_name = ''
		dirname = 'db/%s_%s' % (st_symbol, st_name)

		# 最新数据
		content = req.fetch(ReqUtil.REP_TYPE_CUR)
		json_data = json.loads(content)
		file_path = ResUtil.get_quote_file_path(dirname)
		with open(file_path, 'w') as outfile:
			json.dump(json_data, outfile)
		print content

	# 家电的厨电细分行业
	def fetch_jiadian_chudian_finforms_data_from_network(self):
		self.fetch_finforms_data_from_network('SZ002508') # 老板电器
		self.fetch_finforms_data_from_network('SZ002035') # 华帝股份
		self.fetch_finforms_data_from_network('SZ002543') # 万和电气
		self.fetch_finforms_data_from_network('SZ002032') # 苏泊尔
		self.fetch_finforms_data_from_network('SZ002242') # 九阳股份
		self.fetch_finforms_data_from_network('SZ002677') # 浙江美大
		self.fetch_finforms_data_from_network('SZ002403') # 爱仕达

	def fetch_jiadian_chudian_curdata_from_network(self):
		self.fetch_curdata_from_network('SZ002508') # 老板电器
		self.fetch_curdata_from_network('SZ002035') # 华帝股份
		self.fetch_curdata_from_network('SZ002543') # 万和电气
		self.fetch_curdata_from_network('SZ002032') # 苏泊尔
		self.fetch_curdata_from_network('SZ002242') # 九阳股份
		self.fetch_curdata_from_network('SZ002677') # 浙江美大
		self.fetch_curdata_from_network('SZ002403') # 爱仕达

	# 房地产的 PPP 细分行业
	def fetch_fangdichan_ppp_finforms_data_from_network(self):
		self.fetch_finforms_data_from_network('SH600340') # 华夏幸福

	def fetch_fangdichan_ppp_curdata_from_network(self):
		self.fetch_curdata_from_network('SH600340') # 华夏幸福

	# 其它
	def fetch_others_finforms_from_network(self):
		self.fetch_finforms_data_from_network('SH600298') # 安琪酵母

	def fetch_others_curdata_from_network(self):
		self.fetch_curdata_from_network('SH600298') # 安琪酵母
