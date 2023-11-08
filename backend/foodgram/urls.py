from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('follows.urls')),
    path('api/tags/', include('tags.urls')),
    path('api/ingredients/', include('ingredients.urls')),
    path('api/recipes/', include('recipes.urls')),
    path('api/', include('users.urls')),
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.authtoken')),
    path("__debug__/", include("debug_toolbar.urls")),
] + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)
