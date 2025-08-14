from django.contrib import admin

# Register your models here.
from .models import Article, Comment

class CommentInLine(admin.TabularInline):
    model = Comment
    extra = 0
    
class ArticleAdmin(admin.ModelAdmin):
    inlines = [
        CommentInLine
    ]

admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)