#1.找到未加密的参数  #window.arsea(参数，xxxx,xxx,xxx)
#2.想办法把参数进行加密（必须参考网易的逻辑），params，encSecKey => encText,encSecKey => encSecKey
#3.请求到网易，拿到评论信息
import requests
from bs4 import BeautifulSoup
import re

url = 'https://music.163.com/weapi/comment/resource/comments/get?csrf_token=83f15165720d7d5ef6f11287aff56b43'

#请求方式是POST
data = {
    "csrf_token":"",
    "cursor":"-1",
    "offset":"0",
    "orderType":"1",
    "pageNo":"1",
    "pageSize":"20",
    "rid":"R_SO_4_1325905146",
    "threadId":"R_SO_4_1325905146"
}
