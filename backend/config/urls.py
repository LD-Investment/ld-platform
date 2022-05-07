from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # API base url
    path("api/", include("config.api_router")),
]

if settings.DEBUG or settings.ENABLE_DEBUG_TOOLBAR:
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]

if settings.DEBUG or settings.ENABLE_DOCS:
    if "drf_yasg" in settings.INSTALLED_APPS:
        from django.conf.urls import url
        from drf_yasg import openapi
        from drf_yasg.views import get_schema_view
        from rest_framework import permissions

        schema_view = get_schema_view(
            openapi.Info(
                title="L&D Platform API",
                default_version="v0.0.1",
                description="L&D Platform API Swagger",
                terms_of_service="https://www.google.com/policies/terms/",
                contact=openapi.Contact(email="david.jeong0724@gmail.com"),
                license=openapi.License(name="BSD License"),
            ),
            public=True,
            permission_classes=(permissions.AllowAny,),
        )

        docs_urlpatterns = [
            url(
                r"^swagger(?P<format>\.json|\.yaml)$",
                schema_view.without_ui(cache_timeout=0),
                name="schema-json",
            ),
            url(
                r"^swagger/$",
                schema_view.with_ui("swagger", cache_timeout=0),
                name="schema-swagger-ui",
            ),
            url(
                r"^redoc/$",
                schema_view.with_ui("redoc", cache_timeout=0),
                name="schema-redoc",
            ),
        ]

        urlpatterns += [path(r"docs/", include(docs_urlpatterns))]
