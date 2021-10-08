from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField("о себе", blank=True)
    date_of_birth = models.DateField("дата рождения", blank=True, null=True)
    photo = models.ImageField("фотография", upload_to="users/%Y/%m/%d", blank=True)
    website_url = models.CharField("website", max_length=255, blank=True)
    facebook_url = models.CharField("facebook", max_length=255, blank=True)
    instagram_url = models.CharField("instagram", max_length=255, blank=True)
    twitter_url = models.CharField("twitter", max_length=255, blank=True)

    def __str__(self):
        return str(self.user)


class Contact(models.Model):
    full_name = models.CharField("имя пользователя", max_length=255)
    email = models.EmailField("адрес электронной почты")
    subject = models.CharField("тема", max_length=255)
    message = models.TextField("сообщение", max_length=2000)

    def __str__(self):
        return self.full_name
