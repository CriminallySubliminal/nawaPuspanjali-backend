# filters.py
from django_filters import rest_framework as filters
from .models import NotebookVariant, Notebook

class NotebookVariantFilter(filters.FilterSet):
    """Filter for variants"""
    brand = filters.NumberFilter(field_name='notebook__brand__id')
    notebook_type = filters.NumberFilter(field_name='notebook__notebook_type__id')
    size = filters.NumberFilter(field_name='size__id')
    ruling = filters.NumberFilter(field_name='ruling__id')
    min_price = filters.NumberFilter(field_name='price_per_dozen', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price_per_dozen', lookup_expr='lte')
    min_pages = filters.NumberFilter(field_name='no_of_pages', lookup_expr='gte')
    
    class Meta:
        model = NotebookVariant
        fields = ['size', 'ruling', 'is_active']

class NotebookFilter(filters.FilterSet):
    brand = filters.NumberFilter(field_name='brand__id')
    notebook_type = filters.NumberFilter(field_name='notebook_type__id')
    # size = filters.NumberFilter(field_name='size__id')
    # ruling = filters.NumberFilter(field_name='ruling__id')
    
    class Meta:
        model  = Notebook
        fields = ['brand', 'notebook_type']