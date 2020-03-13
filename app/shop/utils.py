from django.utils.text import slugify


def get_image(instance, filename):
    slug = slugify(instance.name[:30])
    format = filename.split(".")[-1]
    dir_name = instance.__class__.__name__.lower()
    return f"{dir_name}s/{slug}.{format}"
