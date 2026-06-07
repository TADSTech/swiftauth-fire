import os
import pytest
from unittest.mock import MagicMock, patch
import firebase_admin
from swifttauth_fire.core import init_firebase, verify_id_token

@pytest.fixture(autouse=True)
def reset_firebase_apps():
    # Clear initialized firebase apps before/after each test
    firebase_admin._apps.clear()
    yield
    firebase_admin._apps.clear()

def test_init_firebase_raises_value_error_if_no_credentials():
    # Remove env var if present
    if "FIREBASE_SERVICE_ACCOUNT_PATH" in os.environ:
        del os.environ["FIREBASE_SERVICE_ACCOUNT_PATH"]
    
    with pytest.raises(ValueError) as excinfo:
        init_firebase()
    assert "Firebase credentials not found" in str(excinfo.value)

@patch("firebase_admin.credentials.Certificate")
@patch("firebase_admin.initialize_app")
def test_init_firebase_with_path(mock_initialize_app, mock_certificate):
    mock_cert = MagicMock()
    mock_certificate.return_value = mock_cert
    
    init_firebase("path/to/key.json")
    
    mock_certificate.assert_called_once_with("path/to/key.json")
    mock_initialize_app.assert_called_once_with(mock_cert)

@patch("firebase_admin.credentials.Certificate")
@patch("firebase_admin.initialize_app")
def test_init_firebase_with_env_var(mock_initialize_app, mock_certificate):
    os.environ["FIREBASE_SERVICE_ACCOUNT_PATH"] = "env/path/to/key.json"
    mock_cert = MagicMock()
    mock_certificate.return_value = mock_cert
    
    init_firebase()
    
    mock_certificate.assert_called_once_with("env/path/to/key.json")
    mock_initialize_app.assert_called_once_with(mock_cert)
    
    del os.environ["FIREBASE_SERVICE_ACCOUNT_PATH"]

@patch("swifttauth_fire.core.init_firebase")
@patch("firebase_admin.auth.verify_id_token")
def test_verify_id_token_success(mock_verify_id_token, mock_init_firebase):
    mock_verify_id_token.return_value = {"uid": "123", "email": "test@example.com"}
    
    result = verify_id_token("mock-token")
    
    mock_init_firebase.assert_called_once()
    mock_verify_id_token.assert_called_once_with("mock-token")
    assert result["uid"] == "123"

@patch("swifttauth_fire.core.init_firebase")
@patch("firebase_admin.auth.verify_id_token")
def test_verify_id_token_failure(mock_verify_id_token, mock_init_firebase):
    mock_verify_id_token.side_effect = Exception("Invalid token signature")
    
    with pytest.raises(ValueError) as excinfo:
        verify_id_token("invalid-token")
    
    assert "Invalid or expired token: Invalid token signature" in str(excinfo.value)
