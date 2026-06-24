import unittest
from unittest.mock import patch, MagicMock
import json
from antigravity.agents.agente_jules_auditor import JulesAuditorAgent

class TestJulesAuditorAgent(unittest.TestCase):

    @patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'fake_key'})
    def setUp(self):
        self.agent = JulesAuditorAgent()

    def test_auditar_proposta_empty(self):
        """Testa o comportamento com proposta vazia"""
        result = self.agent.auditar_proposta("")
        self.assertEqual(result, {'erro': 'Proposta vazia'})

    def test_auditar_proposta_none(self):
        """Testa o comportamento com proposta None"""
        result = self.agent.auditar_proposta(None)
        self.assertEqual(result, {'erro': 'Proposta vazia'})

    @patch.dict('os.environ', {}, clear=True)
    def test_auditar_proposta_no_api_key(self):
        """Testa o comportamento quando não há chave de API"""
        agent = JulesAuditorAgent()
        result = agent.auditar_proposta("Proposta de teste")
        self.assertEqual(result["status_auditoria"], "REPROVADO")
        self.assertIn("A ANTHROPIC_API_KEY falhou", result["erros_encontrados"][0])
        self.assertEqual(result["proposta_corrigida"], "Proposta de teste")

    @patch('anthropic.Anthropic')
    def test_auditar_proposta_success(self, MockAnthropic):
        """Testa o cenário de sucesso com resposta mockada do Anthropic"""
        # Configurar o mock do cliente
        mock_client = MagicMock()
        self.agent.client = mock_client

        # Configurar a resposta mockada
        mock_response = MagicMock()
        mock_content = MagicMock()

        # Payload JSON que simula a resposta do Claude
        expected_payload = {
            "status_auditoria": "APROVADO",
            "erros_encontrados": [],
            "proposta_corrigida": "Proposta corrigida de teste",
            "observacoes_qa": "Tudo ok"
        }
        mock_content.text = json.dumps(expected_payload)
        mock_response.content = [mock_content]

        mock_client.messages.create.return_value = mock_response

        # Executar a função
        result = self.agent.auditar_proposta("Proposta bruta de teste")

        # Verificar se o método messages.create foi chamado corretamente
        mock_client.messages.create.assert_called_once()
        call_args = mock_client.messages.create.call_args[1]
        self.assertEqual(call_args['model'], "claude-3-5-sonnet-20240620")

        # Verificar o resultado
        self.assertEqual(result, expected_payload)

    @patch('anthropic.Anthropic')
    def test_auditar_proposta_api_exception(self, MockAnthropic):
        """Testa o cenário onde a API do Anthropic lança uma exceção"""
        mock_client = MagicMock()
        self.agent.client = mock_client

        # Configurar o mock para lançar exceção
        mock_client.messages.create.side_effect = Exception("API Error")

        result = self.agent.auditar_proposta("Proposta bruta de teste")

        self.assertEqual(result["status_auditoria"], "REPROVADO")
        self.assertTrue(any("Erro crítico do Motor Claude: API Error" in erro for erro in result["erros_encontrados"]))
        self.assertEqual(result["proposta_corrigida"], "Proposta bruta de teste")

if __name__ == '__main__':
    unittest.main()
