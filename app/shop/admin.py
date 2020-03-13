from django.contrib import admin

from shop.models import Author
from shop.models import Genre
from shop.models import Book


admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Book) 
