from django.shortcuts import render

# Create your views here.
def main_page_view(request):
    return render(request, 'restaurant/index.html')

def menu_page_view(request):
    return render(request, 'restaurant/menu.html')

def profile_page_view(request):
    return render(request, 'restaurant/profile.html')

def qrcode_view(request):
    return render(request, 'restaurant/qr-code.html')