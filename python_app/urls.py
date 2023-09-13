from django.urls import path
from .views import *

urlpatterns=[
    path('index/',index),
    path('success/',success),

    path('register/',register),
    path('login/',login),
    path('myprofile/',myprofile),
    path('logout/',logout_views),

    path('edit_myprofile/<int:id>',edit_myprofile),
    path('edit_image/<int:id>',edit_image),
    path('delete/<int:id>',delete),

    path('change_password/<int:id>',change_password),
    path('forgot_password/',forgot_password),

    path('add_money/<int:id>',add_money),
    path('add_money_success/',add_money_success),
    path('add_money_display/',add_money_display),

    path('withdraw/<int:id>',withdraw),
    path('withdraw_success/',withdraw_success),
    path('withdraw_display/',withdraw_display),

    path('checkbalance/<int:id>',checkbalance),
    path('balance_display',balance_display),


    path('course_registration/',course_registration),
    path('course_payment/',course_payment),
    path('payment_success/',payment_success),
    path('login_course/',login_course),
    path('course_profile/',course_profile),

    path('admin_login/',admin_login),
    path('admin_profile_page/',admin_profile_page),
    path('admin_logout/',admin_logout),

    path('admin_news_feed_upload/',admin_news_feed_upload),
    path('admin_news_feed_display/',admin_news_feed_display),
    path('admin_news_feed_edit/<int:id>',admin_news_feed_edit),
    path('admin_news_feed_delete/<int:id>',admin_news_feed_delete),

    path('admin_video_notes_upload/',admin_video_notes_upload),
    path('admin_video_notes_display/',admin_video_notes_display),
    path('admin_video_notes_edit/<int:id>',admin_video_notes_edit),
    path('admin_video_notes_delete/<int:id>',admin_video_notes_delete),

    path('teachers_info/',teachers_info),
    path('teachers_register/',teachers_register),
    path('teachers_login/',teachers_login),
    path('teachers_profile/',teachers_profile),
    path('teacher_logout/',teacher_logout),

    path('teachers_profile_edit/<int:id>',teachers_profile_edit),
    path('teachers_profile_delete/<int:id>',teachers_profile_delete),

    path('teacher_video_notes_upload/',teacher_video_notes_upload),
    path('teacher_video_notes_display/',teacher_video_notes_display),
    path('teacher_video_notes_edit/<int:id>',teacher_video_notes_edit),
    path('teacher_video_notes_delete/<int:id>',teacher_video_notes_delete),

    path('teacher_news_feed_upload/',teacher_news_feed_upload),
    path('teachers_news_feed_display/',teachers_news_feed_display),
    path('teacher_news_feed_edit/<int:id>',teacher_news_feed_edit),
    path('teacher_news_feed_delete/<int:id>',teacher_news_feed_delete),
    path('teaches_VN_student_display/',teaches_VN_student_display),

    path('save/<int:id>',save),
    path('save_VN_display/',save_VN_display),
    path('remove/<int:id>',remove),

    path('send_conformation_mail_VN/',send_conformation_mail_VN),
    path('conform_VN/<int:id>',confirm_VN),

    path('send_conformation_mail_NEWS/',send_conformation_mail_NEWS),
    path('conform_NEWS/<int:id>',confirm_NEWS),




]