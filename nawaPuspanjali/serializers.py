# serializers.py
from rest_framework import serializers
from .models import *

class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ['id', 'name', 'slug', 'display_order']


class RulingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ruling
        fields = ['id', 'name', 'slug']


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'slug', 'description']


class NotebookTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotebookType
        fields = ['id', 'name', 'slug']


class NotebookVariantListSerializer(serializers.ModelSerializer):
    """Serializer for variant in list view"""
    size = SizeSerializer(read_only=True)
    ruling = RulingSerializer(read_only=True)
    price_per_unit = serializers.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        read_only=True
    )
    
    class Meta:
        model = NotebookVariant
        fields = [
            'id', 'slug', 'size', 'ruling', 'no_of_pages', 'price_per_dozen', 'price_per_unit', 'is_active'
        ]


class NotebookListSerializer(serializers.ModelSerializer):
    """Serializer for notebook list - shows base notebook with all variants"""
    brand = BrandSerializer(read_only=True)
    notebook_type = NotebookTypeSerializer(read_only=True)
    variants = NotebookVariantListSerializer(many=True, read_only=True)
    available_sizes = SizeSerializer(many=True, read_only=True)
    available_rulings = RulingSerializer(many=True, read_only=True)
    
    class Meta:
        model = Notebook
        fields = [
            'id', 'name', 'slug', 'brand', 'notebook_type',
            'base_description', 'is_active',
            'variants', 'available_sizes', 'available_rulings',
            'created_at', 'updated_at'
        ]


class NotebookVariantDetailSerializer(serializers.ModelSerializer):
    """Detailed variant serializer"""
    size = SizeSerializer(read_only=True)
    ruling = RulingSerializer(read_only=True)
    notebook_name = serializers.CharField(source='notebook.name', read_only=True)
    notebook_brand = BrandSerializer(source='notebook.brand', read_only=True)
    notebook_type = NotebookTypeSerializer(source='notebook.notebook_type', read_only=True)
    price_per_unit = serializers.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        read_only=True
    )
    
    class Meta:
        model = NotebookVariant
        fields = [
            'id', 'slug','notebook_name', 'notebook_brand', 'notebook_type','size', 'ruling','no_of_pages', 'price_per_dozen', 'price_per_unit',
            'front_cover', 'back_cover','full_description', 'display_name','is_active','created_at', 'updated_at'
        ]


class NotebookDetailSerializer(serializers.ModelSerializer):
    """Detailed notebook with all variants"""
    brand = BrandSerializer(read_only=True)
    notebook_type = NotebookTypeSerializer(read_only=True)
    variants = NotebookVariantDetailSerializer(many=True, read_only=True)
    
    class Meta:
        model = Notebook
        fields = [
            'id', 'name', 'slug',
            'brand', 'notebook_type',
            'base_description',
            'variants',
            'is_active',
            'created_at', 'updated_at'
        ]