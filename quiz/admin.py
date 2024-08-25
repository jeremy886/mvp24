from django.contrib import admin
from .models import Quiz, Question, Choice, UserAnswer
from django.db import models


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ('text', 'tags', 'difficulty', 'created_at')
    search_fields = ('text', 'difficulty')


class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'max_questions')
    search_fields = ('title',)
    filter_horizontal = ('questions',)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'questions':
            kwargs['queryset'] = Question.objects.order_by('-created_at')
        return super().formfield_for_manytomany(db_field, request, **kwargs)


class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'question', 'selected_choice', 'is_correct')
    list_filter = ('quiz', 'user', 'is_correct')
    search_fields = ('quiz__title', 'user__username', 'question__text')
    raw_id_fields = ('user', 'quiz', 'question', 'selected_choice')


admin.site.register(UserAnswer, UserAnswerAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Quiz, QuizAdmin)
