from django import forms
import re
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from .models import Student

class RegistrationForm(forms.Form):
    email = forms.EmailField(label='Email')
    first_name = forms.CharField(label='Tên')
    username = forms.CharField(label='Tài Khoản',max_length=30)
    password1 = forms.CharField(label='Mật khẩu', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Nhập Lại Mật khẩu', widget=forms.PasswordInput())

    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1= self.cleaned_data['password1']    
            password2= self.cleaned_data['password2']    
            if password1 == password2 and password1 :
                return password2
        raise forms.ValidationError('Mật khẩu không hợp lệ!')

    def clean_username(self):
        username = self.cleaned_data["username"]
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError("tên tk có ký tự đặt biệt!")
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist: 
            return username
        raise forms.ValidationError("tài khoản đã tồn tại")

    def save(self):
        user = User.objects.create_user(username=self.cleaned_data['username'], email =self.cleaned_data['email'], password=self.cleaned_data['password1'], first_name = self.cleaned_data['first_name'])
        Student.objects.create(user = user,name = self.cleaned_data['first_name'])