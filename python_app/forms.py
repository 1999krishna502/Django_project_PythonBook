from django import forms
from .views import *

class register_forms(forms.Form):
    fullname = forms.CharField(max_length=30)
    username = forms.CharField(max_length=30)
    email = forms.EmailField()
    image = forms.FileField()
    password = forms.CharField(max_length=30)
    confirm_password = forms.CharField(max_length=30)


class login_forms(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=30)

class course_reg_forms(forms.Form):
    fname = forms.CharField(max_length=30)
    lname = forms.CharField(max_length=30)
    DOB = forms.DateField()
    gender = forms.CharField(max_length=30)
    address1 = forms.CharField(max_length=30)
    address2 = forms.CharField(max_length=30)
    city = forms.CharField(max_length=30)
    phone = forms.IntegerField()
    email = forms.EmailField()
    course = forms.CharField(max_length=50)
    amount = forms.IntegerField()

class course_login_forms(forms.Form):
    email = forms.EmailField()
class admin_forms(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30)

class news_feed_form(forms.Form):
    topic = forms.CharField(max_length=300)
    content = forms.CharField(max_length=3000)

class video_notes_forms(forms.Form):
    video_name = forms.CharField(max_length=30)
    video_file = forms.FileField()
    pdf_name = forms.CharField(max_length=30)
    pdf_file = forms.FileField()

class teachers_form(forms.Form):
    name = forms.CharField(max_length=30)
    email = forms.EmailField()
    password = forms.CharField(max_length=30)
    confirm_password = forms.CharField(max_length=30)

class teachers_login_form(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=30)

class confirm_form(forms.Form):
    confirm = forms.BooleanField()
