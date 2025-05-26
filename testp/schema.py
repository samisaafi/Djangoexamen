# DJANGO_DS_MAIN/schema.py
import graphene
from admin_themes.schema import AdminThemeQuery, AdminThemeMutation
# Import queries/mutations from other apps if you have them, e.g.:
# from main.schema import MainAppQuery, MainAppMutation

class Query(AdminThemeQuery, graphene.ObjectType):
    # Add other app queries here if needed
    pass

class Mutation(AdminThemeMutation, graphene.ObjectType):
    # Add other app mutations here if needed
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)