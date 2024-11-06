#1.拿到页面源代码
#2.使用bs4进行解析，拿到数据
import csv

from bs4 import BeautifulSoup
import requests
url = "http://www.xinfadi.com.cn/getPriceData.html"
resp = requests.get(url)
print(resp.text)

f = open('菜价.csv',mode='w',encoding='utf-8')
csvwriter = csv.writer(f)

#解析数据
#1.把页面源代码交给BeautifulSoup进行处理，生成bs对象
page = BeautifulSoup(resp.text,"html.parser") #指定html解析器
#2.从bs对象中查找数据
#find (标签，属性=值)
#find_all(标签，属性=值)
#table = page.find("table",class_="hq_table")#class是python的关键字，可以在后面加一个下划线，避免报错
table = page.find("table",attrs={"class":"hq_table"})
#拿到所有数据行
#trs = table.find_all("tr")
#for tr in trs:#每一行
    #tds = tr.find_all("td") #拿到每行中的所有td
    #name = tds[0].text #.text 表示拿到被标签标记的内容
