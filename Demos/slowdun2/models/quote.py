# -*- coding: utf-8 -*-

import utils.util_cons as Cons

### 资产负债表
class QUOTE(object):
    current = 0.0 # 当前股价
    totalShares = 0.0 # 总股本
    float_shares = 0.0 # 流通股本
    dividend = 0.0 # 每股股息
    time = '' # 记录的时间
    currency_unit = '' # 货币单位，例如 CNY
    
    @staticmethod
    def as_self(d):
        obj = QUOTE()
        obj.__dict__.update(d)
        return obj

    def __init__(self, **entries):
        self.__dict__.update(entries)
        for k in self.__dict__.keys():
            if self.__dict__[k] is None:
                if k == 'current' or k == 'totalShares' or k == 'float_shares' or k == 'dividend' or k == 'time' or k == 'currency_unit':
                    self.__dict__[k] = ''
                else:
                    self.__dict__[k] = 0.0

            if k == 'current' or k == 'totalShares' or k == 'float_shares' or k == 'dividend':
                self.__dict__[k] = float(self.__dict__[k])
