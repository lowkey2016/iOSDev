# -*- coding: utf-8 -*-

### 利润表
class GSLRB(object):
    begindate = ""
    enddate = ""

    biztotinco = 0.0 # 营业总收入
    bizinco = 0.0 # 营业收入
    inteinco = 0.0 # 利息收入
    realsale = 0.0 # 房地产销售收入
    otherbizinco = 0.0 # 其他业务收入

    biztotcost = 0.0 # 营业总成本
    bizcost = 0.0 # 营业成本
    inteexpe = 0.0 # 利息支出
    realsalecost = 0.0 # 房地产销售成本
    deveexpe = 0.0 # 研发费用
    otherbizcost = 0.0 # 其他业务成本
    biztax = 0.0 # 营业税金及附加
    salesexpe = 0.0 # 销售费用
    manaexpe = 0.0 # 管理费用
    finexpe = 0.0 # 财务费用

    asseimpaloss = 0.0 # 资产减值损失
    valuechgloss = 0.0 # 公允价值变动收益
    inveinco = 0.0 # 投资收益
    assoinveprof = 0.0 # 其中:对联营企业和合营企业的投资收益
    exchggain = 0.0 # 汇兑收益
    otherbizprof = 0.0 # 其他业务利润

    perprofit = 0.0 # 营业利润
    nonoreve = 0.0 # 营业外收入
    nonoexpe = 0.0 # 营业外支出
    noncassetsdisl = 0.0 # 非流动资产处置损失
    
    totprofit = 0.0 # 利润总额
    incotaxexpe = 0.0 # 所得税费用
    netprofit = 0.0 # 净利润
    parenetp = 0.0 # 归属于母公司所有者的净利润
    minysharrigh = 0.0 # 少数股东损益
    
    basiceps = 0.0 # 基本每股收益
    dilutedeps = 0.0 # 稀释每股收益

    othercompinco = 0.0 # 其他综合收益
    parecompinco = 0.0 # 归属于母公司所有者的其他综合收益
    minysharinco = 0.0 # 归属于少数股东的其他综合收益
    compincoamt = 0.0 # 综合收益总额
    parecompincoamt = 0.0 # 归属于母公司所有者的综合收益总额
    minysharincoamt = 0.0 # 归属于少数股东的综合收益总额

    @staticmethod
    def as_self(d):
        obj = GSLRB()
        obj.__dict__.update(d)
        return obj

    def __init__(self, **entries):
        self.__dict__.update(entries)
        for k in self.__dict__.keys():
            if self.__dict__[k] is None:
                if k == 'begindate' or k =='enddate':
                    self.__dict__[k] = ''
                else:
                    self.__dict__[k] = 0.0
