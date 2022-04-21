from django.contrib import admin
from .models import *


# Register your models here.

# class QuestionInline(admin.TabularInline):
#     model = QuestionAdmin
#     max_num = 30
#     min_num = 1


# @admin.register(Survey)
# class PostAdmin(admin.ModelAdmin):
#     inlines = [QuestionInline, ]
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)
    search_fields = ['name']

class SurveyAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "category", "author",)
    list_display_links = ("id", "title")
    search_fields = ["title"]
    list_filter = ("category",)

class SumbitionAdmin(admin.ModelAdmin):
    list_display = ("id", "participant_email")
    list_display_links = ("id", "participant_email")
    search_fields = ("participant_email",)


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ("id", "question")
    list_display_links = ("id", "question")
    search_fields = ["text"]
    list_filter = ("text",)

class ChoiceInline(admin.TabularInline):
    model = Choice
    max_num = 20
    min_num = 2

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline, ]
    list_display = ("id", "survey")
    list_display_links = ("id", "survey")
    search_fields = ["survey"]
    list_filter = ("survey",)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "survey")
    list_display_links = ("id", "name", "email", "survey")
    search_fields = ["name"]
    list_filter = ("survey",)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Survey, SurveyAdmin)
admin.site.register(Sumbition, SumbitionAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Rating)
admin.site.register(RatingStar)