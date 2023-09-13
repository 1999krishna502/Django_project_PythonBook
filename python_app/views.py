from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.http import HttpResponse
from .forms import *
from .models import *
import os

# Create your views here.

def index(request):
    a = news_feed_model.objects.all()
    return render(request,'index.html',{'a': a})

def success(request):
    return render(request,'success.html')

def register(request):
    if request.method=="POST":
        a=register_forms(request.POST,request.FILES)
        if a.is_valid():
            fn=a.cleaned_data['fullname']
            un=a.cleaned_data['username']
            em=a.cleaned_data['email']
            im=a.cleaned_data['image']
            psw=a.cleaned_data['password']
            cpsw=a.cleaned_data['confirm_password']
            a=register_model.objects.all()
            for i in a:
                if (un == i.username or em == i.email):
                    return HttpResponse('allready exist')
            else:
                if cpsw == psw:
                    b = register_model(fullname=fn, username=un, email=em, image=im,password=psw,balance=0)
                    b.save()
                    return redirect(login)
                else:
                    return HttpResponse("password doesn't match! ")
        else:
            return HttpResponse('registration failed invalid datas!')
    return render(request,'register.html')

def login(request):
    if request.method == "POST":
        a = login_forms(request.POST)
        if a.is_valid():
            em = a.cleaned_data['email']
            psw = a.cleaned_data['password']
            b = register_model.objects.all()
            for i in b:
                if i.email == em and i.password == psw:
                    request.session['id']=i.id
                    return redirect(myprofile)
            else:
                return HttpResponse('login failed')
    return render(request,'login.html')

def myprofile(request):
    try:
        id1=request.session['id']
        a=register_model.objects.get(id=id1)
        img=str(a.image).split('/')[-1]
        return render(request,'myprofile.html',{'a':a,'img':img})
    except:
        return redirect(index)

def logout_views(request):
    logout(request)
    return redirect(login)


def edit_myprofile(request,id):
    a = register_model.objects.get(id=id)
    img = str(a.image).split('/')[-1]
    if request.method=='POST':
        a.fullname = request.POST.get('fullname')
        a.username = request.POST.get('username')
        a.email = request.POST.get('email')
        a.save()
        return redirect(myprofile)
    return render(request,'edit_myprofile.html',{'a':a , 'img':img})

def edit_image(request,id):
    a = register_model.objects.get(id=id)
    img = str(a.image).split('/')[-1]
    if request.method == 'POST':
        if request.FILES.get('image') == None:
            a.save()
        else:
            a.image = request.FILES['image']
            a.save()
        a.save()
        return redirect(myprofile)
    return render(request,'edit_image.html',{'a': a, 'img': img})

def delete(request,id):
    a = register_model.objects.get(id=id)
    os.remove(str(a.image))
    a.delete()
    return redirect(register)

def add_money(request,id):
    a = register_model.objects.get(id=id)
    if request.method == 'POST':
        am = request.POST.get('amount')
        password = request.POST.get('password')
        request.session['am'] = am
        if password == a.password:
            a.balance += int(am)
            a.save()
            b = deposit_model(amount=am, uid=request.session['id'])
            b.save()
            return redirect(add_money_success)
        else:
            return HttpResponse('failed')
    return render(request, 'add_money.html')

def add_money_success(request):
    am=request.session['am']
    return render(request,'addamountsuccess.html',{'am':am})

def add_money_display(request):
    a=deposit_model.objects.all() #fetchall
    id=request.session['id']
    return render(request,'add_money_display.html',{'a':a,'id':id})

def withdraw(request,id):
    a = register_model.objects.get(id=id)
    if request.method == 'POST':
        am = request.POST.get('amount')
        password = request.POST.get('password')
        request.session['am'] = am
        if password == a.password:
            if (a.balance >= int(am)):
                a.balance -= int(am)
                a.save()
                b = withdraw_model(amount=am, uid=request.session['id'])
                b.save()
                return redirect(withdraw_success)
            else:
                return HttpResponse('insufficient balance...')
        else:
            return HttpResponse('password incorrect..')
    return render(request, 'withdraw.html')

def withdraw_success(request):
    am=request.session['am']
    return render(request,'withdraw_success.html',{'am':am})

def withdraw_display(request):
    a=withdraw_model.objects.all() #fetchall
    id=request.session['id']
    return render(request,'withdraw_display.html',{'a':a,'id':id})

def checkbalance(request,id):
    a = register_model.objects.get(id=id)
    if request.method == 'POST':
        request.session['email'] = a.email
        request.session['balance'] = a.balance
        password = request.POST.get('password')
        if password == a.password:
            return redirect(balance_display)
        else:
            return HttpResponse('wrong password..')
    return render(request,'checkbalance.html')

def balance_display(request):
    email = request.session['email']
    ba = request.session['balance']
    return render(request,'balance_display.html',{'balance':ba,'email':email})


# ******************************************* sequrity *************************************************************** #
def forgot_password(request):
    a=register_model.objects.all()
    if request.method=='POST':
        em=request.POST.get('email')
        for i in a:
            if(i.email==em):
                id=i.id
                subject="password change"
                message=f"http://127.0.0.1:8000/python_app/change_password/{id}"
                frm='akkunni222@gmail.com'
                to=em
                send_mail(subject,message,frm,[to])
                return HttpResponse("check email")
        else:
            return HttpResponse("sorry")
    return render(request,'forgot_password.html')

def change_password(request,id):
    a=register_model.objects.get(id=id)
    if request.method == 'POST':
        p1 = request.POST.get('password')
        p2 = request.POST.get('re_password')
        if p1 == p2:
            a.password = p1
            a.save()
            return redirect(login)
        else:
            return HttpResponse('sorry')
    return render(request, 'change_password.html')

# ******************************************************************************************************************** #



# ************************************************** Course ********************************************************** #
def course_registration(request):
    if request.method == "POST":
        a=course_reg_forms(request.POST)
        if a.is_valid():
            fn=a.cleaned_data['fname']
            ln=a.cleaned_data['lname']
            dob=a.cleaned_data['DOB']
            g=a.cleaned_data['gender']
            a1=a.cleaned_data['address1']
            a2=a.cleaned_data['address2']
            city=a.cleaned_data['city']
            em=a.cleaned_data['email']
            pn=a.cleaned_data['phone']
            course=a.cleaned_data['course']
            am=a.cleaned_data['amount']
            a=course_reg_models.objects.all()
            for i in a:
                if(em==i.email):
                    return HttpResponse('already exit')
            else:
                b=course_reg_models(fname=fn,lname=ln,DOB=dob,gender=g,address1=a1,address2=a2,city=city,email=em,phone=pn,course=course,amount=am)
                b.save()
                return redirect(course_payment)
        else:
            return HttpResponse('failed..')
    return render(request,'Course_Registration.html')

def course_payment(request):
    id=request.session['id']
    a=register_model.objects.get(id=id)
    if request.method == 'POST':
        em = request.POST.get('email')
        request.session['am'] = em
        am = request.POST.get('amount')
        request.session['am'] = am
        course=request.POST.get('course')
        request.session['course']=course
        if em == a.email:
            if (a.balance >= int(am)):
                a.balance -= int(am)
                a.save()
                b = withdraw_model(amount=am, uid=request.session['id'])
                b.save()
                return redirect(payment_success)
            else:
                return HttpResponse('insufficient balance...')
        else:
            return HttpResponse('incorrect email..')
    return render(request,'course_feepayment.html',{'a':a})

def payment_success(request):
    am=request.session['am']
    return render(request,"payment_success.html",{'am':am})

def login_course(request):
    if request.method == "POST":
        a = course_login_forms(request.POST)
        if a.is_valid():
            em = a.cleaned_data['email']
            b = course_reg_models.objects.all()
            for i in b:
                if i.email == em :
                    request.session['id']=i.id
                    return redirect(course_profile)
            else:
                return HttpResponse('login failed')
    return render(request,'course_login.html')

def course_profile(request):
    try:
        id=request.session['id']
        a=course_reg_models.objects.get(id=id)
        return render(request, 'course_profile.html', {'a': a})
    except:
        return HttpResponse('failed')

# ******************************************************************************************************************** #

# ************************************************ Admin session ******************************************************#
def admin_login(request):
    if request.method=='POST':
        a=admin_forms(request.POST)
        if a.is_valid():
            username = a.cleaned_data['username']
            password = a.cleaned_data['password']
            User = authenticate(request,username=username,password=password)
            if User is not None:
                return redirect(admin_profile_page)
            else:
                return HttpResponse('login failed..')
    return render(request,'admin_login.html')

def admin_profile_page(request):
       return render(request,'admin_profile_page.html')

def admin_logout(request):
    logout(request)
    return redirect(index)

def admin_news_feed_upload(request):
    if request.method == 'POST':
        a=news_feed_form(request.POST)
        if a.is_valid():
            top = a.cleaned_data['topic']
            content = a.cleaned_data['content']
            b = news_feed_model(topic=top,content=content)
            b.save()
            return redirect(admin_news_feed_display)
        else:
            return HttpResponse('failed')
    return render(request,'admin_news_feed_upload.html')

def admin_news_feed_display(request):
    a = news_feed_model.objects.all()
    return render(request, 'admin_news_feed_display.html', {'a': a})

def admin_news_feed_edit(request,id):
    a=news_feed_model.objects.get(id=id)
    if request.method=='POST':
        a.topic=request.POST.get('topic')
        a.content=request.POST.get('content')
        a.save()
        return redirect(admin_news_feed_display)
    return render(request,'admin_news_feeds_edit.html',{'a':a})

def admin_news_feed_delete(request,id):
    a=news_feed_model.objects.get(id=id)
    a.delete()
    return redirect(admin_news_feed_display)

def admin_video_notes_upload(request):
    if request.method=='POST':
        a=video_notes_forms(request.POST,request.FILES)
        if a.is_valid():
            vn=a.cleaned_data['video_name']
            vf = a.cleaned_data['video_file']
            pn=a.cleaned_data['pdf_name']
            pf = a.cleaned_data['pdf_file']
            b=video_notes_model(video_name=vn,video_file=vf,pdf_name=pn,pdf_file=pf)
            b.save()
            return redirect(admin_video_notes_display)
        else:
            return HttpResponse('not added')
    return render(request,'admin_video_notes_upload.html')

def admin_video_notes_display(request):
    a=video_notes_model.objects.all()
    idd=[]
    vdnm = []
    v=[]
    pdnm=[]
    pdf=[]
    for i in a:
        id=i.id
        idd.append(id)
        vn=i.video_name
        vdnm.append(vn)
        vi=str(i.video_file).split('/')[-1]
        v.append(vi)
        p=i.pdf_name
        pdnm.append(p)
        pd=str(i.pdf_file).split('/')[-1]
        pdf.append(pd)
    pair=zip(idd,vdnm,v,pdnm,pdf)
    return render(request,'admin_video_notes_display.html',{'a': pair})

def admin_video_notes_edit(request,id):
    a=video_notes_model.objects.get(id=id)
    video_file=str(a.video_file).split('/')[-1]
    pdf_file=str(a.pdf_file).split('/')[-1]
    if request.method=='POST':
        a.video_name=request.POST.get('video_name')
        a.pdf_name= request.POST.get('pdf_name')
        if request.FILES.get('video_file')==None:
            a.save()
        else:
            a.video_file=request.FILES['video_file']
        if request.FILES.get('pdf_file')==None:
            a.save()
        else:
            a.pdf_file=request.FILES['pdf_file']
            a.save()
        return redirect(admin_video_notes_display)
    return render(request, 'admin_video_notes_edit.html', {'a': a, 'video_file': video_file, 'pdf_file': pdf_file})

def admin_video_notes_delete(request,id):
    a=video_notes_model.objects.get(id=id)
    a.delete()
    return redirect(admin_video_notes_display)
#**********************************************************************************************************************#

#********************************************* Teachers secssion ******************************************************#
def teachers_info(request):
    return render(request,'teachers_info.html')

def teachers_register(request):
    if request.method == 'POST':
        a=teachers_form(request.POST)
        if a.is_valid():
            name=a.cleaned_data['name']
            em=a.cleaned_data['email']
            psw=a.cleaned_data['password']
            cpsw=a.cleaned_data['confirm_password']
            a=teachers_model.objects.all()
            for i in a:
                if (name == i.name or em == i.email):
                    return HttpResponse('allready exist')
            else:
                if cpsw == psw:
                    b = teachers_model(name=name, email=em,password=psw)
                    b.save()
                    return redirect(teachers_login)
                else:
                    return HttpResponse("password doesn't match! ")
        else:
            return HttpResponse('registration failed invalid datas!')
    return render(request,'teachers_register.html')


def teachers_login(request):
    if request.method == "POST":
        a = teachers_login_form(request.POST)
        if a.is_valid():
            em = a.cleaned_data['email']
            psw = a.cleaned_data['password']
            b = teachers_model.objects.all()
            for i in b:
                if i.email == em and i.password == psw:
                    request.session['id']=i.id
                    return redirect(teachers_profile)
            else:
                return HttpResponse('login failed')
    return render(request,'teachers_login.html')

def teachers_profile(request):
    try:
        id1=request.session['id']
        a=teachers_model.objects.get(id=id1)
        return render(request,'teachers_profile.html',{'a':a})
    except:
        return redirect(teachers_login)

def teacher_logout(request):
    logout(request)
    return redirect(teachers_login)

def teachers_profile_edit(request,id):
    a = teachers_model.objects.get(id=id)
    if request.method=='POST':
        a.name = request.POST.get('name')
        a.email = request.POST.get('email')
        a.save()
        return redirect(teachers_profile)
    return render(request,'teachers_profile_edit.html',{'a':a})

def teachers_profile_delete(request,id):
    a = teachers_model.objects.get(id=id)
    a.delete()
    return redirect(teachers_register)

def teacher_video_notes_upload(request):
    if request.method=='POST':
        a=video_notes_forms(request.POST,request.FILES)
        if a.is_valid():
            vn=a.cleaned_data['video_name']
            vf = a.cleaned_data['video_file']
            pn=a.cleaned_data['pdf_name']
            pf = a.cleaned_data['pdf_file']
            b=video_notes_model(video_name=vn,video_file=vf,pdf_name=pn,pdf_file=pf)
            b.save()
            return redirect(send_conformation_mail_VN)
        else:
            return HttpResponse('not added')
    return render(request,'teacher_VN_upload.html')

def teacher_video_notes_display(request):
    a=video_notes_model.objects.all()
    idd=[]
    vdnm = []
    v=[]
    pdnm=[]
    pdf=[]
    for i in a:
        id=i.id
        idd.append(id)
        vn=i.video_name
        vdnm.append(vn)
        vi=str(i.video_file).split('/')[-1]
        v.append(vi)
        p=i.pdf_name
        pdnm.append(p)
        pd=str(i.pdf_file).split('/')[-1]
        pdf.append(pd)
    pair=zip(idd,vdnm,v,pdnm,pdf)
    return render(request,'teacher_VN_display.html',{'a': pair})

def teacher_video_notes_edit(request,id):
    a=video_notes_model.objects.get(id=id)
    video_file=str(a.video_file).split('/')[-1]
    pdf_file=str(a.pdf_file).split('/')[-1]
    if request.method=='POST':
        a.video_name=request.POST.get('video_name')
        a.pdf_name= request.POST.get('pdf_name')
        if request.FILES.get('video_file')==None:
            a.save()
        else:
            a.video_file=request.FILES['video_file']
        if request.FILES.get('pdf_file')==None:
            a.save()
        else:
            a.pdf_file=request.FILES['pdf_file']
            a.save()
        return redirect(teacher_video_notes_display)
    return render(request, 'teachers_VN_edit.html', {'a': a, 'video_file': video_file, 'pdf_file': pdf_file})

def teacher_video_notes_delete(request,id):
    a=video_notes_model.objects.get(id=id)
    a.delete()
    return redirect(teacher_video_notes_display)

def teacher_news_feed_upload(request):
    if request.method == 'POST':
        a=news_feed_form(request.POST)
        if a.is_valid():
            top = a.cleaned_data['topic']
            content = a.cleaned_data['content']
            b = news_feed_model(topic=top,content=content)
            b.save()
            return redirect(send_conformation_mail_NEWS)
        else:
            return HttpResponse('failed')
    return render(request,'teachers_NEWS_upload.html')

def teachers_news_feed_display(request):
    a = news_feed_model.objects.all()
    return render(request, 'teacher_NEWS_display.html', {'a': a})

def teacher_news_feed_edit(request,id):
    a=news_feed_model.objects.get(id=id)
    if request.method=='POST':
        a.topic=request.POST.get('topic')
        a.content=request.POST.get('content')
        a.save()
        return redirect(teachers_news_feed_display)
    return render(request,'teacher_NEWS_edit.html',{'a':a})

def teacher_news_feed_delete(request,id):
    a=news_feed_model.objects.get(id=id)
    a.delete()
    return redirect(teachers_news_feed_display)

def teaches_VN_student_display(request):
    a=video_notes_model.objects.all()
    idd=[]
    vdnm = []
    v=[]
    pdnm=[]
    pdf=[]
    for i in a:
        id=i.id
        idd.append(id)
        vn=i.video_name
        vdnm.append(vn)
        vi=str(i.video_file).split('/')[-1]
        v.append(vi)
        p=i.pdf_name
        pdnm.append(p)
        pd=str(i.pdf_file).split('/')[-1]
        pdf.append(pd)
    pair=zip(idd,vdnm,v,pdnm,pdf)
    return render(request, 'teachers_VN_student_display.html', {'a': pair})

def save(request,id):
    a=video_notes_model.objects.get(id=id)
    b=save_model.objects.all()
    for i in b:
        if i.VNid==a.id and i.uid==request.session['id']:
            return HttpResponse('already exist..')
    b=save_model(video_name=a.video_name,video_file=a.video_file,pdf_name=a.pdf_name,pdf_file=a.pdf_file,VNid=a.id,uid=request.session['id'])
    b.save()
    return redirect(save_VN_display)

def save_VN_display(request):
    a=save_model.objects.all()
    idd=[]
    vdnm = []
    v=[]
    pdnm=[]
    pdf=[]
    for i in a:
        id=i.id
        idd.append(id)
        vn=i.video_name
        vdnm.append(vn)
        vi=str(i.video_file).split('/')[-1]
        v.append(vi)
        p=i.pdf_name
        pdnm.append(p)
        pd=str(i.pdf_file).split('/')[-1]
        pdf.append(pd)
    pair=zip(idd,vdnm,v,pdnm,pdf)
    return render(request,'Saved_files_display.html',{'a':pair})

def remove(request,id):
    a=save_model.objects.get(id=id)
    a.delete()
    return redirect(save_VN_display)

def send_conformation_mail_VN(request):
    a=teachers_model.objects.all()
    if request.method=='POST':
        em=request.POST.get('email')
        for i in a:
            if(i.email==em):
                id=i.id
                subject="Conformation Message"
                message=f"http://127.0.0.1:8000/python_app/conform_VN/{id}"
                frm=em
                to='akkunni222@gmail.com'
                send_mail(subject,message,frm,[to])
                return HttpResponse("checking for conformation...")
        else:
            return HttpResponse("sorry")
    return render(request,'send_conformation_mail.html')


def confirm_VN(request, id):
    teacher = teachers_model.objects.get(id=id)
    if request.method == 'POST':
        try:
            a = request.POST.get('confirm')
            if a == 'true':
                b = confirm_model.objects.get(teacher=teacher)
                b.confirm = True
                b.save()
                return HttpResponse('Successfully confirmed')
            else:
                return redirect(teacher_video_notes_display)
        except:
            return HttpResponse('Teacher not found')
    return render(request, 'confirm.html', {'teacher': teacher})


def send_conformation_mail_NEWS(request):
    a=teachers_model.objects.all()
    if request.method=='POST':
        em=request.POST.get('email')
        for i in a:
            if(i.email==em):
                id=i.id
                subject="Conformation Message"
                message=f"http://127.0.0.1:8000/python_app/conform_NEWS/{id}"
                frm=em
                to='akkunni222@gmail.com'
                send_mail(subject,message,frm,[to])
                return HttpResponse("checking for conformation...")
        else:
            return HttpResponse("sorry")
    return render(request,'send_conformation_mail.html')

def confirm_NEWS(request, id):
    teacher = teachers_model.objects.get(id=id)
    if request.method == 'POST':
        try:
            a = request.POST.get('confirm')
            if a == 'true':
                b = confirm_model.objects.get(teacher=teacher)
                b.confirm = True
                b.save()
                return HttpResponse('Successfully confirmed')
            else:
                return redirect(teachers_news_feed_display)
        except:
            return HttpResponse('Teacher not found')
    return render(request, 'confirm.html', {'teacher': teacher})