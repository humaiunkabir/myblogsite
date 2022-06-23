
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('loginsubmit/', views.loginsubmit, name='loginsubmit'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('registersubmit/', views.registrationsubmit, name='registersubmit'),
    path('profile/', views.getAuthor, name='profile'),
    path('article/<int:id>', views.getSingle, name='singlepost'),
    path('categorywisearticle/<int:id>',
         views.getCategoryWisePost, name='categorypost'),
    path('newposttem', views.newposttemplate, name='posttemplate'),
    path('postreport/', views.getpostreport, name='postreport'),
    path('update/<int:pid>', views.getUpdateInfo, name='updatepost'),
    path('delete/<int:pid>', views.getdeletepost, name='delete'),

]
