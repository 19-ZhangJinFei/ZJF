import re

# findall方法:匹配字符串中所有的符合正则的内容，用的并不多
lst = re.findall(r"\d+", "我的电话号是：10086,我女朋友的电话是：10010")
print(list)

# finditer: 匹配字符串中的所有的内容，返回的是迭代器
it = re.finditer(r"\d+", "我的电话号是：10086,我女朋友的电话是：10010")
for i in it:
    print(i.group())

# search返回的结果是match对象，拿数据需要.group(),search的特点：找到一个结果就返回
s = re.search(r"\d+", "我的电话号是10086，我女朋友的电话是：10010")
print(s.group())

print("-----------------------------------------------------------------------")

#match是从头开始匹配
s = re.match(r"\d+","10086,我女朋友的电话是：10010")
print(s.group())

print("-----------------------------------------------------------------------")

#预加载正则表达式
obj = re.compile(r"\d+")
ret = obj.finditer("我的电话号是10086，我女朋友的电话是：10010")
print(ret)
for i in ret:
    print(i.group())

rett = obj.findall("wojdawonfiaw1000000000000")
print(rett)

s = """
<div class='jay'><span id='1'>张进飞</span></div>
<div class='jj'><span id='1'>温欣雨</span></div>
<div class='jesfes'><span id='1'>爸爸</span></div>
<div class='jgretwr'><span id='1'>德玛西亚</span></div>
<div class='trqwfwe'><span id='1'>哎呦尼亚</span></div>
"""
obj = re.compile(r"<div class='(?P<wocaonima>.*?)'><span id='\d'>(?P<wahaha>.*?)</span></div>",re.S) #re.S:让.能匹配换行符

result = obj.finditer(s)
for it in result:
    print(it.group("wahaha"))
    print(it.group("wocaonima"))