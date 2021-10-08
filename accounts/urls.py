from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Вход/выход в/из учетной записи
    path("user/login", views.user_login, name="login"),
    path("user/logout", views.user_logout, name="logout"),
    # Смена пароля
    path(
        "user/password-change",
        auth_views.PasswordChangeView.as_view(
            template_name="accounts/password/password_change_form.html"
        ),
        name="password_change",
    ),
    path(
        "user/password-change/done",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="accounts/password/password_change_done.html"
        ),
        name="password_change_done",
    ),
    # Сброс пароля
    path(
        "user/password-reset",
        auth_views.PasswordResetView.as_view(
            template_name="accounts/password/password_reset_form.html"
        ),
        name="password_reset",
    ),
    path(
        "user/password-reset/done",
        auth_views.PasswordResetDoneView.as_view(
            template_name="accounts/password/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "user/password-reset/confirm/<uidb64>/<token>",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/password/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "user/password-reset/complete",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/password/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    # Регистрация пользователя
    path("user/register", views.user_register, name="register"),
    # Изменение профиля
    path("user/<int:pk>/profile/edit", views.profile_edit, name="profile_edit"),
    # Просмотр профиля
    path("user/<int:pk>/profile", views.profile, name="profile"),
    # Панель управления
    path("user/<int:pk>/dashboard/", views.dashboard, name="dashboard"),
    # Форма обратной связи
    path("contacts/", views.contacts, name="contacts"),
]
