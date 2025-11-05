from django.shortcuts import render
from django.views.generic import ListView
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from .models import Property
from .utils import get_all_properties


@method_decorator(cache_page(60 * 15), name='dispatch')  # Cache for 15 minutes
class PropertyListView(ListView):
    model = Property
    template_name = 'properties/property_list.html'
    context_object_name = 'properties'

    def get_queryset(self):
        """Return all properties ordered by creation date."""
        return Property.objects.all().order_by('-created_at')


@cache_page(60 * 15)
def property_list(request):
    """Function-based view that returns all properties as JSON.

    Response cached in Redis for 15 minutes by the @cache_page decorator.
    Returns JSON in the shape: {"data": [ {property fields...}, ... ] }
    """
    qs = get_all_properties()
    data = []
    for p in qs:
        data.append({
            'id': p.id,
            'title': p.title,
            'description': p.description,
            'price': str(p.price),
            'location': p.location,
            'bedrooms': p.bedrooms,
            'bathrooms': p.bathrooms,
            'square_feet': p.square_feet,
            'property_type': p.property_type,
            'status': p.status,
            'created_at': p.created_at.isoformat() if p.created_at else None,
            'updated_at': p.updated_at.isoformat() if p.updated_at else None,
        })

    return JsonResponse({'data': data})