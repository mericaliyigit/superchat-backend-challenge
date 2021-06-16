# Our urls in the app
from django.urls import path
from . import views


urlpatterns = [
    path('',views.MainView.as_view(), name ='Home'),
    path('create_contact',views.CreateContact.as_view(),name='CreateContact'),
    path('contacts', views.Contacts.as_view(),name='Contacts'),
    path('send_message', views.SendMessage.as_view(),name='SendMessage'),
    path('conversations', views.Conversations.as_view(),name='Conversations'),
    path('githook', views.githubhook,name='Githook'),

]