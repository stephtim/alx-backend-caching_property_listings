from django.shortcuts import render
from django.views.generic import ListView
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from .models import Property

@method_decorator(cache_page(60 * 15), name='dispatch')  # Cache for 15 minutes
class PropertyListView(ListView):
    model = Property
    template_name = 'properties/property_list.html'
    context_object_name = 'properties'
    
    def get_queryset(self):
        """Return all properties ordered by creation date."""
        return Property.objects.all().order_by('-created_at')