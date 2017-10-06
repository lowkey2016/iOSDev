# -*- coding: utf-8 -*-

import re

class RegUtil(object):
	@classmethod
	def match_one_from_re(self, desc, content):
		pattern = re.compile(desc.decode('utf-8'), re.S)
		items = re.findall(pattern, content)
		if len(items) == 0:
			return None
		else:
			return items[0]
