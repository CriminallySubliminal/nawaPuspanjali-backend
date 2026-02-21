from django.db import models
from django.utils.text import slugify
from decimal import Decimal
from django.core.validators import MinValueValidator
from cloudinary.models import CloudinaryField
import string
import random

class SlugMixin(models.Model):
    slug = models.SlugField(max_length = 255, unique=True, blank=True)

    class Meta:
        abstract = True
    
    def get_slug_source(self):
        if hasattr(self, 'slug_source'):
            if isinstance(self.slug_source, str):
                return getattr(self, self.slug_source, '')
            elif isinstance(self.slug_source, (list, tuple)):
                return ' '.join(str(getattr(self, field, '')) for field in self.slug_source)
        return getattr(self, 'name', str(self.pk or ''))

    def generate_unique_slug(self):
        base_slug = slugify(self.get_slug_source())
        # if not base_slug:
        #     return f"item-{self.pk or self._generate_random_string()}"
        slug = base_slug
        counter = 1

        ModelClass = self.__class__
        
        while ModelClass.objects.filter(slug = slug).exclude(pk=self.pk).exists():
            suffix =  f"--{counter}"
            slug = f"{base_slug}{suffix}"
            counter += 1

        return slug
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug()
        super().save(*args, **kwargs)



class Brand(SlugMixin, models.Model):
    name = models.CharField(max_length=50, unique=True)
    paper = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default = True)
    display_order = models.PositiveIntegerField(default=0)

    slug_source = 'name'
    
    class Meta:
        ordering = ['display_order','name']
    
    def __str__(self):
        return self.name
    

class NotebookType(SlugMixin, models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    display_order = models.PositiveIntegerField(default=0)

    slug_source = 'name'

    class Meta:
        ordering = ['display_order','name']
    
    def __str__(self):
        return self.name
    
class Size(SlugMixin, models.Model):

    choices=[('mm', 'Millimeters'), ('cm', 'Centimeters'), ('in', 'Inches')]

    name = models.CharField(max_length=50, unique=True)
    width = models.FloatField(default=0.0)
    height = models.FloatField(default=0.0)
    unit = models.CharField(max_length=10, choices=choices, default='mm')
    display_order = models.IntegerField(default = 0)
    
    slug_source =  'name'

    class Meta:
        ordering = ['display_order','name']
    
    def __str__(self):
        return self.name
    
    @property
    def dimensions(self):
        return f'{self.width} x {self.height} {self.unit}'

    
class Ruling(SlugMixin, models.Model):
    name = models.CharField(max_length = 100, unique = True)
    description = models.TextField(blank=True)

    slug_source = 'name'
    
    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
    
# models.py
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

class Notebook(SlugMixin, models.Model):
    """
    Base notebook product - represents the general notebook
    Example: "300 No. Puspanjali Copy"
    """
    name = models.CharField(max_length=255)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='notebooks')
    notebook_type = models.ForeignKey(NotebookType, on_delete=models.CASCADE, related_name='notebooks')
    image = CloudinaryField(
        folder='notebooks/images',
        transformation=[
            {
                'quality': 85,
                'fetch_format': 'auto',
            },
        ]
    )
    
    # General description (common to all variants)
    base_description = models.TextField(blank=True, help_text="General description for all variants")
    
    # Availability
    is_active = models.BooleanField(default=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Slug
    slug_source = ['name', 'brand__name']
    
    class Meta:
        ordering = ['brand__name', 'notebook_type__name', 'name']
        unique_together = [['name', 'brand', 'notebook_type']]
        indexes = [
            models.Index(fields=['brand', 'notebook_type']),
            models.Index(fields=['is_active'])
        ]
    
    def get_slug_source(self):
        brand_name = self.brand.name if self.brand else ''
        return f"{self.name} {brand_name}"
    
    def __str__(self):
        return f"{self.name} - {self.brand.name}"
    
    @property
    def available_sizes(self):
        """Get all sizes this notebook is available in"""
        return Size.objects.filter(notebook_variants__notebook=self).distinct()
    
    @property
    def available_rulings(self):
        """Get all rulings this notebook is available in"""
        return Ruling.objects.filter(notebook_variants__notebook=self).distinct()


class NotebookVariant( SlugMixin, models.Model):
    """
    Specific variant of a notebook with size, ruling, price, and images
    Example: "300 No. Puspanjali Copy - Book Size - 2-lined ruling"
    """
    notebook = models.ForeignKey(
        Notebook, 
        on_delete=models.CASCADE, 
        related_name='variants'
    )
    size = models.ForeignKey(
        Size, 
        on_delete=models.CASCADE, 
        related_name='notebook_variants'
    )
    ruling = models.ForeignKey(
        Ruling, 
        on_delete=models.CASCADE, 
        related_name='notebook_variants'
    )
    gsm = models.PositiveIntegerField(default=0)
    
    # Variant-specific details
    
    price_per_unit = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    
    # Variant-specific description (optional)
    variant_description = models.TextField(
        blank=True,
        help_text="Additional details specific to this size/ruling combination"
    )
    
    # Availability
    is_active = models.BooleanField(default=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    class Meta:
        ordering = ['notebook', 'size__display_order', 'ruling__name']
        unique_together = [['notebook', 'size', 'ruling']]
        indexes = [
            models.Index(fields=['notebook', 'size', 'ruling']),
            models.Index(fields=['is_active'])
        ]
        verbose_name = 'Notebook Variant'
        verbose_name_plural = 'Notebook Variants'
    
    def get_slug_source(self):
        
        notebook_name = self.notebook.name if self.notebook else ''
        size_name = self.size.name if self.size else ''
        ruling_name = self.ruling.name if self.ruling else ''
        
        return f"{notebook_name} {size_name} {ruling_name}"


    def __str__(self):
        return f"{self.notebook.name} - {self.size.name} - {self.ruling.name}"
    
    @property
    def full_description(self):
        """Combine base and variant descriptions"""
        descriptions = []
        if self.notebook.base_description:
            descriptions.append(self.notebook.base_description)
        if self.variant_description:
            descriptions.append(self.variant_description)
        return "\n\n".join(descriptions)
    
    @property
    def display_name(self):
        """Full display name with all attributes"""
        return f"{self.notebook.name} ({self.size.name}, {self.ruling.name})"
    
    # @property
    # def price_per_unit(self):
    #     """Calculate price per single notebook"""
    #     return self.price_per_dozen / 12.00

    
    def clean(self):
        """Validation"""
        super().clean()
        
        # Ensure notebook is active if variant is active
        if self.is_active and not self.notebook.is_active:
            from django.core.exceptions import ValidationError
            raise ValidationError('Cannot activate variant when base notebook is inactive')