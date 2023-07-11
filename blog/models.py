from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# Create your models here.
from django.urls import reverse


class Genre(models.Model):
    # id создавать не надо. Джанго сделает его сам
    title = models.CharField(max_length=255, verbose_name='Название')  # title VARCHAR(255)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Comics(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(default='Здесь будет описание', verbose_name='Описание')
    artist = models.CharField(max_length=255, default='Кто-то', verbose_name='Художник')
    writer = models.CharField(max_length=255, default='Кто-то', verbose_name='Сценарист')
    poster = models.ImageField(upload_to='posters', null=True, blank=True, verbose_name='Постер')
    # null=True - может быть пустой в базе   blank=True - можно не заполнять поле
    views = models.IntegerField(default=0, verbose_name='Просмотры')
    genres = models.ManyToManyField(Genre, verbose_name='Жанры')
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None,
                               null=True, blank=True)


    def get_absolute_url(self):
        return reverse('comic', kwargs={'pk':self.pk})

    def get_poster(self):
        try:
            return self.poster.url
        except:
            return 'https://upload.wikimedia.org/wikipedia/ru/thumb/d/d2/Shingeki_no_Kyojin.jpg/230px-Shingeki_no_Kyojin.jpg'


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Комикс'
        verbose_name_plural = 'Комиксы'

class Volume(models.Model):
    number = models.IntegerField(default=1, verbose_name='Номер тома')
    comics = models.ForeignKey(Comics, on_delete=models.CASCADE, verbose_name='Комикс') # Удалить детей волной

    def __str__(self):
        return f'{self.comics} - {self.number}'

    class Meta:
        verbose_name = 'Том'
        verbose_name_plural = 'Тома'


class Chapter(models.Model):
    number = models.IntegerField(default=1, verbose_name='Глава')
    volume = models.ForeignKey(Volume, on_delete=models.CASCADE, verbose_name='Том')

    def __str__(self):
        return f'{self.volume} - {self.number}'

    class Meta:
        verbose_name = 'Глава'
        verbose_name_plural = 'Главы'


class Picture(models.Model):
    image = models.ImageField(upload_to='images/', blank=True, null=True, verbose_name='Изображение')
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, verbose_name='Глава')

    def __str__(self):
        return self.chapter

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'


# Создать модель Comment
# Котарая знает Комикс Пользователя Текст и Дату
# Создать форму для заполнения текста
# Улучшить Детали Комикса чтобы выводить форму, только если зарегестрировать
# Прописать вьюшку для сохранения комментария
# Доработать детали статьи для вывода комментариев
# Сделать куски HTML для вывода формы и комментариев

class Comment(models.Model):
    comic = models.ForeignKey(Comics, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарии'
        verbose_name_plural = 'Комментарии'


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    photo = models.ImageField(upload_to='profiles/', blank=True, null=True)
    profile_bg = models.ImageField(upload_to='profile_bgs/', blank=True, null=True)
    bio = models.CharField(default='Обо мне', max_length=255, blank=True, null=True)


    def __str__(self):
        return self.user.username


    def get_profile_bg(self):
        try:
            return self.profile_bg.url
        except:
            return 'https://images.wallpaperscraft.ru/image/single/mandala_uzor_abstraktsiia_149799_1920x1200.jpg'

    def get_photo(self):
        try:
            return self.photo.url
        except:
            return 'https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460__340.png'

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

