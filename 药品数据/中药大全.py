import re
import requests
import random
import csv
from lxml import html

class ChineseMedicineSpider(object):

    def __init__(self):
        self.headers = {'User-Agent': random.choice(['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'])}
        self.data_list = []  # 用于存储所有中药材数据
        self.csv_file = 'chinese_medicine_data.csv'
        self.fieldnames = ['名称', '英文名', '药用部位', '植物形态', '产地分布', '采收加工', '药材性状', '性味归经', '功效与作用', '临床应用', '药理研究', '化学成分', '使用禁忌', '配伍药方']

        # 初始化CSV文件
        with open(self.csv_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
            writer.writeheader()  # 写入表头

    # 启动爬虫
    def run_spider(self):
        pages = int(input('请输入需要爬取的页数：（小于或等于45）'))
        if pages >= 0 and pages <= 45:
            print('爬虫开始运行！！！')
            self.get_chinese_medicine(pages)
            print('爬虫运行结束！！！')
        else:
            print("输入无效！！！")

    def get_chinese_medicine(self, pages):
        for page in range(1, pages + 1):
            url = f'http://www.zhongyoo.com/name/page_{page}.html'
            resp = requests.get(url, self.headers)

            if resp.status_code == 200:
                tree = html.fromstring(resp.content.decode('gbk'))

                zy_name_list = tree.xpath('//div[@class="sp"]/span/a/img/@alt')
                zy_info_list = tree.xpath('//div[@class="sp"]/span/a/@href')

                for i, zy_name in enumerate(zy_name_list):
                    chinese_medicine = {'名称': zy_name}
                    print(zy_name)

                    info_url = zy_info_list[i]
                    self.get_chinese_medicine_info(info_url, chinese_medicine)

                    # 保存当前药材信息到CSV文件
                    self.save_to_csv(chinese_medicine)

            else:
                print("响应结果为空")

    def get_chinese_medicine_info(self, info_url, chinese_medicine):
        try:
            resp = requests.get(info_url, self.headers).content.decode('gbk', errors='ignore')  # 忽略解码错误

            pattern = r'<p></p>([\s\S]*?)<p></p>'
            match = re.search(pattern, resp)
            if match:
                text = re.sub(r"<[^>]+>", "", match.group(1))
                text = re.sub(r"\s+【", "\n【", text)
                text = re.sub(r"^\s*", "", text)
                text = re.sub(r"相关推荐文章.*", "", text, flags=re.DOTALL)
                info = re.sub(r"\s*$", "", text)

                # 分析并填充字段
                self.extract_fields(info, chinese_medicine)
            else:
                chinese_medicine['info'] = "暂无详细信息,请等待管理员添加!"
        except Exception as e:
            print(f"获取信息时出错: {info_url}, 错误信息: {e}")

    def extract_fields(self, info, chinese_medicine):
        # 根据需要解析并填充其他字段
        fields = ['英文名', '药用部位', '植物形态', '产地分布', '采收加工', '药材性状', '性味归经', '功效与作用', '临床应用', '药理研究', '化学成分', '使用禁忌', '配伍药方']
        for field in fields:
            pattern = rf'【{field}】(.*?)【'
            match = re.search(pattern, info + '【', re.DOTALL)
            chinese_medicine[field] = match.group(1).strip() if match else "暂无"

    def save_to_csv(self, chinese_medicine):
        with open(self.csv_file, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
            writer.writerow(chinese_medicine)  # 写入数据行

if __name__ == '__main__':
    zy = ChineseMedicineSpider()
    zy.run_spider()
