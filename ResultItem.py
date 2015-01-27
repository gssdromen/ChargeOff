# coding:UTF-8

class ResultItem(object):
    # nhxbjye-拟核销本金余额
    # hxbj-核销本金
    # hxyqbj-核销逾期本金
    # hxydqlx-核销已到期利息
    # hxwdqlx-核销未到期利息
    # hxyx-核销逾息
    # hxfx-核销罚息
    def __init__(self,rtnum=None, name=None, nhxbjye=None, hxbj=None, hxyqbj=None, hxydqlx=None, hxwdqlx=None, hxyx=None, hxfx=None):
        # super(ResultItem, self).__init__()
        self.rtnum = rtnum
        self.name = name
        self.nhxbjye = nhxbjye
        self.hxbj = hxbj
        self.hxyqbj = hxyqbj
        self.hxydqlx = hxydqlx
        self.hxwdqlx = hxwdqlx
        self.hxyx = hxyx
        self.hxfx = hxfx
