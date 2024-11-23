import logging
import time
from django.utils import timezone

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        
        response = self.get_response(request)
        
        duration = time.time() - start_time
        
        log_data = {
            'timestamp': timezone.now().isoformat(),
            'method': request.method,
            'path': request.path,
            'status': response.status_code,
            'duration': duration,
            'user': request.user.username if request.user.is_authenticated else 'anonymous'
        }
        
        logger.info(f"Request: {log_data}")
        
        return response 