from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify as django_slugify
from django.urls import reverse
from django.utils import timezone

from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField


class Post(models.Model):
    STATUS_CHOICES = (
        ("черновик", "Черновик"),
        ("опубликовано", "Опубликовано"),
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="автор публикации",
    )
    unique_mark = models.SlugField(
        "уникальная метка", max_length=250, null=False, unique_for_date="published_date"
    )
    title = models.CharField("заголовок публикации", max_length=250)
    image_url = models.CharField("фото публикации", max_length=250)
    text = RichTextField("текст публикации")
    created_date = models.DateTimeField("дата создания", auto_now_add=True)
    published_date = models.DateTimeField("дата публикации", default=timezone.now)
    updated_date = models.DateTimeField("дата изменения", auto_now=True)
    status = models.CharField(
        "статус", max_length=12, choices=STATUS_CHOICES, default="опубликовано"
    )
    tags = TaggableManager()
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="blog_posts", verbose_name="лайки"
    )

    class Meta:
        ordering = ("-created_date",)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            "blog:post_detail",
            args=[
                self.published_date.year,
                self.published_date.strftime("%m"),
                self.published_date.strftime("%d"),
                self.pk,
                self.unique_mark,
            ],
        )

    def total_likes(self):
        return self.likes.count()

    def slugify(self):
        alphabet = {
            "а": "a",
            "б": "b",
            "в": "v",
            "г": "g",
            "д": "d",
            "е": "e",
            "ё": "yo",
            "ж": "zh",
            "з": "z",
            "и": "i",
            "й": "j",
            "к": "k",
            "л": "l",
            "м": "m",
            "н": "n",
            "о": "o",
            "п": "p",
            "р": "r",
            "с": "s",
            "т": "t",
            "у": "u",
            "ф": "f",
            "х": "kh",
            "ц": "ts",
            "ч": "ch",
            "ш": "sh",
            "щ": "shch",
            "ы": "i",
            "э": "e",
            "ю": "yu",
            "я": "ya",
        }
        return django_slugify("".join(alphabet.get(w, w) for w in self.lower()))

    def save(self, *args, **kwargs):
        self.unique_mark = Post.slugify(self.title)
        super(Post, self).save(*args, **kwargs)


class Comment(models.Model):
    related_post = models.ForeignKey(
        Post,
        related_name="comments",
        on_delete=models.CASCADE,
        verbose_name="связанная публикация",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="автор комментария",
    )
    text = RichTextField("комментарий", blank=False)
    created_date = models.DateTimeField("дата создания", auto_now_add=True)
    updated_date = models.DateTimeField("дата изменения", auto_now=True)
    status = models.BooleanField(default=True)

    class Meta:
        ordering = ("created_date",)

    def __str__(self):
        return "Комментарий от {} к {}".format(self.author, self.related_post)
