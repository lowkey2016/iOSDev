# -*- coding: utf-8 -*-

### 资产负债表
class ZCFZB(object):
    reportdate = "" # 报表日期
    curfds = 0.0 # 货币资金
    tradfinasset = 0.0 # 交易性金融资产
    notesrece = 0.0 # 应收票据
    accorece = 0.0 # 应收账款
    prep = 0.0 # 预付款项
    interece = 0.0 # 应收利息
    dividrece = 0.0 # 应收股利
    otherrece = 0.0 # 其他应收款
    inve = 0.0  # 存货
    prepexpe = 0.0 # 待摊费用
    othercurrasse = 0.0 # 其他流动资产
    totcurrasset = 0.0 # 流动资产合计
    avaisellasse = 0.0 # 可供出售金融资产
    holdinvedue = 0.0 # 持有至到期投资
    longrece = 0.0 # 长期应收款
    equiinve = 0.0 # 长期股权投资
    otherlonginve = 0.0 # 其他长期投资
    inveprop = 0.0 # 投资性房地产
    fixedasseimmo = 0.0 # 固定资产原值
    accudepr = 0.0 # 累计折旧
    fixedassenetw = 0.0 # 固定资产净值
    fixedasseimpa = 0.0 # 固定资产减值准备
    fixedassenet = 0.0 # 固定资产净额
    consprog = 0.0 # 在建工程
    engimate = 0.0 # 工程物资
    prodasse = 0.0 # 生产性生物资产
    comasse = 0.0 # 公益性生物资产
    hydrasset = 0.0 # 油气资产
    intaasset = 0.0 # 无形资产
    deveexpe = 0.0 # 开发支出
    goodwill = 0.0 # 商誉
    logprepexpe = 0.0 # 长期待摊费用
    defetaxasset = 0.0 # 递延所得税资产
    othernoncasse = 0.0 # 其他非流动资产
    totalnoncassets = 0.0 # 非流动资产合计
    totasset = 0.0 # 资产总计
    shorttermborr = 0.0 # 短期借款
    tradfinliab = 0.0 # 交易性金融负债
    notespaya = 0.0 # 应付票据
    accopaya = 0.0 # 应付账款
    advapaym = 0.0 # 预收款项
    copeworkersal = 0.0 # 应付职工薪酬
    taxespaya = 0.0 # 应交税费
    intepaya = 0.0 # 应付利息
    divipaya = 0.0 # 应付股利
    otherpay = 0.0 # 其他应付款
    shorttermbdspaya = 0.0 # 应付短期债券
    duenoncliab = 0.0 # 一年内到期的非流动负债
    othercurreliabi = 0.0 # 其他流动负债
    totalcurrliab = 0.0 # 流动负债合计
    longborr = 0.0 # 长期借款
    bdspaya = 0.0 # 应付债券
    longpaya = 0.0 # 长期应付款
    specpaya = 0.0 # 专项应付款
    longdefeinco = 0.0 # 长期递延收益
    defeincotaxliab = 0.0 # 递延所得税负债
    othernoncliabi = 0.0 # 其他非流动负债
    totalnoncliab = 0.0 # 非流动负债合计
    totliab = 0.0 # 负债合计
    paresharrigh = 0.0 # 归属于母公司股东权益合计
    minysharrigh = 0.0 # 少数股东权益
    righaggr = 0.0 # 所有者权益(或股东权益)合计
    totliabsharequi = 0.0 # 负债和所有者权益

    @staticmethod
    def as_self(d):
        obj = ZCFZB()
        obj.__dict__.update(d)
        return obj

    def __init__(self, **entries):
        self.__dict__.update(entries)
