from selenium import webdriver
import time
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get('https://www.csdn.net/')
time.sleep(2)
text_label = driver.find_element(By.XPATH,'//*[@id="toolbar-search-input"]')
text_label.send_keys('Dream丶Killer')
time.sleep(2)
text_label.clear()
print(text_label.is_displayed())
print(text_label.get_attribute('placeholder'))
button = driver.find_element(By.XPATH,'//*[@id="toolbar-search-button"]/span')
print(button.size)
print(button.text)

