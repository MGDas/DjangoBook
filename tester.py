import requests
from bs4 import BeautifulSoup as bs

response = requests.get("https://book24.ru/product/ya-tvoy-desert-5493403/")

text = response.text

soup = bs(text, 'html.parser')

params = soup.select(".item-tab__chars-item")

for param in params:
    lable = param.select_one(".item-tab__chars-key").text
    if lable == "Автор:":
        author_name = param.select_one(".item-tab__chars-value a")
        print(author_name['data-link'])
        print(f"Автор: {author_name.text}. Url: ")
        break
