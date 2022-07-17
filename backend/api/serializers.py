from recipes.models import Ingredient, Recipe, Tag
from users.models import Follow
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from djoser.serializers import UserSerializer
from users.models import User


class UsersSerializer(UserSerializer):
    is_subscribed = SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed'
        )

    def get_is_subscribed(self, obj: User):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Follow.objects.filter(user=self.context['request'].user,
                                     author=obj).exists()


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
        model = Tag
        fields = '__all__'
        ref_name = 'ReadOnlyUsers'
