app_name = 'accounts'
from django.urls import path, include

from accounts import views
from accounts.views import RegisterView

urlpatterns = [
    path('profile', views.profile_page_view, name='profile'),
    path('qrcode', views.qrcode_view, name='qrcode'),
    path('login', views.login_view, name="login"),
    path('register', RegisterView.as_view(), name="register"),
    path('', include('django.contrib.auth.urls'))
]