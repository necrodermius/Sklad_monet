# Generated by Django 5.2 on 2025-04-22 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0002_dish_dietary_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='DietaryOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.RemoveField(
            model_name='dish',
            name='dietary_type',
        ),
        migrations.AddField(
            model_name='dish',
            name='dietary_types',
            field=models.ManyToManyField(blank=True, to='restaurant.dietaryoption'),
        ),
    ]
