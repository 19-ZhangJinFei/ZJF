from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# 创建 Chrome 浏览器实例
web = webdriver.Chrome()

# 打开网页
web.get("http://lagou.com")

# 等待页面加载
time.sleep(1)

# 找到输入框 输入python => 输入回车/点击搜索按钮
search_input = web.find_element(By.XPATH, '//*[@id="search_input"]')
search_input.send_keys("python", Keys.ENTER)

# 等待搜索结果加载
time.sleep(1)

# 查找存放数据的位置 进行数据提取
# 找到页面中存放数据的所有li
li_list = web.find_elements(By.XPATH, '//*[@id="s_position_list"]/ul/li')
for li in li_list:
    job_name = li.find_element(By.TAG_NAME, "h3").text
    job_price = li.find_element(By.XPATH, "./div/div/div[2]/div/span").text
    job_company = li.find_element(By.XPATH, "./div/div[2]/div/a").text
    print(job_name, job_company, job_price)

# 关闭浏览器
web.quit()
