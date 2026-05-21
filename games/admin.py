from django.contrib import admin
from .models import Game, Review, Category, Screenshot

class ScreenshotInline(admin.TabularInline):
    model = Screenshot
    extra = 3

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'developer', 'category', 'created_at')
    inlines = [ScreenshotInline]

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("game", "author", "rating", "created_at")

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

