# from django.contrib.auth import get_user_model
from django.db.models import F, Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from weasyprint import HTML

from recipes.models import Cart, Ingredient, IngredientRecipe, Recipe, Tag

from .filters import IngredientSearchFilter
from .pagination import CustomPagination
from .serializers import (CartSerializer, CreateRecipeSerializer,
                          IngredientSerializer, RecipeSerializer,
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
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeSerializer
        return CreateRecipeSerializer

    @staticmethod
    def post_method_for_actions(request, pk, serializers):
        data = {'user': request.user.id, 'recipe': pk}
        serializer = serializers(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def delete_method_for_actions(request, pk, model):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        model_instance = get_object_or_404(model, user=user, recipe=recipe)
        model_instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=('post'))
    def shopping_cart(self, request, pk):
        return self.post_method_for_actions(
            request, pk, serializers=CartSerializer
        )

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        return self.delete_method_for_actions(
            request=request, pk=pk, model=Cart)

    @action(detail=False, methods=('get',))
    def download_shopping_cart(self, request):
        shopping_list = IngredientRecipe.objects.filter(
            recipe__cart__user=request.user
        ).values(
                name=F('ingredient__name'),
                measurement_unit=F('ingredient__measurement_unit')
            ).annotate(amount=Sum('amount')).values_list(
                'ingredient__name', 'amount', 'ingredient__measurement_unit'
            )
        html_template = render_to_string('recipes/pdf_template.html',
                                         {'ingredients': shopping_list})
        html = HTML(string=html_template)
        result = html.write_pdf()
        response = HttpResponse(result, content_type='application/pdf;')
        response['Content-Disposition'] = 'inline; filename=shopping_list.pdf'
        response['Content-Transfer-Encoding'] = 'binary'
        return response


class IngredientViewSet(ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (IngredientSearchFilter,)
    search_fields = ('^name',)


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
