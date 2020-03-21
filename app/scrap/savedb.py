import json

from pytils.translit import slugify

from scrap.parser import PATH_TO_JSON_FILE_BOOK
from scrap.parser import PATH_TO_JSON_FILE_AUTHOR

from shop.models import Author
from shop.models import Genre
from shop.models import Book


def get_author_data():
    with open(f"{PATH_TO_JSON_FILE_AUTHOR}", "r") as file:
        data = json.load(file)
        return data


def get_book_data():
    with open(f"{PATH_TO_JSON_FILE_BOOK}", "r") as file:
        data = json.load(file)
        return data

def save_genre():
    data = get_book_data()

    for d in data:
        genre, status = Genre.objects.update_or_create(
            name=d['genre'],
            defaults={
                'slug': slugify(d['genre'])
            }
        )
        if status:
            print(f"{genre} .............SAVED........")
        else:
            print(f"{genre} .............UPDATED........")


def save_authors():
    data = get_author_data()

    for d in data:
        name = d['name']
        description = d['description']
        img_url = d['image_url']

        author, status = Author.objects.get_or_create(
            name=name,
            description=description,
            img_url=img_url
        )
        if status:
            print(f"{author} .............SAVED........")
        else:
            print(f"{author} .............UPDATED........")

def get_author(name):
    try:
        author = Author.objects.filter(name=name)
    except:
        author = None

    return author


def get_genre(name):
    try:
        genre = Genre.objects.get(name=name)
    except:
        genre = None

    return genre

def check_key_author(data):
    try:
        author_name = data['author'][0]['name']
    except:
        author_name = None

    return author_name

def save_books():
    data = get_book_data()

    for d in data:
        author = get_author(check_key_author(d))
        genre = get_genre(d['genre'])
        name = d.get('book_name', None)
        description = d.get('description', None)
        img_url = d.get('image_url', None)

        book, status = Book.objects.update_or_create(
            name=name,
            defaults={
                "genre": genre,
                "description": description,
                "img_url": img_url
            }
        )
        book.author.set(author)

        if status:
            print(f"{book} .............SAVED........")
        else:
            print(f"{book} .............UPDATED........")




def save_in_db():
    save_genre()
    save_authors()
    save_books()
