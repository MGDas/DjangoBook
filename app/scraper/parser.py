import aiohttp
import asyncio
import json
import os

from bs4 import BeautifulSoup as bs

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
BASE_URL = "https://book24.ru"

ON_WRITE = []


async def connect(url):

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()
            soup = bs(html, 'html.parser')
            return soup


def write_data():
    with open(f"{BASE_DIR}/data/data.json", "w") as file:
        json.dump(ON_WRITE, file, indent=2, ensure_ascii=False)


async def pars_book(url):

    soup = await connect(url)

    book_name = soup.select_one(".item-detail__title").text
    description = soup.select_one(".collapse-panel__text.js-collapse-text .text-block-d")
    text = ""
    for desc in description.select("p"):
        text += desc.text + '\n\n'

    author_name = None
    genre_name = None

    params = soup.select(".item-tab__chars-item")

    for param in params:
        try:
            lable = param.select_one(".item-tab__chars-key").text
        except:
            continue

        if lable == "Автор:":
            author_name = param.select_one(".item-tab__chars-value a").text

        if lable == "Раздел:":
            genre_name = param.select_one(".item-tab__chars-value a").text

    data = {
        "author": author_name,
        "genre": genre_name,
        "book_name": book_name,
        "description": text
    }
    ON_WRITE.append(data)


async def pars_catalog():

    url = "https://book24.ru/catalog/"
    soup = await connect(url)

    books = soup.select(".book__image-link.js-item-element.ddl_product_link")

    tasks = []
    for book in books:
        task = asyncio.create_task(pars_book(BASE_URL + book['href']))
        tasks.append(task)

    await asyncio.gather(*tasks)

    write_data()



















if __name__ == '__main__':
    asyncio.run(pars_catalog())
