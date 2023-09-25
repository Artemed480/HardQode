from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    """Продукт"""
    owner = models.CharField('Владелец', max_length=100)
    users = models.ManyToManyField(User, verbose_name='Пользователи')

    def __str__(self):
        return self.owner

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Lesson(models.Model):
    """Урок"""
    name = models.CharField('Название', max_length=250)
    link = models.URLField('Ссылка')
    time = models.PositiveBigIntegerField('Время ролика')
    product = models.ManyToManyField(Product, verbose_name='продукт')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class Viewing(models.Model):
    """Прогресс"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='Урок')
    viewing_time = models.PositiveBigIntegerField('Время просмотра')
    last_view = models.DateTimeField('Последний просмотр', auto_now=True)
    result = models.CharField('Результат', max_length=14, blank=True)

    def set_result(self):
        lesson_time = self.lesson.time
        if self.viewing_time >= lesson_time * 0.8:
            self.result = 'Просмотрено'
        else:
            self.result = 'Не просмотрено'
        self.save()

    def __str__(self):
        return f'{self.user.username} - {self.lesson.name}'

    class Meta:
        verbose_name = 'Просмотр'
        verbose_name_plural = 'Просмотры'
