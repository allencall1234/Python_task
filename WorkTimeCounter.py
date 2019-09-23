import csv
import queue
import time
from datetime import datetime

weeks = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
q = queue.Queue(maxsize=1000)
filename = 'worktime.csv'
time_reg = '2018/7'


def read_csv_rows(path):
    '''
    读取数据
    '''
    print("path = " + path)
    with open(path, 'r') as f:
        reader = csv.reader(f)
        for item in reader:
            if str(item[4]).startswith(time_reg):
                q.put(item)


def timeToMin(formatTime):
    try:
        arr = formatTime.split(':')
        return int(arr[0]) * 60 + int(arr[1])
    except Exception as e:
        print(e)
    return 0


def calculateTime(currDate, time1, time2):
    currWeek = 0
    try:
        currWeek = datetime.strptime(currDate, '%Y/%m/%d').weekday()
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
        print('  加班' + str(result // 60) + '小时' + str(result % 60) + '分')
        return result


def main():
    '''
    主函数
    '''
    minTimes = 0
    try:
        read_csv_rows(filename)

        last = q.get()
        while not q.empty():
            curr = q.get()

            if str(curr[4]) != str(last[4]):
                last = curr
            else:
                print(last[4] + '号打卡', end='')
                minTimes = minTimes + calculateTime(str(last[4]), str(last[5]).split(' ')[1],
                                                    str(curr[5]).split(' ')[1])
                if not q.empty():
                    last = q.get()

        print('加班打卡时间：' + str(minTimes // 60) + '小时' + str(minTimes % 60) + '分')
        print("break")
    except:
        print("读取配置信息异常!")


if __name__ == '__main__':
    main()
