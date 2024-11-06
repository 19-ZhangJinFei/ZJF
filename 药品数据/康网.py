import requests
import csv
from lxml import html
from bs4 import BeautifulSoup

# 1. 获取网页源码并转换成文本格式
def getcon():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    }
    url = "http://www.cnkang.com/cm/zcy/bxy/"
    res = requests.get(url, headers=headers)
    res.encoding = 'utf-8'
    analyse(res.text)

# 2. 解析网页源码
def analyse(res):
    soup = BeautifulSoup(res, 'html.parser')
    med = soup.select('.catalog04 dd a')
    med_name = []
    med_url = []

    for item in med:
        temp_url = 'http://www.cnkang.com' + item['href']
        med_name.append(item.text)
        med_url.append(temp_url)

    detailed_information(med_name, med_url)

# 3. 爬取各味药品的详细信息
def detailed_information(name, url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    }

    all_medicines = []

    for i in range(len(url)):
        temp_url = url[i]
        print(f"正在爬取：{name[i]} ({i + 1}/{len(url)})")
        temp_res = requests.get(temp_url, headers=headers)

        # 检查响应状态
        if temp_res.status_code == 200:
            medicine_info = crawler(temp_res)
            all_medicines.append({
                '名称': name[i],
                '简介': medicine_info.get('Introduction', ''),
                '药性': medicine_info.get('Medicinal', ''),
                '功效': medicine_info.get('Efficacy', ''),
                '适应症': medicine_info.get('Indications', '')
            })
            save_to_csv(all_medicines)  # 边爬取边存储
        else:
            print(f"无法获取 {temp_url} 的数据，状态码：{temp_res.status_code}")

# 4. 用来在源码中爬取具体信息
def crawler(res):
    try:
        tree = html.etree.HTML(res.content, html.etree.HTMLParser(encoding='utf-8'))
        introduction = tree.xpath('//div[@class="zh05b"]//p[1]/text()')
        medicinal = tree.xpath('//div[@class="zh05b"]//p[2]/text()')
        efficacy = tree.xpath('//div[@class="zh05b"]//p[3]/text()')
        indications = tree.xpath('//div[@class="zh05b"]//p[4]/text()')

        return {
            'Introduction': ''.join(introduction).strip(),
            'Medicinal': ''.join(medicinal).strip(),
            'Efficacy': ''.join(efficacy).strip(),
            'Indications': ''.join(indications).strip()
        }
    except Exception as e:
        print(f"解析错误：{e}")
        return {}

# 保存数据到 CSV 文件
def save_to_csv(medicines):
    keys = medicines[0].keys()  # 获取字段名
    with open('medicines_8.csv', 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(medicines)

if __name__ == "__main__":
    getcon()
