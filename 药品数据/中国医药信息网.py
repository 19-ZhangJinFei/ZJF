import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# 基础URL和分页参数
base_url = "https://www.dayi.org.cn"
list_url_template = "https://www.dayi.org.cn/list/5/{}"

# 初始化一个空的DataFrame来存储药品信息
df = pd.DataFrame(columns=["药品名称", "药品介绍"])

# 遍历分页并获取药品信息
for page_num in range(1, 11):  # 假设我们只爬取前10页，你可以根据需要调整页数
    list_url = list_url_template.format(page_num)

    try:
        response = requests.get(list_url)
        response.raise_for_status()  # 检查请求是否成功
        soup = BeautifulSoup(response.text, "html.parser")

        # 查找所有药品详情页面的URL
        for item in soup.find_all("div", class_="public-node"):
            drug_name_tag = item.find("div", class_="title-left").find("a")
            drug_name = drug_name_tag.get_text(strip=True)
            drug_url = base_url + drug_name_tag["href"]

            # 获取药品介绍页面
            drug_response = requests.get(drug_url)
            drug_response.raise_for_status()
            drug_soup = BeautifulSoup(drug_response.text, "html.parser")

            # 提取药品介绍
            drug_content = drug_soup.find("div", class_="node-main-content").get_text(strip=True)

            # 将提取的信息添加到DataFrame中
            df = df.append({
                "药品名称": drug_name,
                "药品介绍": drug_content
            }, ignore_index=True)

            # 为了避免对服务器造成过大压力，可以添加延时（这里设置为1秒）
            time.sleep(1)

    except Exception as e:
        print(f"Error fetching page {page_num}: {e}")

    # 将DataFrame保存到CSV文件中
df.to_csv("medicines_info.csv", index=False, encoding="utf-8-sig")
print("Data has been saved to medicines_info.csv")