import pytest
from unittest.mock import MagicMock, patch
from antigravity.agents.agente_especialistas import AgenteEspecialista

def test_gerar_draft_proposta_sem_client():
    # Testa quando o client do OpenAI não é inicializado (ex: sem API key)
    with patch('os.getenv', return_value=None):
        agente = AgenteEspecialista()
        resultado = agente.gerar_draft_proposta("dor genérica", "eletrica", "alta")
        assert "Erro: OPENAI_API_KEY ausente ou inválida" in resultado

@patch('antigravity.agents.agente_especialistas.OpenAI')
def test_gerar_draft_proposta_sucesso(mock_openai_class):
    # Configura o mock para retornar um client com o método chat.completions.create
    mock_client = MagicMock()
    mock_openai_class.return_value = mock_client

    # Configura a resposta mockada do OpenAI
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "  Proposta mockada com sucesso.  "
    mock_client.chat.completions.create.return_value = mock_response

    # Instancia o agente e executa
    with patch('os.getenv', return_value='fake_key'):
        agente = AgenteEspecialista()

    resultado = agente.gerar_draft_proposta("Problema no painel", "eletrica", "urgente")

    # Verifica o resultado
    assert resultado == "Proposta mockada com sucesso."
    mock_client.chat.completions.create.assert_called_once()

    # Verifica que as mensagens continham algo relevante
    args, kwargs = mock_client.chat.completions.create.call_args
    assert "messages" in kwargs
    messages = kwargs["messages"]
    assert len(messages) == 2
    assert "role" in messages[0] and messages[0]["role"] == "system"
    assert "role" in messages[1] and messages[1]["role"] == "user"

@patch('antigravity.agents.agente_especialistas.OpenAI')
def test_gerar_draft_proposta_excecao(mock_openai_class):
    # Configura o mock para disparar uma exceção ao criar o completion
    mock_client = MagicMock()
    mock_openai_class.return_value = mock_client
    mock_client.chat.completions.create.side_effect = Exception("Erro simulado API")

    with patch('os.getenv', return_value='fake_key'):
        agente = AgenteEspecialista()

    resultado = agente.gerar_draft_proposta("Problema complexo", "automacao", "baixa")

    assert "[Erro Catastrófico no Agente Especialista]: Falha ao conectar ao cérebro OpenAi. Erro simulado API" in resultado
