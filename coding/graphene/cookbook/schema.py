import graphene
from ingredients.queries import IngredientsQueries
from ingredients.mutations import IngredientsMutations


class Query(IngredientsQueries):
    pass


class Mutation(IngredientsMutations):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
