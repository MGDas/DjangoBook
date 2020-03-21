import time

from django.core.management.base import BaseCommand
from scrap.savedb import save_in_db
from scrap.parser import main as save_data_in_file


class Command(BaseCommand):

    def handle(self, *args, **options):

        start = time.time()

        save_data_in_file()
        save_in_db()

        end = time.time()

        total_time = str(end - start)[:5]
        print(total_time)
