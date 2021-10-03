from django.urls import path, include

from rest_framework.routers import DefaultRouter
from recipe import views

routers = DefaultRouter(trailing_slash=False)
routers.register("tags", views.TagViewSet)

app_name = "recipe"

urlpatterns = [
    path("", include(routers.urls))
]
