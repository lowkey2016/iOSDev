#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import re
from models.zcfzb import ZCFZB
from models.gslrb import GSLRB
from models.xjllb import XJLLB
from models.fjsj import FJSJ
from models.stock import Stock
from utils.util_res import ResUtil
from utils.util_req import ReqUtil
from managers.st_mgr import StMgr
from analyzers.anlz_mgr import AnlzMgr
import json

def match_one_from_re(desc, content):
	pattern = re.compile(desc.decode('utf-8'), re.S)
	items = re.findall(pattern, content)
	if len(items) == 0:
		return None
	else:
		return items[0]

if __name__ == "__main__":
	reload(sys)
	sys.setdefaultencoding('utf8')

	st_mgr = StMgr()

	# json_data = ResUtil.read_json('test_zcfzb.json')
	# zcfzb = json.loads(json_data, object_hook=ZCFZB.as_self)
	# print zcfzb.__dict__

	# json_data = ResUtil.read_json('test_gslrb.json')
	# gslrb = json.loads(json_data, object_hook=GSLRB.as_self)
	# print gslrb.__dict__

	# json_data = ResUtil.read_json('test_xjllb.json')
	# xjllb = json.loads(json_data, object_hook=XJLLB.as_self)
	# print xjllb.__dict__

	# json_data = ResUtil.read_json('test_fjsj.json')
	# fjsj = json.loads(json_data, object_hook=FJSJ.as_self)
	# print fjsj.__dict__
	
	# st_mgr.fetch_fangdichan_ppp_data_from_network()

	AnlzMgr.draw_jiadian_chudians()
	# AnlzMgr.draw_fangdichan_ppp()
