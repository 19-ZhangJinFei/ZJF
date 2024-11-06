#1.拿到主页面的源代码，然后提取到子页面的链接地址，href
#2.通过href拿到子页面的内容，从子页面找到图片的下载
#3.下载图片
import requests
from bs4 import BeautifulSoup
import time

url = "https://www.umei.cc/bizhitupian/weimeibizhi/"
resp = requests.get(url)
resp.encoding = 'utf-8'  # 处理乱码。要跟网站的charset值对应
# print(resp.text)

# 把源代码交给bs
main_page = BeautifulSoup(resp.text, "html.parser")
alist = main_page.find("div", class_="listlbc_cont_l").find_all("a")
# print(alist)

# 目标是拿到a标签里面href的值
for a in alist:
    # print('https://www.umei.cc'+ a.get('href'))    # 直接通过get就可以拿到属性的值
    href = 'https://www.umei.cc' + a.get('href')

    # 拿到子页面的源代码
    child_page_resp = requests.get(href)
    child_page_resp.encoding = 'utf-8'
    child_page_text = child_page_resp.text

    # 从子页面中拿到图片的下载路径
    child_page = BeautifulSoup(child_page_text, "html.parser")
    section = child_page.find("div", class_="img")
    # print(section)
    # break   # 测试用

    # 从section标签里找img
    img = section.find("img")
    # print(img.get("src"))
    # break
    src = img.get("src")

    # 下载图片
    img_resp = requests.get(src)
    # img_resp.content   # 这里拿到的是字节
    img_name = src.split("/")[-1]  # 命名，url中的最后一个/以后的内容，如9e5827678bd12db0999a573254e40d1e.jpg
    with open("img_test/" + img_name, mode="wb") as f:
        f.write(img_resp.content)  # 图片内容写入文件
    print("over", img_name)
    time.sleep(1)  # 给服务器缓冲时间，防止被干掉

f.close()
print("all over")
