#1.如何提取单页面的数据
#2.上线程池，多个页面同时提取
import requests
from lxml import etree
def download_one_page(url):
    #拿到页面源代码
    resp = requests.get(url)
    print(resp.json())
if __name__ == '__main__':
    download_one_page("http://www.xinfadi.com.cn/getPriceData.html")