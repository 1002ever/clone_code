from django.contrib import admin
from django.utils.html import mark_safe
from . import models

# Register your models here.

@admin.register(models.RoomType, models.Facility, models.Amenity, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):

    """ Item Admin Definition """

    list_display = (
        "name", 
        "used_by",
    )

    def used_by(self, obj):
        return obj.rooms.count()

# Admin 속 Admin 을 넣는 방법
class PhotoInline(admin.TabularInline):

    model = models.Photo

# InlineModelAdmin 다른 방식, 보여주는 방식이 다름.
# class PhotoInline(admin.StackedInline):

#     model = models.Photo    

@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):

    """ Room Admin Definition """

    # 인라인 어드민, 맨 아래 들어감
    inlines = (PhotoInline,)

    fieldsets = (
        (
            "Basic Info",
            {"fields": ("name", "description", "country", "city", "address", "price")}
        ),
        (
            "Times",
            {"fields": ("check_in", "check_out", "instant_book")}
        ),
        (
            "Space",
            {"fields": ("guests", "beds", "bedrooms", "baths")}
        ),
        (
            "More About the Spaces",
            {
                # 해당 영역을 접을 수 있게 됨.
                # 너무 많은 내용을 담을 때 유용
                "classes": ("collapse",),
                "fields": ("amenities", "facilities", "house_rules")
            }
        ),
        (
            "Last Details",
            {"fields": ("host",)}
        ),
    )

    list_display = (
        "name",
        "country",
        "city",
        "price",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        # 함수의 결과도 display 가능
        "count_amenities",
        "count_photos",
        "total_rating",
    )

    list_filter = (
        "instant_book",
        "host__superhost",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
        "city",
        "country",
    )

    # host들이 굉장히 많아졌을 때, 리스트로 선택하기가 곤란
    # raw_id_fields에서 돋보기를 누르면 작은 해당 panel 을 띄워줌
    # 그 곳에서 검색이나 필터를 해서 유저를 선택하면
    # 그 데이터의 id가 저장 됨
    raw_id_fields = ("host",)

    # 검색창 만들기 => 여러 옵션이 있음, 장고 문서에 Admin Panel 확인
    # host는 외래키, 그 외래키로 접근 + 그 필드를 바탕으로 검색할 때
    search_fields = ("city", "host__username",)

    # Admin에서 DB 다룰 때, Many To Many 속성인 것 Filter로 다루기
    filter_horizontal = ("amenities", "facilities", "house_rules",)

    # 첫 번째 인자 self는 현재 클래스, 두 번째 인자 obj는 현재 선택된 행
    def count_amenities(self, obj):
        return obj.amenities.count()

    # 해당 함수가 Admin Panel에서 보여질 이름 설정
    count_amenities.short_description = "Amenities Count"

    def count_photos(self, obj):
        return obj.photos.count()

    count_photos.short_description = "Photos Count"

@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    """  Photo Admin Definition """

    list_display = ('__str__', "get_thumbnail",)

    def get_thumbnail(self, obj):
        print(obj.file.url)
        return mark_safe(f"<img width='70px' src='{obj.file.url}'/>")
    get_thumbnail.short_description = "Thumbnail"