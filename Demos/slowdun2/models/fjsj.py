# -*- coding: utf-8 -*-

### 附加数据
class FJSJ(object):
    name = "" # 名字
    reportdate = "" # 报表日期
    finstmtcomments = "" # 财报意见
    acntfirm = "" # 会计师事务所
    finstmtspecials = "" # 董事会在财报中提出的注意事项
    sharecount = 0.0 # 股份总数

    shorttermborrdetail = "" # 短期借款明细
    longborrdetail = "" # 长期借款明细
    
    curfds_cash = 0.0 # 货币资金中的库存现金
    curfds_bank = 0.0 # 货币资金中的银行存款
    curfds_other = 0.0 # 货币资金中的其他货币资金
    curfds_limit = 0.0 # 货币资金中的使用受限资金
    
    notesrece_bank = 0.0 # 应收票据中的银行承兑汇票
    notesrece_business = 0.0 # 应收票据中的商业承兑汇票
    notesrece_other = 0.0 # 应收票据中的其它部分
    
    accorece_credit_tot = 0.0 # 按信用风险特征组合计坏账准备的应收账款
    accorece_credit_bad = 0.0 # 按信用风险特征组合计坏账准备的应收账款坏账准备
    accorece_single_tot = 0.0 # 单项金额不重大但单独计坏账准备的应收账款
    accorece_single_bad = 0.0 # 单项金额不重大但单独计坏账准备的应收账款坏账准备
    accorece_single_imp_tot = 0.0 # 期末单项金额重大并单项计坏账准备的应收账款
    accorece_single_imp_bad = 0.0 # 期末单项金额重大并单项计坏账准备的应收账款坏账准备
    accorece_0_1_tot = 0.0 # 账龄小于1年的应收账款
    accorece_0_1_bad = 0.0 # 账龄小于1年的应收账款坏账准备
    accorece_1_2_tot = 0.0 # 账龄1-2年的应收账款
    accorece_1_2_bad = 0.0 # 账龄1-2年的应收账款坏账准备
    accorece_2_3_tot = 0.0 # 账龄2-3年的应收账款
    accorece_2_3_bad = 0.0 # 账龄2-3年的应收账款坏账准备
    accorece_3_4_tot = 0.0 # 账龄3-4年的应收账款
    accorece_3_4_bad = 0.0 # 账龄3-4年的应收账款坏账准备
    accorece_4_5_tot = 0.0 # 账龄4-5年的应收账款
    accorece_4_5_bad = 0.0 # 账龄4-5年的应收账款坏账准备
    accorece_5_n_tot = 0.0 # 账龄大于5年的应收账款
    accorece_5_n_bad = 0.0 # 账龄大于5年的应收账款坏账准备
    accorece_bad_standard = "" # 应收账款的坏账计提标准

    prep_0_1 = 0.0 # 1年内的预付款项
    prep_1_n = 0.0 # 1年以上的预付款项

    otherrecedetail = "" # 其他应收款明细

    inverevvallossstandard = "" # 存货跌价计提标准
    inverevvallosstot = 0.0 # 存货跌价计提总额
    inveincal = "" # 存货的成本计价方法
    inveoutcal = "" # 存货的发出计价方法
    inve_prod = 0.0 # 存货产量
    inve_sale = 0.0 # 存货销量
    inve_save = 0.0 # 存货存量
    inve_unit = 0.0 # 产销存单位

    holdinvedue_inrate = 0.0 # 持有至到期投资的实际利率，百分数
    holdinvedue_losscur = 0.0 # 持有至到期投资的减值数额
    holdinvedue_lossback = 0.0 # 持有至到期投资的减值转回数额

    avaisellassecur = 0.0 # 可供出售金融资产的期末账面余额
    avaisellassecost = 0.0 # 可供出售金融资产的买入成本

    invepropcal = "" # 投资性房地产的计量模式

    fixedassedepolicy = "" # 固定资产的折旧政策
    intaassetdmopolicy = "" # 无形资产的摊销政策
    findevexp = 0.0 # 财报中记录的开发支出

    emplyescnt = 0.0 # 公司员工总数
    equfinpubpri = 0.0 # 权益性筹资的发行价
    debtfininrate = 0.0 # 债务性筹资的利率，百分数

    @staticmethod
    def as_self(d):
        obj = FJSJ()
        obj.__dict__.update(d)
        return obj

    def __init__(self, **entries):
        self.__dict__.update(entries)
        for k in self.__dict__.keys():
            if self.__dict__[k] is None:
                str_keys = ['name', 'reportdate', 'finstmtcomments', 'acntfirm', 'finstmtspecials', 'shorttermborrdetail', 'longborrdetail', 'accorece_bad_standard', 'otherrecedetail', 'inverevvallossstandard', 'inveincal', 'inveoutcal', 'invepropcal', 'fixedassedepolicy', 'intaassetdmopolicy']
                if k in str_keys:
                    self.__dict__[k] = ''
                else:
                    self.__dict__[k] = 0.0

        # 应收账款坏账计提总额
        self.accorece_bad_tot = self.accorece_credit_bad + self.accorece_single_bad + self.accorece_single_imp_bad

        # 产量和存量之和
        self.inve_prodandsave = self.inve_prod + self.inve_save
