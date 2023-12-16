from time import timezone

from django.contrib.auth import logout, login
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.db.models.signals import post_save, pre_save, pre_delete
from django.dispatch import receiver
import random
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from django.http import HttpRequest, HttpResponse
from django.utils.timezone import now


class UserProfile(models.Model):
    user = models.OneToOneField(
        editable=True,
        blank=True,
        null=True,
        default=None,
        verbose_name="Модель пользователя",
        help_text='<small class="text-muted">Тут лежит "ссылка" на модель пользователя</small><hr><br>',
        to=User,
        on_delete=models.CASCADE,
        related_name="profile",  # user.profile
    )
    avatar = models.ImageField(verbose_name="Аватарка", upload_to="users/avatars", default=None, null=True, blank=True)

    class Meta:
        """Вспомогательный класс"""

        app_label = "auth"
        ordering = ("-user", "avatar")
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"

    def __str__(self):
        return f"<UserProfile {self.User.username}>"


@receiver(post_save, sender=User)
def create_user_model(sender, instance, created, **kwargs):
    UserProfile.objects.get_or_create(user=instance)


class BusIdea(models.Model):
    author = models.ForeignKey(verbose_name="Автор", to=User, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='images/ideas', null=True, blank=True)
    file = models.FileField(upload_to='files/products', null=True, blank=True)
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Ideacomments(models.Model):
    idea = models.ForeignKey(to=BusIdea, verbose_name="К какомй идее", max_length=200, on_delete=models.CASCADE)
    author = models.ForeignKey(to=User, verbose_name="Автор", max_length=200, on_delete=models.CASCADE)  # +-
    text = models.TextField("Текст комментария", default="")
    date_time = models.DateTimeField("Дата и время создания", default=now)

    class Meta:
        app_label = "django_app"
        ordering = ("-date_time", "idea")
        verbose_name = "Комментарий к посту"
        verbose_name_plural = "Комментарии к постам"

    def __str__(self):
        return f"{self.date_time} {self.author.username} {self.idea .title} {self.text[:20]}"


class IdeaRatings(models.Model):
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)  # OneToMany +-
    idea = models.ForeignKey(to=BusIdea, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

    class Meta:
        app_label = "django_app"
        ordering = ("-idea", "author")
        verbose_name = "Рейтинг к новости"
        verbose_name_plural = "Рейтинги к новостям"

    def __str__(self):
        if self.status:
            like = "ЛАЙК"
        else:
            like = "ДИЗЛАЙК"
        return f"{self.idea.title} {self.author.username} {like}"

class Resume(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name='author')
    post = models.CharField(max_length=100,default='')
    image = models.ImageField(upload_to='images/resumes', null=True, blank=True)
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    skills = models.TextField()
    experience = models.TextField()
    education = models.TextField()

    def __str__(self):
        return self.full_name

class Resumecomments(models.Model):
    resume = models.ForeignKey(to=Resume, verbose_name="К какомй идее", max_length=200, on_delete=models.CASCADE)
    author = models.ForeignKey(to=User, verbose_name="Автор", max_length=200, on_delete=models.CASCADE)  # +-
    text = models.TextField("Текст комментария", default="")
    date_time = models.DateTimeField("Дата и время создания", default=now)


    def __str__(self):
        return f"{self.date_time} {self.author.username}  {self.text[:20]}"


class ResumeRatings(models.Model):
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)  # OneToMany +-
    resume = models.ForeignKey(to=Resume, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)


    def __str__(self):
        if self.status:
            like = "ЛАЙК"
        else:
            like = "ДИЗЛАЙК"
        return f"{self.author.username} {like}"



class Room(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('name',)


class Message(models.Model):
    room = models.ForeignKey(Room, related_name="messages", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="messages", on_delete=models.CASCADE)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-date_added',)



class Product(models.Model):
    article = models.CharField(max_length=5, unique=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_in_stock = models.PositiveIntegerField(default=0)
    quantity_on_hand = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name



