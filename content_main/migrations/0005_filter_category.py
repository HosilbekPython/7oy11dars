# Generated by Django 5.1.7 on 2025-03-19 18:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content_main', '0004_filter_product_filters'),
    ]

    operations = [
        migrations.AddField(
            model_name='filter',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='filters', to='content_main.category'),
            preserve_default=False,
        ),
    ]
