# Generated by Django 5.2.3 on 2025-07-05 17:35

import imagekit.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Thing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image', imagekit.models.fields.ProcessedImageField(blank=True, default='base_thing.webp', null=True, upload_to='', verbose_name='Логотип')),
                ('status', models.BooleanField(choices=[(0, 'Потеря'), (1, 'Находка')], default=1, help_text='Выберите статус вещи: потерянная или найденная.', verbose_name='Статус')),
                ('address', models.TextField(blank=True, help_text='Адрес, где была потеряна или найдена вещь.', null=True, verbose_name='Адрес')),
                ('date_lost_or_found', models.CharField(blank=True, max_length=64, null=True, verbose_name='Дата потери/нахождения')),
            ],
            options={
                'verbose_name': 'Вещь',
                'verbose_name_plural': 'Вещи',
                'ordering': ['-created_at'],
            },
        ),
    ]
