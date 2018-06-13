# -*-coding:utf-8-*-
from django import forms
from common import final
from dateutil.relativedelta import relativedelta
import re
import datetime


class ShareSaveForm(forms.Form):

    form_name_value = forms.CharField(max_length=50, min_length=1, required=True)
    form_sex_value = forms.IntegerField(max_value=2, required=True)
    form_birthday_value = forms.DateField(required=False)
    form_phone_value = forms.CharField(max_length=11, required=False)
    form_origin_value = forms.CharField(max_length=200, required=False, widget=forms.Textarea)
    form_old_address_value = forms.CharField(max_length=30, required=False)
    form_new_address_value = forms.CharField(max_length=30, required=False)

    form_photo_value_1 = forms.ImageField(required=False)
    form_photo_description_1 = forms.CharField(max_length=200, required=False, widget=forms.Textarea)
    form_photo_value_2 = forms.ImageField(required=False)
    form_photo_description_2 = forms.CharField(max_length=200, required=False, widget=forms.Textarea)
    form_photo_value_3 = forms.ImageField(required=False)
    form_photo_description_3 = forms.CharField(max_length=200, required=False, widget=forms.Textarea)
    form_photo_value_4 = forms.ImageField(required=False)
    form_photo_description_4 = forms.CharField(max_length=200, required=False, widget=forms.Textarea)

    def clean_form_name_value(self):
        name = self.cleaned_data.get('form_name_value')
        if not re.search(u'^[a-zA-Z0-9\u4e00-\u9fa5]+$', name):
            raise forms.ValidationError('姓名不可乱填哦')
        if name in final.FinalList.DIRTY_LIST:
            raise forms.ValidationError('你的名字很特殊啊')
        return name

    def clean_form_birthday_value(self):
        birthday = self.cleaned_data.get('form_birthday_value')
        if birthday is not None:
            now = datetime.datetime.now()
            now_date = datetime.date(now.year, now.month, now.day)
            year = relativedelta(now_date, birthday).years
            if year <= 0 or year >= 150:
                raise forms.ValidationError('你的年龄不适合使用')
        return birthday

    def clean_form_phone_value(self):
        phone = self.cleaned_data.get('form_phone_value')
        if phone != '':
            if len(phone) != 11:
                raise forms.ValidationError('手机号长度应为11位')
            if not re.search('^\d+$', phone):
                raise forms.ValidationError('手机号只能是数字')
        return phone

    def clean_form_old_address_value(self):
        address = self.cleaned_data.get('form_old_address_value')
        if address != '':
            if len(re.findall('-', address)) != 2:
                raise forms.ValidationError('故乡住址有误')
        return address

    def clean_form_new_address_value(self):
        address = self.cleaned_data.get('form_new_address_value')
        if address != '':
            if len(re.findall('-', address)) != 2:
                raise forms.ValidationError('现住址有误')
        return address
