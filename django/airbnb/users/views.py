from django.shortcuts import render, redirect, reverse
from django.views import View
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib.auth import authenticate, login, logout
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
    form_class = forms.SignupForm
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