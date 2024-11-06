import csv
import aiofiles
import asyncio
import aiohttp
from lxml import etree


# 得到子页面的url
async def Get_Son_Url(headers):
    href = []
    for i in range(0, 251, 25):
        url = f"https://movie.douban.com/top250?start={i}&filter="
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=headers) as resp:
                    main_page = etree.HTML(await resp.text())
                    for num in range(1, 26):
                        href += main_page.xpath(f'//*[@id="content"]/div/div[1]/ol/li[{num}]/div/div[1]/a/@href')
                    print(f'爬取{i}')
            except Exception as e:
                print(f"在获取子页面URL时出现错误: {e}")
    return href


# 得到子页面的数据并写入文件
# 得到子页面的数据并写入文件
async def Get_Mess(headers, url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            lxml = etree.HTML(await resp.text())

            # 所有的信息
            all_dic = {}

            # 获取排名信息并处理索引错误
            rank = lxml.xpath(f'//*[@id="content"]/div[1]/span[1]/text()')
            if rank:
                all_dic['rank'] = rank[0]
            else:
                all_dic['rank'] = "未获取到排名信息"

            # 获取电影名称信息并处理索引错误
            name = lxml.xpath(f'//*[@id="content"]/h1/span[1]/text()')
            if name:
                all_dic['name'] = name[0]
            else:
                all_dic['name'] = "未获取到电影名称信息"

            for fun in range(1, 4):
                label = lxml.xpath(f'//*[@id="content"]/span[{fun}]/span[1]/text()')
                message = lxml.xpath(f'//*[@id="content"]/span[{fun}]/span[2]/a/text()')

                if message:
                    messages = '、'.join(message)
                    all_dic[label[0]] = messages
                else:
                    all_dic[label[0]] = "未获取到相关信息"

            all = lxml.xpath('//*[@id="content"]/span[@class="pl"]')
            mess = lxml.xpath('//*[@id="content"]/span/text()')
            label2 = [lxml.xpath(f'//*[@id="content"]/span[@class="pl"][{eve}]/text()')[0] for eve in range(len(all))]

            for i in range(len(all)):
                index1 = mess.index(label2[i])
                index2 = mess.index(label2[i + 1]) if i!= len(all) - 1 else len(mess)

                if mess[index1 + 1: index2]:
                    all_dic[label2[i]] = '、'.join(mess[index1 + 1: index2])
                else:
                    all_dic[label2[i]] = "未获取到相关信息"

            summary = lxml.xpath('//*[@id="link-report-intra"]/span[1]/text()')
            if summary:
                all_dic['summary'] = summary
            else:
                all_dic['summary'] = "未获取到电影简介信息"

            rating = lxml.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/strong/text()')
            if rating:
                all_dic['rating'] = rating
            else:
                all_dic['rating'] = "未获取到评分信息"

            votes = lxml.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/div/div[2]/a/span;text()')
            if votes:
                all_dic['votes'] = votes
            else:
                all_dic['votes'] = "未获取到投票数信息"

            for win in range(5):
                stars = lxml.xpath(f'//*[@id="interest_sectl"]/div[1]/div[3]/div[{win + 1}]/span[2]/text()')
                if stars:
                    all_dic[f'{5 - win}星'] = stars[0]
                else:
                    all_dic[f'{5 - win}星'] = "未获取到星级分布信息"

            # 写入.csv文件
            # 将子页面的数据存入为.csv
            async def DownLoad(headers, href):
                async with aiohttp.ClientSession() as session:
                    tasks = [asyncio.create_task(Get_Mess(headers, url)) for url in href]
                    await asyncio.gather(*tasks)


# 主线程
async def main():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0",
        'Cookie':'bid=UfG4qzKFh50; _pk_id.100001.4cf6=13f8d7c141b84ece.1729871385.; __yadk_uid=GwekXg4Ty5h9e2CzomOxJF2T1Rmv3qas; ll="118099"; _vwo_uuid_v2=D438F089E83474700FE470B489B9CBEE0|51c3dbddccc7c48ab29c68e49be7a8bb; __utma=30149280.613583757.1730032355.1730032355.1730032355.1; __utmz=30149280.1730032355.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=223695111.1255257204.1730032355.1730032355.1730032355.1; __utmz=223695111.1730032355.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _pk_ses.100001.4cf6=1',
    }

    href = await Get_Son_Url(headers)
    print(href)
    await DownLoad(headers, href)


if __name__ == '__main__':
    asyncio.run(main())