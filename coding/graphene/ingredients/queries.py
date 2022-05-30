import graphene

from ingredients.models import Category, Ingredient
from ingredients.types import CategoryType, IngredientType


class IngredientsQueries(graphene.ObjectType):
    all_ingredients = graphene.List(IngredientType)
    category_by_name = graphene.Field(CategoryType, name=graphene.String(required=True))

    @staticmethod
    def resolve_all_ingredients(parent, info):
        # We can easily optimize query count in the resolve method
        return Ingredient.objects.select_related("category").all()

    @staticmethod
    def resolve_category_by_name(parent, info, name):
        try:
            return Category.objects.get(name=name)
        except Category.DoesNotExist:
            return None
