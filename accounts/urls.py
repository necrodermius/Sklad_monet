from django.urls import path, include

from accounts import views

urlpatterns = [
    path('profile', views.profile_page_view),
    path('qrcode', views.qrcode_view),
    path('login', views.login_view),
    path('', include('django.contrib.auth.urls'))
]