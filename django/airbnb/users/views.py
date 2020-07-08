import os
import requests
from django.shortcuts import render, redirect, reverse
from django.views import View
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib.auth import authenticate, login, logout
from django.core.files.base import ContentFile
from django.contrib.auth.forms import UserCreationForm
from . import forms, models



# 로그인 요소 수동 작성

# class LoginView(View):
    
#     def get(self, request):
#         form = forms.LoginForm(initial={"email": "itn@las.com"})
#         context = {
#             "form": form,
#         }
#         return render(request, "users/login.html", context)

#     def post(self, request):
#         form = forms.LoginForm(request.POST)

#         if form.is_valid():
#             email = form.cleaned_data.get("email")
#             password = form.cleaned_data.get("password")

#             # 인증되면 User를 return 해줌
#             user = authenticate(request, username=email, password=password)
            
#             # 인증안되면 None일 것이므로
#             if user is not None:
#                 login(request, user)
#                 return redirect(reverse("core:home"))

#         context = {
#             "form": form,
#         }
#         return render(request, "users/login.html", context)

def log_out(request):
    logout(request)
    return redirect(reverse("core:home"))


# 로그인 짜여져 있는 방법
# -> 이 방법은 email이 아니라 username을 쓰는 것으로
#    고정되어 있음.. 이 점이 불편한 점.
#    원하는 필드로 로그인 요청하려면, 위의 방법처럼
#    수동으로 작성해줘야 함

class LoginView(FormView):

    template_name = "users/login.html"
    form_class = forms.LoginForm
   
    # generic view에서는 타이밍 로딩 문제로
    # reverse 사용 시 문제가 된다.
    # 해당 폼을 로딩하는 시점에
    # 다른 곳의 url 및 템플릿이 로딩되지 않았기 때문
    # success_url = reverse("core:home")

    # reverse_lazy를 쓰면 바로 URL을 작성해놓는 것이 아니라
    # 나중에 필요할 때 URL을 작성함.
    success_url = reverse_lazy("core:home")

    # 초기값도 줄 수 있음
    initial = {
        "email": "1002ever@naver.com"
    }

    # FormView를 쓰면 is_valid 등을 자동으로 해주지만,
    # 사용자가 정한 폼의 유효성 검사를 하려면
    # 아래와 같이 오버라이딩 해주면 됨

    # 사용자 설정의 form_valid
    # form 이라는 변수는 위에서 form_class를 정해줄 때
    # 자동으로 들어간다.
    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)

        return super().form_valid(form)


class SignupView(FormView):
    template_name = "users/signup.html"
    
    # 수동 폼 작성한 것을 할당
    #   => 장고가 제공하는 폼 기능을 사용할 수 없음
    # form_class = forms.SignupForm
    form_class = UserCreationForm

    success_url = reverse_lazy("core:home")

    initial = {
        "first_name": "yw",
        "last_name": "k",
        "email": "1002ever@naver.com",
    }

    # 폼이 유효할 떄 수행하는 함수 => 회원가입 완료 시 수행
    def form_valid(self, form):
        # DB 저장
        form.save()

        # 가입 완료 시 로그인
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        
        user.verify_email()

        return super().form_valid(form)


def complete_verification(request, key):
    try:
        user = models.User.objects.get(email_secret=key)
        user.email_verified = True
        user.email_secret = ""
        user.save()
        # to do: add success message
    except models.User.DoesNotExist:
        # to do: add error message
        pass

    return redirect(reverse("core:home"))

# github oauth apps 사용법 documentation
# https://developer.github.com/apps/building-oauth-apps/authorizing-oauth-apps/

# ㄱ. github_login 함수 진입 => 깃헙 로그인 페이지 이동
# ㄴ. authorize 성공 시 callback 함수로 가게끔 redirect
#     => 이 과정에서 request에는 code가 담김
# ㄷ. code 및 여러 인자를 쓰면 token을 받아 올 수 있음.
#     => 이를 requests 라이브러리를 이용하여 받아옴
# ㄹ. token을 이용하여 github api를 가져옴
# ㅁ. github api를 받아오는 데 성공하면 이를 바탕으로 회원가입 및 로그인 진행

def github_login(request):

    client_id = os.environ.get("GH_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/github/callback"

    return redirect(f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user")

class GithubException(Exception):
    # 원하는 만큼 exception 추가 가능
    pass

def github_callback(request):

    try:
        # 깃헙 로그인 시 코드를 줌
        # access token을 받기 위한 코드를 주는 것
        # token을 갖게 되면 github api에 접근이 가능

        client_id = os.environ.get("GH_ID")
        client_secret = os.environ.get("GH_SECRET")
        code = request.GET.get("code", None)

        if code is not None:
            token_request = requests.post(
                f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}",
                headers={"Accept": "application/json"}
            )
            token_request_json = token_request.json()
            error = token_request_json.get("error", None)

            if error is not None:
                raise GithubException()
            else:
                access_token = token_request_json.get("access_token")
                profile_request = requests.get(
                    "https://api.github.com/user",
                    headers={
                        "Authorization": f"token {access_token}",
                        "Accept": "application/json",                   
                    },
                )

                # 요청이 제대로 이뤄지고, github API 까지 따왔다면
                # 받아온 json에 login 값이 있을 것이므로
                # status 용도로 username을 지정
                profile_json = profile_request.json()
                username = profile_json.get("login", None)
                print(profile_json)

                if username is not None:
                    # profile_json에 email, name, bio이 없어서
                    # 일단은 임시로 값 할당..
                    name = "kyw"
                    email = "1002ever@naver.com"
                    bio = ""
                    try:
                        # 이미 해당 이메일로 유저가 있고,
                        # 그게 깃헙으로 가입한 사람이라면
                        # 그냥 단순 로그인
                        user = models.User.objects.get(email=email)
                        if user.login_method != models.User.LOGIN_GITHUB:
                            raise GithubException()
                    except models.User.DoesNotExist:
                        user = models.User.objects.create(
                            email=email,
                            first_name=name,
                            username=email,
                            bio=bio,
                            login_method=models.User.LOGIN_GITHUB,
                            email_verified=True,
                        )
                        # 사용 안 할 비밀번호 셋팅
                        user.set_unusable_password()
                        user.save()
                    login(request, user)
                    return redirect(reverse("core:home"))
                else:
                    raise GithubException()
        else:
            raise GithubException()
    except GithubException:
        # send error message
        return redirect(reverse("users:login"))


# 카카오 로그인

# ㄱ. kakao developers에서 내 앱 생성
# ㄴ. app key를 전달하며, 인증 페이지로 이동
#     => 이는 콜백함수 & 콜백 페이지 uri를 kakao developers에서 등록해줘야 함
# ㄷ. 인증이 완료되면 코드를 줌
# ㄹ. 코드로 토큰을 요청

def kakao_login(request):
    app_key = os.environ.get("K_KEY")
    redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
    return redirect(f"https://kauth.kakao.com/oauth/authorize?client_id={app_key}&redirect_uri={redirect_uri}&response_type=code")

class KakaoException(Exception):
    pass

def kakao_callback(request):
    try:
        app_key = os.environ.get("K_KEY")
        redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
        code = request.GET.get("code")
        
        # 코드로 토큰 요청
        token_request = requests.get(f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={app_key}&redirect_uri={redirect_uri}&code={code}")

        # response를 json으로 return
        token_json = token_request.json()
        error = token_json.get("error", None)
        
        if error is not None:
            raise KakaoException()

        access_token = token_json.get("access_token")
        
        # 토큰으로 api 요청
        profile_request = requests.get(
            "https://kapi.kakao.com//v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"}
        )

        profile_json = profile_request.json()
        email = profile_json.get("kakao_account").get("email")

        if email is None:
            raise KakaoException()

        properties = profile_json.get("properties")
        nickname = properties.get("nickname")
        profile_image = properties.get("profile_image")

        try:
            user = models.User.objects.get(email=email)
            print("유저있음?", user)
            if user.login_method != models.User.LOGIN_KAKAO:
                raise KakaoException()
        except models.User.DoesNotExist:
            user = models.User.objects.create(
                email=email,
                username=email,
                first_name=nickname,
                login_method=models.User.LOGIN_KAKAO,
                email_verified=True,
            )
            user.set_unusable_password()
            user.save()

            if profile_image is not None:
                photo_request = requests.get(profile_image)
                
                # ImageField와 FileField는 아래와 같이
                # 저장이 가능.. => 장고 문서도 한 번 다시 보기.
                # 인자는 순서대로 저장할 파일이름, 파일

                # ContentFile은 0, 1로만 이뤄진 가공되지 않은 data형태를
                # 파일 형태로 포장하여 전달하는 역할

                user.avatar.save(f"{nickname}-avatar", ContentFile(photo_request.content))

        login(request, user)
        return redirect(reverse("core:home"))

    except KakaoException:
        return redirect(reverse("users:login"))