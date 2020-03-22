import aiohttp
import asyncio
import json
import os
import time

from bs4 import BeautifulSoup as bs

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PATH_TO_JSON_FILE_BOOK = os.path.join(BASE_DIR, "data/book_data.json")
PATH_TO_JSON_FILE_AUTHOR = os.path.join(BASE_DIR, "data/author_data.json")
BASE_URL = "https://book24.ru"

ON_WRITE = []
ON_WRITE_AUTHORS = []


def get_soup(html):
    soup = bs(html, 'html.parser')
    return soup

async def connect(url, session):
    async with session.get(url) as response:
        print(f"Connect to {url}")
        html = await response.text()
        return html


def write_data():
    print(f"===== {len(ON_WRITE)} OBJECTS WRITED IN JSON FILE ======")
    with open(f"{PATH_TO_JSON_FILE_BOOK}", "w") as file:
        json.dump(ON_WRITE, file, indent=2, ensure_ascii=False)

def write_data_author():
    print(f"===== {len(ON_WRITE_AUTHORS)} OBJECTS WRITED IN JSON FILE ======")
    with open(f"{PATH_TO_JSON_FILE_AUTHOR}", "w") as file:
        json.dump(ON_WRITE_AUTHORS, file, indent=2, ensure_ascii=False)

def get_book_name(soup):
    try:
        book_name = soup.select_one(".item-detail__title").text
    except:
        book_name = None

    return book_name

def get_book_description(soup):
    try:
        description = soup.select_one(".collapse-panel__text.js-collapse-text .text-block-d")
    except:
        description = None

    text = ""
    if description:
        for desc in description.select("p"):
            text += desc.text + '\n\n'

    return text

def get_params(soup):
    try:
        params = soup.select(".item-tab__chars-item")
    except:
        params = None

    return params

def get_lable(param):
    try:
        lable = param.select_one(".item-tab__chars-key").text
    except:
        lable = None

    return lable

def get_author(param):
    try:
        author_name = param.select_one(".item-tab__chars-value a").text
    except:
        author_name = None

    if author_name:
        try:
            author_url = param.select_one(".item-tab__chars-value a")['href']
        except KeyError:
            author_url = param.select_one(".item-tab__chars-value a")['data-link']
        except:
            author_url = None

        return [{"name": author_name, "url": author_url}]
    return author_name

def get_genre(param):
    try:
        genre_name = param.select_one(".item-tab__chars-value a").text
    except:
        genre_name = None

    return genre_name

def get_author_and_genre(soup):
    params = get_params(soup)

    author_name = None
    genre_name = None

    if params:
        for param in params:
            lable = get_lable(param)
            if lable == "Автор:":
                author_name = get_author(param)
            if lable == "Раздел:":
                genre_name = get_genre(param)

    return author_name, genre_name


def get_book_image_url(soup):
    try:
        book_image_url = soup.select_one(".item-cover__item:nth-child(1) img")['src']
    except:
        book_image_url = None

    return book_image_url

async def pars_book(html):

    soup = get_soup(html)

    book_name = get_book_name(soup)
    description = get_book_description(soup)
    author_name, genre_name = get_author_and_genre(soup)
    book_image_url = get_book_image_url(soup)

    data = {
        "author": author_name,
        "genre": genre_name,
        "book_name": book_name,
        "description": description,
        "image_url": book_image_url
    }
    print(f"# {book_name}....... ADDED FOR WRITE")
    print(f"    Author: {data['author']}")
    print(f"    Genre: {data['genre']}")
    print(f"    Image Url: {data['image_url']}")
    ON_WRITE.append(data)


async def get_data_books(soup):
    try:
        books = soup.select(".book__image-link.js-item-element.ddl_product_link")
        return books
    except Exception as e:
        raise Exception(
            "# ERROR: This page is have not books!"
        )

async def base_page():

    url = "https://book24.ru/catalog/"
    async with aiohttp.ClientSession() as session:
        html = await connect(url, session)
        soup = get_soup(html)

        books = soup.select(".book__image-link.js-item-element.ddl_product_link")

        return books


async def pars_catalog():

    books = await base_page()

    urls = []
    async with aiohttp.ClientSession() as session:
        for book in books:
            book_url = asyncio.create_task(connect(BASE_URL + book['href'], session))
            urls.append(book_url)

        htmls = await asyncio.gather(*urls)

    tasks = []
    for html in htmls:
        task = asyncio.create_task(pars_book(html))
        tasks.append(task)

    await asyncio.gather(*tasks)

    write_data()

def get_author_name(soup):
    try:
        author_name = soup.select_one(".author-item__title").text
    except:
        author_name = None

    return author_name

def get_author_description(soup):
    try:
        description = soup.select_one(".text-block-d").text.strip()
    except:
        description = None

    return description

def get_author_image_url(soup):
    try:
        author_image_url = soup.select_one(".author-item__pic img")['src']
    except:
        author_image_url = None

    return author_image_url

async def pars_author(html):
    soup = get_soup(html)

    author_name = get_author_name(soup)
    description = get_author_description(soup)
    author_image_url = get_author_image_url(soup)

    data = {
        "name": author_name,
        "description": description,
        "image_url": author_image_url
    }
    print(f"# {author_name}....... ADDED FOR WRITE")
    print(f"    Image Url: {data['image_url']}")
    ON_WRITE_AUTHORS.append(data)


def get_authors_urls_from_book_data():
    url_list = []
    with open(f"{PATH_TO_JSON_FILE_BOOK}", "r") as file:
        data = json.load(file)
        for d in data:
            if d['author'] and d['author'][0]['url']:
                url_list.append(d['author'][0]['url'])
    return url_list

async def pars_authors():

    author_urls = get_authors_urls_from_book_data()

    urls = []
    async with aiohttp.ClientSession() as session:
        for author_url in author_urls:
            author_url = asyncio.create_task(connect(BASE_URL + author_url, session))
            urls.append(author_url)

        htmls = await asyncio.gather(*urls)

    tasks = []
    for html in htmls:
        task = asyncio.create_task(pars_author(html))
        tasks.append(task)

    await asyncio.gather(*tasks)

    write_data_author()



def main():

    asyncio.run(pars_catalog())
    asyncio.run(pars_authors())
