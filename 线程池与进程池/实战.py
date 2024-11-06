# 1.如何提取单页面的数据
# 2.上线程池，多个页面同时提取
import requests
from lxml import etree
import csv
from concurrent.futures import ThreadPoolExecutor

f = open("data.csv", mode="w", encoding="utf-8")
csvwriter = csv.writer(f)


def download_one_page(url):
    # 拿到页面源代码
    resp = requests.get(url)
    #print(resp.text)
    html = etree.HTML(resp.text)
    table = html.xpath("/html/body/div[2]/div/div/div/div[4]/div[1]/div/table/tbody")[0]
    # 去掉表头数据的两种方法
    # trs = table.xpath("./tr")[1:]
    trs = table.xpath("./tr")
    # 拿到每个tr
    for tr in trs:
        txt = tr.xpath("./td/text()")
        # 对数据做简单的处理：\\ / 去掉
        txt = (item.replace("\\", "").replace("/", "") for item in txt)
        # 把数据存放在文件中
        csvwriter.writerow(txt)

        print(list(txt))
    print(len(trs))
    print(url, "提取完毕")


if __name__ == '__main__':
    # for i in range(1,22843): #效率极其低下
    # download_one_page(f"http://www.xinfadi.com.cn/priceDetail.html")
    # 创建线程池
    with ThreadPoolExecutor(50) as t:
        for i in range(1, 200):
            # 把下载任务提交给线程池
            t.submit(download_one_page, f"http://www.xinfadi.com.cn/priceDetail.html")
    print("全部下载完毕")