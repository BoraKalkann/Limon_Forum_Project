from django.contrib import admin
from .models import Comment 

class ReplyInline(admin.TabularInline):
    model = Comment
    fk_name = 'parent'  
    extra = 0
    verbose_name = 'Reply'
    verbose_name_plural = 'Replies'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'content_short', 'created_at', 'parent')
    list_filter = ('created_at', 'parent', 'user')
    search_fields = ('user__username', 'content')
    ordering = ('-created_at',)
    inlines = [ReplyInline]

    def content_short(self, obj):
        return obj.content[:50] + ("..." if len(obj.content) > 50 else "")
    content_short.short_description = 'Content'

