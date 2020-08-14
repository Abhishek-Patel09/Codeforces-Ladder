from django.contrib import admin
from . import models

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    ordering = ['name']


class ProblemAdmin(admin.ModelAdmin):
    list_display = ['problemName', 'problemId', 'contestId', 'solvedCount', 'rating', 'category']
    list_filter = ['category', 'rating']

admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Problem, ProblemAdmin)
