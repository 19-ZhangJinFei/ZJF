import csv
import json
import requests

"""
    crwalURL:https://bydrug.pharmcube.com/data/list/subjectVbp
    data: 2524 total
    output_file: ByDrug.csv
"""

def crawl_data(url,page):
    dic = {
        "priority":"u=1, i",
        "referer":"https://bydrug.pharmcube.com/data/list/subjectVbp",
        "5757ec40b855c8e79d1376edde0f4978":"I$WGS3fn6*GENIbFb86egaa4ee341bdGlgSzYYE/H5iN3fwPGKYA==",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "Cookie":"Hm_lvt_aedff73bc4f02be835e11695a0b2066e=1729693712; HMACCOUNT=B40D837B7C6A920E; sajssdk_2015_cross_new_user=1; PHARMCUBEJSESSIONID=e01e2640-671e-42b3-8ed5-5698eec102f9; reLoginPolling=false; isKicked=false; mf_login_track={%22sessionId%22:%22e01e2640-671e-42b3-8ed5-5698eec102f9%22%2C%22employee%22:%22%E5%90%A6%22}; language=cn; tfstk=fXunfhOlAR6f4NsgshzBqBb9uC-9S6a7ZYQ8ezeybRy6N6p72aWuIbkJOuhLEakonuuLJXHgZYh2OJk-v8PzQbspN0dQE7ome8HoNBNzUYkueDK9kXGQPzJxrELxOLI4JKH3T7lwa7PAzozRY0lQPzJOTW-CkXM4xwmmzzRg77VPzzSUUGRgwSSzzJrPQGP4QzyrUk8a7SVAz6yULFRgNRyzzz8rvMyIz23wdLSfu9PXTVN3x878IacmWZEg3XyGw3ggtUyqTRbPzJezJqGrULb8umMirokkrNaKiczaZ4OVq8crGqiYreXbtcl07JU2-6wqJ7czir8fiRunZVqIXsQjsyVmdyueB94uSSZmqvp1zJnm_AqxWOQYumMirok2BND74glcbiSyGaNwwVS5VkP_s-ECkICJNDpHWCAG0_ZU1WyvsCjWOkP_s-dMsi2QY5NUH; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22554332%22%2C%22first_id%22%3A%225e190f7c9ffec747d4a4c0f084668531%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTkyYjljNzgzNGUxZS0wM2E0YTA2OWExNzc1MzgtMWY1MjU2MzYtMTAyNDAwMC0xOTJiOWM3ODM0ZmI0MSIsIiRpZGVudGl0eV9sb2dpbl9pZCI6IjU1NDMzMiIsIiRpZGVudGl0eV9hbm9ueW1vdXNfaWQiOiI1ZTE5MGY3YzlmZmVjNzQ3ZDRhNGMwZjA4NDY2ODUzMSJ9%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%22554332%22%7D%2C%22%24device_id%22%3A%22192b9c7834e1e-03a4a069a177538-1f525636-1024000-192b9c7834fb41%22%7D; uuid=554332; igToolipShowed=true; isHasHover=true; _dx_uzZo5y=18898cfe37be0a22466a5bbf9df77a0db4837bc4cab6004756e5d061a4b6f5d210a45a31; _dx_FMrPY6=671913e2hPX1Fqgt2CMoAdOagDIzTVOJZaMuJQl1; Hm_lpvt_aedff73bc4f02be835e11695a0b2066e=1729696752; grey_fe_pharmcube_investgo=false; grey_fe_pharmcube_pharmainvest=false"
    }
    #POST请求 表单携带的参数
    payload={
        "conditions": [],
        "currentPage": page,
        "field": "",
        "limit": 20,
        "order": "",
        "searchValue": ""
    }
    resp = requests.post(url=url, headers=dic,data=json.dumps(payload))
    data = json.loads(resp.text)
    print(data)
    items = data["obj"]
    for item in items:
        drugname = item["drugName"],
        formulation = item["formulation"],
        specs = item["specs"],
        companynames = item["companyNames"],
        groupname = item["groupName"],
        originalprice = item["originalPrice"],
        bidprice = item["bidPrice"],
        droppercentage = item["dropPercentage"],
        indicationtype = item["indicationType"],
        consistencytime = item["consistencyTime"],
        referencepreparation = item["referencePreparation"],
        province = item["province"]
        csvwriter.writerow([drugname, formulation, specs, companynames, groupname, originalprice, bidprice,
                            droppercentage,indicationtype,consistencytime,referencepreparation,province])



if __name__ == "__main__":
    f = open("ByDrug.csv", mode="w")
    csvwriter = csv.writer(f)
    csvwriter.writerow(["药品名称", "剂型", "规格包装", "企业名称", "中标批次",
                        "中标前单位价格","中标价格", "降幅", "治疗领域", "过评时间",
                        "是否参比制剂" , "供应省份"])
    max_page = 127
    url = "https://bydrug.pharmcube.com/api/byDrug/tools/page/subjectVbp"
    print("=== start excuting ByDrug_cral.py ===\n")
    for page in range(1,max_page+1):
        crawl_data(url,page)
    print("=== end ===\n")