from distutils.util import strtobool

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe, Tag, Ingredient
from recipe.serializers import (
    RecipeDetailSerializer,
    RecipeImageSerializer,
    RecipeSerializer,
    TagSerializer,
    IngredientSerializer
)


class BaseRecipeComponentViewSet(
        viewsets.GenericViewSet,
        mixins.ListModelMixin,
        mixins.CreateModelMixin):
    """Base viewset for user owned recipe components"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        assinged_only = strtobool(
            self.request.query_params.get("assigned_only", "False")
        )
        queryset = self.queryset
        if assinged_only:
            queryset = queryset.filter(recipe__isnull=False)

        return (
            queryset.filter(user=self.request.user)
            .order_by("-name")
            .distinct()
        )

    def perform_create(self, serializer):
        """Create a new component for this user"""
        serializer.save(user=self.request.user)


class TagViewSet(BaseRecipeComponentViewSet):
    """Manage tags in the database"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(BaseRecipeComponentViewSet):
    """Manage tags in the database"""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """Manage recipes in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def _params_to_ints(self, query_params):
        """Convert a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in query_params.split(",")]

    def get_queryset(self):
        """Retrieve the recipes for the authenticated user"""
        tags = self.request.query_params.get("tags")
        ingredients = self.request.query_params.get("ingredients")
        queryset = self.queryset
        if tags:
            tag_ids = self._params_to_ints(tags)
            queryset = queryset.filter(tags__id__in=tag_ids)
        if ingredients:
            ingredient_ids = self._params_to_ints(ingredients)
            queryset = queryset.filter(ingredients__id__in=ingredient_ids)

        return queryset.filter(user=self.request.user).order_by("-id")

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == "retrieve":
            return RecipeDetailSerializer
        elif self.action == "upload_image":
            return RecipeImageSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe for this user"""
        serializer.save(user=self.request.user)

    @action(methods=["POST"], detail=True, url_path="upload-image")
    def upload_image(self, request, *args, **kwargs):
        """Upload and image to a recipe"""
        recipe = self.get_object()
        serializer = self.get_serializer(recipe, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
