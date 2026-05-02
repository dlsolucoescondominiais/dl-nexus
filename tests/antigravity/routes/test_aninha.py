import sys
import unittest
from unittest.mock import patch, MagicMock

# First import main so the module exists
import antigravity.main

# Create a dummy dependency for FastAPI security token verification
from fastapi import Request
async def mock_verify_supabase_jwt(request: Request):
    return {"user": "test_user"}

from fastapi.testclient import TestClient
from antigravity.main import app
from antigravity.routes import aninha

class TestAninhaRoute(unittest.TestCase):
    def setUp(self):
        # Apply the override to the FastAPI dependency injection system
        from antigravity.main import verify_supabase_jwt
        app.dependency_overrides[verify_supabase_jwt] = mock_verify_supabase_jwt
        self.client = TestClient(app)

    def tearDown(self):
        self.client = None
        # Clean up dependency overrides
        app.dependency_overrides = {}

    @patch('antigravity.routes.aninha.aninha')
    @patch('antigravity.routes.aninha.uuid.uuid4')
    @patch('antigravity.routes.aninha.BackgroundTasks.add_task')
    def test_triagem_lead_success(self, mock_add_task, mock_uuid, mock_aninha):
        mock_uuid.return_value = "1234-5678"
        mock_aninha.fazer_triagem.return_value = {"status": "triado", "info": "ok"}

        payload = {
            "nome_condominio": "Condominio Alpha",
            "telefone": "21999999999",
            "email": "alpha@example.com",
            "mensagem_original": "Bomba quebrada",
            "tipo_imovel": "residencial",
            "num_unidades": 50,
            "origem": "whatsapp",
            "prioridade_inferida": "alta"
        }

        response = self.client.post("/api/aninha/triagem", json=payload)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "triado", "info": "ok"})

        expected_lead_data = {
            "lead_id": "1234-5678",
            "nome_condominio": "Condominio Alpha",
            "telefone": "21999999999",
            "email": "alpha@example.com",
            "mensagem_original": "Bomba quebrada",
            "tipo_imovel": "residencial",
            "num_unidades": 50,
            "origem": "whatsapp",
            "prioridade": "alta", # The payload field is prioridade_inferida, but mapped to prioridade
        }
        mock_aninha.fazer_triagem.assert_called_once_with(expected_lead_data)

        # TestClient actually executes BackgroundTasks synchronously.
        # Check if the function logic registered it.
        from antigravity.routes.aninha import disparar_webhook_n8n_background
        mock_add_task.assert_called_once_with(disparar_webhook_n8n_background, {"status": "triado", "info": "ok"})

    @patch('antigravity.routes.aninha.aninha')
    @patch('antigravity.routes.aninha.BackgroundTasks.add_task')
    def test_triagem_lead_exception(self, mock_add_task, mock_aninha):
        mock_aninha.fazer_triagem.side_effect = Exception("Erro interno do agente")

        payload = {
            "nome_condominio": "Condominio Beta",
            "telefone": "21888888888",
            "email": "beta@example.com",
            "mensagem_original": "Manutencao",
            "origem": "site",
            "prioridade_inferida": "baixa"
        }

        response = self.client.post("/api/aninha/triagem", json=payload)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {"detail": "Erro interno do agente"})

        # When an exception occurs, the background task is not added/executed
        mock_add_task.assert_not_called()

    @patch('antigravity.routes.aninha.requests.post')
    def test_disparar_webhook_success(self, mock_post):
        mock_post.return_value.status_code = 200
        from antigravity.routes.aninha import disparar_webhook_n8n_background
        resultado_triagem = {"status": "sucesso"}

        disparar_webhook_n8n_background(resultado_triagem)

        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        self.assertEqual(kwargs['json'], resultado_triagem)
        self.assertIn('X-DL-API-KEY', kwargs['headers'])

    @patch('antigravity.routes.aninha.requests.post')
    def test_disparar_webhook_failure_swallowed(self, mock_post):
        mock_post.side_effect = Exception("Connection Timeout")
        from antigravity.routes.aninha import disparar_webhook_n8n_background
        resultado_triagem = {"status": "sucesso"}

        try:
            disparar_webhook_n8n_background(resultado_triagem)
        except Exception:
            self.fail("disparar_webhook_n8n_background raised an exception unexpectedly!")

        mock_post.assert_called_once()

if __name__ == '__main__':
    unittest.main()
