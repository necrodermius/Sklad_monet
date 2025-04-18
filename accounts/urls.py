app_name = 'accounts'
from django.urls import path, include
from accounts import views
from accounts.views import RegisterView, QrPageView
urlpatterns = [
    path('profile', views.profile_page_view, name='profile'),
    path('qr-image/<str:signed_user_id>/', views.qrcode_view, name='qr_image'),
    path('qr/', QrPageView.as_view(), name='qr_page'),
    path('redeem/<str:signed_user_id>/', views.redeem_bonus, name='redeem'),
    path('login', views.login_view, name="login"),
    path('register', RegisterView.as_view(), name="register"),
    path('', include('django.contrib.auth.urls'))
]