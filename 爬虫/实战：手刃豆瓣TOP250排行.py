#拿到页面源代码,requests
#通过re来提取想要的有效信息    re
import requests
import re
import csv
pege = input("请输入你要开始爬取的排名：")
url = "https://movie.douban.com/top250?start={page}&filter="\

headers = {
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0"
}
resp = requests.get(url,headers = headers)
page_content = resp.text
#解析数据
obj = re.compile(r'<li>.*?<div class="item">.*?<span class="title">(?P<name>.*?)'
                 r'</span>.*?<p class="">.*?<br>(?P<year>.*?)&nbsp.*?<span'
                 r'.*?<span class="rating_num" property="v:average">(?P<score>.*?)</span>'
                 r'.*?<span>(?P<sum>.*?)人评价</span>',re.S)
#开始匹配
result = obj.finditer(page_content)
f = open("data.csv",mode="w",encoding="utf-8",newline="")
csvwriter = csv.writer(f)
for it in result:
    #print(it.group('name'))
    #print(it.group('score'))
    #print(it.group("num"))
    #print(it.group('year').strip())
    dic = it.groupdict()
    dic['year'] = dic['year'].strip()
    csvwriter.writerow(dic.values())
f.close()
print("over!")
#思路：确定起始定位和结束定位
#obj = re.compile(r"",re.S)
#print(resp.text)