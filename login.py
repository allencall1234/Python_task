# -*- coding: utf-8 -*-
import requests
from requests.exceptions import RequestException

MaxRetryTimes = 5


def auto_login(userName, pwd, retryTimes):
    '''
    获取网页html内容并返回
    '''
    paras = {
        'opr': "pwdLogin",
        'userName': userName,
        'pwd': pwd,
        'rememberPwd': 0
    }
    url = 'http://10.10.1.248/ac_portal/login.php'
    try:
        # 获取网页内容，返回html数据
        response = requests.post(url, paras)
        # 通过状态码判断是否获取成功
        print("login result " + str(response.status_code))
        if response.status_code == 200:
            return response.text
        else:
            if retryTimes > 0:
                auto_login(userName, pwd, retryTimes - 1)
            return None

    except RequestException as e:
        return None


def main():
    '''
    主函数
    '''
    param = []
    try:
        for line in open("/Users/macadmin/Desktop/account"):
            param.append(line.strip("\n"))

        if len(param) < 2:
            raise Exception("读取配置信息异常!")
        else:
            print(param)
            auto_login(param[0], param[1], MaxRetryTimes)
    except:
        print("读取配置信息异常!")


if __name__ == '__main__':
    main()
