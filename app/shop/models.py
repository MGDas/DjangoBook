from django.db import models
from django.utils.text import slugify

from shop.utils import get_image


class BaseModel(models.Model):
    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class ImgUrl(models.Model):

    img_url = models.URLField(blank=True, null=True)
    class Meta:
        abstract = True


class Author(BaseModel, ImgUrl):
    name = models.CharField(max_length=500, db_index=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to=get_image, blank=True, null=True)


class Genre(BaseModel, ImgUrl):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True)
    image = models.ImageField(upload_to=get_image, blank=True, null=True)


class Book(BaseModel, ImgUrl):
    name = models.CharField(max_length=500, db_index=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to=get_image, blank=True, null=True)

    author = models.ManyToManyField(Author, blank=True)

    genre = models.ForeignKey(
        Genre,
        related_name='books',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
