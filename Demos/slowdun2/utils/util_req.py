# -*- coding: utf-8 -*-

import os
import json
import urllib2
import time
import cookielib
from fake_useragent import UserAgent
from util_res import ResUtil

class ReqUtil(object):
	REP_TYPE_MAIN = 0
	REP_TYPE_PROFIT = 1
	REP_TYPE_ASSETS = 2
	REP_TYPE_CUR = 3
	REP_TYPE_FEEDBACK = 4
	REP_TYPE_CASH = 5

	def __init__(self, st_symbol):
		assert st_symbol is not None
		self.st_symbol = st_symbol
		self.ua = UserAgent().random
		self.proxies = None
		self.load_cookie_from = ResUtil.get_file_path("cookie_xq.txt")
		self.save_cookie_to = self.load_cookie_from
		if not os.path.isfile(self.load_cookie_from):
			os.open(self.load_cookie_from)

	def send(self, url, headers, payload):
		assert url is not None
		self.url = url
		if headers is not None:
			self.headers = headers
		else:
			self.headers = {}
		self.payload = payload
		self.headers["User-Agent"] = self.ua
		if self.payload is not None:
			data = urllib.urlencode(self.payload)
		else:
			data = None
		cookie = cookielib.MozillaCookieJar()
		cookie.load(self.load_cookie_from, ignore_discard=True, ignore_expires=True)
		handler = urllib2.HTTPCookieProcessor(cookie)
		if self.proxies is not None:
			proxy_handler = urllib2.ProxyHandler(self.proxies)
			opener = urllib2.build_opener(proxy_handler, handler)
		else:
			opener = urllib2.build_opener(handler)
		req = urllib2.Request(url=self.url, headers=self.headers, data=data)
		resp = opener.open(req)
		content = resp.read().decode('utf-8')
		code = resp.getcode()
		if code < 400:
			if self.save_cookie_to is not None and self.save_cookie_to != '':
				cookie.save(self.save_cookie_to, ignore_discard=True, ignore_expires=True)
			else:
				cookie.save(self.load_cookie_from, ignore_discard=True, ignore_expires=True)
		else:
			content = None
		return content

	def fetch(self, report_type):
		now = int(time.time())
		size = (2017 - 2000) * 4
		if ReqUtil.REP_TYPE_MAIN == report_type:
			url = "https://xueqiu.com/stock/f10/finmainindex.json?symbol=%s&page=1&size=%d&_=%d" % (self.st_symbol, size, now)
		elif ReqUtil.REP_TYPE_PROFIT == report_type:
			url = "https://xueqiu.com/stock/f10/incstatement.json?symbol=%s&page=1&size=%d&_=%d" % (self.st_symbol, size, now)
		elif ReqUtil.REP_TYPE_ASSETS == report_type:
			url = "https://xueqiu.com/stock/f10/balsheet.json?symbol=%s&page=1&size=%d&_=%d" % (self.st_symbol, size, now)
		elif ReqUtil.REP_TYPE_CUR == report_type:
			url = "https://xueqiu.com/v4/stock/quote.json?code=%s&_=%d" % (st_symbol, now)
		elif ReqUtil.REP_TYPE_FEEDBACK == report_type:
			url = "https://xueqiu.com/stock/f10/bonus.json?symbol=%s&page=1&size=%d&_=%d" % (self.st_symbol, size, now)
		elif ReqUtil.REP_TYPE_CASH == report_type:
			url = "https://xueqiu.com/stock/f10/cfstatement.json?symbol=%s&page=1&size=%d&_=%d" % (self.st_symbol, size, now)
		else:
			return None
		content = self.send(url, {}, None)
		return content

	def prepare(self):
		url = "https://xueqiu.com/S/%s" % self.st_symbol
		return self.send(url, {}, None)

		# request = urllib2.Request(url)
		# request.add_header('User-Agent', g_ua)
		# request.add_header('Cookie', g_cookie)
		# response = urllib2.urlopen(request)
		# dic = json.loads(response.read())
		# if REP_TYPE_CUR == report_type:
		# 	dat = dic[st_symbol]
		# 	return dat
		# else:
		# 	dat_list = dic["list"]
		# 	if assert_if_size_err:
		# 		assert size == len(dat_list)
		# 	des_list = []
		# 	for i, el in enumerate(dat_list):
		# 		if 0 == i or (1 == (i + 1 - months_from_2017) % 4):
		# 			des_list.append(el)
		# 	return des_list
