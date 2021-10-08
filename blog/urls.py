from django.urls import path
from . import views


urlpatterns = [
    # Главная страница
    path("", views.index, name="index"),
    # Все публикации
    path("blog/", views.post_list, name="post_list"),
    # Добавление публикации
    path("blog/create", views.post_create, name="post_create"),
    # Редактирование публикации
    path("blog/<int:pk>/update", views.post_update, name="post_update"),
    # Удаление публикации
    path("blog/<int:pk>/delete", views.post_delete, name="post_delete"),
    # Фильтр по тегам
    path("blog/tag/<tag_mark>", views.post_list, name="post_list_by_tag"),
    # Конткретная публикация
    path(
        "blog/<int:year>/<int:month>/<int:day>/<int:pk>/<post>",
        views.post_detail,
        name="post_detail",
    ),
    # Поделиться публикацией
    path("blog/<int:pk>/share", views.post_share, name="post_share"),
    # Поиск по публикациям
    path("blog/search", views.post_search, name="post_search"),
    # Поставить лайк публикации
    path("blog/like/<int:pk>", views.post_like, name="post_like"),
]
