"""
TODO: Impliment a web scraping tool with Beautiful Soup or Scrapy and output them to json or csv
site: 

"""
from bs4 import BeautifulSoup   
import requests

user_search = input("Give me what to search: ").replace(" ", "+")

search_engine = 'https://www.amazon.com/s?url=search-alias%253Daps&field-keywords=' + user_search

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}
data = requests.get(search_engine,headers=headers)
if data.status_code != 200:
    print("something is wrong with the site or the internet error code: ", data.status_code)
    exit()

print("amazon status code:", data.status_code)
soup = BeautifulSoup(data.content, 'html.parser')

file = open("soup_data.html", "w+")

file.write(str(soup))

file.close