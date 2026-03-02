from django.contrib import admin
from .models import Question, Answer


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'question_type', 'difficulty', 'views', 'likes', 'created_at')
    search_fields = ['text']
    list_filter = ['question_type', 'difficulty']
    readonly_fields = ['views', 'likes', 'created_at', 'updated_at']
    fieldsets = (
        (None, {
            'fields': ('text', 'question_type', 'difficulty', 'tags'),
        }),
        ('Engagement', {
            'fields': ('views', 'likes'),
            'description': 'These counters are managed automatically.',
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'votes', 'created_at')
    list_filter = ['question']
    search_fields = ['text']
    readonly_fields = ['created_at', 'updated_at']
