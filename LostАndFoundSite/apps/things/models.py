from django.db import models
from django.urls import reverse
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit, Transpose




class Thing(models.Model):
    """Модель для хранения информации о вещах, которые были потеряны или найдены."""

    class ThingStatus(models.IntegerChoices):
        LOST = 0, 'Потеря'
        FOUND = 1, 'Находка'

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = ProcessedImageField(
        verbose_name='Логотип', blank=True, null=True,
        processors=[
            Transpose(),
            ResizeToFit(width=500, upscale=False)
        ],
        format='WEBP',
        options={'quality': 80}, default='base_thing.webp'
    )
    status = models.BooleanField(
        default=ThingStatus.FOUND,
        choices=ThingStatus,
        verbose_name='Статус',
        help_text="Выберите статус вещи: потерянная или найденная."
    )
    address = models.TextField(
        blank=True, null=True,
        verbose_name='Адрес',
        help_text="Адрес, где была потеряна или найдена вещь."
    )
    owner = models.ForeignKey(
        'users.User', on_delete=models.CASCADE,
        related_name='things',
        verbose_name='Создатель',
        help_text="Пользователь, который создал запись о вещи.",
        null=True, blank=True
    )
    date_lost_or_found = models.CharField(max_length=64, verbose_name="Дата потери/нахождения", blank=True, null=True)

    def get_absolute_url(self):
        """Возвращает абсолютный URL для доступа к детали вещи."""
        return reverse('things:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Вещь"
        verbose_name_plural = "Вещи"
        ordering = ["-created_at"]

