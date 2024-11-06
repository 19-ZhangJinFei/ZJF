from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 创建 Chrome 浏览器实例
web = webdriver.Chrome()

# 打开目标网站
web.get("https://www.csdn.net/")

try:
    # 等待目标元素加载
    element = WebDriverWait(web, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[2]/div[4]/div[1]/div[3]/div/div[2]/div/div[1]/h3/a'))
    )
    # 点击目标元素
    element.click()
except Exception as e:
    print(f"Error: {e}")

