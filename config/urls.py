"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from quickcheck.views import (
    StoryViewSet,
    JobViewSet,
    CommentViewSet,
    PollViewSet,
    PollOptViewSet,
    AllItemsViewSet
)
from accounts.views import UserViewSet


API_TITLE = 'QuickCheck API'
API_DESCRIPTION = 'A Web API for navigating HackerNews.'
schema_view = get_schema_view(
    openapi.Info(
        title=API_TITLE,
        default_version='v1',
        description=API_DESCRIPTION,
        contact=openapi.Contact(email="alphadev.onyenso@gmail.com")
    ),
    public=True,
    permission_classes=[AllowAny],

)


router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"stories", StoryViewSet, basename="story")
router.register(r"jobs", JobViewSet, basename="job")
router.register(r"comments", CommentViewSet, basename="comment")
router.register(r"polls", PollViewSet, basename="poll")
router.register(r"pollopts", PollOptViewSet, basename="pollopt")
router.register(r"all", AllItemsViewSet, basename="all")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path("swagger-docs/", schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('docs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc')
]
