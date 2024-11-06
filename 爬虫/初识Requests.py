#安装requests
#pip install requests
#国内镜像 pip install -i https://pypi.tuna.tsinghua.edu.cn/simple requests
import requests

query = input("请输入一个你喜欢的明星\n")

url = f"https://www.sogou.com/web?query={query}"

dic = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0"
}#设置请求头，绕过验证系统

resp = requests.get(url,headers = dic)#处理了一个小小的反爬，如果不设置dic，爬虫程序会自带一个headers去访问页面，从而被识别出来
print(resp)#返回响应的结果：即成功或者失败，200表示成功
print(resp.text) #返回响应的内容,拿到页面的源代码,结果，被页面的验证码功能拦截，需要做一个改进，设置headers(请求头)