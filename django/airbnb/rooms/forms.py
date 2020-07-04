from django import forms
# 폼 필드 추가용 django_countries
from django_countries.fields import CountryField
from . import models


class SearchForm(forms.Form):

    # widget 속성은 폼에서 해당 input의 형태를 설정해주는 속성
    # help_text 속성은 해당 input 설명 메시지 덧붙이는 것

    city = forms.CharField(initial="Anywhere")
    country = CountryField(default="KR").formfield()
    room_type = forms.ModelChoiceField(required=False, empty_label="Any Kind", queryset=models.RoomType.objects.all())
    price = forms.IntegerField(required=False)
    guests = forms.IntegerField(required=False, help_text="How many people will be staying?")
    bedrooms = forms.IntegerField(required=False)
    beds = forms.IntegerField(required=False)
    baths = forms.IntegerField(required=False)
    instant_book = forms.BooleanField(required=False)
    superhost = forms.BooleanField(required=False)
    amenities = forms.ModelMultipleChoiceField(required=False, queryset=models.Amenity.objects.all(), widget=forms.CheckboxSelectMultiple)
    facilities = forms.ModelMultipleChoiceField(required=False, queryset=models.Facility.objects.all(), widget=forms.CheckboxSelectMultiple)
