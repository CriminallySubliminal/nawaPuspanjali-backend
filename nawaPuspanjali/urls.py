# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NotebookViewSet, NotebookVariantViewSet, filter_options

router = DefaultRouter()
router.register(r'notebooks', NotebookViewSet, basename='notebook')
router.register(r'notebook-variants', NotebookVariantViewSet, basename='notebook-variant')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/filter-options/', filter_options, name='filter-options'),
]