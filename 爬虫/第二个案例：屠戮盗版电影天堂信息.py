#1.定位到2024必看片
#2.从2024必看片中提取到子页面的链接地址
#3.请求子页面的链接地址，拿到我们想要的下载地址...

import requests
import re

domain = "https://www.dytt89.com/"
resp = requests.get(domain,verify=False)
resp.encoding = 'gb2312'   #指定字符集
#print(resp.text)
#拿到ul里面的li
obj1 = re.compile(r"2024必看热片.*?<ul>(?P<ul>.*?)</ul>", re.S)
obj2 = re.compile(r"<a href='(?P<href>.*?)'", re.S)
obj3 = re.compile(r'<li>.*?《(?P<movie>.*?)》.*?</li>', re.S)
result1 = obj1.finditer(resp.text)
child_href_list = []
for it in result1:
    ul = it.group('ul')
	#print(ul)
    #提取子页面链接
    result2 = obj2.finditer(ul)
    for itt in result2:
        #拼接子页面的url地址:域名+子页面地址
        child_href = domain + itt.group('href').strip("/")
        child_href_list.append(child_href)#把子页面链接保存起来
        print(child_href)
#提取子页面内容
for href in child_href_list:
    child_resp = requests.get(href,verify=False)
    child_resp.encoding = 'gb2312'
    #print(child_href_list)
    result3 = obj3.search(child_resp.text)
    if result3:
        print(result3.group('movie'))
        #print(result3.group('download'))
        # break   #测试用
    else:
        print('没有找到电影名称或者下载链接')
