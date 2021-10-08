from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe

import markdown

from ..models import Post

register = template.Library()


@register.simple_tag
def total_posts():
    return Post.objects.filter(post_status="опубликовано").count()


@register.inclusion_tag("blog/post/../../templates/blog/post_list.html")
def show_latest_posts(count=5):
    latest_posts = Post.objects.filter(post_status="опубликовано").order_by(
        "-published_date"
    )[:count]
    return {"latest_posts": latest_posts}


@register.simple_tag
def get_most_commented_posts(count=5):
    return (
        Post.objects.filter(post_status="опубликовано")
        .annotate(total_comments=Count("comments"))
        .order_by("-total_comments")[:count]
    )


@register.filter(name="markdown")
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
