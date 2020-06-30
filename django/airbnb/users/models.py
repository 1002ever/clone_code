from django.contrib.auth.models import AbstractUser
from django.db import models

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

    # null = True 만으로는 해당 값을 공백으로 둔 채로 저장이 불가
    # null = True 는 DB에 값을 저장하지 않아도 된다는 의미
    # blank = True 는 페이지에서 값을 입력하지 않아도 된다는 의미
    avatar = models.ImageField(blank=True)
    gender = models.CharField(
        choices=GENDER_CHOICES, max_length=10, blank=True
    )
    bio = models.TextField(blank=True)
    birthdate = models.DateField(null=True)

    # max_length는 DB에 저장될 최대 문자열 길이
    language = models.CharField(
        choices=LANGUAGE_CHOICES, max_length=2, blank=True
    )
    currency = models.CharField(
        choices=CURRENCY_CHOICES, max_length=3, blank=True
    )
    
    superhost = models.BooleanField(default=False)