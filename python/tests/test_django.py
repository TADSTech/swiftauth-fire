import pytest
from unittest.mock import MagicMock, patch
from django.conf import settings

if not settings.configured:
    settings.configure()

from swifttauth_fire.django import swiftt_auth_required

# Mock django objects for testing without a full django project setup
class MockRequest:
    def __init__(self, auth_header=None):
        self.META = {}
        if auth_header:
            self.META['HTTP_AUTHORIZATION'] = auth_header
        self.firebase_user = None

def test_django_decorator_missing_auth_header():
    request = MockRequest()
    
    @swiftt_auth_required
    def dummy_view(req):
        return "success"
        
    response = dummy_view(request)
    # response should be a JsonResponse with 401
    assert response.status_code == 401
    assert b"Missing or invalid Authorization header" in response.content

def test_django_decorator_invalid_header_format():
    request = MockRequest("NotBearer token123")
    
    @swiftt_auth_required
    def dummy_view(req):
        return "success"
        
    response = dummy_view(request)
    assert response.status_code == 401
    assert b"Missing or invalid Authorization header" in response.content

@patch("swifttauth_fire.django.verify_id_token")
def test_django_decorator_success(mock_verify):
    mock_user = {"uid": "user_django", "name": "Django User"}
    mock_verify.return_value = mock_user
    request = MockRequest("Bearer valid-django-token")
    
    @swiftt_auth_required
    def dummy_view(req):
        return "view_called"
        
    response = dummy_view(request)
    assert response == "view_called"
    assert request.firebase_user == mock_user
    mock_verify.assert_called_once_with("valid-django-token")

@patch("swifttauth_fire.django.verify_id_token")
def test_django_decorator_verification_failure(mock_verify):
    mock_verify.side_effect = ValueError("Token expired")
    request = MockRequest("Bearer expired-token")
    
    @swiftt_auth_required
    def dummy_view(req):
        return "success"
        
    response = dummy_view(request)
    assert response.status_code == 401
    assert b"Token expired" in response.content
