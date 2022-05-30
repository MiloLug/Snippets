import graphene
from graphene_django import DjangoObjectType

from ingredients.models import Category, Ingredient


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id", "name", "ingredients")


class IngredientType(DjangoObjectType):
    name = graphene.Field(graphene.String, first_letter=graphene.String(required=False))
    class Meta:
        model = Ingredient
        fields = ("id", "name", "notes", "category")

    @staticmethod
    def resolve_name(instance, info, first_letter=None):
        if first_letter:
            return instance.name if instance.name[0] == first_letter else None
        return instance.name
