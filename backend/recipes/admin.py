from django.contrib import admin

from .models import Tag, Ingredient, Recipe, IngredientRecipe


class BaseAdminSettings(admin.ModelAdmin):
    """Базовая кастомизация админ панели."""
    empty_value_display = '-пусто-'
    list_filter = ('author', 'name', 'tags')


class TagAdmin(BaseAdminSettings):
    """
    Кастомизация админ панели (управление тегам).
    """
    list_display = (
        'name',
        'color',
        'slug'
    )
    list_display_links = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)


class IngredientAdmin(BaseAdminSettings):
    """
    Кастомизация админ панели (управление ингредиентами).
    """
    list_display = (
        'name',
        'measurement_unit'
    )
    list_display_links = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)


class RecipeAdmin(BaseAdminSettings):
    """
    Кастомизация админ панели (управление рецептами).
    """
    list_display = (
        'name',
        'author'
    )
    list_display_links = ('name',)
    search_fields = ('name',)
    list_filter = ('author', 'name', 'tags')


class IngredientRecipeAdmin(admin.ModelAdmin):
    """
    Кастомизация админ панели (управление ингридиентами в рецептах).
    """
    list_display = (
        'recipe',
        'ingredient',
        'amount',
    )
    list_filter = ('recipe', 'ingredient')


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(IngredientRecipe, IngredientRecipeAdmin)
