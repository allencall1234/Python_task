# -*- coding: utf-8 -*-
import queue
from collections import deque

from datetime import datetime
import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException

timeReg = "2018-08"
weeks = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']


class Item:
    # 定义基本属性
    date = ''
    time = ''
    desc = ''
    cardId = ''
    remark = ''

    # 定义构造方法
    def __init__(self, date, time, desc, remark, cardId):
        self.date = date
        self.time = time
        self.desc = desc
        self.cardId = cardId
        self.remark = remark

    def __str__(self):
        return str(self.time) + ',' + self.desc + ',' + self.cardId + ' ' + self.remark


headers1 = {
    'Host': 'hress.dafycredit.com:8083',
    'Content-Length': '408',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    'Cache-Control': 'no-cache',
    'Origin	': 'chrome-extension://fhbjgbiflinjbdggehcddcbncdddomop',
    'Postman-Token': 'aec3fba7-0d8e-30f0-a287-d9e218389caa',
    'Content-Type': 'text/plain;charset=UTF-8',
    'Accept	': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cookie': 'ASP.NET_SessionId=4purjy45ddspjpqkdtesvjuf'
}


def fetch_and_analysis():
    rawData = '{"FuncName":"fm.WindowProcess.GetTableContext"}{:ky->w{"Path":"1.1001.440","Parameters":{},"Data":{"A6":{"Data":{},"Parameters":{},"FMKey":"A6","PKey":"","PageSize":2147483647,"AllowChoice":false}},"OperaParam":{"CurrentTreeFMKey":"A6"},"Width":1537,"Height":594,"Url":"http://hress.dafycredit.com:8083/Window/Window.aspx?wind=210028","Init":true,"CurrentForm":"A6","ParamHtml":"","Popup":true,"WinType":208}'
    url = 'http://hress.dafycredit.com:8083/AjaxJSONProcess.aspx'
    try:
        response = sessionId.post(url, rawData)
        if response.status_code == 200:
            return response.text
    except Exception as e:
        return None


header2 = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
sessionId = requests.session()


def timeToMin(formatTime):
    try:
        arr = formatTime.split(':')
        return int(arr[0]) * 60 + int(arr[1])
    except Exception as e:
        print(e)
    return 0


def calculateTime(currDate, time1, time2, remark):
    currWeek = 0
    try:
        currWeek = datetime.strptime(currDate, '%Y-%m-%d').weekday()
    except Exception as e:
        print(e)
    print("时间：" + time1 + '-' + time2 + '  ' + weeks[currWeek], end='')
    if currWeek > 4:
        result = timeToMin(time2) - timeToMin(time1) - 60
    else:
        result = timeToMin(time2) - timeToMin(time1) - 9 * 60
    if result < 0:
        print('  异常')
        return 0
    else:
        print('  加班' + str(result // 60) + '小时' + str(result % 60) + '分' + '  ' + remark)
        return result


def parseText(resultText):
    soups = BeautifulSoup(resultText, "html.parser")  # soup转化
    resultList = soups.select('#fixRBody_A6 table tr')

    results = deque()
    tempDate = ''
    tempDateCount = 0

    for result in resultList:
        soups = BeautifulSoup(str(result), "html.parser")
        iTime = soups.select('td[c="XDATETIME"]')[0].text
        iDate = soups.select('td[c="TERM"]')[0].text
        iDesc = soups.select('td[c="INOUTFLAG"]')[0].text
        iRemark = soups.select('td[c="REMARK"]')[0].text
        iCardId = soups.select('td[c="CARDID"]')[0].text

        if tempDate != iDate:
            tempDate = iDate
            tempDateCount = 0
        else:
            tempDateCount += 1
        item = Item(iDate, iTime, iDesc, iRemark, iCardId)
        print(str(item))
        if iDate.startswith(timeReg):
            if tempDateCount > 1:  ###去重，避免补卡数据造成混乱
                results.pop()
            results.append(item)

    if len(results) > 0:
        last = results.pop()
    minTimes = 0
    while len(results) > 0:
        curr = results.pop()

        if str(curr.date) != str(last.date):
            last = curr
        else:
            print(last.date + '号打卡', end='')
            remark = last.remark
            if len(remark) == '':
                remark = curr.remark

            minTimes = minTimes + calculateTime(str(last.date), str(last.time).split(' ')[1],
                                                str(curr.time).split(' ')[1], remark)
            if len(results) > 0:
                last = results.pop()

    print('加班打卡时间：' + str(minTimes // 60) + '小时' + str(minTimes % 60) + '分')
    print("break")
    pass


def auto_login():
    '''
    获取网页html内容并返回
    '''
    paras = {
        '__VIEWSTATE': 'J6Rlj7Ztl0wVAYNSDGMTRAfGsjzoZ5aAncPyVSrv82O0keNbWr08qMN94dx5sLC8JuxbVZA1pIT1mKok60NYfs6DZvm3WL+FqshL0fY64n2Q/DXP+LArR72M+ONT9rUi54c9S5vNgE9rPjCuZWq0p24ALIHNhqO8IIS11Vy3Dxw5p0ZMmkQfkYuRfxG5pGuYWiyxk0BCxMuFsdQ3jriE0IARzzqwLDFnUk/fTPrvc9kUHkeQ0S/d1F7iL2Lzji+NmsPcMzbznCs+Dtci5O2ZMUWiY1XLEBUzB+MrJTicaotEIayv5ec1YDOuBTvlMsKuH3wJb/234DZg12KVC5IMm/Y/d7/GcyRXezj0qS6oGoreVvxG0TUkoZ3fYKv8lLVNKQGPrGCVvyxSrdmBAeCRCsgdVsMSoRL+YcQIo9oBaFt/rV8dw7LuLbD7MQUTNDd6VGCaychWCPkwbU+djqPTePCgQVj8D8UeeB3ECgI5bKR+wpLe58tElMWFh9qVHQnhdY6gCg==',
        '__EVENTVALIDATION': '5EF2mMPgNZ03/DOCwkdeJnqrw1ebyWH45Dmptw8FmtmMdtWuL7szCysh8rbKfSHPMHFVb2QjxOrgud8oK3rgA3jLn3olUjRqXiY4qU3f/FeeMxY/4EKFF24xeSA=',
        'userid': '524202',
        'pwd': 'z_lt199149',
        'ctl02': '登录'
    }
    url = 'http://hress.dafycredit.com:8083/Loginx.aspx?logout=1&logoutSso=1'
    try:
        # 获取网页内容，返回html数据
        response = sessionId.post(url, paras, header2)
        # 通过状态码判断是否获取成功
        if response.status_code == 200:
            # print(response.text)
            resultText = fetch_and_analysis()
            parseText(resultText)
        return None
    except RequestException as e:
        print(e)
        return None


def main():
    '''
    主函数
    '''
    # param = []
    try:
        #     for line in open("D:\\abc.txt"):
        #         param.append(line.strip("\n"))
        #
        #     if len(param) < 2:
        #         raise Exception("读取配置信息异常!")
        #     else:
        #         auto_login(param[0], param[1])
        print(auto_login())
    except Exception as e:
        print(e)
        print("读取配置信息异常!")


if __name__ == '__main__':
    main()
