#示例网站：www.endata.com
#能不能让我的程序连接到浏览器，让浏览器来完成各种复杂的操作，我们只接受最后的结果
#selenium:自动化测试工具
#可以：打开浏览器，然后像人一样去操作浏览器
#程序员可以从selenium中直接提取网页中的各种信息
#环境搭建：
	# pip install selenium -i 清华源
	#下载浏览器驱动:https://googlechromelabs.github.io/chrome-for-testing/#stable
    #谷歌版本;版本 130.0.6723.58（正式版本）
    #把解压的浏览器驱动 chromedriver 放在python解释器所在的文件夹
    #让selenium启动谷歌浏览器
from selenium.webdriver import Chrome

#1.创建浏览器对象
web = Chrome()
#2.打开一个网址
web.get("http://www.baidu.com")

print(web.title)