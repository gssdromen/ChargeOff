# coding:UTF-8

import sys
import os
import shutil
from datetime import *
import HttpHelper
from Constants import Constants
from LineItem import LineItem
from HKJHB import HKJHB
from ResultItem import ResultItem
from ZJHKItem import ZJHKItem
from bs4 import BeautifulSoup
from xlwt.Workbook import *



class Main(object):
    """docstring for ClassName"""
    def __init__(self):
        super(Main, self).__init__()
        # self.arg = arg
        self.http = HttpHelper.HttpHelper()
        self.reset()
        self.constant = Constants()

    def getCookies(self):
        fileHandle = open('acc.txt', 'r')
        line = fileHandle.readline()
        aList = line.split('|')
        dic={}
        dic["loginName"]=aList[0]
        dic["password"]=aList[1]
        # dic["loginName"]="wuyinjun"
        # dic["password"]="vfs2"
        dic["save.x"] = '0'
        dic["save.y"] = '0'
        self.http.sendRequest('post', self.constant.baseurl + "/vfs2/login.html", dic)

    def writeCustomerLog(self):
        print u'开始写入详细报告'
        path = "D:\\down\\detail.xls"
        excel = Workbook()
        for i in range(len(self.allCustomerHKJHB)):
            hkjhb = self.allCustomerHKJHB[i]
            zjhks = self.allCustomerZJHK[i]
            #zjhks = []
            zjhkStartline = len(hkjhb.lines) + 4
            w_sheet = excel.add_sheet(hkjhb.rtnum+hkjhb.name)
            # 写还款计划表的表头
            w_sheet.write(0, 0, u"还款序号")
            w_sheet.write(0, 1, u"到期日")
            w_sheet.write(0, 2, u"还款额")
            w_sheet.write(0, 3, u"本金部分")
            w_sheet.write(0, 4, u"利息部分")
            # 写直接汇款的表头
            w_sheet.write(0, 7, u"分期序号")
            w_sheet.write(0, 8, u"结算类型")
            w_sheet.write(0, 9, u"金额")
            w_sheet.write(0, 10, u"放款日期")
            w_sheet.write(0, 11, u"收款日期")
            # 写还款计划表的数据
            for i in range(len(hkjhb.lines)):
                line = hkjhb.lines[i]
                w_sheet.write(i+1, 0, line.index)
                w_sheet.write(i+1, 1, line.payBackDate.strftime('%Y%m%d'))
                w_sheet.write(i+1, 2, line.payBackMoney)
                w_sheet.write(i+1, 3, line.payBackMoneyBJ)
                w_sheet.write(i+1, 4, line.payBackMoneyLX)
            # 写直接汇款的数据
            for i in range(len(zjhks)):
                line = zjhks[i]
                w_sheet.write(i+1, 7, line.payIndex)
                w_sheet.write(i+1, 8, line.payType)
                w_sheet.write(i+1, 9, line.payBackMoney)
                w_sheet.write(i+1, 10, line.loanDate)
                w_sheet.write(i+1, 11, line.payBackDate)
        excel.save(path)
        print 'end'

    def writeResultsToExcel(self):
        print u'开始写入核销结果'
        path = "D:\\down\\ChargeOffResult.xls"
        excel = Workbook()
        w_sheet = excel.add_sheet('0')
        # 写表格头
        w_sheet.write(0, 0, u"序号")
        w_sheet.write(0, 1, u"申请编号")
        w_sheet.write(0, 2, u"合同编号")
        w_sheet.write(0, 3, u"借款人")
        w_sheet.write(0, 4, u"拟核销本金余额")
        w_sheet.write(0, 5, u"核销本金")
        w_sheet.write(0, 6, u"核销逾期本金")
        w_sheet.write(0, 7, u"核销已到期利息")
        w_sheet.write(0, 8, u"核销未到期利息")
        w_sheet.write(0, 9, u"核销逾息")
        w_sheet.write(0, 10, u"核销罚息")
        for i in range(len(self.allCustomerResult)):
            item = self.allCustomerResult[i]
            applyNum = self.allCustomer[i]
            w_sheet.write(i+1, 0, i+1)
            w_sheet.write(i+1, 1, applyNum)
            w_sheet.write(i+1, 2, item.rtnum)
            w_sheet.write(i+1, 3, item.name)
            w_sheet.write(i+1, 4, item.nhxbjye)
            w_sheet.write(i+1, 5, item.hxbj)
            w_sheet.write(i+1, 6, item.hxyqbj)
            w_sheet.write(i+1, 7, item.hxydqlx)
            w_sheet.write(i+1, 8, item.hxwdqlx)
            w_sheet.write(i+1, 9, item.hxyx)
            w_sheet.write(i+1, 10, item.hxfx)
        excel.save(path)
        print 'end'

    def calculateAll(self):
        print u'开始计算核销金额，基准日期为' + self.today.strftime('%Y%m%d')
        map(self.calculateOne, self.allCustomerHKJHB)
        # for item in self.allCustomerHKJHB:
        #     self.calculateOne(item, self.today)
        print 'end'

    def calculateOne(self, hkjhb):
        today = self.today
        #today = datetime.today()
        deltaDays = timedelta(days=10)
        print u'开始计算：' + hkjhb.rtnum + '  ' + hkjhb.name
        # nhxbjye-拟核销本金余额
        # hxbj-核销本金
        # hxyqbj-核销逾期本金
        # hxydqlx-核销已到期利息
        # hxwdqlx-核销未到期利息
        # hxyx-核销逾息
        # hxfx-核销罚息
        nhxbjye = 0
        hxbj = 0
        hxyqbj = 0
        hxydqlx = 0
        hxwdqlx = 0
        hxyx = 0
        hxfx = 0
        lines = hkjhb.lines
        for item in lines:
            # 逾期未超过十天
            if item.payBackDate + deltaDays > today:
                hxbj += float(item.payBackMoneyBJ)
                # hxwdqlx += float(item.payBackMoneyLX)
            # 逾期超过十天
            else:
                hxyqbj += float(item.payBackMoneyBJ)
                # hxydqlx += float(item.payBackMoneyLX)
            # 利息与本金不同，利息不是按10天而是按当天是否到期分的
            if item.payBackDate > today:
                hxwdqlx += float(item.payBackMoneyLX)
            else:
                hxydqlx += float(item.payBackMoneyLX)
        nhxbjye = hxbj + hxyqbj
        hxyx, hxfx = self.getYXFX(hkjhb.rtnum)
        result = ResultItem(hkjhb.rtnum, hkjhb.name, nhxbjye, hxbj, hxyqbj, hxydqlx, hxwdqlx, hxyx, hxfx)
        self.allCustomerResult.append(result)

    # 暂不使用
    def getAllYXFX(self):
        for item in self.allCustomer:
            self.getYXFX(item)

    # 逾息罚息，顺便存直汇记录
    def getYXFX(self, rtnum):
        yuxi = 0
        faxi = 0
        dic = {}
        dic['applyId'] = ''
        dic['contractId'] = rtnum
        html = BeautifulSoup(self.http.sendRequest('post', self.constant.baseurl+"/vfs2/innerpage/loanafterportlet/disposalQueryList.html", dic))
        # 得到直接汇款详细
        rrprtdList = html.find(id='rrprtdList')
        if rrprtdList:
            trs = rrprtdList.find_all('tr')
            del trs[0]
            temp = []
            for tr in trs:
                tds = tr.find_all('td')
                payIndex = tds[1].text.strip()
                payType = tds[3].text.strip()
                payBackMoney = self.changeTextToFloat(tds[4].text.strip())
                loanDate = tds[5].text.strip()
                payBackDate = tds[6].text.strip()
                zjhkItem = ZJHKItem(payIndex, payType, payBackMoney,loanDate, payBackDate)
                temp.append(zjhkItem)
                if payType == u'车贷-逾息':
                    yuxi += payBackMoney
                elif payType == u'车贷-罚息':
                    faxi += payBackMoney
            self.allCustomerZJHK.append(temp)
            return (yuxi, faxi)
        else:
            self.allCustomerZJHK.append([])
            return (0,0)

    def getAllHKJHB(self):
        print u'开始拉取客户还款计划表'
        self.reset()
        with open(u'D:\\新建文件夹\\a.txt', 'r') as f:
            for line in f:
                num = line.strip()
                if 'RT' in num:
                    num = self.getApplyNumFromRtNum(num)
                self.allCustomer.append(num)
        for item in self.allCustomer:
            self.allCustomerHKJHB.append(self.getHKJHBfromHtml(self.getHKJHB(item)))
        print 'end'

    def getHKJHB(self, num):
        url = self.constant.baseurl + '/vfs2/innerpage/loanafterportlet/buildContractAccessoryTwo.html?applyID=' + num
        html = BeautifulSoup(self.http.sendRequest('get', url))
        # print html
        return html

    def getApplyNumFromRtNum(self, rtnum):
        url = self.constant.baseurl + ''
        dict = {"contractID": rtnum, "flag": "Y"}
        html = BeautifulSoup(self.http.sendRequest('post', self.constant.baseurl + '/vfs2/loanapply/amendApplyAccount.html', dict))
        tds = html.find(class_="odd").find_all("td")
        return tds[1].text.strip()

    def getHKJHBfromHtml(self, html):
        needs = html.find_all('td', class_='tableStrong')
        # print needs
        zipCode = needs[1].text.strip()
        # 判断地址是否有两行
        if len(needs) == 8:
            address = needs[3].text.strip().encode('UTF-8')
        else:
            address = needs[3].text.strip().encode('UTF-8') + needs[4].text.strip().encode('UTF-8')
        name = needs[-2].text.strip()
        needs = html.find_all('table', class_='tbBlock')
        table = needs[2]
        needs = needs[1].find_all('td', class_='tdLeftH20')
        rtnum = needs[0].text[10:].strip()
        loanDate = needs[2].text[9:].strip()
        print rtnum + ':' + name
        # 开始获得详细
        lines = []
        trs = table.find_all('tr')
        del trs[0]
        for tr in trs:
            tds = tr.find_all('td')
            index = tds[0].text.strip()
            payBackDate = datetime.strptime(tds[1].text.strip(), '%Y%m%d')
            # print payBackDate
            payBackMoney = tds[2].text.strip()
            payBackMoneyBJ = tds[3].text.strip()
            payBackMoneyLX = tds[4].text.strip()
            lines.append(LineItem(index, payBackDate, payBackMoney, payBackMoneyBJ, payBackMoneyLX))
        return HKJHB(zipCode, address, name, rtnum, loanDate, lines)

    def getChargeOffDay(self):
        print u'请输入核销日期：格式为YYYY.MM.DD,回车表示今天'
        temp = raw_input()
        if temp == '':
            self.today = datetime.today()
            # print self.today
            return
        try:
            temp = temp.split('.')
            year = temp[0]
            month = temp[1]
            day = temp[2]
            self.today = datetime(int(year), int(month), int(day), int(8))
            # print self.today
        except Exception, e:
            print u'日期格式错误'
            raise e
        else:
            pass
        finally:
            pass

    def reset(self):
        self.allCustomer = []
        self.allCustomerHKJHB = []
        self.allCustomerZJHK = []
        self.allCustomerResult = []

    def changeTextToFloat(self, text):
        # print text
        text = text.replace(',', '')
        return float(text)

def main():
    ex = Main()
    ex.getCookies()
    ex.getChargeOffDay()
    ex.getAllHKJHB()
    ex.calculateAll()
    ex.writeResultsToExcel()
    ex.writeCustomerLog()
    #ex.getAllYXFX()

if __name__ == '__main__':
    main()
