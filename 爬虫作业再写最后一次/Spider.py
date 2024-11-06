import requests
from bs4 import BeautifulSoup
import csv
import pymysql
import random


def crawl_movie(url1):
    headers_list = [
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0'},
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/88.0.4324.190 Safari/537.36'},
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/88.0.4324.190 Edge/88.0.705.81'},
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Trident/7.0; rv:11.0) like Gecko'}
    ]

    resp1 = requests.get(url1, headers=random.choice(headers_list))
    soup1 = BeautifulSoup(resp1.text, 'html.parser')
    ol = soup1.find("ol", class_="grid_view")

    # 添加检查 ol 是否为 None 的逻辑
    if ol is None:
        print(f"无法找到电影列表，URL: {url1}")
        return []

    movie_list_1 = []

    for i in ol.find_all("li"):
        url2 = i.find('a')['href']
        resp2 = requests.get(url2, headers=random.choice(headers_list))
        soup2 = BeautifulSoup(resp2.text, 'html.parser')

        top = soup2.find("span", class_="top250-no").text if soup2.find("span", class_="top250-no") else None

        h1 = soup2.find("h1")
        title = h1.find("span").text.split()[0] if h1 and h1.find("span") else None

        year = h1.find("span", class_="year").get_text()[1:-1] if h1 and h1.find("span", class_="year") else None
        area = soup2.find("div", id="info").find('span', class_='pl',
                                                 string='制片国家/地区:').next_sibling.strip() if soup2.find("div",
                                                                                                             id="info") else None
        language = soup2.find("div", id="info").find('span', class_='pl',
                                                     string='语言:').next_sibling.strip() if soup2.find("div",
                                                                                                        id="info") else None
        runtime = soup2.find("span", property="v:runtime").get_text() if soup2.find("span",
                                                                                    property="v:runtime") else None
        score = soup2.find("strong", class_="ll rating_num").get_text() if soup2.find("strong",
                                                                                      class_="ll rating_num") else None
        comment = soup2.find("span", property="v:votes").get_text() + "人" if soup2.find("span",
                                                                                         property="v:votes") else None

        if soup2.find("span", class_="all hidden"):
            summary = "".join(soup2.find("span", class_="all hidden").text.split())
        else:
            summary = "".join(soup2.find("span", property="v:summary").text.split()) if soup2.find("span",
                                                                                                   property="v:summary") else None

        movie_info = {
            'top': top if top else 'NULL',
            'title': title if title else 'NULL',
            'year': year if year else 'NULL',
            'area': area if area else 'NULL',
            'language': language if language else 'NULL',
            'runtime': runtime if runtime else 'NULL',
            'score': score if score else 'NULL',
            'comment': comment if comment else 'NULL',
            'summary': summary if summary else 'NULL'
        }
        movie_list_1.append(movie_info)

    return movie_list_1


def save_to_csv(movie_list_2):
    with open('movie_info.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['top', 'title', 'year', 'area', 'language', 'runtime', 'score', 'comment', 'summary']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for movie in movie_list_2:
            writer.writerow(movie)
    print("CSV 保存成功！！！")


def save_to_mysql(movie_info_list_3):
    connection = pymysql.connect(host='localhost', user='root', password='Zsfenfang.123', database='movies')
    cursor = connection.cursor()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS movie_info (
        top VARCHAR(20),
        title VARCHAR(25),
        year INT,
        area VARCHAR(30),
        language VARCHAR(50),
        runtime VARCHAR(50),
        score FLOAT,
        comment VARCHAR(20),
        summary VARCHAR(1300)
    )
    """
    cursor.execute(create_table_query)

    for movie_info in movie_info_list_3:
        insert_query = """
        INSERT INTO movie_info (top, title, year, area, language, runtime, score, comment, summary)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (movie_info['top'], movie_info['title'], movie_info['year'], movie_info['area'],
                  movie_info['language'], movie_info['runtime'], movie_info['score'], movie_info['comment'],
                  movie_info['summary'])
        cursor.execute(insert_query, values)

    connection.commit()
    cursor.close()
    connection.close()
    print("MySQL 保存成功！！！")


if __name__ == '__main__':
    all_movies = []
    for i in range(0, 251, 25):
        url = f'https://movie.douban.com/top250?start={i}&filter='
        movie_list = crawl_movie(url)
        all_movies.extend(movie_list)  # 合并所有电影信息到一个列表

    save_to_csv(all_movies)
    save_to_mysql(all_movies)
