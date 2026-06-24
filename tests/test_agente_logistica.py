import unittest
from unittest.mock import patch, MagicMock
from antigravity.agents.agente_logistica import AgenteCartografo

class TestAgenteCartografo(unittest.TestCase):

    @patch('antigravity.agents.agente_logistica.os.getenv')
    def test_calcular_viabilidade_missing_api_key(self, mock_getenv):
        mock_getenv.return_value = None
        agente = AgenteCartografo()

        result = agente.calcular_viabilidade("Rua Ficticia, 123")

        self.assertEqual(result["status"], "erro")
        self.assertEqual(result["msg"], "API_KEY do Google Ausente ou Inválida.")
        self.assertEqual(result["distancia_km"], 0)

    @patch('antigravity.agents.agente_logistica.os.getenv')
    @patch('antigravity.agents.agente_logistica.requests.get')
    def test_calcular_viabilidade_success_verde(self, mock_get, mock_getenv):
        mock_getenv.return_value = "TEST_API_KEY"
        agente = AgenteCartografo()

        mock_response = MagicMock()
        mock_response.json.return_value = {
            "status": "OK",
            "rows": [{
                "elements": [{
                    "status": "OK",
                    "distance": {"value": 15000}, # 15.0 km
                    "duration": {"text": "30 mins"}
                }]
            }]
        }
        mock_get.return_value = mock_response

        result = agente.calcular_viabilidade("Rua Ficticia, 123")

        self.assertEqual(result["status"], "sucesso")
        self.assertEqual(result["farol_viabilidade"], "VERDE")
        self.assertEqual(result["distancia_km"], 15.0)
        self.assertEqual(result["custo_sugerido_viagem"], 0.0)

    @patch('antigravity.agents.agente_logistica.os.getenv')
    @patch('antigravity.agents.agente_logistica.requests.get')
    def test_calcular_viabilidade_success_amarelo(self, mock_get, mock_getenv):
        mock_getenv.return_value = "TEST_API_KEY"
        agente = AgenteCartografo()

        mock_response = MagicMock()
        mock_response.json.return_value = {
            "status": "OK",
            "rows": [{
                "elements": [{
                    "status": "OK",
                    "distance": {"value": 45000}, # 45.0 km
                    "duration": {"text": "1 hora 10 mins"}
                }]
            }]
        }
        mock_get.return_value = mock_response

        result = agente.calcular_viabilidade("Rua Longe, 456")

        self.assertEqual(result["status"], "sucesso")
        self.assertEqual(result["farol_viabilidade"], "AMARELO")
        self.assertEqual(result["distancia_km"], 45.0)
        self.assertEqual(result["custo_sugerido_viagem"], 180.0)

    @patch('antigravity.agents.agente_logistica.os.getenv')
    @patch('antigravity.agents.agente_logistica.requests.get')
    def test_calcular_viabilidade_success_vermelho(self, mock_get, mock_getenv):
        mock_getenv.return_value = "TEST_API_KEY"
        agente = AgenteCartografo()

        mock_response = MagicMock()
        mock_response.json.return_value = {
            "status": "OK",
            "rows": [{
                "elements": [{
                    "status": "OK",
                    "distance": {"value": 80000}, # 80.0 km
                    "duration": {"text": "2 horas"}
                }]
            }]
        }
        mock_get.return_value = mock_response

        result = agente.calcular_viabilidade("Rua Muito Longe, 789")

        self.assertEqual(result["status"], "sucesso")
        self.assertEqual(result["farol_viabilidade"], "VERMELHO (FORA_DE_RAIO)")
        self.assertEqual(result["distancia_km"], 80.0)
        self.assertEqual(result["custo_sugerido_viagem"], 350.0)

    @patch('antigravity.agents.agente_logistica.os.getenv')
    @patch('antigravity.agents.agente_logistica.requests.get')
    def test_calcular_viabilidade_element_error(self, mock_get, mock_getenv):
        mock_getenv.return_value = "TEST_API_KEY"
        agente = AgenteCartografo()

        mock_response = MagicMock()
        mock_response.json.return_value = {
            "status": "OK",
            "rows": [{
                "elements": [{
                    "status": "ZERO_RESULTS"
                }]
            }]
        }
        mock_get.return_value = mock_response

        result = agente.calcular_viabilidade("Endereço Inexistente")

        self.assertEqual(result["status"], "erro")
        self.assertEqual(result["msg"], "CEP / Endereço não mapeável.")
        self.assertEqual(result["distancia_km"], 0)

    @patch('antigravity.agents.agente_logistica.os.getenv')
    @patch('antigravity.agents.agente_logistica.requests.get')
    def test_calcular_viabilidade_top_level_error(self, mock_get, mock_getenv):
        mock_getenv.return_value = "TEST_API_KEY"
        agente = AgenteCartografo()

        mock_response = MagicMock()
        mock_response.json.return_value = {
            "status": "REQUEST_DENIED",
            "error_message": "Key is invalid"
        }
        mock_get.return_value = mock_response

        result = agente.calcular_viabilidade("Rua Ficticia, 123")

        self.assertEqual(result["status"], "erro")
        self.assertEqual(result["msg"], "Google Api Error: Key is invalid")
        self.assertEqual(result["distancia_km"], 0)

    @patch('antigravity.agents.agente_logistica.os.getenv')
    @patch('antigravity.agents.agente_logistica.requests.get')
    def test_calcular_viabilidade_http_exception(self, mock_get, mock_getenv):
        mock_getenv.return_value = "TEST_API_KEY"
        agente = AgenteCartografo()

        mock_get.side_effect = Exception("Connection Timeout")

        result = agente.calcular_viabilidade("Rua Ficticia, 123")

        self.assertEqual(result["status"], "erro")
        self.assertEqual(result["msg"], "HTTP Falha: Connection Timeout")
        self.assertEqual(result["distancia_km"], 0)

if __name__ == '__main__':
    unittest.main()
