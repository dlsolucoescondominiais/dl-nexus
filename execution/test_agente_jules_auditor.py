import os
import json
import pytest
from unittest.mock import MagicMock, patch
from antigravity.agents.agente_jules_auditor import JulesAuditorAgent

def test_auditar_proposta_no_api_key():
    with patch.dict(os.environ, clear=True):
        agent = JulesAuditorAgent()
        result = agent.auditar_proposta("proposta")
        assert result["status_auditoria"] == "REPROVADO"
        assert result["erros_encontrados"] == ["A ANTHROPIC_API_KEY falhou ou não existe no ambiente."]
        assert result["observacoes_qa"] == "Falha no motor do Diretor (Sem chave API)."

@patch("antigravity.agents.agente_jules_auditor.anthropic.Anthropic")
def test_auditar_proposta_success(mock_anthropic):
    mock_client = MagicMock()
    mock_anthropic.return_value = mock_client

    mock_content_block = MagicMock()
    mock_content_block.text = json.dumps({
        "status_auditoria": "APROVADO",
        "erros_encontrados": [],
        "proposta_corrigida": "proposta limpa",
        "observacoes_qa": "Parecer"
    })

    mock_response = MagicMock()
    mock_response.content = [mock_content_block]
    mock_client.messages.create.return_value = mock_response

    with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "fake_key"}):
        agent = JulesAuditorAgent()
        result = agent.auditar_proposta("proposta bruta")

        assert result["status_auditoria"] == "APROVADO"
        assert result["proposta_corrigida"] == "proposta limpa"
        mock_client.messages.create.assert_called_once()

@patch("antigravity.agents.agente_jules_auditor.anthropic.Anthropic")
def test_auditar_proposta_api_error(mock_anthropic):
    mock_client = MagicMock()
    mock_anthropic.return_value = mock_client
    mock_client.messages.create.side_effect = Exception("Timeout API")

    with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "fake_key"}):
        agent = JulesAuditorAgent()
        result = agent.auditar_proposta("proposta bruta")

        assert result["status_auditoria"] == "REPROVADO"
        assert result["erros_encontrados"] == ["Erro crítico do Motor Claude: Timeout API"]

@patch("antigravity.agents.agente_jules_auditor.anthropic.Anthropic")
def test_auditar_proposta_invalid_json(mock_anthropic):
    mock_client = MagicMock()
    mock_anthropic.return_value = mock_client

    mock_content_block = MagicMock()
    mock_content_block.text = "Isto não é um JSON válido"
    mock_response = MagicMock()
    mock_response.content = [mock_content_block]
    mock_client.messages.create.return_value = mock_response

    with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "fake_key"}):
        agent = JulesAuditorAgent()
        result = agent.auditar_proposta("proposta bruta")

        assert result["status_auditoria"] == "REPROVADO"
        assert "Erro crítico do Motor Claude: Expecting value" in result["erros_encontrados"][0]
