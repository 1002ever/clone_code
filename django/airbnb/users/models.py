import uuid
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.mail import send_mail
from django.utils.html import strip_tags
# 템플릿 로드 & 그를 string으로 바꿔주는 함수 import
from django.template.loader import render_to_string

# Create your models here.
class User(AbstractUser):   

    # 어디서 해당 클래스 이용 시, Description을 달아주는 셈
    """ Custom User Model """

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"

    GENDER_CHOICES = (
        # 앞이 DB에 저장 값, 뒤가 페이지에 보여질 값
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_OTHER, "Other"),
    )

    LANGUAGE_ENGLISH = "en"
    LANGUAGE_KOREAN = "ko"

    LANGUAGE_CHOICES = (
        (LANGUAGE_ENGLISH, "English"),
        (LANGUAGE_KOREAN, "Korean"),
    )

    CURRENCY_USD = "usd"
    CURRENCY_KRW = "krw"

    CURRENCY_CHOICES = (
        (CURRENCY_USD, "USD"),
        (CURRENCY_KRW, "KRW"),
    )

    LOGIN_EMAIL = "email"
    LOGIN_GITHUB = "github"
    LOGIN_KAKAO = "kakao"

    LOGIN_CHOICES = (
        (LOGIN_EMAIL, "Email"),
        (LOGIN_GITHUB, "Github"),
        (LOGIN_KAKAO, "Kakao"),
    )

    # null = True 만으로는 해당 값을 공백으로 둔 채로 저장이 불가
    # null = True 는 DB에 값을 저장하지 않아도 된다는 의미
    # blank = True 는 페이지에서 값을 입력하지 않아도 된다는 의미
    avatar = models.ImageField(upload_to="avatars", blank=True)
    gender = models.CharField(
        choices=GENDER_CHOICES, max_length=10, blank=True
    )
    bio = models.TextField(blank=True)
    birthdate = models.DateField(null=True)

    # max_length는 DB에 저장될 최대 문자열 길이
    language = models.CharField(
        choices=LANGUAGE_CHOICES, max_length=2, blank=True, default=LANGUAGE_KOREAN,
    )
    currency = models.CharField(
        choices=CURRENCY_CHOICES, max_length=3, blank=True, default=CURRENCY_KRW,
    )
    
    superhost = models.BooleanField(default=False)

    # 이메일 전송 확인 관련
    email_verified = models.BooleanField(default=False)
    email_secret = models.CharField(max_length=20, default="", blank=True)

    # 깃헙 로그인 관련
    login_method = models.CharField(
        max_length=50, choices=LOGIN_CHOICES, default=LOGIN_EMAIL
    )

    def verify_email(self):
        if self.email_verified is False:
            secret = uuid.uuid4().hex[:20]
            self.email_secret = secret

            html_message = render_to_string("emails/verify_email.html", {"secret": secret,})
            # 제목, 메시지, 발신인 이메일주소, 받는 주소들, 에러 처리 방식
            send_mail(
                "Verify Airbnb Account",
                # html 태그를 벗긴 상태를 return하는 함수
                # 어떤 경우, html 태그를 못 보내는 경우도 있어서
                # 이런 text도 미리 준비 해두는 것
                strip_tags(html_message),
                settings.EMAIL_FROM,
                [self.email],
                fail_silently=False,
                html_message=html_message,  
            )

            self.save()
        return