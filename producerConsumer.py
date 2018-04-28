import csv
import json
import threading
import time
import queue
import requests

digits = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
          'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
          'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', ]
BASE_URL = "https://www.pgyer.com/"
q = queue.Queue(maxsize=1000)
filename = 'zlt.csv'
headers = ['website']
flag = True


def urlTest(name):
    try:
        response = requests.post(BASE_URL + name)
        data = json.loads(str(response.text))
        if data['code'] == '1':
            url = []
            url.append(BASE_URL + name)
            write_csv_headers(filename, url)
    except Exception as e:
        print("")


def producer():  # 生产者
    num1 = 8
    num2 = 33
    num3 = 44
    num4 = 25
    while num1 < 47 and num2 < 52 and num3 < 52 and num4 < 52:
        q.put(digits[num1] + digits[num2] + digits[num3] + digits[num4])
        num4 = num4 + 1
        if num4 >= 52:
            num4 = 0
            num3 = num3 + 1
            if num3 >= 52:
                num3 = 0
                num2 = num2 + 1
                if num2 >= 52:
                    num2 = 0
                    num1 = num1 + 1


def consumer():  # 消费者
    while True:
        url = q.get()
        print("测试地址:%s%s" % (BASE_URL, url))
        urlTest(url)


def write_csv_headers(path, headers):
    '''
    写入表头
    '''
    with open(path, 'a', encoding='gb18030', newline='') as f:
        f_csv = csv.DictWriter(f, headers)
        f_csv.writeheader()


def write_csv_rows(path, headers, rows):
    '''
    写入行
    '''
    with open(path, 'a', encoding='gb18030', newline='') as f:
        f_csv = csv.DictWriter(f, headers)
        f_csv.writerows(rows)


def main():
    '''
    主函数
    '''
    write_csv_headers(filename, headers)
    threading.Thread(target=producer).start()
    for i in range(30):
        threading.Thread(target=consumer).start()


if __name__ == '__main__':
    print("start!!!")
    main()
