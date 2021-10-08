from django.contrib import admin
from .models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "unique_mark", "author", "published_date", "status")
    list_filter = ("status", "created_date", "published_date", "author")
    search_fields = ("title", "text")
    prepopulated_fields = {"unique_mark": ("title",)}
    raw_id_fields = ("author",)
    date_hierarchy = "published_date"
    ordering = ["status", "published_date"]


admin.site.register(Post, PostAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ("author", "related_post", "created_date", "status")
    list_filter = ("status", "created_date", "updated_date")
    search_fields = ("author", "text")


admin.site.register(Comment, CommentAdmin)
