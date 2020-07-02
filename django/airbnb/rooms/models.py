from django.db import models
from django_countries.fields import CountryField
from core import models as core_models
from users import models as users_models



class AbstractItem(core_models.TimeStampedModel):

    """ Abstract Item """

    name = models.CharField(max_length=80)

    class Meta:
        abstract = True
    
    def __str__(self):
        return self.name

class RoomType(AbstractItem):

    """ RoomType Object Definition """

    class Meta:
        verbose_name_plural = "Room Type"

class Amenity(AbstractItem):

    """ Amenity Object Definition """

    class Meta:
        verbose_name_plural = "Amenities"


class Facility(AbstractItem):

    """ Facility Object Definition """

    class Meta:
        verbose_name_plural = "Facilities"

class HouseRule(AbstractItem):

    """ HouseRule Object Definition """

    class Meta:
        verbose_name_plural = "House Rule"

# Create your models here.
# core의 TimeStampedModel 이 models.Model 을 상속했기 때문에
# models.Model을 상속할 필요가 없음
class Room(core_models.TimeStampedModel):

    """ Room Model Definition """

    name = models.CharField(max_length=140)
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=80)
    price = models.IntegerField()
    address = models.CharField(max_length=140)
    guests = models.IntegerField()
    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    baths = models.IntegerField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)
    # related_name 설정 시 
    # 부모에서 자식을 room_set 이 아니라 rooms 로 접근 가능
    host = models.ForeignKey(
        users_models.User, related_name="rooms", on_delete=models.CASCADE
    )
    room_type = models.ForeignKey(RoomType, related_name="rooms", on_delete=models.SET_NULL, null=True)
    amenities = models.ManyToManyField(Amenity, related_name="rooms", blank=True)
    facilities = models.ManyToManyField(Facility, related_name="rooms", blank=True)
    house_rules = models.ManyToManyField(HouseRule, related_name="rooms", blank=True)


    def __str__(self):
        return self.name

    # 해당 레코드 저장 시 이 함수를 수행하는데
    # 이를 오버라이딩 함으로써 저장 전 동작을 추가하거나
    # 특정 경우, 저장하지 않도록 분기 처리할 수도 있음 
    def save(self, *args, **kwargs):
        self.city = str.capitalize(self.city)
        # 여기가 진짜 저장
        super().save(*args, **kwargs)

    def total_rating(self):
        all_reviews = self.reviews.all()
        all_ratings = 0
        if len(all_reviews) > 0:
            for review in all_reviews:
                all_ratings += review.rating_average()
            return round(all_ratings / len(all_reviews), 1)
        return 0

class Photo(core_models.TimeStampedModel):

    """ Photo Model Definition """

    caption = models.CharField(max_length=50)
    file = models.ImageField(upload_to="room_photos")
    room = models.ForeignKey(Room, related_name="photos", on_delete=models.CASCADE)
    
    def __str__(self):
        return self.caption