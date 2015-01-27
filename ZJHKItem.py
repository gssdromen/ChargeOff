# coding:UTF-8

class ZJHKItem(object):
    #分期序号 结算类型 金额 放款日期 收款日期
    def __init__(self, payIndex=None, payType=None, payBackMoney=None, loanDate=None, payBackDate=None):
        # super(ResultItem, self).__init__()
        self.payIndex = payIndex
        self.payType = payType
        self.payBackMoney = payBackMoney
        self.loanDate = loanDate
        self.payBackDate = payBackDate
