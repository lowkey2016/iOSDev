# -*- coding: utf-8 -*-

import os
import sys
import re
from models.zcfzb import ZCFZB
from models.gslrb import GSLRB
from models.xjllb import XJLLB
from utils.util_res import ResUtil
from utils.util_req import ReqUtil
from utils.util_re import RegUtil
import json

class StMgr(object):
	def fetch_data_from_network(self, st_symbol):
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

	def fetch_fangdichan_ppp_data_from_network(self):
		self.fetch_data_from_network('SH600340') # 华夏幸福

	def fetch_jiadian_chudian_data_from_network(self):
		self.fetch_data_from_network('SZ002508') # 老板电器
		self.fetch_data_from_network('SZ002035') # 华帝股份
		self.fetch_data_from_network('SZ002543') # 万和电气
		self.fetch_data_from_network('SZ002032') # 苏泊尔
		self.fetch_data_from_network('SZ002242') # 九阳股份
		self.fetch_data_from_network('SZ002677') # 浙江美大
		self.fetch_data_from_network('SZ002403') # 爱仕达

	def fetch_others_from_network(self):
		self.fetch_data_from_network('SH600298') # 安琪酵母
