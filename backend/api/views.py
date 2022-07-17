# from django.contrib.auth import get_user_model
from recipes.models import Ingredient, Recipe, Tag
from rest_framework.viewsets import ModelViewSet
from .pagination import CustomPagination
from .filters import IngredientSearchFilter
from djoser.views import UserViewSet

from .serializers import (IngredientSerializer, RecipeSerializer,
                          TagSerializer)


class UsersViewSet(UserViewSet):
    pagination_class = CustomPagination


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class IngredientViewSet(ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (IngredientSearchFilter,)
    search_fields = ('^name',)


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
