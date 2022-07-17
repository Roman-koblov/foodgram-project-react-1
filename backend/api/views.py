# from django.contrib.auth import get_user_model
from recipes.models import Ingredient, Recipe, Tag
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .pagination import CustomPagination
from .filters import IngredientSearchFilter
from djoser.views import UserViewSet

from .serializers import (IngredientSerializer, RecipeSerializer,
                          TagSerializer)


class UsersViewSet(UserViewSet):
    pagination_class = CustomPagination

    @action(['get'], detail=False, permission_classes=[IsAuthenticated])
    def me(self, request, *args, **kwargs):
        self.get_object = self.get_instance
        return self.retrieve(request, *args, **kwargs)


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
