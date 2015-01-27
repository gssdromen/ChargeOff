# coding:UTF-8

class HKJHB(object):
    def __init__(self, zipCode=None, address=None, name=None, rtnum=None, loanDate=None, lines=None):
        # super(ResultItem, self).__init__()
        self.zipCode = zipCode
        self.address = address
        self.name = name
        self.rtnum = rtnum
        self.loanDate = loanDate
        self.lines = lines
