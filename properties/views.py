from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from .utils import get_all_properties

# Cache view response for 15 minutes
@cache_page(60 * 15)
def property_list(request):
    """
    Returns all property listings as JSON.
    Uses Redis low-level caching (1 hour) for the queryset,
    and view-level caching (15 mins) for the response.
    """
    properties = get_all_properties()
    return JsonResponse({"data": properties})