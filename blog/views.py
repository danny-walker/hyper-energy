from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.db.models import Count
from django.contrib import messages

from taggit.models import Tag
from haystack.query import SearchQuerySet

from .models import Post
from .forms import PostForm, CommentForm, EmailPostForm


@login_required
def post_create(request):
    if not request.user.is_staff:
        messages.error(
            request, "У Вас нет необходимых прав для совершения этого действия"
        )
        return HttpResponseRedirect(reverse("blog:post_list"))
    if request.method == "POST":
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            new_post = post_form.save(commit=False)
            new_post.author = request.user
            new_post.published_date = timezone.now()
            new_post.save()
            for tag in post_form.cleaned_data["tags"]:
                new_post.tags.add(tag)
            return HttpResponseRedirect(new_post.get_absolute_url())
    else:
        post_form = PostForm()
    return render(request, "blog/posts/post_create.html", {"post_form": post_form})


@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, id=pk)
    if post.author != request.user:
        messages.error(
            request, "У Вас нет необходимых прав для совершения этого действия"
        )
        return HttpResponseRedirect(post.get_absolute_url())
    if request.method == "POST":
        post_form = PostForm(request.POST, instance=post)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            if post.tags != post_form.cleaned_data["tags"]:
                post.tags.clear()
                for tag in post_form.cleaned_data["tags"]:
                    post.tags.add(tag)
            return HttpResponseRedirect(post.get_absolute_url())
    else:
        post_form = PostForm(instance=post)
    return render(request, "blog/posts/post_update.html", {"post_form": post_form})


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.method == "POST":
        if post.author == request.user:
            post.delete()
            return HttpResponseRedirect(reverse("blog:post_list"))
        else:
            messages.error(
                request, "У Вас нет необходимых прав для совершения этого действия"
            )
    return HttpResponseRedirect(post.get_absolute_url())


def post_detail(request, year, month, day, pk, post):
    post = get_object_or_404(
        Post,
        id=pk,
        unique_mark=post,
        status="опубликовано",
        published_date__year=year,
        published_date__month=month,
        published_date__day=day,
    )

    comments = post.comments.filter(status=True)

    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.author = request.user
            new_comment.related_post = post
            new_comment.created_date = timezone.now()
            new_comment.save()
            return HttpResponseRedirect(post.get_absolute_url())
    else:
        comment_form = CommentForm()

    post_tags_ids = post.tags.values_list("id", flat=True)
    similar_posts = Post.objects.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count("tags")).order_by(
        "-same_tags", "-published_date"
    )[:4]
    total_likes = post.total_likes()
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        liked = True
    return render(
        request,
        "blog/posts/post_detail.html",
        {
            "post": post,
            "similar_posts": similar_posts,
            "comments": comments,
            "total_likes": total_likes,
            "comment_form": comment_form,
            "liked": liked,
        },
    )


def post_share(request, pk):
    post = get_object_or_404(Post, id=pk, status="опубликовано")
    sent = False
    form_data = {}
    if request.method == "POST":
        email_form = EmailPostForm(request.POST)
        if email_form.is_valid():
            form_data = email_form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) советует Вам почитать "{}"'.format(
                form_data["sender_name"], form_data["sender_email"], post.title
            )
            message = 'Почитайте "{}" на {}\n\nКомментарий {}\'s : {}'.format(
                post.title,
                post_url,
                form_data["sender_name"],
                form_data["sender_comments"],
            )
            send_mail(
                subject,
                message,
                "hyper_energy_tech@outlook.com",
                [form_data["recipient_email"]],
            )
            sent = True
    else:
        email_form = EmailPostForm()
    return render(
        request,
        "blog/posts/post_share.html",
        {"post": post, "email_form": email_form, "sent": sent, "form_data": form_data},
    )


def post_list(request, tag_mark=None):
    object_list = Post.objects.filter(status="опубликовано")
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
        request, "blog/posts/post_list.html", {"page": page, "posts": posts, "tag": tag}
    )


def post_search(request):
    query = {}
    results = {}
    total_results = {}
    if request.method == "GET":
        query = request.GET.get("query")
        results = SearchQuerySet().models(Post).filter(content=query).load_all()
        total_results = results.count()
    return render(
        request,
        "blog/posts/post_search.html",
        {"query": query, "results": results, "total_results": total_results},
    )


@login_required
def post_like(request, pk):
    post = get_object_or_404(Post, id=pk)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    like_data = {"post": post, "liked": liked, "total_likes": post.total_likes()}
    if request.is_ajax():
        html = render_to_string(
            "blog/posts/includes/post_like.html", like_data, request=request
        )
        return JsonResponse({"html": html})


def index(request):
    latest_posts = Post.objects.filter(status="опубликовано").order_by(
        "-published_date"
    )[:3]
    return render(request, "blog/index.html", {"latest_posts": latest_posts})
