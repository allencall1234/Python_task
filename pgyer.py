import csv
import json
import threading
import time
import queue
import requests
from bs4 import BeautifulSoup

headers1 = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    'cookie': '_ga=GA1.2.2106573312.1501050518; MEIQIA_EXTRA_TRACK_ID=0xLHlVKet28BbcHRHaMyiAZenyj; _gid=GA1.2.150407911.1524650473; PHPSESSID=dkm2cummu8cpcbotqb3ct3nag5; pgyx2_session=w0Bv9Ca1FSyPzwvwp1PyMNAqDiVbx4hdQCyxnPq9g4bn2OWIvlmdPnlm0pc4B%2BpHFTxESi73ygcnQZAbTlDSCb5sCgYKXoh8xwdejIl0ywmQYhvHk7bMwPXx1cNQPTXdAJZPpVde%2BitmEAEfRwYLcn0kaiVB2wEsqjSp6X9MhXbfsUb3H8G1kcwpWpgqm5ENVzixlaoKM4BlwVE0x7EfYcyXQZPXCGimyziXJrAfE5E9VraYn1gtd23mOcbR%2FDwhglXe79I7V1J2eSXrqsX805U%2FMAf5BKoVznH5eyMf45%2Bc5ziV6%2FD%2BrIryt7OYYu8XCziLAXzDLNz1A%2B73C6goTBZv0W7wOTSnZ4%2B241oRcEmB9QDmPG0j31gQPDVSSpd0W0US%2Ftruxt%2FbyIFff%2FY5i86I9qqLwGWlif%2F9FjAMwKafVlJoyYy8QseYe4tdjzYa5GCJ%2Fc57iV9UeF4egGKcQOQH4UJJ7SN%2BOsObtgG9GxoBUaORkaP56hg3a4%2BBz4cumvqu22zMwusxndMZ3q2IImoH%2BilDeYa41KKaA%2FwGHaxqF7jQ6Z9YCbFy7CPbJOmj%2FbF5LKB%2FwnXUq9lyY32SObGmXwzMxnSYj9F%2F%2FD5eLeQG%2BCeyYLMaMYo50qzIIzgnZ4%2BQk6FzqDpsdV4RneKS48zxeEfpL1JqSWmi%2Bkc4rwAkKNoECzMB%2FXHyAHf1vmWp0l5JqPVcoQKaTE%2FyDtNUcw7mGmfWhisz3iGibYbyZegrxTp7kQ5FK5Qftfr2py6E36n6dw8amsZJ9tnNXrs6kwv3w5INKuppqTu8v611fXdtDltzAB4fOKofAHopI5GJ41FD%2B4WTkeg5NwYBohla6SwdmtpHa3rrMytF8w7ZU2MYb%2BZUX1TscN0HsdWrq3TpxvKol9QVAQYbY1ftCuKppbYX%2By4lqiyGVCpcqxxo%2FEI%3D; _gat=1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
}
BASE_URL = "https://www.pgyer.com/"
q = queue.Queue(maxsize=10000)
filename = 'Z.csv'
savePath = "SaveZ.csv"
headers = ['website']
flag = True


def urlTest(url):
    try:
        response = requests.get(url, headers=headers1)
        soups = BeautifulSoup(response.text, "html.parser")  # soup转化
        # 获取小说题目
        txt = soups.select('title')[0].text
        if not txt.startswith("哎呦"):
            rows = []
            rows.append(url)
            rows.append(txt)
            write_csv_headers(savePath, rows)
    except Exception as e:
        print("")

def consumer():  # 消费者
    time.sleep(5)
    try:
        while True:
            url = q.get()
            print("测试地址："+url)
            urlTest(url)
    except Exception as e:
        print(e)


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


def read_csv_rows(path):
    '''
    读取数据
    '''
    with open(path, 'r') as f:
        reader = csv.reader(f)
        for item in reader:
            q.put(str(item[0]))

def main():
    '''
    主函数
    '''
    read_csv_rows(filename)
    # threading.Thread(target=read_csv_rows(filename)).start()
    for i in range(10):
        threading.Thread(target=consumer()).start()

if __name__ == '__main__':
    print("start!!!")
    main()
