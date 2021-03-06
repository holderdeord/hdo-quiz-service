from django.shortcuts import redirect
from rest_framework.pagination import PageNumberPagination

from api.permissions import AllowAnyOrDjangoModelPermissionsOrAnonReadOnly
from api.serializers.manuscript import ManuscriptSerializer, CategorySerializer, ManuscriptListSerializer, \
    HdoCategorySerializer
from quiz.models import Manuscript, Category, HdoCategory
from rest_framework import exceptions, permissions, views, reverse, authentication

from rest_framework.generics import (
    get_object_or_404, RetrieveAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView)


class ManuscriptView(views.APIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def get_queryset(self, category_id):
        return Manuscript.objects.filter(category_id=category_id).orderby('?')

    def redirect(self, request, category_id, format=None, queryset=None):
        queryset = queryset or self.get_queryset(category_id)

        if len(queryset) > 0:
            return redirect(reverse.reverse('api:manuscript', request=request, format=format, kwargs={
                'category_id': category_id,
                'manuscript_id': queryset[0].pk,
            }))
        else:
            raise exceptions.NotFound()

    def get(self, request, category_id, manuscript_id=None, format=None):
        queryset = self.get_queryset(category_id)

        if manuscript_id:
            manuscript = get_object_or_404(queryset, pk=manuscript_id)
        else:
            return self.redirect(request, category_id)


class ManuscriptDetailView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [AllowAnyOrDjangoModelPermissionsOrAnonReadOnly]
    queryset = Manuscript.objects.select_related('category', 'hdo_category')
    serializer_class = ManuscriptSerializer


class ManuscriptListView(ListCreateAPIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [AllowAnyOrDjangoModelPermissionsOrAnonReadOnly]
    queryset = Manuscript.objects.select_related('category', 'hdo_category')
    serializer_class = ManuscriptListSerializer
    pagination_class = PageNumberPagination


class CategoryRetrieveView(RetrieveAPIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryListView(ListCreateAPIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.AllowAny]
    queryset = Category.objects
    serializer_class = CategorySerializer


class HdoCategoryListView(ListCreateAPIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.AllowAny]
    queryset = HdoCategory.objects
    serializer_class = HdoCategorySerializer
