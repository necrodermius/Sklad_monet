from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class DietaryOption(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Dietary Option"
        verbose_name_plural = "Dietary Options"

    def __str__(self):
        return self.name

class Dish(models.Model):
    name = models.CharField(max_length=100)
    ingredients = models.TextField()
    image = models.ImageField(upload_to='images/', null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False)
    dietary_types = models.ManyToManyField(DietaryOption)

    class Meta:
        verbose_name = "Dish"
        verbose_name_plural = "Dishes"

    def __str__(self):
        return self.name