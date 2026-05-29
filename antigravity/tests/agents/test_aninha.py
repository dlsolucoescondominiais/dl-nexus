import sys
from unittest.mock import MagicMock

# Mock openai module before importing the agent
sys.modules['openai'] = MagicMock()

import unittest
from unittest.mock import patch
from antigravity.agents.aninha import AninhaAgent, Porte

class TestAninhaAgent(unittest.TestCase):
    def setUp(self):
        self.agent = AninhaAgent()

    @patch('antigravity.agents.aninha.AninhaAgent.calcular_porte')
    @patch('antigravity.agents.aninha.AninhaAgent.analisar_mensagem_ia')
    def test_fazer_triagem(self, mock_analisar_mensagem_ia, mock_calcular_porte):
        # Configurar o mock
        mock_analisar_mensagem_ia.return_value = {
            "urgencia": "alta",
            "categoria_servico": "eletrica",
            "parecer": "Lead qualificado para DL Praxis Elétrica e DL VoltCharge."
        }
        mock_calcular_porte.return_value = Porte.GRANDE

        # Dados de entrada simulados - O código usa `lead_data.get("mensagem", "")`
        lead_data = {
            "mensagem": "Preciso de um orçamento para a parte elétrica do meu condomínio, os carros elétricos estão derrubando a energia.",
            "num_unidades": 150,
            "lead_id": "12345",
            "nome_condominio": "Condomínio Teste",
            "telefone": "21999999999",
            "email": "teste@exemplo.com",
            "origem": "whatsapp"
        }

        # Executar a função
        resultado = self.agent.fazer_triagem(lead_data)

        # Asserts
        mock_analisar_mensagem_ia.assert_called_once_with(lead_data["mensagem"])
        mock_calcular_porte.assert_called_once_with(150)
        self.assertEqual(resultado["status"], "triado")
        self.assertEqual(resultado["motivo"], "Lead qualificado para DL Praxis Elétrica e DL VoltCharge.")
        self.assertEqual(resultado["lead_id"], "12345")
        self.assertEqual(resultado["urgencia"], "alta")
        self.assertEqual(resultado["categoria_servico"], "eletrica")
        self.assertEqual(resultado["porte"], Porte.GRANDE.value)
        self.assertEqual(resultado["proxima_acao_obrigatoria"], "Agendar Avaliação Técnica")
        self.assertEqual(resultado["nome_condominio"], "Condomínio Teste")
        self.assertEqual(resultado["telefone"], "21999999999")
        self.assertEqual(resultado["email"], "teste@exemplo.com")
        self.assertEqual(resultado["origem"], "whatsapp")
        self.assertIn("timestamp", resultado)

    @patch('antigravity.agents.aninha.AninhaAgent.calcular_porte')
    @patch('antigravity.agents.aninha.AninhaAgent.analisar_mensagem_ia')
    def test_fazer_triagem_missing_units(self, mock_analisar_mensagem_ia, mock_calcular_porte):
        mock_analisar_mensagem_ia.return_value = {
            "urgencia": "baixa",
            "categoria_servico": "seguranca",
            "parecer": "Porteiro precisa de câmera."
        }
        mock_calcular_porte.return_value = Porte.PEQUENO

        # Test without num_unidades and without mensagem
        lead_data = {
            "lead_id": "999"
        }

        resultado = self.agent.fazer_triagem(lead_data)

        mock_analisar_mensagem_ia.assert_called_once_with("")
        mock_calcular_porte.assert_called_once_with(None)

        self.assertEqual(resultado["porte"], Porte.PEQUENO.value)
        self.assertEqual(resultado["motivo"], "Porteiro precisa de câmera.")
        self.assertEqual(resultado["categoria_servico"], "seguranca")
        self.assertEqual(resultado["urgencia"], "baixa")
