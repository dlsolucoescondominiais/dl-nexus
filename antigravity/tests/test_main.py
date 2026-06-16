import pytest
from unittest.mock import Mock, patch
from fastapi import Request, HTTPException
import jwt
from antigravity.main import verify_supabase_jwt
import antigravity.main

@pytest.mark.asyncio
async def test_missing_secret():
    with patch.object(antigravity.main, 'SUPABASE_JWT_SECRET', None):
        request = Mock(spec=Request)
        with pytest.raises(HTTPException) as excinfo:
            await verify_supabase_jwt(request)
        assert excinfo.value.status_code == 500
        assert "ausente no servidor" in excinfo.value.detail

@pytest.mark.asyncio
async def test_missing_auth_header():
    with patch.object(antigravity.main, 'SUPABASE_JWT_SECRET', 'secret'):
        request = Mock(spec=Request)
        request.headers = {}
        with pytest.raises(HTTPException) as excinfo:
            await verify_supabase_jwt(request)
        assert excinfo.value.status_code == 401
        assert "ausente ou formato inválido" in excinfo.value.detail

@pytest.mark.asyncio
async def test_invalid_auth_header_format():
    with patch.object(antigravity.main, 'SUPABASE_JWT_SECRET', 'secret'):
        request = Mock(spec=Request)
        request.headers = {"Authorization": "Basic token"}
        with pytest.raises(HTTPException) as excinfo:
            await verify_supabase_jwt(request)
        assert excinfo.value.status_code == 401

@pytest.mark.asyncio
async def test_expired_token():
    with patch.object(antigravity.main, 'SUPABASE_JWT_SECRET', 'secret'):
        request = Mock(spec=Request)
        request.headers = {"Authorization": "Bearer some_expired_token"}

        with patch('jwt.decode', side_effect=jwt.ExpiredSignatureError):
            with pytest.raises(HTTPException) as excinfo:
                await verify_supabase_jwt(request)
            assert excinfo.value.status_code == 401

@pytest.mark.asyncio
async def test_invalid_token():
    with patch.object(antigravity.main, 'SUPABASE_JWT_SECRET', 'secret'):
        request = Mock(spec=Request)
        request.headers = {"Authorization": "Bearer some_invalid_token"}

        with patch('jwt.decode', side_effect=jwt.InvalidTokenError):
            with pytest.raises(HTTPException) as excinfo:
                await verify_supabase_jwt(request)
            assert excinfo.value.status_code == 403

@pytest.mark.asyncio
async def test_valid_token():
    with patch.object(antigravity.main, 'SUPABASE_JWT_SECRET', 'secret'):
        request = Mock(spec=Request)
        request.headers = {"Authorization": "Bearer valid_token"}
        expected_payload = {"sub": "user_id"}

        with patch('jwt.decode', return_value=expected_payload):
            payload = await verify_supabase_jwt(request)
            assert payload == expected_payload
