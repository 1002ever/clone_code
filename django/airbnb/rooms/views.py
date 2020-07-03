# 1번 방식으로 했을 때 import

# import math
# from django.urls import reverse
# from django.utils import timezone
# from django.http import Http404
# from django.shortcuts import render, redirect
# from django.core.paginator import Paginator, EmptyPage
# from . import models


# 2번 방식으로 했을 때 import

from django.shortcuts import render, redirect
from django_countries import countries
from django.urls import reverse
from django.utils import timezone
from django.views.generic import ListView, DetailView
from django.http import Http404
from . import models


# 1. Class Based Views가 아닌 수동적인 View 구성

# # paginator를 사용하지 않는 버전
# # def all_rooms(request):
# #     # request.GET 이라는 요청에 대한 응답에 대해 (여러 클래스, 명령어를 갖음)
# #     # key가 page인 값을 불러오기, 해당 값이 None 이면 default = 1로 부여
# #     # request 는 WSGIRequest 형식을 리턴
# #     # request.GET 는 해당 request를 파이썬이 다룰 수 있는 형태로 바꿔서 리턴하는 셈
# #     page = request.GET.get("page", 1)
# #     # page가 빈 값이면 1을 할당, 비어있지 않으면 int화
# #     # 단, 무조건 숫자형을 받는다는 전제가 필요..
# #     page = int(page or 1)
# #     page_size = 10
# #     limit = page_size * page
# #     offset = limit - page_size
# #     page_rooms = models.Room.objects.all()[offset : limit]
# #     page_count = math.ceil(models.Room.objects.count() / 10)
# #     context = {
# #         "page_rooms": page_rooms,
# #         "page": page,
# #         "pages": page_count,
# #         "page_range": range(1, page_count+1),
# #     }
# #     return render(request, "rooms/home.html", context)

# def all_rooms(request):
#     # 기본값이 필요 X, 페이지네이터가 다 알아서 처리해줌
#     page = request.GET.get("page")

#     # 이렇게 하자마자 바로 모든 QuerySet 이 불려오지 않음.
#     # QuerySet은 lazy 해서 자기가 필요할 때만 불려옴
#     room_list = models.Room.objects.all()

#     # paginator에 자료를 10개씩 쪼개어 저장
#     # orphans 는 갖는 데이터 수가 해당 수 보다 적으면 그 페이지를 숨기라는 것
#     # 마지막 페이지만 데이터 수가 적으면 그 페이지만 텅텅 비어보일 것..
#     paginator = Paginator(room_list, 10, orphans=5)

#     # get_page로 page 값 넘겨주면 그 페이지 데이터를 갖는 자료 리턴
#     # get_page 말고 page도 있는데, 이는 에러를 컨트롤 할 수 있음
#     # 단, get_page는 에러 처리는 못하지만, page가 입력되지 않아도 기본값을 넣어줌
#     # page는 기본값이 무조건 있어야하고, int 변환 처리도 필요
#     rooms = paginator.get_page(page)

#     # page를 활용하여 에러를 제어하는 예시
#     # page_num = request.GET.get("page", 1)
#     # room_list = models.Room.objects.all()
#     # paginator = Paginator(room_list, 10, orphans=5)
#     # try:
#     #     rooms = paginator.page(int(page))
#     #     context = {
#     #         "page": rooms,
#     #     }
#     #     return render(request, "rooms/room_list.html", context)
#     # # EmptyPage 에러를 import 해줘야 함
#     # # 모든 에러를 처리하고 싶다면 except Exciption
#     # # 하지만 어떤 에러인지 구분 안되므로 권장되지 않음.
#     # except EmptyPage:
#     #     return redirect("/")
        

#     context = {
#         "page": rooms,
#     }
#     return render(request, "rooms/room_list.html", context)

# 2. Abstract 방식으로 구현한 View.
#    Class Based Views로 구성한 코드
#    Class Based Views 기반 클래스들(ListView, DetailView 등)은
#    모두 get_context_data 함수를 가짐
#    내가 만든 class view에서 get_context_data를 재정의 => return 은 context
#    context = super().get_context_data(**kwargs)
#    context['키값'] = 추가할 value
#    이렇게 해주면 템플릿에서 context도 이용이 가능

class HomeView(ListView):

    """ HomeView Definition """

    model = models.Room
    paginate_by = 10
    paginate_orphans = 5
    ordering = "created"
    # obj_list 이름을 바꿔줌
    context_object_name = "rooms"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        context["now"] = now
        return context

# Detail 페이지의 function based view

# def room_detail(request, pk):
#     try:
#         room = models.Room.objects.get(pk=pk)
#         context = {
#             "room": room,
#         }
#         return render(request, "rooms/room_detail.html", context)
#     except models.Room.DoesNotExist:
#         return redirect(reverse("core:home"))
#         # redirect가 아니라 404 페이지 보여주고 싶을 때
#         # base.html 위치에 404.html 을 만들어서
#         # 페이지를 커스터마이징 해줄 수도 있음
#         # 이 떄, DEBUG 를 False로 바꿔주고,
#         # ALLOWED_HOSTS 를 변경해줘야 함
#         # raise Http404()

class RoomDetail(DetailView):

    """ RoomDetail Definition """

    # 이렇게만 정해주면 `모델명_detail.html` 템플릿으로
    # 주어진 pk에 해당하는 레코드를 `모델명`에 담아서 전달  
    model = models.Room


def search(request):
    city = request.GET.get("city", "Anywhere")
    city = str.capitalize(city)
    country = request.GET.get("country", "KR")
    room_type = int(request.GET.get("room_type", 0))
    price = int(request.GET.get("price", 0))
    guests = int(request.GET.get("guests", 0))
    bedrooms = int(request.GET.get("bedrooms", 0))
    beds = int(request.GET.get("beds", 0))
    baths = int(request.GET.get("baths", 0))

    # url에서 키 값이 amenites인 것, facilities인 것을
    # 리스트화하여 가져옴
    s_amenities = request.GET.getlist("amenities")
    s_facilities = request.GET.getlist("facilities")

    instant = request.GET.get("instant", False)
    super_host = request.GET.get("super_host", False)

    room_types = models.RoomType.objects.all()
    amenities = models.Amenity.objects.all()
    facilities = models.Facility.objects.all()

    form = {
        "city": city,
        "s_room_type": room_type,
        "s_country": country,
        "price": price,
        "guests": guests,
        "bedrooms": bedrooms,
        "beds": beds,
        "baths": baths,
        "s_amenities": s_amenities,
        "s_facilities": s_facilities,
        "instant": instant,
        "super_host": super_host,
    }

    choices = {
        "countries": countries,
        "room_types": room_types,
        "amenities": amenities,
        "facilities": facilities,
    }
    context = {**form, **choices}

    return render(request, "rooms/search.html", context)