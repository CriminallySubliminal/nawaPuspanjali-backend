# serializers.py
from rest_framework import serializers
from .models import *
from cloudinary.utils import cloudinary_url

class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ['id', 'name', 'width', 'height', 'unit', 'slug', 'display_order']


class RulingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ruling
        fields = ['id', 'name', 'slug']


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'slug', 'display_order', 'description']


class NotebookTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotebookType
        fields = ['id', 'name', 'display_order', 'slug']


class NotebookVariantListSerializer(serializers.ModelSerializer):
    """Serializer for variant in list view"""
    size = SizeSerializer(read_only=True)
    ruling = RulingSerializer(read_only=True)
    
    
    class Meta:
        model = NotebookVariant
        fields = [
            'id', 'slug', 'size', 'ruling', 'price_per_unit', 'is_active'
        ]


class NotebookListSerializer(serializers.ModelSerializer):
    """Serializer for notebook list - shows base notebook with all variants"""
    brand = BrandSerializer(read_only=True)
    notebook_type = NotebookTypeSerializer(read_only=True)
    variants = NotebookVariantListSerializer(many=True, read_only=True)
    available_sizes = SizeSerializer(many=True, read_only=True)
    available_rulings = RulingSerializer(many=True, read_only=True)
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = Notebook
        fields = [
            'id', 'name', 'slug', 'brand', 'notebook_type','image',
            'base_description', 'is_active',
            'variants', 'available_sizes', 'available_rulings',
            'created_at', 'updated_at'
        ]

    def get_image(self,obj):
        return obj.image.url if obj.image else None



class NotebookVariantDetailSerializer(serializers.ModelSerializer):
    """Detailed variant serializer"""
    size = SizeSerializer(read_only=True)
    ruling = RulingSerializer(read_only=True)
    notebook_name = serializers.CharField(source='notebook.name', read_only=True)
    notebook_brand = BrandSerializer(source='notebook.brand', read_only=True)
    notebook_type = NotebookTypeSerializer(source='notebook.notebook_type', read_only=True)
   
    class Meta:
        model = NotebookVariant
        fields = [
            'id', 'slug','notebook_name', 'notebook_brand', 'notebook_type','size', 'ruling', 'gsm', 'price_per_unit',
            'full_description', 'display_name','is_active','created_at', 'updated_at'
        ]


class NotebookDetailSerializer(serializers.ModelSerializer):
    """Detailed notebook with all variants"""
    brand = BrandSerializer(read_only=True)
    notebook_type = NotebookTypeSerializer(read_only=True)
    variants = NotebookVariantDetailSerializer(many=True, read_only=True)
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = Notebook
        fields = [
            'id', 'name', 'slug',
            'brand', 'notebook_type',
            'image',
            'base_description',
            'variants',
            'is_active',
            'created_at', 'updated_at'
        ]
    
    def get_image(self,obj):
        return obj.image.url if obj.image else None