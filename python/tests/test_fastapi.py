import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from swifttauth_fire.fastapi import get_current_user

@patch("swifttauth_fire.fastapi.verify_id_token")
def test_get_current_user_success(mock_verify):
    mock_user = {"uid": "fastapi-123", "email": "fastapi@example.com"}
    mock_verify.return_value = mock_user
    
    credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials="valid-token")
    result = get_current_user(credentials)
    
    assert result == mock_user
    mock_verify.assert_called_once_with("valid-token")

@patch("swifttauth_fire.fastapi.verify_id_token")
def test_get_current_user_failure(mock_verify):
    mock_verify.side_effect = ValueError("Invalid signature")
    
    credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials="bad-token")
    
    with pytest.raises(HTTPException) as excinfo:
        get_current_user(credentials)
        
    assert excinfo.value.status_code == 401
    assert "Invalid authentication credentials: Invalid signature" in excinfo.value.detail
    assert excinfo.value.headers == {"WWW-Authenticate": "Bearer"}
