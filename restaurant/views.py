from django.shortcuts import render
from .models import Category, Dish, DietaryOption

# Create your views here.
def main_page_view(request):
    categories = Category.objects.all()
    all_dishes = Dish.objects.all()
    return render(request, 'restaurant/index.html', {'categories': categories, 'dishes': all_dishes})

def menu_page_view(request):
    categories = Category.objects.all()
    filters = DietaryOption.objects.all()
    dishes = Dish.objects.all()

    category_filter = request.GET.get('category')
    if category_filter:
        dishes = dishes.filter(category__id=category_filter)

    filter_option = request.GET.get('filter')
    if filter_option:
        dishes = dishes.filter(dietary_options__id=filter_option)

    return render(request, 'restaurant/menu.html', {
        'categories': categories,
        'filters': filters,
        'dishes': dishes
    })

