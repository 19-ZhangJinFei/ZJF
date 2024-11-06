from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

web = Chrome()

web.get("http://lagou.com")

el = web.find_element(By.XPATH,'//*[@id="changeCityBox"]/p[1]/a')
el.click()

time.sleep(1)

web.find_element(By.XPATH,'//*[@id="search_input"]').send_keys("python", Keys.ENTER)

time.sleep(1)

web.find_element(By.XPATH,'//*[@id="s_position_list"]/ul/li[1]/div[1]/div[1]/div[1]/a/h3').click()
# 在selenium眼中 新窗口是默认切换不过来的

web.switch_to.window(web.window_handles[-1])

# 在新窗口中提取内容
job_detail = web.find_element(By.XPATH,'//*[@id="job_detail"]/dd[2]/div').text
print(job_detail)

# 关掉子窗口
web.close()
# 变更selenium的窗口视角 回到原本的窗口
web.switch_to.window(web.window_handles[0])
print(web.find_element(By.XPATH,'//*[@id="s_position_list"]/ul/li[1]/div[1]/div[1]/div[1]/a/h3').text)
