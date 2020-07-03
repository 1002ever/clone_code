from django.urls import path
from . import views


app_name = "rooms"

urlpatterns = [
    # Detail 페이지 FBV url
    # path("<int:pk>", views.room_detail, name="detail"),

    # Detail 페이지 CBV url
    path("<int:pk>", views.RoomDetail.as_view(), name="detail"),

    path("search/", views.search, name="search"),
]

