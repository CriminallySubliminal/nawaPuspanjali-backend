# views.py
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import *
from .serializers import BrandSerializer, NotebookDetailSerializer, NotebookListSerializer, NotebookTypeSerializer, NotebookVariantListSerializer, NotebookVariantDetailSerializer, RulingSerializer, SizeSerializer
from .filters import NotebookVariantFilter, NotebookFilter

class NotebookVariantViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = NotebookVariant.objects.select_related(
        'notebook', 
        'notebook__brand', 
        'notebook__notebook_type',
        'size', 
        'ruling'
    ).filter(is_active=True, notebook__is_active=True)
    
    serializer_class = NotebookVariantListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = NotebookVariantFilter
    search_fields = ['notebook__name', 'notebook__brand__name']
    ordering_fields = ['price_per_dozen', 'no_of_pages', 'notebook__name']
    ordering = ['notebook__brand__name', 'notebook__name', 'size__display_order']
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return NotebookVariantDetailSerializer
        return NotebookVariantListSerializer


class NotebookViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Notebook.objects.prefetch_related(
        'variants',
        'variants__size',
        'variants__ruling'
    ).select_related('brand', 'notebook_type').filter(is_active=True)
    
    serializer_class = NotebookListSerializer
    filterset_class = NotebookFilter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'brand__name']
    ordering_fields = ['name', 'brand__name']
    ordering = ['brand__name', 'name']
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return NotebookDetailSerializer
        return NotebookListSerializer


# Filter options endpoint
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def filter_options(request):
    """Return all available filter options"""
    return Response({
        'brands': BrandSerializer(Brand.objects.filter(is_active=True), many=True).data,
        'notebook_types': NotebookTypeSerializer(NotebookType.objects.all(), many=True).data,
        'sizes': SizeSerializer(Size.objects.all(), many=True).data,
        'rulings': RulingSerializer(Ruling.objects.all(), many=True).   data,
    })