# Generated by Django 5.1.7 on 2025-03-10 10:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='category/image/')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='content_main.category')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('slug', models.SlugField(max_length=250, unique=True)),
                ('descriotion', models.CharField(blank=True, max_length=500, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('discount', models.IntegerField(default=0)),
                ('quantitiy', models.IntegerField(default=50)),
                ('volume', models.CharField(choices=[('kg', 'Kilogram'), ('l', 'Liter'), ('dona', 'Dona')], max_length=4)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='content_main.category')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='content_main.product')),
            ],
        ),
        migrations.CreateModel(
            name='ProduktImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='product/images/')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='image', to='content_main.product')),
            ],
        ),
    ]
