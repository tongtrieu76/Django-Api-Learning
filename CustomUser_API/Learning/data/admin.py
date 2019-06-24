from .models import CustomUser, Blog
from django.contrib import admin


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    fields = ('username', 'favorites')
    list_display = ['email', 'username', 'favorites']


@admin.register(Blog)
class AdminBlog(admin.ModelAdmin):
    fields = ('title', 'content', 'vote', 'accountID')
    list_display = ['title', 'vote', 'accountID']
    list_filter = ('accountID',)

