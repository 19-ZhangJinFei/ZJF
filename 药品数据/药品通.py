import requests
from bs4 import BeautifulSoup
import pandas as pd

# 初始化一个空的DataFrame来存储药品信息
df = pd.DataFrame(columns=["药品名称", "适应症", "参考价"])

# 基础URL和分页处理
base_url = "https://ypk.39.net/jiating/"
current_page = 1

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Cookie': 'track39id=2243ad4e766307f5adcda2f57104261f; Hm_lvt_eeeef2d289cfb1ec7eb1a2771c02a426=1729859297,1730122930; HMACCOUNT=AB7BD42384A25347; Hm_lpvt_eeeef2d289cfb1ec7eb1a2771c02a426=1730124149',
}

while True:
    # 构造当前页的URL
    page_url = f"{base_url}p{current_page}/"

    # 发送HTTP请求获取页面内容
    try:
        response = requests.get(page_url, headers=headers, timeout=20)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"请求失败: {e}")
        break

    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(response.text, "html.parser")

    # 查找药品列表
    drug_list = soup.find_all("div", class_="drugs-brief")
    if not drug_list:  # 如果没有找到药品列表，说明已经到了最后一页或页面结构有变化
        break

    # 遍历药品列表
    for drug_item in drug_list:
        # 提取药品名称
        name_tag = drug_item.find("p", class_="drugs-ul-tit").find("a")
        if name_tag:
            drug_name = name_tag.get_text(strip=True)

            # 提取适应症描述
            indication_tag = drug_item.find("p", class_="drugs-ul-txt")
            if indication_tag:
                indication = indication_tag.get_text(strip=True)
            else:
                indication = ""

            # 提取参考价
            price_tag = drug_item.find("p", class_="commonly-drug-price")
            if price_tag:  # 先检查 price_tag 是否存在
                price_span = price_tag.find("span")
                if price_span:
                    price = price_span.get_text(strip=True)
                else:
                    price = ""
            else:
                price = ""


            df = df._append({
                "药品名称": drug_name,
                "适应症": indication,
                "参考价": price
            }, ignore_index=True)

    current_page += 1


df.to_csv("medicines_info.csv", index=False, encoding="utf-8-sig")
print("Data has been saved to medicines_info.csv")
