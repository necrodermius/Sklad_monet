from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def str(self):
        return self.name

class Dish(models.Model):
    name = models.CharField(max_length=100)
    ingredients = models.TextField()
    image = models.ImageField(upload_to='media/images/', null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False)

    class Meta:
        verbose_name = "Dish"
        verbose_name_plural = "Dishes"

    def str(self):
        return self.name