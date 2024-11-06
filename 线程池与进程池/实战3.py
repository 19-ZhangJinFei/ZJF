import requests
from concurrent.futures import ThreadPoolExecutor
import time
import csv


def get_data(page):
    url = 'http://www.xinfadi.com.cn/getPriceData.html'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0'
    }
    data = {
        'limit': 20,
        'current': page,
        'pubDateStartTime': '',
        'pubDateEndTime': '',
        'prodPcatid': '',
        'prodCatid': '',
        'prodName': ''
    }

    f = open('data.csv', mode='a', newline='', encoding='utf-8-sig')
    csvwriter = csv.writer(f)
    resp = requests.post(url, headers=headers, data=data)
    resp.encoding = 'utf-8'
    lists = resp.json()['list']
    for item in lists:
        prodName = item['prodName']
        prodCat = item['prodCat']
        pubDate = item['pubDate']
        avgPrice = item['avgPrice']
        highPrice = item['highPrice']
        lowPrice = item['lowPrice']
        csvwriter.writerow([prodName, prodCat, highPrice, lowPrice, avgPrice, pubDate])
        print('完成')
    resp.close()
    f.close()


if __name__ == '__main__':
    with ThreadPoolExecutor(80) as t:
        for i in range(1, 180):
            t.submit(get_data, i)

            time.sleep(0.1)
        print('over!')
        t.shutdown()