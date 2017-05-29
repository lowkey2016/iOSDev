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
	if st_symbol is None:
		return None
	if months_from_2017 < 1 or months_from_2017 > 4:
		print "error months_from_2017: %d" % months_from_2017
		return None
	now = int(time.time())
	size = months_from_2017 + (2016 - 2007 + 1) * 4 # 一直算到 2007 Q1
	if REP_TYPE_MAIN == report_type:
		url = "https://xueqiu.com/stock/f10/finmainindex.json?symbol=%s&page=1&size=%d&_=%d" % (st_symbol, size, now)
	elif REP_TYPE_PROFIT == report_type:
		url = "https://xueqiu.com/stock/f10/incstatement.json?symbol=%s&page=1&size=%d&_=%d" % (st_symbol, size, now)
	elif REP_TYPE_ASSETS == report_type:
		url = "https://xueqiu.com/stock/f10/balsheet.json?symbol=%s&page=1&size=%d&_=%d" % (st_symbol, size, now)
	elif REP_TYPE_CUR == report_type:
		url = "https://xueqiu.com/v4/stock/quote.json?code=%s&_=%d" % (st_symbol, now)
	elif REP_TYPE_FEEDBACK == report_type:
		url = "https://xueqiu.com/stock/f10/bonus.json?symbol=%s&page=1&size=%d&_=%d" % (st_symbol, size, now)
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
		return dat_list

def floaty(num):
	return float(num or 0.0)

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

	def __repr__(self):
		return "[%s] 财报季度 = %s, EPS = %f, NAV = %f, 每股现金流 = %f, 每股经营性现金流 = %f, 资产总额 = %f, 负债总额 = %f, 股东权益合计 = %f" \
		% (self.symbol, self.reportdate, self.basiceps, self.naps, self.opercashpershare, self.peropecashpershare, self.totalassets, self.totalliab, self.totsharequi)

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

		self.grosprofit = self.bizinco - self.bizcost # 毛利润 = 营业收入 - 营业成本
		self.grosmargin = self.grosprofit / self.bizinco # 毛利率
		self.oprprofitratio = self.perprofit / self.biztotinco # 营业利润率
		self.totprofitratio = self.totprofit / self.biztotinco # 税前净利率
		self.netprofitratio = self.netprofit / self.biztotinco # 税后净利率
		self.rednetprofit = self.netprofit + self.noncassetsdisl # 还原税前净利
		self.rednetprofitratio = self.rednetprofit / self.biztotinco # 还原税前净利率
		self.salenmangexpratio = (self.salesexpe + self.manaexpe) / self.grosprofit # 销售及一般管理费用占毛利润的比例
		self.inteexpratio = self.inteexpe / self.grosprofit # 利息支出占毛利润的比例
		self.deveexpratio = self.deveexpe / self.grosprofit # 研发费用占毛利润的比例

	def __repr__(self):
		s1 = "[%s] from %s to %s, 营业总收入 = %f, 营业收入 = %f, 营业总成本 = %f, 营业成本 = %f, 利息支出 = %f,\
		研发费用 = %f, 销售费用 = %f, 管理费用 = %f, 营业利润 = %f, 非流动资产处置损失 = %f, 税前净利 = %f, 税后净利 = %f\
		EPS 基本每股收益 = %f\n" % \
		(self.symbol, self.begindate, self.enddate, self.biztotinco, self.bizinco, self.biztotcost, self.bizcost, self.inteexpe,\
			self.deveexpe, self.salesexpe, self.manaexpe, self.perprofit, self.noncassetsdisl, self.totprofit, self.netprofit,\
		 	self.basiceps)
		s2 = "[%s] 毛利润 = %f, 毛利率 = %f, 营业利润率 = %f, 税前净利率 = %f, 税后净利率 = %f, 还原税前净利 = %f, 还原税前净利率 = %f,\
		销售及一般管理费用占毛利润的比例 = %f, 利息支出占毛利润的比例 = %f, 研发费用占毛利润的比例 = %f" %\
		(self.symbol, self.grosprofit, self.grosmargin, self.oprprofitratio, self.totprofitratio, self.netprofitratio, self.rednetprofit, self.rednetprofitratio,\
			self.salenmangexpratio, self.inteexpratio, self.deveexpratio)
		return s1 + s2

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

		self.totsharequi = self.totasset - self.totliab # 股东权益
		self.eq = self.totsharequi / self.totasset # Eq
		self.curassetoftotliab = self.totcurrasset / self.totliab # 流动资产 / 总负债（企业应变危机的能力）

	def __repr__(self):
		s1 = "[%s] 财报季度 = %s, 流动资产 = %f, 总资产 = %f, 流动负债 = %f, 总负债 = %f, 应收账款 = %f, 存货 = %f\
		长期股权投资 = %f, 投资性房地产 = %f, 固定资产原值 = %f, 累计折旧 = %f, 在建工程 = %f, 一年内到期的非流动负债 = %f\n" % \
		(self.symbol, self.reportdate, self.totcurrasset, self.totasset, self.totalcurrliab, self.totliab, self.accorece, self.inve,\
			self.equiinve, self.inveprop, self.fixedasseimmo, self.accudepr, self.consprog, self.duenoncliab)
		s2 = "[%s] 股东权益 = %f, Eq = %f, 流动资产 / 总负债（企业应变危机的能力） = %f" % (self.symbol, self.totsharequi, self.eq, self.curassetoftotliab)
		return s1 + s2

#################################################################################
### 4. 市场数据
#################################################################################
class CurMarketData(object):
	def __init__(self, sym, d):
		if sym is not d["symbol"]:
			pass
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
		return "[%s, %s] 股价 = %f, 总股本 = %f, 流通股本 = %f, EPS = %f, NAV = %f, 每股股息 = %f, PER 动 = %f, PER 静 = %f, PB = %f" % \
		(self.symbol, self.name, self.current, self.totalShares, self.float_shares, self.eps, self.net_assets, self.dividend, self.pe_ttm, self.pe_lyr, self.pb)

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
		return "[%s] 分红公告日期 = %s, 分红实施年度 = %s, 总结 = %s, 股权登记日 = %s" % (self.symbol, self.bonusimpdate, self.bonusyear, self.summarize, self.recorddate)

#################################################################################
### 6. 综合数据
#################################################################################
# class ComplexData(object):
# 	def __init__(self, *main_dats, *pro_dats, *aset_dats, cur_dat, *fb_dats):
# 		self.main_dat = main_dat
# 		self.pro_dat = pro_dat
# 		self.aset_dat = aset_dat
# 		self.cur_dat = cur_dat
# 		self.fb_dat = fb_dat

# 		self.roeBefore # 税前 ROE
# 		self.roeAfter # 税后 ROE
# 		self.roaBefore # 税前 ROA
# 		self.roaAfter # 税后 ROA
# 		self.roePredict # ROE 预测
# 		self.accudeprofgrosprofit # 折旧费用占毛利润的比例
# 		self.profittoinv # 盈余再投资率
# 		self.value12 # 12倍PER价值估算
# 		self.value15 # 15倍PER价值估算

# test
st_symbol = 'SH600519'
months = 1

type = REP_TYPE_MAIN
dat_list = common_read_data(st_symbol, months, type)
dat0 = dat_list[0]
d0 = MainFinData(st_symbol, dat0)
print d0

type = REP_TYPE_PROFIT
dat_list = common_read_data(st_symbol, months, type)
dat0 = dat_list[0]
d0 = ProfitData(st_symbol, dat0)
print d0

type = REP_TYPE_ASSETS
dat_list = common_read_data(st_symbol, months, type)
dat0 = dat_list[0]
d0 = AssetsData(st_symbol, dat0)
print d0

type = REP_TYPE_CUR
dat0 = common_read_data(st_symbol, 1, type)
d0 = CurMarketData(st_symbol, dat0)
print d0

type = REP_TYPE_FEEDBACK
dat_list = common_read_data(st_symbol, months, type)
dat0 = dat_list[0]
d0 = FeedbackData(st_symbol, dat0)
print d0






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
