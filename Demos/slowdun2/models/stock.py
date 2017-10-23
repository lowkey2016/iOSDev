# -*- coding: utf-8 -*-

import json
from zcfzb import ZCFZB
from gslrb import GSLRB
from xjllb import XJLLB
from fjsj import FJSJ
from quote import QUOTE
from utils.util_res import ResUtil
import utils.util_cons as Cons

class Stock(object):
	def __init__(self, symbol, name, year_from=0, year_to=9999):
		assert symbol is not None and symbol != ""
		self.symbol = symbol
		self.name = name

		st_dir = 'db/%s_%s' % (symbol, name)

		# 解析资产负债表
		fname = '%s/zcfzb.json' % st_dir
		if ResUtil.is_file_exists(fname):
			json_data = json.loads(ResUtil.read_json(fname))
		else:
			json_data = None
		if json_data is not None and type(json_data) == type({}) and json_data['name'] == name and json_data['list'] is not None:
			des_dics = {}
			json_list = json_data['list']
			for dic in json_list:
				reportdate = dic['reportdate'] # ex. 20161231
				year = reportdate[0:4]
				monthday = reportdate[4:]
				if monthday == '1231' and int(year) >= year_from and int(year) <= year_to:
					tmp = ZCFZB(**dic)
					des_dics[year] = tmp
			self.zcfzbs = des_dics
			# print self.zcfzbs

		# 解析利润表
		fname = '%s/gslrb.json' % st_dir
		if ResUtil.is_file_exists(fname):
			json_data = json.loads(ResUtil.read_json(fname))
		else:
			json_data = None
		if json_data is not None and type(json_data) == type({}) and json_data['name'] == name and json_data['list'] is not None:
			des_dics = {}
			json_list = json_data['list']
			for dic in json_list:
				reportdate = dic['enddate'] # ex. 20161231
				year = reportdate[0:4]
				monthday = reportdate[4:]
				if monthday == '1231' and int(year) >= year_from and int(year) <= year_to:
					tmp = GSLRB(**dic)
					des_dics[year] = tmp
			self.gslrbs = des_dics
			# print self.gslrbs

		# 解析现金流量表
		fname = '%s/xjllb.json' % st_dir
		if ResUtil.is_file_exists(fname):
			json_data = json.loads(ResUtil.read_json(fname))
		else:
			json_data = None
		if json_data is not None and type(json_data) == type({}) and json_data['name'] == name and json_data['list'] is not None:
			des_dics = {}
			json_list = json_data['list']
			for dic in json_list:
				reportdate = dic['enddate'] # ex. 20161231
				year = reportdate[0:4]
				monthday = reportdate[4:]
				if monthday == '1231' and int(year) >= year_from and int(year) <= year_to:
					tmp = XJLLB(**dic)
					des_dics[year] = tmp
			self.xjllbs = des_dics
			# print self.xjllbs

		# 解析附加数据
		fname = '%s/fjsj.json' % st_dir
		if ResUtil.is_file_exists(fname):
			json_data = json.loads(ResUtil.read_json(fname))
		else:
			json_data = None
		if json_data is not None and type(json_data) == type({}) and json_data['name'] == name and json_data['list'] is not None:
			des_dics = {}
			json_list = json_data['list']
			for dic in json_list:
				reportdate = dic['reportdate'] # ex. 20161231
				year = reportdate[0:4]
				monthday = reportdate[4:]
				if monthday == '1231' and int(year) >= year_from and int(year) <= year_to:
					tmp = FJSJ(**dic)
					des_dics[year] = tmp
			self.fjsjs = des_dics
		else:
			self.fjsjs = {}
			# print self.fjsjs

		# 解析最新数据
		fname = '%s/quote.json' % st_dir
		if ResUtil.is_file_exists(fname):
			json_data = json.loads(ResUtil.read_json(fname))
		else:
			json_data = None
		if json_data is not None and type(json_data) == type({}) and json_data[symbol] is not None:
			des_dics = {}
			dic = json_data[symbol]
			if symbol == dic['symbol']:
				tmp = QUOTE(**dic)
				self.quote = tmp
			else:
				self.quote = None
			# print self.quote
