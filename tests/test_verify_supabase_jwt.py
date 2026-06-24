import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
import jwt
import time
from antigravity.main import verify_supabase_jwt
import antigravity.main as main_module

SECRET = "test_secret_key_123_very_long_secure_string"

@pytest.fixture
def mock_request():
    request = MagicMock()
    request.headers.get.return_value = None
    return request

@pytest.mark.asyncio
async def test_verify_supabase_jwt_missing_secret(monkeypatch, mock_request):
    monkeypatch.setattr(main_module, "SUPABASE_JWT_SECRET", None)
    with pytest.raises(HTTPException) as excinfo:
        await verify_supabase_jwt(mock_request)
    assert excinfo.value.status_code == 500
    assert "Configuração de segurança crítica" in excinfo.value.detail

@pytest.mark.asyncio
async def test_verify_supabase_jwt_missing_header(monkeypatch, mock_request):
    monkeypatch.setattr(main_module, "SUPABASE_JWT_SECRET", SECRET)
    mock_request.headers.get.return_value = None
    with pytest.raises(HTTPException) as excinfo:
        await verify_supabase_jwt(mock_request)
    assert excinfo.value.status_code == 401
    assert "ausente" in excinfo.value.detail

@pytest.mark.asyncio
async def test_verify_supabase_jwt_invalid_header_format(monkeypatch, mock_request):
    monkeypatch.setattr(main_module, "SUPABASE_JWT_SECRET", SECRET)
    mock_request.headers.get.return_value = "TokenWithoutBearer123"
    with pytest.raises(HTTPException) as excinfo:
        await verify_supabase_jwt(mock_request)
    assert excinfo.value.status_code == 401
    assert "formato inválido" in excinfo.value.detail

@pytest.mark.asyncio
async def test_verify_supabase_jwt_expired_token(monkeypatch, mock_request):
    monkeypatch.setattr(main_module, "SUPABASE_JWT_SECRET", SECRET)
    payload = {"sub": "user123", "exp": time.time() - 1000}
    token = jwt.encode(payload, SECRET, algorithm="HS256")
    mock_request.headers.get.return_value = f"Bearer {token}"
    with pytest.raises(HTTPException) as excinfo:
        await verify_supabase_jwt(mock_request)
    assert excinfo.value.status_code == 401
    assert "expirado" in excinfo.value.detail

@pytest.mark.asyncio
async def test_verify_supabase_jwt_invalid_token(monkeypatch, mock_request):
    monkeypatch.setattr(main_module, "SUPABASE_JWT_SECRET", SECRET)
    mock_request.headers.get.return_value = "Bearer invalid.token.here"
    with pytest.raises(HTTPException) as excinfo:
        await verify_supabase_jwt(mock_request)
    assert excinfo.value.status_code == 403
    assert "inválido" in excinfo.value.detail

@pytest.mark.asyncio
async def test_verify_supabase_jwt_valid_token(monkeypatch, mock_request):
    monkeypatch.setattr(main_module, "SUPABASE_JWT_SECRET", SECRET)
    payload = {"sub": "user123", "exp": time.time() + 1000}
    token = jwt.encode(payload, SECRET, algorithm="HS256")
    mock_request.headers.get.return_value = f"Bearer {token}"

    result = await verify_supabase_jwt(mock_request)
    assert result["sub"] == "user123"
