import pandas as pd
import requests
import re
from bs4 import BeautifulSoup

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    'Cookie': 'JSESSIONID=5D28FA32A7084B5374A7329A64E1EF27; clientlanguage=zh-CN'
}


# 获取药物种类
def drug_type():
    url = 'https://www.gzzcybk.com/classify.jspx#'
    html_text = requests.get(url, headers=header)
    # 获取网页的文本内容
    html = html_text.text
    # 解析获取到的文本内容
    soup = BeautifulSoup(html, 'lxml')
    drug_fun2 = soup.find_all("a", href=["javascript:void(0);", "#"])
    new_fun_list = []
    for link in drug_fun2:
        fun_name = link.text.strip()
        new_fun_list.append(fun_name)
    new_list = new_fun_list[1:len(new_fun_list) - 1]
    df = pd.DataFrame(new_list)
    df.to_excel('药物种类.xlsx', sheet_name='d', index=False)
    return new_list


# 获取网址，并将网址加入列表all_list中
def gwt():
    drug_list = []
    len_fun_drug = []
    fun_baseurl = 'https://www.gzzcybk.com/classify/page.jspx?catId='
    drug_page = '&parentId=&libId=&pageNo='

    for i in range(6, 79):  # 目标数量（6，79）
        fun_list = []
        for z in range(1, 200):  # 这里控制页数
            full_url = fun_baseurl + str(i) + drug_page + str(z)
            response = requests.get(full_url, headers=header)
            html_name = response.text
            pattern = '<font>([\u4e00-\u9fa5]*)</font>'
            name_list = re.findall(pattern, html_name)
            fun_list += name_list
        if fun_list:
            drug_list.append(fun_list)
            n = len(fun_list)
            len_fun_drug.append(n)
    return drug_list, len_fun_drug


# 数据处理
def pro_data(a, b, c):
    type_len_list = []
    for i, j in zip(a, c):
        type_len_list.append([i, j])
    typedata = pd.DataFrame(type_len_list, columns=['药物分类', '药物数量'])
    typedata.to_excel('药物分类与数量.xlsx', sheet_name='d')

    alldrug = pd.DataFrame(b, index=a)
    alldrug.to_excel("药物.xlsx", sheet_name='s')


# 爬取药物分类
a = drug_type()
# 爬取网页药物名称,并接受返回结果
x, y = gwt()
# 传入数据并处理
pro_data(a, x, y)
print('爬取完成')
