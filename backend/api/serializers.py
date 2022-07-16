from recipes.models import Ingredient, Recipe, Tag
from rest_framework.serializers import ModelSerializer
from users.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email', 'username', 'first_name', 'last_name', "password"
        )
        ref_name = 'ReadOnlyUsers'


class RecipeSerializer(ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'
        ref_name = 'ReadOnlyUsers'


class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'
        ref_name = 'ReadOnlyUsers'


class TagSerializer(ModelSerializer):
    class Meta:
        model: Tag
        fields = '__all__'
        ref_name = 'ReadOnlyUsers'
