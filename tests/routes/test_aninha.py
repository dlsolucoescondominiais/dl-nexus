import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
import os

# Mock dependencies before importing the app
os.environ["SUPABASE_JWT_SECRET"] = "dummy_secret_for_tests"

from antigravity.main import app
from antigravity.main import verify_supabase_jwt

app.dependency_overrides[verify_supabase_jwt] = lambda: {"sub": "user_123", "role": "authenticated"}

client = TestClient(app)

def test_receber_mensagem_error_path():
    """
    Test the error path for the receiving message endpoint, where an exception
    is thrown by the internal aninha agent and should correctly bubble up as HTTP 500.
    """
    with patch('antigravity.routes.aninha.aninha.analisar_mensagem_ia') as mock_analisar:
        mock_analisar.side_effect = Exception("Simulated fatal internal error in IA parsing")

        # Testing the endpoint that receives a raw message query parameter
        response = client.post("/api/aninha/receber_mensagem?mensagem=Ajuda_por_favor", headers={"Authorization": "Bearer fake_token"})

        assert response.status_code == 500
        assert "Erro na Aninha: Simulated fatal internal error in IA parsing" in response.json()["detail"]
