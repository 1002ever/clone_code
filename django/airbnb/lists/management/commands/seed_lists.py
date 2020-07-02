import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from users import models as user_models
from lists import models as list_models
from rooms import models as room_models


class Command(BaseCommand):
    
    help = 'This command creates many lists.'

    def add_arguments(self, parser):
        parser.add_argument("--number", default=2, type=int, help="How many lists do you want to create")

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        users = user_models.User.objects.all()
        rooms = room_models.Room.objects.all()
        seeder.add_entity(list_models.List, number, {
            "user": lambda x: random.choice(users),
        })
        created = seeder.execute()
        cleaned = flatten(list(created.values()))
        for pk in cleaned:
            lists = list_models.List.objects.get(pk=pk)
            to_add = rooms[random.randint(0, 5) : random.randint(6, 30)]
            # 쿼리셋을 추가하는 것이 아니라 이를 언패킹해서 전달할 것이므로
            # * 붙이기
            lists.rooms.add(*to_add)

        self.stdout.write(self.style.SUCCESS(f"{number} lists created!"))
        