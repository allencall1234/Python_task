import csv
import difflib
import json
import queue
import threading

import xlrd

import requests
import re
from bs4 import BeautifulSoup

q = queue.Queue(maxsize=1000)
banks = {'中国工商银行': '1',
         '工商银行': '1',
         '中国农业银行': '2',
         '中国银行': '3',
         '中国建设银行': '4',
         '建设银行': '4',
         '交通银行': '8',
         '中国邮政储蓄银行': '9',
         '中信银行': '10',
         '中国光大银行': '11',
         '华夏银行': '12',
         '中国民生银行': '13',
         '广东发展银行': '14',
         '平安银行': '69',
         '招商银行': '16',
         '兴业银行': '17',
         '上海浦东发展银行': '18',
         '渤海银行': '23',
         '其他银行': '75'}

provinces = {
    '北京市': 0,
    '天津市': 2,
    '河北省': 3,
    '山西省': 4,
    '内蒙古自治区': 5,
    '辽宁省': 6,
    '吉林省': 7,
    '黑龙江省': 8,
    '上海市': 9,
    '江苏省': 10,
    '浙江省': 11,
    '安徽省': 12,
    '福建省': 13,
    '江西省': 14,
    '山东省': 15,
    '河南省': 16,
    '湖北省': 17,
    '湖南省': 18,
    '广东省': 19,
    '广西壮族自治区': 20,
    '海南省': 21,
    '四川省': 22,
    '重庆市': 23,
    '贵州省': 24,
    '云南省': 25,
    '西藏自治区': 26,
    '陕西省': 27,
    '甘肃省': 28,
    '青海省': 29,
    '宁夏回族自治区': 30,
    '新疆维吾尔族自治区': 31,
    '台湾': 32,
    '香港': 33,
    '澳门': 34
}

citys = {}


def lianhanghao(item, bankCode, provinceCode, cityCode, keyWord, retry=0):
    '''
    url = 'http://www.lianhanghao.com/index.php?bank=4&province=19&city=232&key=西丽支行'
    :param bankCode:
    :param provinceCode:
    :param cityCode:
    :param keyWord:
    :return:
    '''

    url = 'http://www.lianhanghao.com/index.php?bank=%s&province=%s&city=%s&key=%s' % (
        bankCode, provinceCode, cityCode, keyWord)
    # url = 'http://www.lianhanghao.com/index.php?bank=4&province=19&city=232&key=西丽支行'
    # url = 'http://www.lianhanghao.com/index.php?bank=4&province=15&city=180&key=博兴县'
    print("url = " + url)
    try:
        response = requests.get(url)
        soups = BeautifulSoup(bytes.decode(response.content), "html.parser")
        # content = bytes.decode(response.content)

        result = soups.select('tbody tr')
        if len(result) > 1:
            srcAddr = str(item[4])
            # srcAddr = '中国建设银行股份有限公司博兴支行纯梁分理处'
            maxSimilar = 0
            index = 0
            for res in result:
                addr1 = res.select('td')[1].text
                similar = get_equal_rate(srcAddr, addr1)
                print("相似度：" + addr1 + "," + str(similar))
                if similar > maxSimilar:
                    maxSimilar = similar
                    dest = res.select('td')
                    index = result.index(res) + 1

            resultID = dest[0].text
            resultAddress1 = dest[1].text
            resultAddress2 = re.sub(r'^.*%', '', dest[3].text)
            print("resultId = " + resultID + ",add1 = " + resultAddress1 + ",add2 = " + resultAddress2)

            item.append(resultID)
            item.append(resultAddress1)
            item.append(resultAddress2)
            item.append(str(len(result)) + "选" + str(index) + ",匹配度" + str(maxSimilar))
            write_csv_headers('bankresult.csv', item)
        elif len(result) == 1:
            dest = result[0].select('td')
            resultID = dest[0].text
            resultAddress1 = dest[1].text
            resultAddress2 = re.sub(r'^.*%', '', dest[3].text)
            print("resultId = " + resultID + ",add1 = " + resultAddress1 + ",add2 = " + resultAddress2)
            item.append(resultID)
            item.append(resultAddress1)
            item.append(resultAddress2)
            write_csv_headers('bankresult.csv', item)
        else:
            if len(keyWord) >= 3 and retry < 3:
                print("改变关键字重试")
                lianhanghao(item, bankCode, provinceCode, cityCode, keyWord[:-1], retry + 1)
            elif len(keyWord) >= 2 and retry < 3:
                print("更换关键字重试")
                lianhanghao(item, bankCode, provinceCode, cityCode, str(item[4])[-3:], retry + 1)
            else:
                item.append("")
                item.append("")
                item.append("")
                item.append("找不到有效的联行号")
                print("找不到有效的联行号")
                write_csv_headers('bankresult.csv', item)
    except Exception as e:
        print(e)


def get_equal_rate(str1, str2):
    '''
    字符串相似度检测
    :param str1:
    :param str2:
    :return:
    '''
    str1 = re.sub(r'^.*银行', '', str1)
    str1 = re.sub(r'^.*有限公司', '', str1)

    str2 = re.sub(r'^.*银行', '', str2)
    str2 = re.sub(r'^.*有限公司', '', str2)
    return difflib.SequenceMatcher(None, str1, str2).quick_ratio()


def write_csv_headers(path, headers):
    '''
    写入表头
    '''
    with open(path, 'a', encoding='gb18030', newline='') as f:
        f_csv = csv.DictWriter(f, headers)
        f_csv.writeheader()


def read_csv_rows(path):
    '''
    读取数据
    '''
    with open(path, 'r') as f:
        reader = csv.reader(f)
        for item in reader:
            q.put(str(item[0]))


def read_exel_rows(path):
    workbook = xlrd.open_workbook(path)
    sheet = workbook.sheet_by_index(0)  # sheet索引从0开始
    for i in range(sheet.nrows):
        q.put(sheet.row_values(i))


def core_bizz(item):
    try:
        bankStr = re.sub(r'银行.*$', "", item[4]) + "银行"
        if banks.get(bankStr) is None:
            bankCode = '75'
        else:
            bankCode = banks.get(bankStr)

        print(bankStr + ":" + bankCode)

        province = str(item[6])
        provinceCode = str(provinces.get(province))
        cityUrl = 'http://www.lianhanghao.com/index.php/Index/Ajax?id=' + provinceCode
        if citys.get(provinceCode) is None:
            response = requests.get(cityUrl)
            content = bytes.decode(response.content)
            citys[provinceCode] = content
            cityDic = content
        else:
            # print("response : " + citys.get(provinceCode))
            cityDic = citys.get(provinceCode)

        if cityDic.startswith(u'\ufeff'):
            cityDic = cityDic.encode('utf8')[3:].decode('utf8')
        dics = json.loads(cityDic)
        # print(dics)

        city = str(item[7])
        for val in dics:
            # print(str(val))
            if val['name'] == city:
                cityCode = val['id']
                break

        print("cityCode = " + cityCode)

        keyWord = str(item[8])
        lianhanghao(item, bankCode, provinceCode, cityCode, keyWord)

    except Exception as e:
        print(e)


def start():
    while not q.empty():
        item = q.get()
        print(str(item))
        core_bizz(item)


if __name__ == '__main__':
    print("开始查询")
    # lianhanghao(4, 19, 232, '西丽支行')
    read_exel_rows('bank.xlsx')
    print('size = ' + str(q.qsize()))
    q.get()

    for i in range(20):
        threading.Thread(target=start()).start()
