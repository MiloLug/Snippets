import graphene

from ingredients.models import Ingredient
from ingredients.types import IngredientType


class CreateIngredient(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        notes = graphene.String(required=True)
        category_id = graphene.Int(required=True)

    # The class attributes define the response of the mutation
    ingredient = graphene.Field(IngredientType)

    @staticmethod
    def mutate(parent, info, name, notes, category_id):
        ingredient = Ingredient.objects.create(
            name=name,
            notes=notes,
            category_id=category_id
        )
        # Notice we return an instance of this mutation
        return CreateIngredient(ingredient=ingredient)


class IngredientsMutations(graphene.ObjectType):
    create_ingredient = CreateIngredient.Field()
