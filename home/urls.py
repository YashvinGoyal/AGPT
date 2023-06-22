from django.contrib import admin
from django.urls import path,include
from home import views
urlpatterns = [
    path('',views.home,name='home'),
    path('login',views.loginn,name='login'),
    path('categories',views.choose,name='choose'),
    path('mainlogin',views.mainlogin,name='mainlogin'),
    path('logout',views.logoutt,name="logoutt"),
    path('cat',views.cat,name='cat'),
    path('log',views.log,name='log'),
    path('signup',views.signup,name='signup'),
    path('feedback',views.feedbackk,name='feedback'),
    path('file',views.files,name="files"),
    path('uploadd',views.uploadd,name="uploadd")
]
