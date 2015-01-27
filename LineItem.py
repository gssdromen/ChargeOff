# coding:UTF-8

class LineItem(object):
    def __init__(self, index=None, payBackDate=None, payBackMoney=None, payBackMoneyBJ=None, payBackMoneyLX=None):
        # super(ResultItem, self).__init__()
        self.index = index
        self.payBackDate = payBackDate
        self.payBackMoney = payBackMoney
        self.payBackMoneyBJ = payBackMoneyBJ
        self.payBackMoneyLX = payBackMoneyLX
