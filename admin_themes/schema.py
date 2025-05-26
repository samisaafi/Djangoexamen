import graphene
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import superuser_required # For security
from graphql import GraphQLError

from .models import AdminTheme
from .tasks import compile_scss_and_deploy_assets, analyze_theme_for_accessibility

class AdminThemeType(DjangoObjectType):
    class Meta:
        model = AdminTheme
        fields = '__all__'

class AdminThemeQuery(graphene.ObjectType):
    all_admin_themes = graphene.List(AdminThemeType)
    admin_theme = graphene.Field(AdminThemeType, id=graphene.Int())
    active_admin_theme = graphene.Field(AdminThemeType)

    def resolve_all_admin_themes(root, info):
        return AdminTheme.objects.all()

    def resolve_admin_theme(root, info, id):
        try:
            return AdminTheme.objects.get(pk=id)
        except AdminTheme.DoesNotExist:
            return None

    def resolve_active_admin_theme(root, info):
        try:
            return AdminTheme.objects.get(is_active=True)
        except AdminTheme.DoesNotExist:
            return None

class ApplyAdminTheme(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    Output = AdminThemeType # Returns the updated theme

    @superuser_required # Requires superuser to execute
    def mutate(root, info, id):
        try:
            theme = AdminTheme.objects.get(pk=id)
        except AdminTheme.DoesNotExist:
            raise GraphQLError(f"AdminTheme with ID {id} not found.")

        # Deactivate all other themes
        AdminTheme.objects.filter(is_active=True).exclude(pk=theme.pk).update(is_active=False)

        # Activate the selected theme
        theme.is_active = True
        theme.save()

        analyse_theme_for_accessibility.delay(theme.pk)
        compile_scss_and_deploy_assets.delay(theme.pk)

        return theme

class AdminThemeMutation(graphene.ObjectType):
    apply_admin_theme = ApplyAdminTheme.Field()