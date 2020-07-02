import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from rooms import models as room_models
from users import models as user_models

class Command(BaseCommand):
    
    help = 'This command creates many rooms.'

    def add_arguments(self, parser):
        parser.add_argument("--number", default=2, type=int, help="How many rooms do you want to create")

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        all_users = user_models.User.objects.all()
        room_types = room_models.RoomType.objects.all()
        seeder.add_entity(room_models.Room, number, {
            'name': lambda x: seeder.faker.address(),
            'host': lambda x: random.choice(all_users),
            'room_type': lambda x: random.choice(room_types),
            'guests': lambda x: random.randint(1, 20),
            'price': lambda x: random.randint(1, 300),
            'beds': lambda x: random.randint(1, 5),
            'bedrooms': lambda x: random.randint(1, 5),
            'baths': lambda x: random.randint(1, 5),
        })
        created_rooms = seeder.execute()
        # 2중 리스트를 1중으로 예쁘게 빼주는 flatten 사용
        created_clean = flatten(list(created_rooms.values()))
        amenities = room_models.Amenity.objects.all()
        facilities = room_models.Facility.objects.all()
        rules = room_models.HouseRule.objects.all()
        # fake photo data 추가
        for pk in created_clean:
            # Photo의 외래키인 Room 을 추가해주기 위해 미리 저장
            room = room_models.Room.objects.get(pk=pk)
            for i in range(3, random.randint(8, 10)):
                room_models.Photo.objects.create(
                    caption=seeder.faker.sentence(),
                    room=room,
                    file=f"room_photos/{random.randint(1, 12)}.jpg"
                )
            for a in amenities:
                magic_number = random.randint(0, 15)
                # 랜덤하게 어메니티를 하나씩 추가
                if magic_number % 2 == 0:
                    # 다대다 방식에서 추가하는 방식 => add
                    room.amenities.add(a)
            for f in facilities:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.facilities.add(f)
            for r in rules:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.house_rules.add(r)

        self.stdout.write(self.style.SUCCESS(f"{number} rooms created!"))