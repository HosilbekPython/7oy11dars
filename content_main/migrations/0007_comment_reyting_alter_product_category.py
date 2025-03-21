# Generated by Django 5.1.7 on 2025-03-21 21:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content_main', '0006_filter_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='reyting',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products', to='content_main.category'),
        ),
    ]
