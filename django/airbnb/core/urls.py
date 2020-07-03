from django.urls import path
from rooms import views as room_views


app_name = "core"

urlpatterns = [
    # 1. Class Based Views 가 아닌 경우
    # path("", room_views.all_rooms, name="home"),
    
    # 2. Class Based Views인 경우
    #    as_view는 해당 클래스를 view 함수로 바꿔주는 함수
    path("", room_views.HomeView.as_view(), name="home"),
]