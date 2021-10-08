from crispy_forms.helper import FormHelper
from django import forms
from . import models


class PostForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ("title", "tags", "image_url", "text")
        labels = {
            "title": "Заголовок публикации:",
            "tags": "Теги:",
            "image_url": "Ссылка на фото:",
            "text": "Текст публикации:",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        for field in self.fields.values():
            field.widget.attrs["style"] = "max-width:835px; margin-bottom: 10px;"


class EmailPostForm(forms.Form):
    sender_name = forms.CharField(max_length=50, label="Имя отправителя:")
    sender_email = forms.EmailField(label="Адрес электронной почты отправителя:")
    recipient_email = forms.EmailField(label="Адрес электронной почты получателя:")
    sender_comments = forms.CharField(
        required=False, widget=forms.Textarea, label="Комментарий отправителя:"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        for field in self.fields.values():
            field.widget.attrs["style"] = "max-width:500px; margin-bottom: 10px;"


class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ["text"]
        labels = {
            "text": "",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False


class SearchForm(forms.Form):
    query = forms.CharField(label=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
