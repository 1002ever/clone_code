from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("core.urls", namespace="core")),
    # path("users", include("users.urls", namespace="users")),
    path("rooms/", include("rooms.urls", namespace="rooms")),
]

# 개발자 모드일 때는 로컬 파일루트로 들어오도록 설정
# 개발자 모드가 아닐 때는 AWS 같은 서버로 내 파일을 upload할 것이므로
# 그 경우에는 달리 경로를 설정해줘야 함
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)