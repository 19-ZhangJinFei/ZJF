import requests

url ="https://movie.douban.com/j/chart/top_list"
#如果url参数名称过长，可以使用另外一种方法重新封装参数
#重新封装参数
param = {
            "type":"24",
            "interval_id":"100:90",
            "action":"",
            "start":"0",
            "limit":"20",
}

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0"
}
resp = requests.get(url=url,params=param,headers=headers)
print(resp.text)
#倘若没有信息，则证明自己被反爬虫了