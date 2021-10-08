from crispy_forms.helper import FormHelper
from django import forms
from django.contrib.auth.models import User

from .models import Profile, Contact


class LoginForm(forms.Form):
    username = forms.CharField(label="Имя пользователя:")
    password = forms.CharField(label="Пароль:", widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        for field in self.fields.values():
            field.widget.attrs["style"] = "max-width:500px; margin-bottom: 10px;"


class UserRegistrationForm(forms.ModelForm):
    password_1 = forms.CharField(label="Пароль:", widget=forms.PasswordInput)
    password_2 = forms.CharField(label="Повторите пароль:", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")
        labels = {
            "username": "Имя пользователя:",
            "first_name": "Имя:",
            "last_name": "Фамилия:",
            "email": "Адрес электронной почты:",
        }

    def clean_password_2(self):
        cleaned_data = self.cleaned_data
        if cleaned_data["password_1"] != cleaned_data["password_2"]:
            raise forms.ValidationError("Пароли не совпадают!")
        return cleaned_data["password_2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        User._meta.get_field("email")._unique = True
        for field in self.fields.values():
            field.widget.attrs["style"] = "max-width:500px; margin-bottom: 10px;"


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")
        labels = {
            "first_name": "Имя:",
            "last_name": "Фамилия:",
            "email": "Адрес электронной почты:",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        for field in self.fields.values():
            field.widget.attrs["style"] = "max-width:500px; margin-bottom: 10px;"


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            "date_of_birth",
            "bio",
            "photo",
            "website_url",
            "facebook_url",
            "instagram_url",
            "twitter_url",
        )
        labels = {
            "date_of_birth": "Дата рождения:",
            "bio": "О себе:",
            "photo": "Фотография:",
            "website_url": "Ссылка на Ваш сайт:",
            "facebook_url": "Ссылка на Ваш аккаунт в Facebook:",
            "instagram_url": "Ссылка на Ваш аккаунт в Instagram:",
            "twitter_url": "Ссылка на Ваш аккаунт в Twitter:",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        for field in self.fields.values():
            field.widget.attrs["style"] = "max-width:500px; margin-bottom: 10px;"


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = "__all__"
        labels = {
            "full_name": "Ф.И.О.:",
            "email": "Адрес электронной почты:",
            "subject": "Тема:",
            "message": "Сообщение:",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        for field in self.fields.values():
            field.widget.attrs["style"] = "max-width:555px; margin-bottom: 10px;"
