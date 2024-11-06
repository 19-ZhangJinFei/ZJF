import requests
from bs4 import BeautifulSoup
import json
from zipfile import ZipFile, ZIP_DEFLATED

headers_m = {
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
}
url ="https://www.umei.cc/katongdongman/katongtupian/"
resp=requests.get(url,headers=headers_m)
resp.encoding='utf-8'
page = BeautifulSoup(resp.text,'html.parser')
divs =page.find('div',attrs={'class':'item_list infinite_scroll'}).find_all('div',attrs={'class':'title'})
url_1="https://www.umei.cc"
for i in divs:
    hrefs = i.find('a')
    pic_url=url_1+hrefs.get('href')
    pic_page=requests.get(pic_url,headers=headers_m)
    pic_page.encoding='utf-8'
    open_pic=BeautifulSoup(pic_page.text,'html.parser')
    pic_load=open_pic.find('script',attrs={'type':'application/ld+json'})
    json_load=json.loads(pic_load.text)
    down_url=(json_load['images'][0])
    pic_resp=requests.get(down_url)
    pic_name=down_url.split('/')[-1]
    with open('img/'+pic_name,'wb') as f:
        f.write(pic_resp.content)
        f.close()
print('ok')