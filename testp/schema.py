# DJANGO_DS_MAIN/schema.py
import graphene
import graphql_jwt
import main.schema
# Import queries/mutations from other apps if you have them, e.g.:
# from main.schema import MainAppQuery, MainAppMutation

class Query(main.schema.AdminThemeQuery, graphene.ObjectType):
    # Add other app queries here if needed
    pass

class Mutation(main.schema.AdminThemeMutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)