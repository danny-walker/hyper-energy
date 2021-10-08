from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from taggit.models import Tag

from blog.models import Post
from .forms import (
    LoginForm,
    UserRegistrationForm,
    UserEditForm,
    ProfileEditForm,
    ContactForm,
)
from .models import Profile


def user_login(request):
    if request.user.is_authenticated:
        return render(request, "blog/index.html")
    else:
        if request.method == "GET":
            request.session["login_from"] = request.META.get("HTTP_REFERER", "/")
        if request.method == "POST":
            form = LoginForm(request.POST)
            if form.is_valid():
                cleaned_data = form.cleaned_data
                user = authenticate(
                    username=cleaned_data["username"], password=cleaned_data["password"]
                )
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return HttpResponseRedirect(request.session["login_from"])
                    else:
                        messages.error(request, "Учетная запись отключена")
                else:
                    messages.error(request, "Неверный логин или пароль")
        else:
            form = LoginForm()
        return render(request, "accounts/login.html", {"form": form})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/")


def user_register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data["password_1"])
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(
                request,
                "accounts/registration/register_done.html",
                {"new_user": new_user},
            )
    else:
        user_form = UserRegistrationForm()
    return render(
        request, "accounts/registration/register.html", {"user_form": user_form}
    )


@login_required
def profile_edit(request, pk):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile, data=request.POST, files=request.FILES
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Профиль успешно обновлен")
        else:
            messages.error(request, "Ошибка обновления профиля")
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(
        request,
        "accounts/profile/profile_edit.html",
        {"user_form": user_form, "profile_form": profile_form, "pk": pk},
    )


def profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, "accounts/profile/profile.html", {"user": user})


@login_required
def dashboard(request, pk, tag_mark=None):
    object_list = Post.objects.filter(author=request.user)
    tag = None

    if tag_mark:
        tag = get_object_or_404(Tag, slug=tag_mark)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 5)
    page = request.GET.get("page")
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(
        request,
        "accounts/profile/dashboard.html",
        {"page": page, "posts": posts, "tag": tag, "pk": pk},
    )


def contacts(request):
    sent = False
    form_data = {}
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            form.save()
            subject = '{} ({}) прислал(а) сообщение "{}"'.format(
                form_data["full_name"], form_data["email"], form_data["subject"]
            )
            message = form_data["message"]
            send_mail(
                subject,
                message,
                "hyper_energy_tech@outlook.com",
                ["kilpatrik@outlook.com"],
            )
            sent = True
            messages.success(request, "Ваше сообщение отправлено")
    form = ContactForm()
    return render(
        request,
        "accounts/contacts.html",
        {"form": form, "sent": sent, "form_data": form_data},
    )
