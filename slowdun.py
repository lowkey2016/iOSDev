#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import urllib2
import re
import thread
import math
import bs4
from bs4 import BeautifulSoup
import os
import shutil
import sys
import time
import json
from collections import namedtuple
reload(sys)
sys.setdefaultencoding('utf8')

g_ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3107.4 Safari/537.36'
g_cookie = 's=7e11qxop7s; webp=1; bid=b58b6b71e770b584f6a86892d0f7de06_j136ussz; u=491494342683238; aliyungf_tc=AQAAAENAY0OZ0woAYF+MPX1aqzDQBCEo; xq_a_token=876f2519b10cea9dc131b87db2e5318e5d4ea64f; xq_a_token.sig=dfyKV8R29cG1dbHpcWXqSX6_5BE; xq_r_token=709abdc1ccb40ac956166989385ffd603ad6ab6f; xq_r_token.sig=dBkYRMW0CNWbgJ3X2wIkqMbKy1M; __utma=1.167412161.1486299610.1496051599.1496054069.52; __utmb=1.1.10.1496054069; __utmc=1; __utmz=1.1496048968.50.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; Hm_lvt_1db88642e346389874251b5a1eded6e3=1494948874,1495523496,1496042769,1496048968; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1496054069'

REP_TYPE_MAIN = 0
REP_TYPE_PROFIT = 1
REP_TYPE_ASSETS = 2
REP_TYPE_CUR = 3
REP_TYPE_FEEDBACK = 4

def common_read_data(st_symbol, months_from_2017, report_type):
	assert st_symbol is not None
	assert months_from_2017 >= 1 and months_from_2017 <= 4
	now = int(time.time())
	size = months_from_2017 + (2016 - 2007 + 1) * 4 # 一直算到 2007 Q1
	assert_if_size_err = True
	if REP_TYPE_MAIN == report_type:
		url = "https://xueqiu.com/stock/f10/finmainindex.json?symbol=%s&page=1&size=%d&_=%d" % (st_symbol, size, now)
	elif REP_TYPE_PROFIT == report_type:
		url = "https://xueqiu.com/stock/f10/incstatement.json?symbol=%s&page=1&size=%d&_=%d" % (st_symbol, size, now)
	elif REP_TYPE_ASSETS == report_type:
		url = "https://xueqiu.com/stock/f10/balsheet.json?symbol=%s&page=1&size=%d&_=%d" % (st_symbol, size, now)
	elif REP_TYPE_CUR == report_type:
		url = "https://xueqiu.com/v4/stock/quote.json?code=%s&_=%d" % (st_symbol, now)
		assert_if_size_err = False
	elif REP_TYPE_FEEDBACK == report_type:
		url = "https://xueqiu.com/stock/f10/bonus.json?symbol=%s&page=1&size=%d&_=%d" % (st_symbol, size, now)
		assert_if_size_err = False
	else:
		return None
	request = urllib2.Request(url)
	request.add_header('User-Agent', g_ua)
	request.add_header('Cookie', g_cookie)
	response = urllib2.urlopen(request)
	dic = json.loads(response.read())
	if REP_TYPE_CUR == report_type:
		dat = dic[st_symbol]
		return dat
	else:
		dat_list = dic["list"]
		if assert_if_size_err:
			assert size == len(dat_list)
		des_list = []
		for i, el in enumerate(dat_list):
			if 0 == i or (1 == (i + 1 - months_from_2017) % 4):
				des_list.append(el)
		return des_list

def floaty(num):
	return float(num or 0.0)

def inty(num):
	return int(num or 0)

#################################################################################
### 1. 主要财务指标
#################################################################################
class MainFinData(object):
	def __init__(self, sym, d):
		self.symbol = sym # 股票代号
		self.reportdate = d['reportdate'] # 财报季度，如 20170331, 20161231, 20160930, 20160630, 20160331
		self.basiceps = floaty(d['basiceps']) # EPS 基本每股收益
		self.naps = floaty(d['naps']) # NAV 每股净资产
		self.opercashpershare = floaty(d['opercashpershare']) # 每股现金流
		self.peropecashpershare = floaty(d['peropecashpershare']) # 每股经营性现金流
		self.totalassets = floaty(d['totalassets']) # 资产总额
		self.totalliab = floaty(d['totalliab']) # 负债总额
		self.totsharequi = floaty(d['totsharequi']) # 股东权益合计

		self.year = inty(self.reportdate[0:4]) # 年份
		self.month = inty(self.reportdate[4:6]) # 月份

	def __repr__(self):
		s0 = "\n============================================================\n"
		s1 = "[%s]主要财务指标 %s\n" % (self.symbol, self.reportdate)
		s2 = "EPS = %f,\nNAV = %f,\n每股现金流 = %f,\n每股经营性现金流 = %f\n" \
		% (self.basiceps, self.naps, self.opercashpershare, self.peropecashpershare)
		s3 = "============================================================\n"
		return s0 + s1 + s2 + s3

#################################################################################
### 2. 综合损益表
#################################################################################
class ProfitData(object):
	def __init__(self, sym, d):
		self.symbol = sym # 股票代号
		self.begindate = d['begindate']
		self.enddate = d['enddate']
		self.biztotinco = floaty(d['biztotinco']) # 营业总收入
		self.bizinco = floaty(d['bizinco']) # 营业收入
		self.biztotcost = floaty(d['biztotcost']) # 营业总成本
		self.bizcost = floaty(d['bizcost']) # 营业成本
		self.inteexpe = floaty(d['inteexpe']) # 利息支出
		self.deveexpe = floaty(d['deveexpe']) # 研发费用
		self.salesexpe = floaty(d['salesexpe']) # 销售费用
		self.manaexpe = floaty(d['manaexpe']) # 管理费用
		self.perprofit = floaty(d['perprofit']) # 营业利润
		self.noncassetsdisl = floaty(d['noncassetsdisl']) # 非流动资产处置损失
		self.totprofit = floaty(d['totprofit']) # 税前净利
		self.netprofit = floaty(d['netprofit']) # 税后净利
		self.basiceps = floaty(d['basiceps']) # EPS 基本每股收益

		self.year = inty(self.enddate[0:4]) # 年份
		self.month = inty(self.enddate[4:6]) # 月份

		self.grosprofit = self.bizinco - self.bizcost # 毛利润 = 营业收入 - 营业成本
		self.grosmargin = self.grosprofit / self.bizinco # 毛利率
		self.oprprofitratio = self.perprofit / self.biztotinco # 营业利润率
		self.totprofitratio = self.totprofit / self.biztotinco # 税前净利率
		self.netprofitratio = self.netprofit / self.biztotinco # 税后净利率
		self.rednetprofit = self.totprofit + self.noncassetsdisl # 还原税前净利
		self.rednetprofitratio = self.rednetprofit / self.biztotinco # 还原税前净利率
		self.salenmangexpratio = (self.salesexpe + self.manaexpe) / self.grosprofit # 销售及一般管理费用占毛利润的比例
		self.inteexpratio = self.inteexpe / self.grosprofit # 利息支出占毛利润的比例
		self.deveexpratio = self.deveexpe / self.grosprofit # 研发费用占毛利润的比例

	def __repr__(self):
		s0 = "\n============================================================\n"
		s1 = "[%s]综合损益表 %s - %s\n" % (self.symbol, self.begindate, self.enddate)
		s2 = "营业总收入 = %f, 营业总成本 = %f, 营业利润 = %f\n" % (self.biztotinco, self.biztotcost, self.perprofit)
		s3 = "营业收入 = %f,  营业成本 = %f, 毛利润 = %f\n" % (self.bizinco, self.bizcost, self.grosprofit)
		s4 = "利息支出 = %f, 利息支出占毛利润的比例 = %f%%\n" % (self.inteexpe, self.inteexpratio * 100)
		s5 = "研发费用 = %f, 研发费用占毛利润的比例 = %f%%\n" % (self.deveexpe, self.deveexpratio * 100)
		s6 = "销售费用 = %f, 管理费用 = %f, 销售及一般管理费用占毛利润的比例 = %f%%\n" % (self.salesexpe, self.manaexpe, self.salenmangexpratio * 100)
		s7 = "还原税前净利 = %f, 非流动资产处置损失 = %f, 税前净利 = %f, 税后净利 = %f\n" % (self.rednetprofit, self.noncassetsdisl, self.totprofit, self.netprofit)
		s8 = "毛利率 = %f%%, 营业利润率 = %f%%, 还原税前净利率 = %f%%, 税前净利率 = %f%%, 税后净利率 = %f%%\n" % (self.grosmargin * 100, self.oprprofitratio * 100, self.rednetprofitratio * 100, self.totprofitratio * 100, self.netprofitratio * 100)
		s9 = "============================================================\n"
		return s0 + s1 + s2 + s3 + s4 + s5 + s6 + s7 + s8 + s9

#################################################################################
### 3. 资产负债表
#################################################################################
class AssetsData(object):
	def __init__(self, sym, d):
		self.symbol = sym # 股票代号
		self.reportdate = d['reportdate'] # 财报季度，如 20170331, 20161231, 20160930, 20160630, 20160331
		self.totcurrasset = floaty(d['totcurrasset']) # 流动资产
		self.totasset = floaty(d['totasset']) # 总资产
		self.totalcurrliab = floaty(d['totalcurrliab']) # 流动负债
		self.totliab = floaty(d['totliab']) # 总负债
		self.accorece = floaty(d['accorece']) # 应收账款
		self.inve = floaty(d['inve']) # 存货
		self.equiinve = floaty(d['equiinve']) # 长期股权投资
		self.inveprop = floaty(d['inveprop']) # 投资性房地产
		self.fixedasseimmo = floaty(d['fixedasseimmo']) # 固定资产原值
		self.accudepr = floaty(d['accudepr']) # 累计折旧
		self.consprog = floaty(d['consprog']) # 在建工程
		self.duenoncliab = floaty(d['duenoncliab']) # 一年内到期的非流动负债

		self.year = inty(self.reportdate[0:4]) # 年份
		self.month = inty(self.reportdate[4:6]) # 月份

		self.totsharequi = self.totasset - self.totliab # 股东权益
		self.eq = self.totsharequi / self.totasset # Eq
		self.curassetoftotliab = self.totcurrasset / self.totliab # 流动资产 / 总负债（企业应变危机的能力）
		self.invtot = self.equiinve + self.inveprop + self.fixedasseimmo + self.consprog # 固定资产 + 长期投资
		self.accrate = self.accorece / self.totasset # 应收账款占总资产的比例
		self.invrate = self.inve / self.totasset # 存货占总资产的比例
		# 流动资产 / 一年内到期的非流动负债（近期面对的经济压力）
		if self.duenoncliab > 0:
			self.curassetofduenliab = (self.totcurrasset / self.duenoncliab)
		else:
			self.curassetofduenliab = 0

	def __repr__(self):
		s0 = "\n============================================================\n"
		s1 = "[%s]资产负债表 %s\n" % (self.symbol, self.reportdate)
		s2 = "总资产 = %f, 总负债 = %f, 股东权益 = %f, Eq = %f%%\n" % (self.totasset, self.totliab, self.totsharequi, self.eq * 100)
		s3 = "流动资产 = %f, 流动负债 = %f, 流动资产 / 总负债（企业应变危机的能力） = %f\n" % (self.totcurrasset, self.totalcurrliab, self.curassetoftotliab)
		s4 = "应收账款 = %f, 应收账款占总资产的比例 = %f%%\n" % (self.accorece, self.accrate * 100)
		s5 = "存货 = %f, 存货占总资产的比例 = %f%%\n" % (self.inve, self.invrate * 100)
		s6 = "长期股权投资 = %f(%f%%), 投资性房地产 = %f(%f%%), 固定资产原值 = %f(%f%%), 在建工程 = %f(%f%%)\n" % \
		(self.equiinve, self.equiinve / self.totasset * 100, self.inveprop, self.inveprop / self.totasset * 100, self.fixedasseimmo, self.fixedasseimmo / self.totasset * 100, self.consprog, self.consprog / self.totasset * 100)
		s7 = "一年内到期的非流动负债 = %f, 流动资产 / 一年内到期的非流动负债（近期面对的经济压力） = %f\n" % (self.duenoncliab, self.curassetofduenliab)
		s8 = "============================================================\n"
		return s0 + s1 + s2 + s3 + s4 + s5 + s6 + s7 + s8

#################################################################################
### 4. 市场数据
#################################################################################
class CurMarketData(object):
	def __init__(self, sym, d):
		assert sym == d["symbol"]
		self.symbol = d["symbol"] # 股票代号
		self.name = d['name'] # 名字
		self.current = floaty(d['current']) # 股价
		self.totalShares = floaty(d['totalShares']) # 总股本
		self.float_shares = floaty(d['float_shares']) #	流通股本
		self.eps = floaty(d['eps']) # 每股收益
		self.net_assets = floaty(d['net_assets']) # 每股净资产
		self.dividend = floaty(d['dividend']) # 每股股息
		self.pe_ttm = floaty(d['pe_ttm']) # 市盈率（动）
		self.pe_lyr = floaty(d['pe_lyr']) # 市盈率（静）
		self.pb = floaty(d['pb']) # 市净率（动）

	def __repr__(self):
		s0 = "\n============================================================\n"
		s1 = "[%s, %s]市场数据\n" % (self.symbol, self.name)
		s2 = "股价 = %f, PER 动 = %f, PER 静 = %f\n" % (self.current, self.pe_ttm, self.pe_lyr)
		s3 = "总市值 = %f亿, 总股本 = %f, 流通股本 = %f, 流通比例 = %f%%\n" % (self.totalShares * self.current / 100000000, self.totalShares, self.float_shares, self.float_shares / self.totalShares * 100)
		s4 = "EPS = %f, NAV = %f, 每股股息 = %f, PB = %f\n" % (self.eps, self.net_assets, self.dividend, self.pb)
		s5 = "============================================================\n"
		return s0 + s1 + s2 + s3 + s4 + s5

#################################################################################
### 5. 分红送配
#################################################################################
class FeedbackData(object):
	def __init__(self, sym, d):
		self.symbol = sym # 股票代号
		self.bonusimpdate = d['bonusimpdate'] # 分红公告日期
		self.bonusyear = d['bonusyear'] # 分红实施年度
		self.summarize = d['summarize'] # 例如：10派1送100
		self.recorddate = d['recorddate'] # 股权登记日

	def __repr__(self):
		s0 = "\n============================================================\n"
		s1 = "[%s]分红送配\n" % self.symbol
		s2 = "分红公告日期 = %s, 分红实施年度 = %s, 股权登记日 = %s\n" % (self.bonusimpdate, self.bonusyear, self.recorddate)
		s3 = "总结 = %s\n" % self.summarize
		s4 = "============================================================\n"
		return s0 + s1 + s2 + s3 + s4


#################################################################################
### 6. 综合数据
#################################################################################
class ComplexData(object):
	def __init__(self, symbol, **wrap):
		main_dats = wrap['main']
		pro_dats = wrap['pro']
		aset_dats = wrap['aset']
		cur_dat = wrap['cur']
		fb_dats = wrap['fb']

		assert symbol is not None and \
		main_dats is not None and len(main_dats) > 0 and \
		pro_dats is not None and len(pro_dats) > 0 and \
		aset_dats is not None and len(aset_dats) > 0 and \
		cur_dat is not None and \
		fb_dats is not None and len(fb_dats) > 0 and \
		len(main_dats) == len(pro_dats) and \
		len(main_dats) == len(aset_dats)

		main_dlast = main_dats[-1]
		assert main_dlast.year == 2007

		self.symbol = symbol
		self.name = cur_dat.name

		main_d0 = main_dats[0]
		accept_first = main_d0.month == 12
		if not accept_first:
			main_dats = main_dats[1:]
			pro_dats = pro_dats[1:]
			aset_dats = aset_dats[1:]
		self.main_pro_aset_dic = {}
		for d in main_dats:
			k = "main_%d" % d.year
			self.main_pro_aset_dic[k] = d
		for d in pro_dats:
			k = "pro_%d" % d.year
			self.main_pro_aset_dic[k] = d
		for d in aset_dats:
			k = "aset_%d" % d.year
			self.main_pro_aset_dic[k] = d
		self.cur_dat = cur_dat
		self.fb_dats = fb_dats

		yearFrom = 2008
		yearTo = main_dats[0].year
		total = 0.0

		self.curyear = yearTo # 综合数据记录的最近一年

		# 2008 - 最近一年 的税前 ROE
		self.roesBeforeDic = {}
		for year in range(yearFrom, yearTo + 1):
			kpro_this = "pro_%d" % year
			kaset_last = "aset_%d" % (year - 1)
			pro_this = self.main_pro_aset_dic[kpro_this]
			aset_last = self.main_pro_aset_dic[kaset_last]
			roe = pro_this.totprofit / aset_last.totsharequi
			self.roesBeforeDic[year] = roe
		# 最近一年税前 ROE
		self.roeBeforeCur = self.roesBeforeDic[yearTo]
		# 2008 - 最近一年 的平均税前 ROE
		total = 0.0
		for year in range(yearFrom, yearTo + 1):
			roe = self.roesBeforeDic[year]
			total = total + roe
		self.roeBeforeAveAll = total / (yearTo - yearFrom + 1)
		# 5年平均税前 ROE
		total = 0.0
		for year in range(yearTo - 4, yearTo + 1):
			roe = self.roesBeforeDic[year]
			total = total + roe
		self.roeBeforeAve5 = total / 5
		# 3年平均税前 ROE
		total = 0.0
		for year in range(yearTo - 2, yearTo + 1):
			roe = self.roesBeforeDic[year]
			total = total + roe
		self.roeBeforeAve3 = total / 3

		# 2008 - 最近一年 的税后 ROE
		self.roesAfterDic = {}
		for year in range(yearFrom, yearTo + 1):
			kpro_this = "pro_%d" % year
			kaset_last = "aset_%d" % (year - 1)
			pro_this = self.main_pro_aset_dic[kpro_this]
			aset_last = self.main_pro_aset_dic[kaset_last]
			roe = pro_this.netprofit / aset_last.totsharequi
			self.roesAfterDic[year] = roe
		# 最近一年税后 ROE
		self.roeAfterCur = self.roesAfterDic[yearTo]
		# 2008 - 最近一年 的平均税后 ROE
		total = 0.0
		for year in range(yearFrom, yearTo + 1):
			roe = self.roesAfterDic[year]
			total = total + roe
		aveAllYears = (yearTo - yearFrom + 1)
		self.roeAfterAveAll = total / (yearTo - yearFrom + 1)
		# 5年平均税后 ROE
		total = 0.0
		for year in range(yearTo - 4, yearTo + 1):
			roe = self.roesAfterDic[year]
			total = total + roe
		self.roeAfterAve5 = total / 5
		# 3年平均税后 ROE
		total = 0.0
		for year in range(yearTo - 2, yearTo + 1):
			roe = self.roesAfterDic[year]
			total = total + roe
		self.roeAfterAve3 = total / 3

		# （税后）ROE 预测
		self.roePredict = (self.roeAfterAve3 * 3 + self.roeAfterAve5 * 5 + self.roeAfterAveAll * aveAllYears) / (3 + 5 + aveAllYears)
		self.roePredict = min(self.roePredict, self.roeAfterAve3, self.roeAfterAve5, self.roeAfterAveAll)

		# ROA
		k1 = 'pro_%d' % yearTo
		k2 = 'aset_%d' % (yearTo - 1)
		self.roaBefore = self.main_pro_aset_dic[k1].totprofit / self.main_pro_aset_dic[k2].totasset # 税前 ROA
		self.roaAfter = self.main_pro_aset_dic[k1].netprofit / self.main_pro_aset_dic[k2].totasset # 税后 ROA
		
		# 2008 - 最近一年 的折旧费用占毛利润的比例
		self.acdofgrsprodic = {}
		for year in range(yearFrom, yearTo + 1):
			kpro = "pro_%d" % year
			kaset = "aset_%d" % year
			pro = self.main_pro_aset_dic[kpro]
			aset = self.main_pro_aset_dic[kaset]
			of = aset.accudepr / pro.grosprofit
			self.acdofgrsprodic[year] = of
		
		# 盈余再投资率 2012 - 2016
		self.profittoinvdic = {}
		for year in range(yearFrom, yearTo + 1):
			if year - yearFrom >= 4:
				kpro_this = "pro_%d" % year
				kpro_last0 = "pro_%d" % (year - 1)
				kpro_last1 = "pro_%d" % (year - 2)
				kpro_last2 = "pro_%d" % (year - 3)
				pro_this = self.main_pro_aset_dic[kpro_this]
				pro_last0 = self.main_pro_aset_dic[kpro_last0]
				pro_last1 = self.main_pro_aset_dic[kpro_last1]
				pro_last2 = self.main_pro_aset_dic[kpro_last2]

				kaset_this = "aset_%d" % year
				kaset_last = "aset_%d" % (year - 4)
				aset_this = self.main_pro_aset_dic[kaset_this]
				aset_last = self.main_pro_aset_dic[kaset_last]

				to = (aset_this.invtot - aset_last.invtot) / (pro_this.netprofit + pro_last0.netprofit + pro_last1.netprofit + pro_last2.netprofit)
				self.profittoinvdic[year] = to
		
		self.value12 = self.cur_dat.net_assets * self.roePredict * 12 # 12倍PER价值估算
		self.value15 = self.cur_dat.net_assets * self.roePredict * 15 # 15倍PER价值估算

		# 安全边际
		self.margin12 = self.value12 / self.cur_dat.current - 1
		self.margin15 = self.value15 / self.cur_dat.current - 1

	def __repr__(self):
		s0 = "\n============================================================\n"
		s1 = "[%s, %s]综合数据\n" % (self.symbol, self.name)
		s2 = "2008 - %d年的税前 ROE = %s\n, %d年税前 ROE = %f\n" % (self.curyear, str(self.roesBeforeDic), self.curyear, self.roeBeforeCur)
		s3 = "2008 - %d年的平均税前 ROE = %f, 5年平均税前 ROE = %f, 3年平均税前 ROE = %f\n" % (self.curyear, self.roeBeforeAveAll, self.roeBeforeAve5, self.roeBeforeAve3)
		s4 = "2008 - %d年的税后 ROE = %s, %d年税后 ROE = %f\n" % (self.curyear, str(self.roesAfterDic), self.curyear, self.roeAfterCur)
		s5 = "2008 - %d年的平均税后 ROE = %f, 5年平均税后 ROE = %f, 3年平均税后 ROE = %f\n" % (self.curyear, self.roeAfterAveAll, self.roeAfterAve5, self.roeAfterAve3)
		s6 = "（税后）ROE 预测 = %f\n" % self.roePredict
		s7 = "税前 ROA = %f, 税后 ROA = %f\n" % (self.roaBefore, self.roaAfter)
		s8 = "2008 - %d年的折旧费用占毛利润的比例 = %s\n" % (self.curyear, str(self.acdofgrsprodic))
		s9 = "盈余再投资率 = %s\n" % str(self.profittoinvdic)
		s10 = "12倍PER价值估算 = %f, 15倍PER价值估算 = %f\n" % (self.value12, self.value15)
		s11 = "安全边际 = %f%%, %f%%\n" % (self.margin12 * 100, self.margin15 * 100)
		s12 = "============================================================\n"
		return s0 + s1 + s2 + s3 + s4+ s5+ s6 + s7 + s8 + s9 + s10 + s11 + s12

# test

# st_symbol = 'SH600519'
# st_name = '贵州茅台'

# st_symbol = 'SZ000651'
# st_name = '格力电器'

# st_symbol = 'SZ000002'
# st_name = '万科A'

# st_symbol = 'SH600660'
# st_name = '福耀玻璃'

# st_symbol = 'SH600009'
# st_name = '上海机场'

# st_symbol = 'SH601006'
# st_name = '大秦铁路'

# st_symbol = 'SH600350'
# st_name = '山东高速'

# st_symbol = 'SH600340'
# st_name = '华夏幸福'

# st_symbol = 'SH600004'
# st_name = '白云机场'

# st_symbol = 'SH600886'
# st_name = '国投电力'

# st_symbol = 'SH600900'
# st_name = '长江电力'

# st_symbol = 'SZ000333'
# st_name = '美的集团'

# st_symbol = 'SH600887'
# st_name = '伊利股份'

# st_symbol = 'SZ002415'
# st_name = '海康威视'

##########
# 汽车制造
##########

# st_symbol = 'SZ000957'; st_name = '中通客车'
# st_symbol = 'SH600104'; st_name = '上汽集团'
# st_symbol = 'SH600066'; st_name = '宇通客车'
# st_symbol = 'SZ000550'; st_name = '江铃汽车'
# st_symbol = 'SZ000550'; st_name = '江铃汽车'
# st_symbol = 'SH600006'; st_name = '东风汽车'
# st_symbol = 'SZ000800'; st_name = '一汽轿车'
# st_symbol = 'SH600760'; st_name = '中航黑豹'
# st_symbol = 'SH600166'; st_name = '福田汽车'
# st_symbol = 'SZ000980'; st_name = '金马股份'
# st_symbol = 'SZ000951'; st_name = '中国重汽'
# st_symbol = 'SH600418'; st_name = '江淮汽车'
# st_symbol = 'SZ000625'; st_name = '长安汽车'

# st_symbol = 'SH601127'; st_name = '小康股份'
# st_symbol = 'SZ002594'; st_name = '比亚迪'
# st_symbol = 'SH601633'; st_name = '长城汽车'
# st_symbol = 'SH601238'; st_name = '广汽集团'
# st_symbol = 'SH600303'; st_name = '曙光股份'

months = 1

fname = "./%s_%s.txt" % (st_name, st_symbol)
file = open(fname, 'w+')

type = REP_TYPE_MAIN
mainfin_list = []
dat_list = common_read_data(st_symbol, months, type)
for el in dat_list:
	d = MainFinData(st_symbol, el)
	mainfin_list.append(d)
print >>file, '*** 主要财务指标 ***'
print >>file, mainfin_list
print >>file, '\n\n'

type = REP_TYPE_PROFIT
pro_list = []
dat_list = common_read_data(st_symbol, months, type)
for el in dat_list:
	d = ProfitData(st_symbol, el)
	pro_list.append(d)
print >>file, '*** 综合损益表 ***'
print >>file, pro_list
print >>file, '\n\n'

type = REP_TYPE_ASSETS
aset_list = []
dat_list = common_read_data(st_symbol, months, type)
for el in dat_list:
	d = AssetsData(st_symbol, el)
	aset_list.append(d)
print >>file, '*** 资产负债表 ***'
print >>file, aset_list
print >>file, '\n\n'

type = REP_TYPE_CUR
el = common_read_data(st_symbol, 1, type)
cur_dat = CurMarketData(st_symbol, el)
print >>file, '*** 最新市场数据 ***'
print >>file, cur_dat
print >>file, '\n\n'

type = REP_TYPE_FEEDBACK
fb_list = []
dat_list = common_read_data(st_symbol, months, type)
for el in dat_list:
	d = FeedbackData(st_symbol, el)
	fb_list.append(d)
print >>file, '*** 分红送配 ***'
print >>file, fb_list
print >>file, '\n\n'

wrap = {}
wrap['main'] = mainfin_list
wrap['pro'] = pro_list
wrap['aset'] = aset_list
wrap['cur'] = cur_dat
wrap['fb'] = fb_list
com_dat = ComplexData(st_symbol, **wrap)
print >>file, '*** 综合数据 ***'
print >>file, com_dat
print >>file, '\n\n'



# ## 114图库女神图集的爬虫类 ##
# class Pics114Spider:

# 	## 初始化方法 ##
# 	def __init__(self, fav_girl_name, allcols_html_url):
# 		self.fav_girl_name = fav_girl_name
# 		self.allcols_html_url = allcols_html_url
# 		self.pics_delta = 10


# 	## 获取女神的图集存放的目录 ##
# 	def get_fav_girl_dir(self, folder_name):
# 		folder_dir = './%s' % (folder_name)
# 		if os.path.exists(folder_dir) == False:
# 			os.mkdir(folder_dir)
# 		return folder_dir


# 	## 获取女神某一个图集的目录 ##
# 	def get_collection_dir(self, folder_name, collection_name):
# 		root_dir = self.get_fav_girl_dir(folder_name)
# 		col_dir = '%s/%s' % (root_dir, collection_name)
# 		if os.path.exists(col_dir) == False:
# 			os.mkdir(col_dir)
# 		return col_dir


# 	## 获取一个网页的 HTML 内容 ##
# 	def get_html_with_url(self, src_url):
# 		try:
# 			request = urllib2.Request(src_url)
# 			response = urllib2.urlopen(request)
# 			data = response.read()
# 			return data
# 		except urllib2.URLError, e:
# 			if hasattr(e, "reason"):
# 				print u"打开 %s 失败，原因：%s" % (src_url, e.reason)
# 				return None


# 	## 下载网络的文件到磁盘 ##
# 	def save_file_with_url(self, src_url, des_path):
# 		# 如果文件已经存在并且文件大小大于 10KB ，就假定其已经下载好
# 		if os.path.exists(des_path) and os.path.getsize(des_path) > 10000:
# 			# 已经下载好的不再重复下载
# 			print 'save %s to %s succ' % (src_url, des_path)
# 			return True
# 		else:
# 			try:
# 				request = urllib2.Request(src_url)
# 				response = urllib2.urlopen(request)
# 				data = response.read()
# 				if data:
# 					f = open(des_path, 'wb')
# 					f.write(data)
# 					f.close()
# 					print 'save %s to %s succ' % (src_url, des_path)
# 					return True
# 				else:
# 					print 'save %s to %s fail' % (src_url, des_path)
# 					return False
# 			except urllib2.URLError, e:
# 				if hasattr(e, "reason"):
# 					print u"打开 %s 失败，原因：%s" % (src_url, e.reason)
# 					return False


# 	## 保存女神的封面 ##
# 	def save_fav_girl_cover(self, fav_girl_name, cover_url):
# 		if cover_url.endswith('.png'):
# 			cover_name = 'cover.png'
# 		else:
# 			cover_name = 'cover.jpg'
# 		des_path = '%s/%s' % (self.get_fav_girl_dir(fav_girl_name), cover_name)
# 		request = urllib2.Request(cover_url)
# 		response = urllib2.urlopen(request)
# 		data = response.read()
# 		if data:
# 			f = open(des_path, 'wb')
# 			f.write(data)
# 			f.close()
# 			print 'save %s succ' % des_path
# 		else:
# 			print 'save %s fail' % des_path


# 	## 保存女神的资料 ##
# 	def save_fav_girl_profile(self, fav_girl_name, profile_str):
# 		des_path = '%s/profile.txt' % (self.get_fav_girl_dir(fav_girl_name))
# 		if profile_str:
# 			f = open(des_path, 'wb')
# 			f.write(profile_str.encode('utf-8'))
# 			f.close()
# 			print 'save %s succ' % des_path
# 		else:
# 			print 'save %s fail' % des_path


# 	## 爬取每一个网页里的女神图片 ##
# 	def get_content_pic_of_url(self, html_url, page_index, collection_dir):
# 		# 获取 Base URL
# 		last_comp = html_url.split('/')[-1]
# 		baseurl = html_url.replace(last_comp, '')
# 		html = self.get_html_with_url(html_url)
# 		if last_comp.endswith('.html'):
# 			last_comp = last_comp.replace('.html', '')
# 		col_id = last_comp.split('_')[0]

# 		# 获取下一页的链接
# 		# 获取本页的图片内容
# 		pattern = re.compile('<div class="articleBody" id="picBody">.*?<a href=\'(.*?)\'><img alt=.*?src="(.*?)".*?</div>', re.S)
# 		items = re.findall(pattern, html)
# 		for item in items:
# 			next_url_ref = item[0]
# 			pic_url = item[1]
# 			break

# 		# 下载图片，然后跳到下一页
# 		des_name = '%d.jpg' % page_index
# 		des_path = '%s/%s' % (collection_dir, des_name)
# 		self.save_file_with_url(pic_url, des_path)

# 		next_url = os.path.join(baseurl, next_url_ref)
# 		if next_url_ref and next_url_ref.startswith(col_id):
# 			self.get_content_pic_of_url(next_url, (page_index + 1), collection_dir)


# 	## 爬取一个集合里的所有图片 ##
# 	def get_pics_of_collection(self, root_name, html_url):
# 		collection_name = ''
# 		collection_dir = ''
# 		collection_pages = 0

# 		# 读取html
# 		try:
# 			html_req = urllib2.Request(html_url)
# 			html_resp = urllib2.urlopen(html_req)
# 			html_content = html_resp.read().decode('utf-8')
# 		except urllib2.URLError, e:
# 			if hasattr(e, "reason"):
# 				print u"连接114图库失败，原因：", e.reason

# 		# 获取网页标题（用于新建目录）
# 		soup = BeautifulSoup(html_content, "lxml")
# 		html_title = soup.title.string
# 		collection_name = html_title

# 		# 获取图片页数
# 		pattern = re.compile('<div class="pages">.*?共(.*?)页:.*?</div>'.decode('utf-8'), re.S)
# 		items = re.findall(pattern, html_content)
# 		for item in items:
# 			collection_pages = int(item)
# 			# 加1个越界值，因为页数可能显示不完整
# 			collection_pages += self.pics_delta
# 			break

# 		# 获取 jpg 的 base 链接
# 		img_baseurl = ''
# 		pattern = re.compile('<div class="articleBody" id="picBody">.*?<img alt.*?src="(.*?)".*?</div>', re.S)
# 		items = re.findall(pattern, html_content)
# 		for item in items:
# 			img_baseurl = item
# 			last_comp = img_baseurl.split('/')[-1]
# 			img_baseurl = img_baseurl.replace(last_comp, '')
# 			break

# 		# 获取存放图片文件的目录
# 		collection_dir = self.get_collection_dir(root_name, collection_name)

# 		# 遍历页数，爬取所有图片
# 		is_rule_valid = False
# 		for i in range(1, collection_pages):
# 			des_name = '%d.jpg' % i
# 			des_path = '%s/%s' % (collection_dir, des_name)
# 			src_url = "%s%d.jpg" % (img_baseurl, i)
# 			save_succ = self.save_file_with_url(src_url, des_path)
# 			# 只要其中一条规则生效，就假定 BaseURL + i.jpg 这种规则是有效的
# 			if is_rule_valid == False and save_succ:
# 				is_rule_valid = True

# 		# 如果 BaseURL + i.jpg 这种规则失效，就换一种规则爬
# 		if is_rule_valid == False:
# 			self.get_content_pic_of_url(html_url, 1, collection_dir)
# 		# 如果 BaseURL + i.jpg 规则失效，并且还没全部下载好，需要断点续爬
# 		# 防那种规则不对，但是又还没下载完整的情况
# 		last_imgname = '%d.jpg' % (collection_pages - self.pics_delta)
# 		last_imgpath = '%s/%s' % (collection_dir, last_imgname)
# 		if os.path.exists(last_imgpath) == False:
# 			self.get_content_pic_of_url(html_url, 1, collection_dir)


# 	## 根据女神获取其所有集合 ##
# 	def get_all_collections(self):
# 		# 读取所有集合的html
# 		fav_girl_name = self.fav_girl_name
# 		allcols_html_url = self.allcols_html_url
# 		try:
# 			allcols_html_req = urllib2.Request(allcols_html_url)
# 			allcols_html_resp = urllib2.urlopen(allcols_html_req)
# 			allcols_html_content = allcols_html_resp.read().decode('utf-8')
# 		except urllib2.URLError, e:
# 			if hasattr(e, "reason"):
# 				print u"连接女神所有图集网页失败，原因：", e.reason
		
# 		# 获取封面
# 		pattern = re.compile('<body style="background:url\((.*?)\) no-repeat.*?px;">', re.S)
# 		items = re.findall(pattern, allcols_html_content)
# 		for item in items:
# 			fav_girl_cover_url = item
# 			self.save_fav_girl_cover(fav_girl_name, fav_girl_cover_url)
# 			break

# 		# 爬取基本资料并写到信息文件中
# 		pattern = re.compile('<div class="top_content">.*?<p class="sp-icent">(.*?)</p>.*?</div>'.decode('utf-8'), re.S)
# 		items = re.findall(pattern, allcols_html_content)
# 		for item in items:
# 			fav_girl_profile = item
# 			self.save_fav_girl_profile(fav_girl_name, fav_girl_profile)
# 			break

# 		# 获取所有集合的链接
# 		pattern = re.compile('<div class="listBox" id="imgList">.*?<ul class="liL">(.*?)</ul></div>', re.S)
# 		items = re.findall(pattern, allcols_html_content)
# 		for item in items:
# 			cols_content = item
# 			break
# 		pattern = re.compile('<li><a href="(.*?)".*?</a><span.*?<a target=.*?</a></span></li>', re.S)
# 		items = re.findall(pattern, cols_content)
# 		for item in items:
# 			collection_url = item
# 			self.get_pics_of_collection(fav_girl_name, collection_url)


# # 开始爬

# # Succ

# # 夏沫GiGi
# # spider = Pics114Spider('夏沫GiGi', 'http://www.du114.com/tag/1289.html')

# # Vian熙芸
# # spider = Pics114Spider('Vian熙芸', 'http://www.du114.com/tag/1718.html')

# # 陈思琪
# # spider = Pics114Spider('陈思琪', 'http://www.du114.com/tag/1554.html')

# # 李七喜
# # spider = Pics114Spider('李七喜', 'http://www.du114.com/tag/1226.html')

# # # 米妮
# # spider = Pics114Spider('米妮', 'http://www.du114.com/tag/1301.html')

# # 杉原杏璃
# # spider = Pics114Spider('杉原杏璃', 'http://www.du114.com/tag/1231.html')

# # 夏瑶
# # spider = Pics114Spider('夏瑶', 'http://www.du114.com/tag/1290.html')

# # 诗朵雅
# # spider = Pics114Spider('诗朵雅', 'http://www.du114.com/tag/1230.html')

# # 杨晓青儿
# # spider = Pics114Spider('杨晓青儿', 'http://www.du114.com/tag/1212.html') 

# # 爬取某个女神的所有图集
# # spider.get_all_collections()

# # 爬取某个图集
# # spider = Pics114Spider('', '')
# # spider.get_pics_of_collection('张圆圆', 'http://www.du114.com/meinvtupian/nayimeinv/74341.html')
