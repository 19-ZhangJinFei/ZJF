import time
import requests
import csv
from bs4 import BeautifulSoup
import datetime
"""
    crwalURL:http://www.doctor001.com/zhongyaodaquan/list_9_{page}.html
    data: 6040 line total  
    output_file: Doctor001.csv
"""

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
    'Cookie': 'Hm_lvt_f6cf9f1803746c0e930f4a5cc1f7d450=1729750088; HMACCOUNT=B40D837B7C6A920E; Hm_lpvt_f6cf9f1803746c0e930f4a5cc1f7d450=1729751662'}

#获取每个中药的跳转链接
def download_mid_html(url):
    resp=requests.get(url=url, headers=headers)
    page = BeautifulSoup(resp.text,"html.parser") #指定html解释器

    links = page.find_all("a", attrs={"class": "preview"})
    urls = []
    for link in links:
        url = "http://www.doctor001.com"+link["href"]
        print(f"url: {url}")
        urls.append(url)
    resp.close()
    time.sleep(2)
    return urls

#获取每个中药的介绍内容 rawData
def medcine_CN(url):
    resp=requests.get(url=url, headers=headers)
    resp.encoding = "gb2312"
    page = BeautifulSoup(resp.text,"html.parser") #指定html解释器
    tr = page.find("tr").text.strip()
    time.sleep(1)
    resp.close()
    return tr





if __name__=='__main__':
    print(f"==== {datetime.datetime.now()} start excuting doctor001_crawl.py === \n")
    total_urls=[]
    max_links_num = 695
    #获取全部的详细也的链接存储到total_urls
    for page in range(1,max_links_num+1):
        url = f"http://www.doctor001.com/zhongyaodaquan/list_9_{page}.html"
        print(f" time: {datetime.datetime.now()}   url: {url}\n")
        page_urls = download_mid_html(url)
        total_urls.extend(page_urls)
    f = open("doctor001_crawl.csv", mode="w")
    csvwriter = csv.writer(f)
    csvwriter.writerow(["时间","请求url","中药文本内容"])
    print("\n\n == start excuting medcine_CN(url) ==\n\n")
    #请求每个链接.html获取页面中药介绍
    for url in total_urls:
        try:
            print(f" time: {datetime.datetime.now()}   url: {url}\n")
            text = medcine_CN(url)
            csvwriter.writerow([datetime.datetime.now(), url, text])
        except Exception as e:
            #PS：报错的链接是404
            print(f"\n\n=== crawl遇到错误: url: {url} {e}\n\n")
    print(f"==== {datetime.datetime.now()} end === \n")

