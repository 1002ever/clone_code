from django.db import models

# Create your models here.
class TimeStampedModel(models.Model):

    """ Time Stamped Model """

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # 아래와 같이 설정해줘야 이 모델을 DB로 올리지 않는다.
    # 이 모델은 단지 여러 app 에서 사용될 필드를 미리 정의해놓는 용도
    # 즉 추상 모델인 셈.
    class Meta:
        abstract = True