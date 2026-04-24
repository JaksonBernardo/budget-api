import pytest
from datetime import timedelta
from api.security.jwt import create_access_token, decode_access_token

def test_create_and_decode_access_token():
    user_id = 1
    company_id = 1
    token = create_access_token(user_id, company_id)
    assert isinstance(token, str)
    
    decoded_id = decode_access_token(token)
    assert decoded_id == user_id

def test_decode_invalid_token():
    assert decode_access_token("invalid-token") is None

def test_decode_wrong_type_token():
    import jwt
    from api.core.settings import Settings
    settings = Settings()
    payload = {"sub": "1", "type": "wrong", "exp": 9999999999}
    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    assert decode_access_token(token) is None
