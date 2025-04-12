from django.shortcuts import render
from .models import Category, Dish

# Create your views here.
def main_page_view(request):
    categories = Category.objects.all()
    all_dishes = Dish.objects.all()
    return render(request, 'restaurant/index.html', {'categories': categories, 'dishes': all_dishes})

def menu_page_view(request) :
    categories = Category.objects.all()
    dishes_by_category = Dish.objects.all()
    return render(request, 'restaurant/menu.html', {'categories': categories, 'dishes': dishes_by_category})

def profile_page_view(request):
    return render(request, 'restaurant/profile.html')

def qrcode_view(request):
    return render(request, 'restaurant/qr-code.html')