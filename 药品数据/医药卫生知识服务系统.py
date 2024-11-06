#coding=utf-8
import os
import requests
import csv
import re
import random
import time
from urllib.error import HTTPError


# 设置代理
UA = ["Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1"
    ]


# 获取url请求
def getJson(medicineID):
    url = 'https://med.ckcest.cn/queryDetails.do'
    this_ua = random.choice(UA)    # 随机选用使用代理
    headers = {
        'User-Agent': this_ua
    }

    # 关键参数
    data = {
        'id': medicineID,
        'nameEn': 'wiki'
    }

    params = {
        'enc': 'utf-8',
    }

    try:
        r = requests.post(url=url, data=data, params=params, headers=headers) # 链接url
        time.sleep(1)  # 避免爬取过快
        r.raise_for_status()    # 判断异常
        r.encoding = r.apparent_encoding  # 转码
        # print(r.json())
        return r.json()  # 返回json文件

    except HTTPError as e:
        # 异常提示
        print('链接异常！！！')
        print('链接异常！！！')
        print('链接异常！！！')
        print(e)
        return ''


# 处理json
def findJson(pageJson, medicineInfo):
    data = pageJson[0]  # 获取列表中的键值对对象
    keysTmp = list(data.keys()) # 转化为列表方便操作
    keysTmp = keysTmp[2:]  # 去除最前面的两个键,id和class


    realKeys = []       # 保存键
    realValues = []     # 保存值

    for key in keysTmp:
        if (key.__eq__("keys")):  # 只取keys之前的做匹配
            break
        key2 = key[:-2]  # 去除最后两个字母Zh 再进行匹配
        valueRaw = data.get(key2)
        if (not valueRaw is None):  # 如果找得到值，证明value存在，加入
            # 此步进行数据清洗，去除p标签，\r\n
            regex = r'</?p>'  # 正则检索 p 标签
            value = re.sub(regex, "", valueRaw.replace('\r', '').replace('\n', ''), re.I)  # sub函数替换p标签为空，re.I不区分大小写

            # 数据加入key-value队列
            realKeys.append(data.get(key))
            realValues.append(value)

    # 保存药品的键值对列表信息
    medicineInfo.append(realKeys)
    medicineInfo.append(realValues)

# 加载ID资源
def readerId(idList):

    path = './'
    file_name = "药品ID.csv"

    # 打开csv文件
    with open(path + file_name, 'r', newline='') as f:
        reader = csv.reader(f)
        headers = next(reader)  # 读取表头
        for row in reader:      # 循环获取表头之后的每一行
            idList.append(row[0])   # 取第一列



# 保存药品信息
def saveMedicine(medicineInfo):

    path = './'
    file_name = medicineInfo[1][0] + ".csv"

    # 写入数据
    with open(path + file_name, 'w+', newline='') as f:     # newline=''保证逐行写入
        writer = csv.writer(f)

        for u in range(len(medicineInfo[0])):
                writer.writerow([medicineInfo[0][u], medicineInfo[1][u]])  # 一次写入一行信息


if __name__ == '__main__':

    print("--------------------爬取开始--------------------")

    idList = []
    readerId(idList)
    for i in range(len(idList)):    # 每一个ID都是页面
        if (i % 10 == 0):  # 提示信息
            print("正在爬取第%d页" % i)

        pageJson = getJson(idList[i])
        # print(pageJson)

        medicineInfo = []           # 药品信息
        findJson(pageJson, medicineInfo)    # 提取药品信息

        saveMedicine(medicineInfo)  # 药品保存到文件


    print("--------------------爬取结束--------------------")
