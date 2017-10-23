# -*- coding: utf-8 -*-

import os
import json

class ResUtil(object):
	@classmethod
	def get_file_path(self, fname):
		fname = 'resources/%s' % fname
		file_path = os.path.join(os.getcwd(), fname)
		return file_path

	@classmethod
	def read_json(self, fname):
		file_path = ResUtil.get_file_path(fname)
		json_data = open(file_path).read()
		return json_data

	@classmethod
	def create_dir_if_needed(self, dirname):
		dirpath = ResUtil.get_file_path(dirname)
		if not os.path.isdir(dirpath):
			os.mkdir(dirpath)

	@classmethod
	def get_zcfzb_file_path(self, st_symbol):
		ResUtil.create_dir_if_needed(st_symbol)
		dirpath = ResUtil.get_file_path(st_symbol)
		file_path = "%s/zcfzb.json" % dirpath
		return file_path

	@classmethod
	def get_gslrb_file_path(self, st_symbol):
		ResUtil.create_dir_if_needed(st_symbol)
		dirpath = ResUtil.get_file_path(st_symbol)
		file_path = "%s/gslrb.json" % dirpath
		return file_path

	@classmethod
	def get_xjllb_file_path(self, st_symbol):
		ResUtil.create_dir_if_needed(st_symbol)
		dirpath = ResUtil.get_file_path(st_symbol)
		file_path = "%s/xjllb.json" % dirpath
		return file_path

	@classmethod
	def get_quote_file_path(self, st_symbol):
		ResUtil.create_dir_if_needed(st_symbol)
		dirpath = ResUtil.get_file_path(st_symbol)
		file_path = "%s/quote.json" % dirpath
		return file_path

	@classmethod
	def is_file_exists(self, fname):
		fpath  = ResUtil.get_file_path(fname)
		return os.path.exists(fpath)

	@classmethod
	def save_html_content(self, html_str, fname):
		with open(ResUtil.get_file_path(fname), 'w') as outfile:
			outfile.write(html_str)
