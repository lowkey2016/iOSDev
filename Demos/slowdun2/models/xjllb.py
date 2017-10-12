# -*- coding: utf-8 -*-

### 现金流量表
class XJLLB(object):
    begindate = ""
    enddate = ""
    
    laborgetcash = 0.0 # 销售商品、提供劳务收到的现金
    receotherbizcash = 0.0 # 收到的其他与经营活动有关的现金
    bizcashinfl = 0.0 # 经营活动现金流入小计
    labopayc = 0.0 # 购买商品、接受劳务支付的现金
    payworkcash = 0.0 # 支付给职工以及为职工支付的现金
    paytax = 0.0 # 支付的各项税费
    payacticash = 0.0 # 支付的其他与经营活动有关的现金
    bizcashoutf = 0.0 # 经营活动现金流出小计
    mananetr = 0.0 # 经营活动产生的现金流量净额

    withinvgetcash = 0.0 # 收回投资所收到的现金
    inveretugetcash = 0.0 # 取得投资收益收到的现金
    fixedassetnetc = 0.0 # 处置固定资产、无形资产和其他长期资产所回收的现金净额
    subsnetc = 0.0 # 处置子公司及其他营业单位收到的现金净额
    receinvcash = 0.0 # 收到的其他与投资活动有关的现金
    reducashpled = 0.0 # 减少质押和定期存款所收到的现金
    invcashinfl = 0.0 # 投资活动现金流入小计
    acquassetcash = 0.0 # 购建固定资产、无形资产和其他长期资产所支付的现金
    invpayc = 0.0 # 投资所支付的现金
    loannetr = 0.0 # 质押贷款净增加额
    subspaynetcash = 0.0 # 取得子公司及其他营业单位支付的现金净额
    payinvecash = 0.0 # 支付的其他与投资活动有关的现金
    incrcashpled = 0.0 # 增加质押和定期存款所支付的现金
    invcashoutf = 0.0 # 投资活动现金流出小计
    invnetcashflow = 0.0 # 投资活动产生的现金流量净额

    invrececash = 0.0 # 吸收投资收到的现金
    subsrececash = 0.0 # 其中：子公司吸收少数股东投资收到的现金
    recefromloan = 0.0 # 取得借款收到的现金
    issbdrececash = 0.0 # 发行债券收到的现金
    recefincash = 0.0 # 收到其他与筹资活动有关的现金
    fincashinfl = 0.0 # 筹资活动现金流入小计
    debtpaycash = 0.0 # 偿还债务支付的现金
    diviprofpaycash = 0.0 # 分配股利、利润或偿付利息所支付的现金
    subspaydivid = 0.0 # 其中：子公司支付给少数股东的股利，利润
    finrelacash = 0.0 # 支付其他与筹资活动有关的现金
    fincashoutf = 0.0 # 筹资活动现金流出小计
    finnetcflow = 0.0 # 筹资活动产生的现金流量净额

    chgexchgchgs = 0.0 # 汇率变动对现金及现金等价物的影响
    cashnetr = 0.0 # 现金及现金等价物净增加额
    inicashbala = 0.0 # 期初现金及现金等价物余额
    finalcashbala = 0.0 # 期末现金及现金等价物余额

    netprofit = 0.0 # 净利润
    minysharrigh = 0.0 # 少数股东权益
    unreinveloss = 0.0 # 未确认的投资损失
    asseimpa = 0.0 # 资产减值准备
    assedepr = 0.0 # 固定资产折旧、油气资产折耗、生产性物资折旧
    realestadep = 0.0 # 投资性房地产折旧、摊销
    intaasseamor = 0.0 # 无形资产摊销
    longdefeexpenamor = 0.0 # 长期待摊费用摊销 
    prepexpedecr = 0.0 # 待摊费用的减少
    accrexpeincr = 0.0 # 预提费用的增加
    dispfixedassetloss = 0.0 # 处置固定资产、无形资产和其他长期资产的损失
    fixedassescraloss = 0.0 # 固定资产报废损失
    valuechgloss = 0.0 # 公允价值变动损失
    defeincoincr = 0.0 # 递延收益增加（减：减少）
    estidebts = 0.0 # 预计负债
    finexpe = 0.0 # 财务费用
    inveloss = 0.0 # 投资损失
    defetaxassetdecr = 0.0 # 递延所得税资产减少
    defetaxliabincr = 0.0 # 递延所得税负债增加
    inveredu = 0.0 # 存货的减少
    receredu = 0.0 # 经营性应收项目的减少
    payaincr = 0.0 # 经营性应付项目的增加
    unseparachg = 0.0 # 已完工尚未结算款的减少(减:增加)
    unfiparachg = 0.0 # 已结算尚未完工款的增加(减:减少)
    other = 0.0 # 其他
    biznetcflow = 0.0 # 经营活动产生现金流量净额
    debtintocapi = 0.0 # 债务转为资本
    expiconvbd = 0.0 # 一年内到期的可转换公司债券
    finfixedasset = 0.0 # 融资租入固定资产
    cashfinalbala = 0.0 # 现金的期末余额
    cashopenbala = 0.0 # 现金的期初余额
    equfinalbala = 0.0 # 现金等价物的期末余额
    equopenbala = 0.0 # 现金等价物的期初余额
    cashneti = 0.0 # 现金及现金等价物的净增加额

    @staticmethod
    def as_self(d):
        obj = XJLLB()
        obj.__dict__.update(d)
        return obj

    def __init__(self, **entries):
        self.__dict__.update(entries)
        for k in self.__dict__.keys():
            if self.__dict__[k] is None:
                if k == 'begindate' or k == 'enddate':
                    self.__dict__[k] = ''
                else:
                    self.__dict__[k] = 0.0

        # 间接法编制的现金流量表中的折旧摊销总和
        self.depamortot = self.assedepr + self.intaasseamor

        # 简化的自由现金流 = 经营现金流净额 - 投资活动现金流出净额
        if self.invnetcashflow < 0:
                outflow = -self.invnetcashflow
        else:
            outflow = 0
        self.simfreecashflow = self.mananetr - outflow
