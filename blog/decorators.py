from rest_framework.throttling import UserRateThrottle
from rest_framework.decorators import throttle_classes
from functools import wraps
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework import status

def rate_limit(key_prefix, limit=100, period=3600):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(self, request, *args, **kwargs):
            if request.user.is_authenticated:
                cache_key = f"{key_prefix}_{request.user.id}"
                current = cache.get(cache_key, 0)
                
                if current >= limit:
                    return Response(
                        {"error": "Rate limit exceeded"},
                        status=status.HTTP_429_TOO_MANY_REQUESTS
                    )
                
                cache.set(cache_key, current + 1, period)
            return view_func(self, request, *args, **kwargs)
        return wrapped_view
    return decorator 