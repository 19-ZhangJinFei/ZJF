#爬取微博话题杨利伟太空一日所有博文内容
#发布者、发布时间、微博内容、形式（文字、图片、视频）、转发数、评论数、点赞数
import requests
from bs4 import BeautifulSoup
import re
import time


headers = {
     'cookie': "SCF=AtEYelUxGJ6UV0m1lGjujWWaJPhn51cBhUnKKZiWU5BwvRGlFL7xFEgOFgAuGrVOWS-gQX-XvYfrtfArqlFPZhU.; SUB=_2A25KHw3cDeRhGeFL7lcR9C_LyzWIHXVpVQ8UrDV8PUNbmtANLUyhkW9Nfeb6JlxOHBzQC8F9mRaUYH-p49nAVPRl; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5MZ82jJa_-KCP4T8kkaoYi5NHD95QNSK-fehBpS054Ws4DqcjMi--NiK.Xi-2Ri--ciKnRi-zNS0-fSK5XeKM71Btt; PC_TOKEN=11934519ec; _s_tentry=passport.weibo.com; Apache=8647067850704.814.1729854905454; SINAGLOBAL=8647067850704.814.1729854905454; ULV=1729854905454:1:1:1:8647067850704.814.1729854905454:",
     'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
     'Referer':'https://s.weibo.com/weibo?q=%E6%9D%A8%E5%88%A9%E4%BC%9F%E7%9A%84%E5%A4%AA%E7%A9%BA%E4%B8%80%E6%97%A5',
     'x-requested-with': 'XMLHttpRequest'
 }

url = 'https://s.weibo.com/weibo?q=%E6%9D%A8%E5%88%A9%E4%BC%9F%E7%9A%84%E5%A4%AA%E7%A9%BA%E4%B8%80%E6%97%A5'
resp = requests.get(url,headers=headers)
#print(resp.text)
page = BeautifulSoup(resp.text,"html.parser") #指定html解析器
print(page)
