# File: MyCarsProject/cars/models.py

import os
import uuid
from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator


# Модель производителя автомобилей
class Manufacturer(models.Model):
    name = models.CharField(max_length=255, verbose_name="Производитель")
    country = models.CharField(max_length=100, verbose_name="Страна")

    def __str__(self):
        return self.name


# Модель тегов
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Тег")

    def __str__(self):
        return self.name


# Пользовательский менеджер для выборки опубликованных автомобилей
class PublishedManager(models.Manager):
    def get_queryset(self):
        # Фильтруем записи, оставляя только опубликованные
        return super().get_queryset().filter(is_published=Car.Status.PUBLISHED)


def car_image_path(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = f"{uuid.uuid4().hex}.{ext}"
    return os.path.join('cars', new_filename)


# Модель автомобиля
class Car(models.Model):
    # Класс-перечисление для статуса публикации
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(
        max_length=255,
        verbose_name="Название автомобиля"
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        db_index=True,
        verbose_name="URL"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Описание"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена",
        validators = [MinValueValidator(0)],
    )

    # Поле для загрузки изображения
    image = models.ImageField(
        upload_to=car_image_path,
        null=True,
        blank=True,
        verbose_name="Изображение"
    )

    time_create = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Время создания"
    )
    time_update = models.DateTimeField(
        auto_now=True,
        verbose_name="Время обновления"
    )

    is_published = models.IntegerField(
        choices=Status.choices,
        default=Status.DRAFT,
        verbose_name="Статус публикации"
    )

    manufacturer = models.ForeignKey(
        Manufacturer,
        on_delete=models.CASCADE,
        related_name='cars',
        verbose_name="Производитель",
        null=True,
        blank=True
    )

    tags = models.ManyToManyField(
        Tag,
        related_name='cars',
        verbose_name="Теги",
        blank=True
    )

    objects = models.Manager()           # Стандартный менеджер
    published = PublishedManager()       # Менеджер для опубликованных записей

    class Meta:
        ordering = ['-time_create']
        indexes = [models.Index(fields=['-time_create'])]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('cars:car_detail', kwargs={'car_slug': self.slug})


# Модель деталей автомобиля (OneToOne)
class CarDetail(models.Model):
    car = models.OneToOneField(
        Car,
        on_delete=models.CASCADE,
        related_name='detail',
        verbose_name="Автомобиль"
    )
    engine = models.CharField(
        max_length=100,
        verbose_name="Двигатель"
    )
    transmission = models.CharField(
        max_length=100,
        verbose_name="Коробка передач"
    )
    mileage = models.PositiveIntegerField(
        verbose_name="Пробег",
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Детали {self.car.title}"
