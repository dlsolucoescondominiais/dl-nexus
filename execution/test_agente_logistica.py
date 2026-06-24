import pytest
from antigravity.agents.agente_logistica import AgenteCartografo

@pytest.fixture
def agente(mocker):
    mocker.patch('os.getenv', return_value="CHAVE_VALIDA")
    return AgenteCartografo()

def test_calcular_viabilidade_endereco_vazio_early_return(agente):
    resultado = agente.calcular_viabilidade("")
    assert resultado.get("erro") == "Endereço não fornecido"

    resultado_none = agente.calcular_viabilidade(None)
    assert resultado_none.get("erro") == "Endereço não fornecido"

def test_calcular_viabilidade_sem_api_key(mocker):
    mocker.patch('os.getenv', return_value=None)
    agente = AgenteCartografo()
    resultado = agente.calcular_viabilidade("Rua Teste, 123")

    assert resultado["status"] == "erro"
    assert "API_KEY do Google Ausente ou Inválida" in resultado["msg"]

def test_calcular_viabilidade_sucesso_verde(agente, mocker):
    mock_response = mocker.MagicMock()
    mock_response.json.return_value = {
        "status": "OK",
        "rows": [{"elements": [{"status": "OK", "distance": {"value": 15000}, "duration": {"text": "20 mins"}}]}]
    }
    mocker.patch('requests.get', return_value=mock_response)

    resultado = agente.calcular_viabilidade("Endereço Próximo")

    assert resultado["status"] == "sucesso"
    assert resultado["farol_viabilidade"] == "VERDE"
    assert resultado["distancia_km"] == 15.0
    assert resultado["custo_sugerido_viagem"] == 0.0

def test_calcular_viabilidade_sucesso_amarelo(agente, mocker):
    mock_response = mocker.MagicMock()
    mock_response.json.return_value = {
        "status": "OK",
        "rows": [{"elements": [{"status": "OK", "distance": {"value": 45000}, "duration": {"text": "50 mins"}}]}]
    }
    mocker.patch('requests.get', return_value=mock_response)

    resultado = agente.calcular_viabilidade("Endereço Médio")

    assert resultado["status"] == "sucesso"
    assert resultado["farol_viabilidade"] == "AMARELO"
    assert resultado["distancia_km"] == 45.0
    assert resultado["custo_sugerido_viagem"] == 180.0

def test_calcular_viabilidade_sucesso_vermelho(agente, mocker):
    mock_response = mocker.MagicMock()
    mock_response.json.return_value = {
        "status": "OK",
        "rows": [{"elements": [{"status": "OK", "distance": {"value": 80000}, "duration": {"text": "1 hora 30 mins"}}]}]
    }
    mocker.patch('requests.get', return_value=mock_response)

    resultado = agente.calcular_viabilidade("Endereço Longe")

    assert resultado["status"] == "sucesso"
    assert resultado["farol_viabilidade"] == "VERMELHO (FORA_DE_RAIO)"
    assert resultado["distancia_km"] == 80.0
    assert resultado["custo_sugerido_viagem"] == 350.0

def test_calcular_viabilidade_falha_na_api_google(agente, mocker):
    mock_response = mocker.MagicMock()
    mock_response.json.return_value = {
        "status": "REQUEST_DENIED",
        "error_message": "Chave inválida, por exemplo"
    }
    mocker.patch('requests.get', return_value=mock_response)

    resultado = agente.calcular_viabilidade("Qualquer Endereço")

    assert resultado["status"] == "erro"
    assert "Google Api Error" in resultado["msg"]

def test_calcular_viabilidade_endereco_nao_mapeavel(agente, mocker):
    mock_response = mocker.MagicMock()
    mock_response.json.return_value = {
        "status": "OK",
        "rows": [{"elements": [{"status": "ZERO_RESULTS"}]}]
    }
    mocker.patch('requests.get', return_value=mock_response)

    resultado = agente.calcular_viabilidade("Endereço Que Não Existe")

    assert resultado["status"] == "erro"
    assert "CEP / Endereço não mapeável" in resultado["msg"]

def test_calcular_viabilidade_excecao_http(agente, mocker):
    mocker.patch('requests.get', side_effect=Exception("Erro de timeout ou conexão"))

    resultado = agente.calcular_viabilidade("Algum Endereço")

    assert resultado["status"] == "erro"
    assert "HTTP Falha" in resultado["msg"]
    assert "Erro de timeout ou conexão" in resultado["msg"]
