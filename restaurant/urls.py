from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page_view),
    path('menu', views.menu_page_view),


]