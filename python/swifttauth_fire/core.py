import os
import firebase_admin
from firebase_admin import credentials, auth

def init_firebase(cred_path=None):
    """
    Initializes the Firebase Admin SDK.
    Uses FIREBASE_SERVICE_ACCOUNT_PATH env var if cred_path is not provided.
    """
    if len(firebase_admin._apps) > 0:
        return firebase_admin.get_app()

    path = cred_path or os.environ.get("FIREBASE_SERVICE_ACCOUNT_PATH")
    if not path:
        raise ValueError(
            "Firebase credentials not found. Set FIREBASE_SERVICE_ACCOUNT_PATH "
            "environment variable or pass cred_path to init_firebase()."
        )
    
    cred = credentials.Certificate(path)
    return firebase_admin.initialize_app(cred)

def verify_id_token(id_token: str):
    """
    Verifies a Firebase ID token.
    Returns the decoded token dictionary (user info) if valid, or raises an Exception.
    """
    # Ensure app is initialized
    init_firebase()
    
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except Exception as e:
        raise ValueError(f"Invalid or expired token: {e}")
