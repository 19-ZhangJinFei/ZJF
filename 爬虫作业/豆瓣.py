import requests
import re
import csv

def get_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        'Referer': 'https://movie.douban.com/',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
    }
    response = requests.get(url, headers=headers, verify=False)
    response.encoding = 'utf-8'  # 指定字符集
    response.raise_for_status()
    response.encoding = response.apparent_encoding
    return response.text





def get_movie_list(html):
    if html is None:  # 检查 html 是否为 None
        return []
    pattern = re.compile(r'<div class="pic".*?em class="">(.*?)</em>.*?<a href="(.*?)">.*?</a>', re.S)
    movie_list = pattern.findall(html)
    return movie_list


def get_content(movie_url):
    html = get_page(movie_url)
    if html is None:  # 检查 html 是否为 None
        return
    # 获取片名
    pattern = re.compile(r'<span property="v:itemreviewed">(.*?)</span>', re.S)
    name = pattern.findall(html)
    print(name)

    # 导演
    pattern = re.compile(r'<a.*?rel="v:directedBy">(.*?)</a>', re.S)
    director = pattern.findall(html)
    print(director)

    # 编剧
    pattern = re.compile(r"<span ><span class='pl'>编剧</span>: <span class='attrs'>(.*?)</span></span><br/>", re.S)
    author = pattern.findall(html)
    if author:
        pattern = re.compile(r'<a href=.*?>(.*?)</a>', re.S)
        author = pattern.findall(author[0])
    print(author)

    # 主演
    pattern = re.compile(r'<a.*?rel="v:starring">(.*?)</a>', re.S)
    actor = pattern.findall(html)
    print(actor)

    # 类型
    pattern = re.compile(r'<span property="v:genre">(.*?)</span>', re.S)
    type = pattern.findall(html)
    print(type)

    # 制片国家/地区
    pattern = re.compile(r'<span class="pl">制片国家/地区:</span>(.*?)<br/>', re.S)
    area = pattern.findall(html)
    print(area)

    # 语言
    pattern = re.compile(r'<span class="pl">语言:</span>(.*?)<br/>', re.S)
    language = pattern.findall(html)
    print(language)

    # 上映时间
    pattern = re.compile(r'<span property="v:initialReleaseDate" content=.*?>(.*?)</span>', re.S)
    time = pattern.findall(html)
    print(time)

    # 片长
    pattern = re.compile(r'<span property="v:runtime" content=.*?>(.*?)</span>', re.S)
    runtime = pattern.findall(html)
    print(runtime)

    # 又名
    pattern = re.compile(r'<span class="pl">又名:</span>(.*?)<br/>', re.S)
    other_name = pattern.findall(html)
    print(other_name)

    # 评分
    pattern = re.compile(r'<strong class="ll rating_num" property="v:average">(.*?)</strong>', re.S)
    score = pattern.findall(html)
    print(score)

    # 简介
    pattern = re.compile(r'<span property="v:summary".*?>(.*?)</span>', re.S)
    introduce = pattern.findall(html)

    if introduce:
        introduce = introduce[0].strip().replace('\n', '').replace('\t', '').replace(
            '                                    <br />                                　　', '')
        print(introduce)

    with open('666.csv', 'a', encoding='utf-8', newline="") as f:
        f.write(movie_url + '\t' + str(name) + '\t' + str(director) + '\t' + str(author) + '\t' +
                str(actor) + '\t' + str(type) + '\t' + str(area) + '\t' + str(language) + '\t' +
                str(time) + '\t' + str(runtime) + '\t' + str(other_name) + '\t' + str(score) + '\t' +
                introduce + '\n')


if __name__ == '__main__':
    for i in range(10):
        url = 'https://movie.douban.com/top250?start=' + str(i * 25)
        print(url)

        html = get_page(url)

        movie_list = get_movie_list(html)
        print(movie_list)

        for movie in movie_list:
            get_content(movie[1])
