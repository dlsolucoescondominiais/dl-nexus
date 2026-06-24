import pytest
from unittest.mock import MagicMock, patch
from antigravity.agents.aninha import AninhaAgent, Porte

def test_calcular_porte():
    agent = AninhaAgent()
    assert agent.calcular_porte(None) == Porte.PEQUENO
    assert agent.calcular_porte(10) == Porte.PEQUENO
    assert agent.calcular_porte(30) == Porte.PEQUENO
    assert agent.calcular_porte(50) == Porte.MEDIO
    assert agent.calcular_porte(100) == Porte.MEDIO
    assert agent.calcular_porte(150) == Porte.GRANDE
    assert agent.calcular_porte(300) == Porte.GRANDE
    assert agent.calcular_porte(400) == Porte.COMPLEXO


def test_analisar_mensagem_ia_no_client():
    agent = AninhaAgent()
    agent.client = None
    result = agent.analisar_mensagem_ia("Olá")
    assert result == {
        "urgencia": "alta",
        "categoria_servico": "eletrica",
        "parecer": "Falha - OPENAI_API_KEY não configurada."
    }

def test_analisar_mensagem_ia_success():
    agent = AninhaAgent()
    agent.client = MagicMock()

    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = '{"urgencia": "baixa", "categoria_servico": "eletrica", "parecer": "parecer de teste"}'
    agent.client.chat.completions.create.return_value = mock_response

    result = agent.analisar_mensagem_ia("Mensagem de teste")
    assert result == {"urgencia": "baixa", "categoria_servico": "eletrica", "parecer": "parecer de teste"}

    agent.client.chat.completions.create.assert_called_once_with(
        model="gpt-4o",
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": agent.system_prompt},
            {"role": "user", "content": "Mensagem do lead B2B: Mensagem de teste"}
        ],
        temperature=0.2
    )

def test_analisar_mensagem_ia_invalid_payload():
    agent = AninhaAgent()
    agent.client = MagicMock()

    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = '{"urgencia": "super_alta", "categoria_servico": "venda_de_pecas", "parecer": "parecer invalido"}'
    agent.client.chat.completions.create.return_value = mock_response

    result = agent.analisar_mensagem_ia("Mensagem de teste invalido")
    assert result == {"urgencia": "media", "categoria_servico": "indefinida", "parecer": "parecer invalido"}

def test_analisar_mensagem_ia_exception():
    agent = AninhaAgent()
    agent.client = MagicMock()

    agent.client.chat.completions.create.side_effect = Exception("API fora do ar")

    result = agent.analisar_mensagem_ia("Mensagem que da erro")
    assert result == {
        "urgencia": "alta",
        "categoria_servico": "indefinida",
        "parecer": "Falha na IA: API fora do ar"
    }
