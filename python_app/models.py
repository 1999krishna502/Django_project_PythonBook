from django.db import models

# Create your models here.


class register_model(models.Model):
    fullname = models.CharField(max_length=30)
    username = models.CharField(max_length=30)
    email = models.EmailField()
    image = models.FileField(upload_to='python_app/static')
    password = models.CharField(max_length=30)
    balance=models.IntegerField()
    def __str__(self):
        return self.username

class course_reg_models(models.Model):
    choice = [
        ('Advanced Python','Advanced Python'),
        ('Python Fullstack Development', 'Python Fullstack Development'),
        ('Python for Data Science , AI & Development', 'Python for Data Science , AI & Development')
    ]
    fname = models.CharField(max_length=30)
    lname = models.CharField(max_length=30)
    DOB = models.DateField()
    gender = models.CharField(max_length=30)
    address1 = models.CharField(max_length=30)
    address2 = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    phone = models.IntegerField()
    email = models.EmailField()
    course = models.CharField(max_length=50)
    amount=models.IntegerField()

class deposit_model(models.Model):
    amount = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    uid = models.IntegerField()

class withdraw_model(models.Model):
    amount = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    uid = models.IntegerField()

class news_feed_model(models.Model):
    topic = models.CharField(max_length=100)
    content = models.CharField(max_length=200)
    date = models.DateField(auto_now_add=True)

class video_notes_model(models.Model):
    video_name = models.CharField(max_length=30)
    video_file = models.FileField(upload_to='python_app/static')
    pdf_name = models.CharField(max_length=30)
    pdf_file = models.FileField(upload_to='python_app/static')

class teachers_model(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    password = models.CharField(max_length=30)


class save_model(models.Model):
    uid=models.IntegerField()
    VNid=models.IntegerField()
    video_name = models.CharField(max_length=30)
    video_file = models.FileField(upload_to='python_app/static')
    pdf_name = models.CharField(max_length=30)
    pdf_file = models.FileField(upload_to='python_app/static')

class confirm_model(models.Model):
    confirm = models.BooleanField(default=False)