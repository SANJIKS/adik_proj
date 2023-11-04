from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView

schema_view = get_schema_view(
    openapi.Info(
        title="Уважаемый",
        default_version='v1000',
        description="I like black boys(big black boys)",
        terms_of_service="https://www.hahahahahahahahahahahahahaha.com/",
        contact=openapi.Contact(email="sanzarmaratov588@gmail.com"),
        license=openapi.License(name="Sanjik License.inc"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('accounts/', include('allauth.urls')),
    path('', include('users.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('tenders/', include('tenders.urls'))
    ]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
            document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
            document_root=settings.MEDIA_ROOT)
