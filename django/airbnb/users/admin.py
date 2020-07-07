from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models

# Register your models here.

# models.py 의 User를 admin 페이지에서 리스트로 정리하여 보여주고 싶을 떄.
# 데코레이터로 연동해줄 모델 설정 후
# admin.ModelAdmin 을 상속한 클래스에서 list_display나 list_filter를 설정

# @admin.register(models.User)
# class CustomUserAdmin(admin.ModelAdmin):

#     """ Custom User Admin """
#     list_display = ("username", "gender", "language", "currency", "superhost")
#     list_filter = ("language", "currency", "superhost",)


# UserAdmin은 admin 페이지에서 User 모델을
# 더 다채롭게 이용하도록 만들어진 클래스
# 단, 커스터마이징한 fieldsets은 기본적으로 보이지 않으므로
# 보이게 하려면 직접 입력해줘야 함.

@admin.register(models.User)
class CustomUserAdmin(UserAdmin):

    """ Custom User Admin """

    fieldsets = UserAdmin.fieldsets + (
        (
            "Custom Profile",
            {
                "fields": (
                    "avatar",
                    "gender",
                    "bio",
                    "birthdate",
                    "language",
                    "currency",
                    "superhost",
                )
            }
        ),
    )

    list_filter = UserAdmin.list_filter + ("superhost",)

    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "language",
        "currency",
        "superhost",
        "is_staff",
        "is_superuser",
        "email_verified",
        "email_secret",
        "login_method",
    )