## Django 시작 전 기초 개념



\*\*\* 파이썬 => 런타임 언어

​                         프로그램이 시작되었는데, 에러가 있으면 폭발,,

​						 => 그래서 `Linter`가 등장 => <u>코드를 치면서 에러가 생길 부분을 미리 감지</u>

​                         (( 컴파일 언어는 프로그램 시작 전 에러를 잡아줌 ))

​						 => 저장 시 줄 맞춤을 해주는 도구는 `Formatter` 

​                                =>  니콜라스가 추천한 Formatter는 black



\*\*\* 파이썬 코드 스타일 가이드 => PEP(Python Enhancement Proposals)



**Tip. 파이썬은 한 줄 당 79자를 넘어가면 안 된다.**  => Linter 내 규칙 (E501)

​		=> 기존의 모니터가 작았기 떄문

​			  모니터가 넓어진 현재는 방해되기도 하는 규칙,

​			  => settings.json 에서   `"python.linting.flake8Args": ["--max-line-length=88"] ` 와 같이

​                   규칙을 수정할 수 있음



### \*\* arguments & keyword arguments

- 개수 제한 없이 인자를 주고 싶을 때 사용하는 개념

  ```python
  # 예시
  
  def plus(a, b, *args, **kwargs):
      print(args)    # (1,1,1,1,1) - 튜플 형태
      print(kwargs)  # {'a': True, 'b': True, 'c': True} - 딕셔너리 형태
      return a+b
  
  # 1은 7개
  plus(1,1,1,1,1,1,1,a=True,b=True,c=True)
  
  ```

  

### \*\* 객체지향 프로그래밍

```python
class Car():
    wheels = 4
    doors = 4
    windows = 4
    seats = 4
    
    #def start():
    #    print("I started")
    
    def start(self):
        print(self.color)
        print("I started")
        
    def __str__(self):
        return "오버라이딩 됨"
    
    # 생성자, 객체 생성 시 자동 호출 됨
    def __init__(self, **kwargs):
                     # color나 price가 주어지지 않으면, black이나 20이 디폴트
        self.color = kwargs.get('color', 'black')
        self.price = kwargs.get('price', '$20')
        
# class의 인자에 다른 클래스 명을 넣어주면 Extends(상속) 함
class Convertible(Car):
    # 재정의하면서 기존 __init__ 기능은 전부 사용하고 싶을 때?
    #    => 부모의 __init__ 도 수행해주면 됨
    # 자신 시점에서 __init__이 덮인거지, 부모의 __init__이 사라진 것은 아니기 때문에
    # super로 접근하면 호출이 가능
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.time = kwargs.get("time", 10)
    
    def take_off(self):
        return "taking off"
    
porche = Car()
porche.color = "Red"

# 아래 호출 시 클래스에서 한 인자를 안 주면 에러 듬
# 파이썬이 메소드에는 자기 자신(인스턴스)을 자동으로 인자로 넣어주기 때문
# 메소드 정의 시 반드시 한 인자 이상을 지정해줘야 함
# => 첫 인자는 자기 자신이므로 보통 self 로 이름 지음
porche.start()	# Red
				# I started
    
    
# 출력하고 싶다는 말은 string으로 변환이 필요하다는 말
# 클래스 자체 메소드로 __str__를 가짐(문자열로 바꿔주는)
#   => print(객체) 시 __str__을 자동으로 호출
# 클래스 정의 시 이를 오버라이딩 하여 재정의 된 return이 출력 됨
print(porche)   # 오버라이딩 됨


sonata = Car(color="green", price="$40")
print(sonata.color, sonata.price)  # green $40



```



### \*\* pipenv 가 필요한 이유 및 Django 프로젝트 환경 설정

- Node의 npm 처럼 Python 만의 패키지 관리자가 없음

  => pip(Package Installer for Python)로 패키지가 관리되는데, 이는 패키지가 전역으로 관리된다는 의미.

  => <u>보통 프로젝트 별로 패키지를 관리하기를 원함</u>

- pipenv 는 일종의 `npm + package.json`

  - pip3 install pipenv     => python 3 을 기반으로 하는 pipenv를 쓸 것이므로,

    ​                                           다른 버전에 씌워지지 않으려면 pip3 을 이용해야 함

  - pipenv --three             => python 3 기반 (가상 환경)프로젝트를 생성

    ​                                      => 성공적으로 생성 시, Pipfile이 만들어짐(`package.json 역할`)

  - pipenv shell                 => 가상환경으로 진입

  - pipenv install Django==버전

  - touch .gitignore 생성 후 gitignore python 검색하여 나온 깃헙 글 복사해서 붙여넣기

    

    **\# 큰 프로젝트 시 아래와 같이 구조를 설계하는 것이 바람직** 

  - django-admin startproject config

  - config 폴더 명을 아무렇게나 바꾸고,

    안에 config 폴더, manage.py 를 바깥으로 꺼내기

  - Ctrl + Shift + P 로 명령 팔레트 열고, python: select interpreter 실행 후

    현재 프로젝트에 적용된 python 선택

    => **<u>.vscode 라는 폴더가 생성됨</u>**

  - 명령 팔레트 열고, python: Select Linter 실행 후 <u>원하는 Linter</u>를 선택

    \<\< airbnb 클론 에서는 flake8 를 선택 \>\>

    - pipenv install flake8 --dev     => Linter 설치

  - Formatter 설치

    \<\< airbnb 클론 에서는 black 을 선택 >\>

    - pip install black --dev --pre










### Django 프로젝트 진행하면서 기억할 내용들

- \_\_init\_\_.py 가 있는 폴더여야지, 외부에서 그 폴더 내 .py 들을 import 하여 이용할 수 있음

  => 이건 더 공부가 필요하겠다..

- settings.py 내 TIME_ZONE = 'Asia/Seoul' 설정 시 한국 시간으로 설정 가능

- Django의 application 은 한 문장으로 정의내릴 수 있는 기능 단위

  ex) rooms => 방을 생성/읽기/수정/삭제 하는 기능

  ​      <u>'그리고' 라는 표현이 필요하다면 다른 App 으로 분리할 것.</u>

  > - application 명은 항상 복수형
  >
  > - application 중 django는 이미 messages 를 가지고 있음.
  >
  >   => chat 기능을 담을 app 생성 시 messages를 만들어서 충돌하는 일이 없게끔 하기.
  >
  >   ​     airbnb 클론에서는 conversations 로 생성

  

- 모든 국가명이 필요할 땐?   =>   `django-countries 깃헙 문서 참조`

  - django-countries 패키지 다운
    - pipenv install django-countries 나 pip install django-countries
  - settings.py 에 app 등록 
    - "django_countries"
  - 이를 사용할 models.py 에서 import
    - from django_countries.fields import CountryField
  - 필드 값 부여
    - country = CountryField()

  

- 장고 프로젝트에서 import 순서?

  1. python 관련 패키지     ex) os
  2. django 관련 패키지     ex) django.db
  3. 외부 패키지                  ex) django_countries                   

  4. 내가 만든 패키지       



- IntegerField 는 정수,

  DecimalField 는 소수

  

- URL 요청은 모두 **GET 요청**

  => 루트/?page=1&city=Seoul  페이지로 들어가면

  ​      <u>request.GET 값은 {'page': ['2'], 'city': ['seoul']} 의 QueryDict 를 가진다.</u>

  

- Django의 verbose_name_plural 기본 설정 때문에   `<< 이는 class Meta 의 기본 설정 때문 >>`

  각 클래스의 이름 뒤에는 s가 자동으로 붙는다.

  => 의도치 않게 문법상 올바르지 않은 모습으로 s가 붙는 경우 발생

  ​     ex) Amenity => Amenitys     원래는 Amenities

  (( 참고 : docs.djangoproject.com/en/2.2/ref/models/options/ ))

  => <u>class Meta를 커스터마이징 해야 함</u>
  
  
  
- Django 프로젝트인 pipenv shell을 python과 연동시키려면?

  - python 내에는 django가 깔려있지 않음.

    => pipenv 내에 Django를 깔았기 때문에, python 호출 시 해당 쉘로 연동 시켜줘야 함

    => `python manage.py shell`

    

  - airbnb 클론 시 User 모델을 살펴볼 때 썼던 명령어

    - from users.models import User

    - User.objects         =>  `UserManager 오브젝트`가 불려옴

      ​                                => ***DB로부터 elements를 가져오게 해주는 오브젝트***

    - User.objects.all()   => 모든 User objects를 **<u>QuerySet</u>**으로 불러옴

      ​                                 => **<u>QuerySet</u>**은 filter를 포함한 여러 기능을 담는 Object

    - kyw = User.objects.get(username="kyw")

    - kyw.room_set                                                      

      => <u>유저를 불러와서, 그를 참조하는 room data로 접근하기</u>  => `RelatedManager 오브젝트` 덕분

      => <u>ManyToMany 관계도 마찬가지</u>

    - kyw.room_set.all()   처럼 UserManager 처럼 사용이 가능

      - room_set 으로 접근하는 것이 아니라 이름을 지정해주려면

        해당 Model 외래키 설정 시 `related_name = "원하는 이름"` 으로 값을 지정해주면 됨

  

- Django 프로젝트 시 시간 불러올 때?

  => `from django.utils import timezone`

  - 왜 python time 패키지를 사용하지 않나?
    - <u>Django app 서버의 시간을 사용하기 위해서.</u>

  

- Django 프로젝트에 Media 업로드 시?

  - settings.py 에 MEDIA_ROOT 를 설정하여 루트를 지정해줘야 함

    - <u>**절대 경로로만 지정해줘야 한다.**</u>

      **=> BASE_DIR 이 절대 경로를 저장하고 있다.**

      `MEDIA_ROOT = os.path.join(BASE_DIR, "원하는 폴더명")`

    - ImageField를 다룰 모델에서 upload_to 로 폴더 구분해주기

      ex) avatar = models.ImageField(upload_to="avatars", blank=True)   

      ​      => <u>원하는 폴더명/avatars 에 저장됨</u>

      ​      file = models.ImageField(upload_to="room_photos")

    

  - 그 후 MEDIA_URL 도 설정해주기

    => URL 로 해당 폴더에 접근할 수 있도록 설정해주는 것

    

  - urls.py 에 media path 추가해주기

    - urls.py 에 settings.py import

      `from django.conf import settings`

      > 왜 from . import settings 가 아닐까?
      >
      > ​	파일명은 바뀔 수 있음.
      >
      > ​	하지만 Django가 정한 settings 의 경로는 바뀌지 않음
      >
      > ​	즉 from django.conf import setting 를 해주면, settings.py가 settings2.py 로 바뀌어도
      >
      > ​	해당 파일을 적절히 import 함

      ```python
      from django.contrib import admin
      from django.urls import path, include
      from django.conf import settings
      from django.conf.urls.static import static
      
      urlpatterns = [
          path('admin/', admin.site.urls),
      ]
      
      # 개발자 모드일 때는 로컬 파일루트로 들어오도록 설정
      # 개발자 모드가 아닐 때는 AWS 같은 서버로 내 파일을 upload할 것이므로
      # 그 경우에는 달리 경로를 설정해줘야 함
      if settings.DEBUG:
          urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
      ```

    

    

- 장고 페이지에서 html 태그(img) 로 Thumbnail 같은 것들을 보여주고 싶을 때?

  => **그냥 \<img src="경로"\> 이런식으로 Django 페이지로 전달하면, 이를 수행하지 않음**

  ​	<u>**왜? => 부정한 사용자가 script 를 수동적으로 입력하여 DB에 접근하면 곤란하기 떄문**</u>

  ​	=> 개발 시 코드에서 수행해도 되는 코드라고 명시가 필요

  ```python
  # 예시
  from django.utils.html import mark_safe
  
  mark_safe(f"<img width='70px' src='{obj.file.url}'/>")
  ```

  

- Django 프로젝트에서 DB를 일괄적으로 저장하고 싶을 때?

  => Command 설정

  - app 폴더 내에 management 폴더 생성

  - management 폴더 내 \_\_init\_\_.py 파일 생성

  - management 폴더 내 commands 폴더 생성

  - commands 폴더 내 \_\_init\_\_.py 파일 생성

  - commands 폴더 내 \`원하는파일명\`.py 생성  => <u>이것이 데이터 생성을 수행할 파이썬 파일</u> 

    - \`원하는파일명\`.py 속에 Command 클래스 작성 => BaseCommand 상속 필요

    - 해당 클래스에는 handle 함수가 필수로 정의되어야 함

      ```python
      # 예시
      from django.core.management.base import BaseCommand
      from rooms.models import Facility
      
      class Command(BaseCommand):
          
          help = 'This command creates facilities.'
      
          def handle(self, *args, **options):
              facilities = [
                  "Private entrance",
                  "Paid parking on premises",
                  "Paid parking off premises",
                  "Elevator",
                  "Parking",
                  "Gym",
              ]
              for f in facilities:
                  Facility.objects.create(name=f)
              self.stdout.write(self.style.SUCCESS("Facilities created!"))
      ```

    - 터미널에서 python manage.py \`원하는파일명\`  입력 시 handle 함수 수행

  

- Django 프로젝트에서 DB에 fake 데이터를 생성하여 저장하고 싶을 때?

  => django-seed 활용

  ​	   \# 장고 시드 설치

  - pipenv install django_seed

    \# INSTALLED_APPS 에 django_seed 추가

  - INSTALLED_APPS = [ ..., "django_seed", ]

  - 

  

- Model 관련

  ​	   **\# Model 확인 및 migration 파일 생성**

  - python manage.py makemigrations

    

    **\# Django와 migration(DB)을 연동**

  - python manage.py migrate

    

    **\# User 모델 Customizing**

  - settings.py 에서 맨 아래 AUTH_USER_MODEL 이라는 변수에 값을 넣기

    => 기존의 AUTH_USER_MODEL 을 덮기 위해

  - AUTH_USER_MODEL에 넣을 model 을 설정

    ex) models.py

    ```python
    # users 의 models.py
    from django.contrib.auth.models import AbstractUser
    from django.db import models
    
    # Create your models here.
    class User(AbstractUser):   
        pass
    ```

    ex) settings.py

    ```python
    # INSTALLED_APPS 에 User 모델이 있는 app 추가 후
    
    AUTH_USER_MODEL = '앱이름.유저모델이름'
    ```

    ex) admin.py

    ```python
    # 이렇게 해줘야 admin 페이지에서 해당 모델을 확인할 수 있다.
    from django.contrib import admin
    from . import models
    
    # Register your models here.
    @admin.register(models.User)
    class CustomUserAdmin(admin.ModelAdmin):
        pass
    
    # admin.site.register(models.User) 로 해도 보이는데 차이가 뭐지..?
    ```

    

  - ImageField를 사용하려면

    => <u>Pillow 패키지를 다운로드 해야 함</u>

    

  - CHOICES, CharField에 값을 선택하게끔 할 수 있다.

    ex) 사용 예시

    ```python
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
    
        avatar = models.ImageField(null=True)
        gender = models.CharField(choices=GENDER_CHOICES, max_length=10, null=True)
        bio = models.TextField(default="")
    ```

  

- 모델의 레코드를 정렬하려면?

  - class Meta 내부에 ordering 변수에다가 기준 값을 리스트로 주면 된다.

    ex)

    ```python
    class RoomType(AbstractItem):
        class Meta:
            verbose_name = "Room Type"
            ordering = ['name']
    ```

    

