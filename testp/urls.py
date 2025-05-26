
from django.contrib import admin
from django.conf import settings
from django.urls import path,include
from .schema import schema
from graphene_django.views import GraphQLView
from .admin_site import custom_admin_site 
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', custom_admin_site.urls),
    path('api/admin_themes/', include('admin_themes.urls')),
    path('graphql/', GraphQLView.as_view(graphiql=True, schema=schema)),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)