from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg
import os
from uuid import uuid4

def path_and_rename(instance, filename):
    upload_to = 'covers/'
    ext = filename.split('.')[-1]

    filename = f'{uuid4().hex}.{ext}'
    return os.path.join(upload_to, filename)


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название жанра")
    slug = models.SlugField(unique=True)  # Короткое имя для URL (например, 'action')

    class Meta:
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Game(models.Model):
    cover_image = models.ImageField(upload_to=path_and_rename,)
    STATUS_CHOICES = [
        ('idea', 'Только идея'),
        ('prototype', 'Прототип'),
        ('demo', 'Демо-версия'),
        ('alpha', 'Альфа-тест'),
        ('beta', 'Бета-тест'),
        ('released', 'Релиз'),
    ]

    title = models.CharField(max_length=200, verbose_name='Название игры')
    description = models.TextField(verbose_name="Описание")
    developer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="games", verbose_name="Разработчик")
    cover_image = models.ImageField(upload_to='cover/', blank=True, null=True, verbose_name="Обложка")
    game_url = models.URLField(blank=True, verbose_name="Ссылка на игру")
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='games',
        verbose_name="Жанр"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='idea',
        verbose_name="Статус разработки"
    )

    likes = models.ManyToManyField(User, related_name='liked_games', blank=True)

    def get_status_color(self):
        colors = {
            'idea': '#6c757d',  # Серый
            'prototype': '#17a2b8',  # Голубой
            'demo': '#ffc107',  # Желтый
            'alpha': '#fd7e14',  # Оранжевый
            'beta': '#007bff',  # Синий
            'released': '#28a745',  # Зеленый
        }
        return colors.get(self.status, '#000')

    def total_likes(self):
        return self.likes.count()

    def get_average_rating(self):
        average = self.reviews.aggregate(Avg('rating'))['rating__avg']
        if average:
            return round(average, 1)
        return "Нет оценок"

    def __str__(self):
        return self.title


class Review(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="reviews")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Тестировщик")
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Оценка"
    )
    text = models.TextField(verbose_name="Отзыв")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Отзыв от {self.author} на {self.game.title}"


class Screenshot(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='screenshots')
    image = models.ImageField(upload_to='screenshots/', verbose_name="Скриншот")

    def __str__(self):
        return f"Скриншот для {self.game.title}"
