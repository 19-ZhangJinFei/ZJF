import csv
import requests
from xml import etree

base_url = 'https://search.cnki.com.cn/api/search/listresult'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    'Cookie': 'SID_search=017049; UM_distinctid=192dc532ceba01-041feedc8a4801-26011951-144000-192dc532cecffc; KEYWORD=%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0; CNZZDATA1257838124=556370863-1730273291-%7C1730276039',
}


def get_page_text(url, headers, search_word, page_num):
    data = {
        'searchType': 'MulityTermsSearch',
        'ArticleType': '0',
        'Page': str(page_num),
        'KeyWd': search_word,
        'Order': '1',
        # 其他参数...
    }
    response = requests.post(url=url, headers=headers, data=data)
    return response.text


def list_to_str(my_list):
    return "".join(my_list)


def get_abstract(url):
    response = requests.get(url=url, headers=headers)
    page_text = response.text
    tree = etree.HTML(page_text)
    abstract = tree.xpath('//div[@class="xx_font"]//text()')
    return list_to_str(abstract)


def parse_page_text(page_text):
    tree = etree.HTML(page_text)
    item_list = tree.xpath('//div[@class="list-item"]')
    page_info = []
    for item in item_list:
        title = list_to_str(item.xpath('./p[@class="tit clearfix"]/a[@class="left"]/@title'))
        link = 'https:' + list_to_str(item.xpath('./p[@class="tit clearfix"]/a[@class="left"]/@href'))
        author = list_to_str(item.xpath('./p[@class="source"]/span[1]/@title'))
        date = list_to_str(item.xpath('./p[@class="source"]/span[last()-1]/text()'))
        keywords = list_to_str(item.xpath('./div[@class="info"]/p[@class="info_left left"]/a[1]/@data-key'))
        abstract = get_abstract(url=link)
        paper_source = list_to_str(item.xpath('./p[@class="source"]/span[last()-2]/text()'))
        paper_type = list_to_str(item.xpath('./p[@class="source"]/span[last()]/text()'))
        download = list_to_str(
            item.xpath('./div[@class="info"]/p[@class="info_right right"]/span[@class="time1"]/text()'))
        refer = list_to_str(item.xpath('./div[@class="info"]/p[@class="info_right right"]/span[@class="time2"]/text()'))

        item_info = [title.strip(), author.strip(), paper_source.strip(), paper_type.strip(),
                     date.strip(), abstract.strip(), keywords.strip(), download.strip(), refer.strip(), link.strip()]
        page_info.append(item_info)
    return page_info


def write_to_csv(file_name, data):
    with open(file_name, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # 写入表头
        writer.writerow(
            ['title', 'author', 'paper_source', 'paper_type', 'date', 'abstract', 'keywords', 'download', 'refer',
             'link'])
        # 写入数据
        writer.writerows(data)


def main(search_word):
    all_data = []
    for page_num in range(1, 6):  # 假设你要爬取前5页
        page_text = get_page_text(base_url, headers, search_word, page_num)
        page_data = parse_page_text(page_text)
        all_data.extend(page_data)

    write_to_csv('666.csv', all_data)


# 使用 "机器学习" 作为搜索词调用主函数
main("机器学习")
