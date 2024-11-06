import requests
import json
# 实现AES加密需要的三个模块
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from base64 import b64encode


# py实现AES-CBC加密
def encrypt_aes(text, key, iv):
    cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv.encode('utf-8'))
    padded_text = pad(text.encode('utf-8'), AES.block_size)
    ciphertext = cipher.encrypt(padded_text)
    return b64encode(ciphertext).decode('utf-8')


# 仿照function b(a, b)构造加密函数
def b(a, b):
    c = b
    d = "0102030405060708"
    e = a
    f = encrypt_aes(e, c, d)
    return f


# 评论数据(i6c)
d = {
    'csrf_token': 'a377fd1409c2d967e66527ddf3ce2c02',  # 可以为空值
    'cursor': '-1',
    'offset': '0',
    'orderType': '1',
    'pageNo': '1',
    'pageSize': '20',  # 评论数
    'rid': 'R_SO_4_167827',  # 歌曲编号
    'threadId': 'R_SO_4_167827'  # 歌曲编号
}

# 16位随机字符串
i = "4BfsFyBWTSe0C5eQ"
# bsu6o(["流泪", "强"])
e = "010001"
# bsu6o(Xo0x.md)
f = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
# bsu6o(["爱心", "女孩", "惊恐", "大笑"])
g = "0CoJUm6Qyw8W8jud"

# 将i6c转化为json格式
d_json = json.dumps(d)

# 调用两次b()函数得出encText
encText = b(d_json, g)
encText = b(encText, i)

# 随机字符串获得encSecKey
encSecKey = "ac120b775a368f6cdf196f173ac16bccaa08e8589fdd824f7445cb71a6f12f7a25da019240ce2f69a214ef34ba2795b057b1cf4fd24fbf4bd9f78167c9c69de4ee8be3bb8bb9119e2a0328219497864558363bc8e5c8a7999822f127dc0d7fc3bbf0a53f3e2e091eba811eb57558dd6290ab4224f636cea2d264bb2ed7c7cee8"

# 请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
}

# 评论数据的请求地址
url = 'https://music.163.com/weapi/comment/resource/comments/get?csrf_token='

# 将encText和encSecKey打包起来
data = {
    'params': encText,
    'encSecKey': encSecKey
}

# 发送post请求并携带encText和encSecKey得到评论的json格式
respond = requests.post(url, headers=headers, data=data).json()
# 打印
print(respond)