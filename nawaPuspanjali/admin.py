# admin.py
from django.contrib import admin
from .models import *

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    model = Brand
    list_display = ['name','display_order','is_active']
    readonly_fields = ['slug']

@admin.register(NotebookType)
class NotebookTypeAdmin(admin.ModelAdmin):
    model = NotebookType
    list_display = ['name','display_order']
    readonly_fields = ['slug']

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    model = Size
    list_display = ['name', 'dimensions', 'slug', 'display_order']
    readonly_fields = ['slug']

    def dimensions(self, obj):
        return obj.dimensions
    dimensions.short_description = 'Dimensions'


@admin.register(Ruling)
class RulingAdmin(admin.ModelAdmin):
    model = Ruling
    list_display = ['name']
    readonly_fields = ['slug']

class NotebookVariantInline(admin.TabularInline):
    model = NotebookVariant
    extra = 1
    fields = [
        'size', 'ruling', 'price_per_unit',
        'is_active'
    ]
    show_change_link = True



@admin.register(Notebook)
class NotebookAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'notebook_type', 'variant_count', 'is_active']
    list_filter = ['brand', 'notebook_type', 'is_active']
    search_fields = ['name', 'brand__name', 'slug']
    readonly_fields = ['slug', 'created_at', 'updated_at']
    list_editable = ['is_active']
    inlines = [NotebookVariantInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'brand', 'notebook_type')
        }),
        ('Description', {
            'fields': ('base_description',),
            'description': 'General description that applies to all variants of this notebook'
        }),
        ('Image',{
            'fields':('image',),
            'description': 'General image for notebook'
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def variant_count(self, obj):
        return obj.variants.count()
    variant_count.short_description = 'Variants'


@admin.register(NotebookVariant)
class NotebookVariantAdmin(admin.ModelAdmin):
    list_display = [
        'display_name', 'slug', 'notebook', 'size', 'ruling',
        'price_per_unit', 'is_active'
    ]
    list_filter = [
        'notebook__brand', 'notebook__notebook_type',
        'size', 'ruling', 'is_active'
    ]
    search_fields = ['notebook__name', 'notebook__brand__name', 'slug']
    readonly_fields = ['slug', 'created_at', 'updated_at', 'display_name', 'full_description']
    list_editable = ['is_active']
    
    fieldsets = (
        ('Notebook', {  
            'fields': ('notebook',)
        }),
        ('Variant Specification', {
            'fields': ('size', 'slug', 'ruling', 'gsm')
        }),
        ('Pricing', {
            'fields': ('price_per_unit',),
            'description': 'Price per unit'
        }),
        ('Description', {
            'fields': ('variant_description', 'full_description'),
            'description': 'Variant-specific details. Full description combines base and variant descriptions.'
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'display_name'),
            'classes': ('collapse',)
        }),
    )
    
    def display_name(self, obj):
        return obj.display_name
    display_name.short_description = 'Full Name'
    
    # def price_per_unit(self, obj):
    #     return f"Rs. {obj.price_per_unit:.2f}"
    # price_per_unit.short_description = 'Price Per Unit'