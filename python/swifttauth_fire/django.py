from functools import wraps
from django.http import JsonResponse
from .core import verify_id_token

def swiftt_auth_required(view_func):
    """
    Django decorator to protect views with Firebase Auth.
    Extracts Bearer token from the Authorization header.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return JsonResponse({'error': 'Unauthorized: Missing or invalid Authorization header'}, status=401)
        
        token = auth_header.split(' ')[1]
        try:
            decoded_token = verify_id_token(token)
            request.firebase_user = decoded_token  # Attach user data to request
        except Exception as e:
            return JsonResponse({'error': f'Unauthorized: {str(e)}'}, status=401)
            
        return view_func(request, *args, **kwargs)
        
    return _wrapped_view
