from django.test import TestCase, Client
from django.urls import reverse
from .models import Category, Dish, DietaryOption
from django.core.files.uploadedfile import SimpleUploadedFile
from decimal import Decimal

class CategoryModelTest(TestCase):
    def test_str_method(self):
        category = Category.objects.create(name="Starters")
        self.assertEqual(str(category), "Starters")

class DietaryOptionModelTest(TestCase):
    def test_str_method(self):
        option = DietaryOption.objects.create(name="Gluten-Free")
        self.assertEqual(str(option), "Gluten-Free")

class DishModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Main Courses")
        self.option = DietaryOption.objects.create(name="Vegan")
        self.dish = Dish.objects.create(
            name="Vegan Burger",
            ingredients="Plant-based patty, lettuce, tomato",
            image=SimpleUploadedFile("burger.jpg", b"file_content", content_type="image/jpeg"),
            price=Decimal('15.00'),
            category=self.category
        )
        self.dish.dietary_types.add(self.option)

    def test_str_method(self):
        self.assertEqual(str(self.dish), "Vegan Burger")

    def test_dish_has_dietary_option(self):
        self.assertIn(self.option, self.dish.dietary_types.all())

class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.starters = Category.objects.create(name="Starters")
        self.main_courses = Category.objects.create(name="Main Courses")

        self.vegan = DietaryOption.objects.create(name="Vegan")
        self.gluten_free = DietaryOption.objects.create(name="Gluten-Free")

        self.starter_dish = Dish.objects.create(
            name="Bruschetta",
            ingredients="Bread, tomato, basil",
            image=SimpleUploadedFile("bruschetta.jpg", b"file_content", content_type="image/jpeg"),
            price=Decimal('8.00'),
            category=self.starters
        )
        self.main_dish = Dish.objects.create(
            name="Grilled Salmon",
            ingredients="Salmon, lemon, herbs",
            image=SimpleUploadedFile("salmon.jpg", b"file_content", content_type="image/jpeg"),
            price=Decimal('20.00'),
            category=self.main_courses
        )
        self.starter_dish.dietary_types.add(self.vegan)
        self.main_dish.dietary_types.add(self.gluten_free)

    def test_main_page_view(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant/index.html')

    def test_menu_page_view(self):
        response = self.client.get('/menu')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant/menu.html')
        self.assertContains(response, "Bruschetta")
        self.assertContains(response, "Grilled Salmon")

    def test_menu_filter_by_category(self):
        response = self.client.get('/menu', {'category': self.starters.id})
        self.assertContains(response, "Bruschetta")
        self.assertNotContains(response, "Grilled Salmon")

    
