from django import forms
from . import models


class LoginForm(forms.Form):
    
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    # 하나하나 확인하는 방법

    # # 이건 약속된 이름
    # # 어떤 필드를 확인하고 싶으면
    # # clean_필드명 으로 작성해줘야 함
    # def clean_email(self):

    #     # 사용자가 입력한 이메일
    #     email = self.cleaned_data

    #     # 존재하면 email 을 clean_data 에 넣음
    #     # 존재하지 않으면 에러 메시지 출력
    #     try:
    #         models.User.objects.get(username=email)
    #         return email
    #     except models.User.DoesNotExist:\
    #         # 문제가 있는 폼 요소 위에 에러 메시지가 뜸
    #         raise forms.ValidationError("User does not exist")

    # def clean_password(self):
    #     email = self.cleaned_data.get("email")
    #     password = self.cleaned_data.get("password")
        
    #     try:
    #         user = models.User.objects.get(username=email)
    #         if user.check_password(password):
    #             return password
    #         else:
    #             raise forms.ValidationError("Password is wrong")
    #     except models.User.DoesNotExist:
    #         pass

    
    # clean 메소드로 한 번에 확인
    # `연관 데이터`를 한 번에 확인

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        try:
            user = models.User.objects.get(email=email)
            # 장고 자체 제공 함수 check_password
            if user.check_password(password):
                return self.cleaned_data
            else:
                self.add_error("password", forms.ValidationError("Password is wrong"))

        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("User does not exist"))


# 모델폼이 아니라 폼을 일일이 작성해주는 방법

class SignupForm(forms.Form):
    
    first_name = forms.CharField(max_length=80)
    last_name = forms.CharField(max_length=80)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password1 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            models.User.objects.get(email=email)
            raise forms.ValidationError("User already exists with that email")
        except models.User.DoesNotExist:
            return email

    def clean_password1(self):
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")

        if password != password1:
            raise forms.ValidationError("Password confirmation does not match")
        else:
            return password

    def save(self):
        first_name = self.cleaned_data.get("first_name")
        last_name = self.cleaned_data.get("last_name")
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        # 그냥 create가 아닌 create_user를 써야
        # password를 암호화하여 저장해줌
        # 순서대로 username, email, password를 인자로 받음
        user = models.User.objects.create_user(email, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()


# 폼과 모델을 자동으로 연동해주는
# 모델폼 활용
# => clean_data 와 save 를 자동으로 해준다.

# class SignupForm(forms.ModelForm):
#     class Meta:
#         model = models.User
#         fields = ["first_name", "last_name", "email",]

#     password = forms.CharField(widget=forms.PasswordInput)
#     password1 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

#     def clean_password1(self):
#         password = self.cleaned_data.get("password")
#         password1 = self.cleaned_data.get("password1")
#         if password != password1:
#             raise forms.ValidationError("Password confirmation does not match")
#         else:
#             return password

#     # ModelForm save 오버라이딩은
#     # Form 과 오버라이딩 인자가 다름
#     def save(self, *args, **kwargs):
#         email = self.cleaned_data.get("email")
#         password = self.cleaned_data.get("password")
#         user = super().save(commit=False)
#         user.username = email
#         # 패스워드를 암호화(해싱) 해줌
#         user.set_password(password)
#         user.save()
