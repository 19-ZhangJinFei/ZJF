import requests
from lxml import etree
import csv

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:131.0) Gecko/20100101 Firefox/131.0"
}

movie_list = []

for page in range(0, 10):
    url = f'https://movie.douban.com/top250?start={page * 25}&filter='
    response = requests.get(url, headers=headers)
    selector = etree.HTML(response.text)
    movies = selector.xpath('//div[@class="item"]')
    for movie in movies:
        title = movie.xpath('.//span[@class="title"][1]/text()')[0]
        director = movie.xpath('.//div[@class="bd"]/p/text()[1]')[0].split()[1]
        actors = movie.xpath('.//div[@class="bd"]/p/text()[2]')[0].split()[1:]

        # 获取上映年份、国籍、类型信息的文本列表
        info_text = movie.xpath('.//div[@class="bd"]/p/text()[3]')
        if info_text:
            year_country_genre_text = info_text[0].split('/')
            if len(year_country_genre_text) >= 1:
                year = year_country_genre_text[0].strip()
            if len(year_country_genre_text) >= 2:
                country = year_country_genre_text[1].strip()
            if len(year_country_genre_text) >= 3:
                genre = year_country_genre_text[2].strip()
        else:
            year = ""
            country = ""
            genre = ""

        rating = movie.xpath('.//div[@class="star"]/span[@class="rating_num"]/text()')[0]

        movie_list.append({
            '电影中文名': title,
            '导演': director,
            '主演': ' '.join(actors),
            '上映年份': year,
            '国籍': country,
            '类型': genre,
            '评分': rating
        })

with open('2.豆瓣电影Top250.csv', 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=('电影中文名', '电影英文名', '电影详情页链接', '导演', '主演', '上映年份', '国籍', '类型', '评分', '评分人数'))
    writer.writeheader()
    writer.writerows(movie_list)

print('豆瓣电影Top250信息已保存到CSV文件。')