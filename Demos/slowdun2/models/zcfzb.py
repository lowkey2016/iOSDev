# -*- coding: utf-8 -*-

import utils.util_cons as Cons

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
    righaggr = 0.0 # 所有者权益(或股东权益)合计
    paidincapi = 0.0 # 实收资本(或股本)
    capisurp = 0.0 # 资本公积
    treastk = 0.0 # 减：库存股
    specrese = 0.0 # 专项储备
    rese = 0.0 # 盈余公积
    generiskrese = 0.0 # 一般风险准备
    unreinveloss = 0.0 # 未确定的投资损失
    undiprof = 0.0 # 未分配利润
    topaycashdivi = 0.0 # 拟分配现金股利
    curtrandiff = 0.0 # 外币报表折算差额
    paresharrigh = 0.0 # 归属于母公司股东权益合计
    minysharrigh = 0.0 # 少数股东权益
    totliabsharequi = 0.0 # 负债和所有者权益
    
    @staticmethod
    def as_self(d):
        obj = ZCFZB()
        obj.__dict__.update(d)
        return obj

    def __init__(self, **entries):
        self.__dict__.update(entries)
        for k in self.__dict__.keys():
            if self.__dict__[k] is None:
                if k == 'reportdate':
                    self.__dict__[k] = ''
                else:
                    self.__dict__[k] = 0.0
                    
        # 应收款总和
        self.rectot = self.notesrece + self.accorece + self.interece + self.dividrece + self.otherrece + self.longrece

        # 经营相关资产总和
        self.manageassetot = self.prep + self.rectot + self.inve
        
        # 生产相关资产总和
        self.prodassetot = self.fixedassenet + self.consprog + self.engimate + self.prodasse + self.comasse + self.hydrasset + self.intaasset + self.deveexpe + self.goodwill + self.prepexpe + self.logprepexpe + self.defetaxasset

        # 投资相关资产总和
        self.inveassetot = self.tradfinasset + self.avaisellasse + self.holdinvedue + self.equiinve + self.otherlonginve + self.inveprop

        # 其它资产总和
        self.otherasettot = self.othercurrasse + self.othernoncasse

        # 速动资产
        self.liquidaset = self.totcurrasset - self.inve

        # 融资性负债合计
        self.finliabtot = self.shorttermborr + self.longborr + self.shorttermbdspaya + self.bdspaya

        # 经营性负债合计
        self.manageliabtot = self.notespaya + self.accopaya + self.advapaym + self.copeworkersal + self.intepaya + self.otherpay + self.longpaya + self.specpaya

        # 分配性负债合计
        self.payliabtot = self.taxespaya + self.divipaya

        # 其它负债合计
        self.otherliabtot = self.tradfinliab + self.duenoncliab + self.longdefeinco + self.defeincotaxliab + self.othercurreliabi + self.othernoncliabi

        # 有息负债
        self.borrtot = self.shorttermborr + self.longborr
        # 有息负债率 = 有息负债 / 总资产
        if self.totasset == 0:
            self.borrate = 0
        else:
            self.borrate = self.borrtot / self.totasset
        # 货币资金有息负债覆盖率 = 货币资金 / 有息负债
        if self.borrtot == 0:
            self.curborrcover = 0.0
        else:
            self.curborrcover = self.curfds / self.borrtot

        # 盈余公积 + 未分配利润
        self.reseandundiprof = self.rese + self.undiprof


        # 格雷厄姆相关指标

        # 清算价值 = (货币资金 + 交易性金融资产) + (应收票据 + 应收账款) * 0.8 + 存货 * 0.6 + (可供出售金融资产 + 持有至到期投资 + 投资性房地产) * 0.5 + (固定资产净额 + 在建工程 + 工程物资) * 0.15 - 总负债
        self.liquidvalue = (self.curfds + self.tradfinasset) + (self.notesrece + self.accorece) * 0.8 + self.inve * 0.6 + (self.avaisellasse + self.holdinvedue + self.inveprop) * 0.5 + (self.fixedassenet + self.consprog + self.engimate) * 0.15 - self.totliab

        # 流动资产价值 = 流动资产 - 总负债
        self.curassetvalue = self.totcurrasset - self.totliab
        # 现金资产价值 = 现金资产 - 总负债
        self.curfdsvalue = self.curfds - self.totliab

        # 资本结构 = 股票市值 / 资本总市值，其中：资本总市值 = 股票市值 + 总负债 + 优先股市值（如果有优先股），格雷厄姆标准：比例很高的是保守型，很低的是投机型，适中的是最优型
        # self.capstruct
