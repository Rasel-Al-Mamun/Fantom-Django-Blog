from django.contrib import admin
from .models import *


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'status', 'created_on']
    prepopulated_fields = {'slug': ('name',)}

    class Meta:
        model = Category


admin.site.register(Category, CategoryAdmin)


class PostAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'category', 'status', 'thumbnail_tag']
    list_filter = ['category']
    readonly_fields = ['thumbnail_tag']
    prepopulated_fields = {'slug': ('title',)}
    list_per_page = 10

    class Meta:
        model = Post


admin.site.register(Post, PostAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'user', 'content', 'status']

    class Meta:
        model = Comment


admin.site.register(Comment, CommentAdmin)
