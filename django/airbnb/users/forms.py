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