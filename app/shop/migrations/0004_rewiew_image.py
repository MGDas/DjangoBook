# Generated by Django 3.0.4 on 2020-03-22 19:10

from django.db import migrations, models
import shop.utils


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_rewiew'),
    ]

    operations = [
        migrations.AddField(
            model_name='rewiew',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=shop.utils.get_image),
        ),
    ]
