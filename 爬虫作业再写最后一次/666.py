import requests
import csv
from bs4 import BeautifulSoup

def parse_single_html(html):
    soup = BeautifulSoup(html, "html.parser")
    article_items = (soup.find("div", class_="article")
                    .find("ol", class_="grid_view")
                    .find_all("div", class_="item")
                     )
    datas = []
    for article_item in article_items:
        rank = article_item.find("div", class_="pic").find("em").get_text()
        title = article_item.find("div", class_="info") \
           .find("div", class_="hd") \
           .find("span", class_="title").get_text()
        stars = (
            article_item.find("div", class_="info")
           .find("div", class_="bd")
           .find("div", class_="star")
           .find_all("span")
        )
        rating_star = stars[0]["class"][0]
        rating_num = stars[1].get_text()
        comments = stars[3].get_text()
        datas.append({
            "rank": rank,
            "title": title,
            "stars": rating_star,
            "rating_star": rating_star.replace("rating", "").replace("-t", ""),
            "rating_num": rating_num,
            "comments": comments.replace("人评价", "")
        })
    return datas

root_url = "https://movie.douban.com/top250"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
}

htmls = []
sum = 0
for i in range(0, 10):
    page = f'?start={sum}&filter='
    url = root_url + page
    response = requests.get(url, headers=headers)
    if response.status_code!= 200:
        print(f"请求网页 {url} 时出现错误，状态码: {response.status_code}")
        continue
    htmls.append(response.text)
    sum += 25

all_datas = []
for html in htmls:
    all_datas.extend(parse_single_html(html))

print("豆瓣电影TOP250.xlsx")

with open('1.bs4Top250.csv', 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=('rank', 'title', 'stars', 'rating_star', 'rating_num', 'comments'))
    writer.writeheader()
    writer.writerows(all_datas)

print('豆瓣电影Top250信息已保存到CSV文件。')