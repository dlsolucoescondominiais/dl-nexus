import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from antigravity.main import app, verify_supabase_jwt

# Mock para pular autenticação JWT do Supabase nos testes
app.dependency_overrides[verify_supabase_jwt] = lambda: {"sub": "test"}
client = TestClient(app)

def test_aprovar_post_error_path():
    with patch("antigravity.routes.marketing.requests.post") as mock_post:
        # Configurar o mock para levantar uma exceção
        mock_post.side_effect = Exception("Erro simulado do n8n")

        # Fazer a requisição
        resp = client.post(
            "/api/marketing/aprovar",
            json={"post_id": "123", "copy_aprovada": "test", "imagem_url": "url"}
        )

        # Verificar se o código de status é 500
        assert resp.status_code == 500
        # Verificar o detalhe do erro
        assert "Erro simulado do n8n" in resp.json()["detail"]

def test_aprovar_post_error_status_code():
    with patch("antigravity.routes.marketing.requests.post") as mock_post:
        # Configurar o mock para retornar um status de erro
        class MockResponse:
            status_code = 400
            text = "Bad Request"
        mock_post.return_value = MockResponse()

        # Fazer a requisição
        resp = client.post(
            "/api/marketing/aprovar",
            json={"post_id": "123", "copy_aprovada": "test", "imagem_url": "url"}
        )

        # Verificar se o código de status é 500 (pois a exceção é levantada e capturada pelo except genérico que retorna 500)
        assert resp.status_code == 500
        assert "Orquestrador n8n retornou erro: Bad Request" in resp.json()["detail"]

def test_geracao_ideia_error_path():
    with patch("antigravity.routes.marketing.openai.OpenAI") as mock_openai:
        # Configurar o mock para levantar uma exceção
        mock_openai.side_effect = Exception("OpenAI Error Simulado")

        # Fazer a requisição
        resp = client.post(
            "/api/marketing/geracao_ideia",
            json={"tema": "Segurança condominial"}
        )

        # Verificar se o código de status é 500
        assert resp.status_code == 500
        # Verificar o detalhe do erro
        assert "OpenAI Error Simulado" in resp.json()["detail"]
