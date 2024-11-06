import bs4
import requests

url = "https://db.yaozh.com/zyzy"

resp = requests.get(url)
#print(resp.text)

page = bs4.BeautifulSoup(resp.text, "html.parser")

print(page)