import requests
import re
from bs4 import BeautifulSoup


def main():
    '''
    主函数
    :return:
    '''
    url = 'http://app.mi.com/details?id=com.giveu.shoppingmall&ref=search'
    try:
        response = requests.get(url)
        content = bytes.decode(response.content)
        print(content)
        p = re.compile(r'\d+\.\d+\.\d+')
        print(p.findall(content)[-1])
    except Exception as e:
        print(e)


def yingyongbaoResult():
    '''
    查询应用宝的app版本号
    :return: 当前应用宝上架的最新版本号
    '''
    url = 'https://sj.qq.com/myapp/detail.htm?apkName=com.giveu.shoppingmall'
    try:
        response = requests.get(url)
        content = bytes.decode(response.content)
        p = re.compile(r'\d+\.\d+\.\d+')
        return p.findall(content)[-1]
    except Exception as e:
        print(e)


def xiaomiResult():
    '''
    查询小米市场的app版本号
    :return: 当前上架的app版本号
    '''
    url = 'http://app.mi.com/details?id=com.giveu.shoppingmall&ref=search'
    try:
        response = requests.get(url)
        content = bytes.decode(response.content)
        p = re.compile(r'\d+\.\d+\.\d+')
        return p.findall(content)[-1]
    except Exception as e:
        print(e)


def huaweiResult():
    '''
    查询华为市场的app版本号
    :return: 当前上架的app版本号
    '''
    url = 'http://app.hicloud.com/app/C100057057'
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
    try:
        response = requests.get(url, headers=header)
        soups = BeautifulSoup(bytes.decode(response.content), "html.parser")
        title = soups.select('title')[0]
        p = re.compile(r'\d+\.\d+\.\d+')
        return p.findall(str(title))[-1]
    except Exception as e:
        print(e)


def app360Result():
    '''
    查询360市场的app版本号
    :return: 当前上架的app版本号
    '''
    url = 'http://zhushou.360.cn/detail/index/soft_id/3876314?recrefer=SE_D_即有生活'
    try:
        response = requests.get(url)
        content = bytes.decode(response.content)
        p = re.compile(r'\d+\.\d+\.\d+')
        return p.findall(content)[0]
    except Exception as e:
        print(e)


def vivoResult():
    '''
    查询vivo和oppo市场的app版本号
    :return: 当前上架的app版本号
    '''
    url = 'http://www.pc6.com/az/611334.html'
    try:
        response = requests.get(url)
        soups = BeautifulSoup(response.text, "html.parser")
        title = soups.select('title')[0]
        p = re.compile(r'\d+\.\d+\.\d+')
        return p.findall(str(title))[-1]
    except Exception as e:
        print(e)


if __name__ == '__main__':
    print("开始查询")
    print("小米市场最新版本：" + xiaomiResult())
    print("应用宝最新版本：" + yingyongbaoResult())
    print("华为市场最新版本：" + huaweiResult())
    print("360助手最新版本：" + app360Result())
    print("vivo市场最新版本：" + vivoResult())
