import sys
import datetime
import importlib
from unittest.mock import MagicMock, patch

# To avoid polluting sys.modules for other tests, we only patch during the import of agencia_dl.
# We then import the module, and the patch.dict context manager cleans up after itself.
mock_modules = {
    'requests': MagicMock(),
    'dotenv': MagicMock(),
    'PIL': MagicMock(),
    'google': MagicMock(),
    'google.oauth2': MagicMock(),
    'google.oauth2.credentials': MagicMock(),
    'google.auth': MagicMock(),
    'google.auth.transport': MagicMock(),
    'google.auth.transport.requests': MagicMock(),
    'google_auth_oauthlib': MagicMock(),
    'google_auth_oauthlib.flow': MagicMock(),
    'googleapiclient': MagicMock(),
    'googleapiclient.discovery': MagicMock(),
    'googleapiclient.http': MagicMock(),
    'imageio_ffmpeg': MagicMock(),
    'google.genai': MagicMock(),
    'vertexai': MagicMock(),
    'vertexai.generative_models': MagicMock(),
    'vertexai.preview': MagicMock(),
    'vertexai.preview.vision_models': MagicMock(),
    'supabase': MagicMock()
}

with patch.dict(sys.modules, mock_modules):
    import execution.agencia_dl as agencia_dl

def test_tema_do_dia_marco_zero():
    """Testa que no marco zero (2026-03-01) o tema é o primeiro do ciclo."""
    marco_zero = datetime.date(2026, 3, 1)
    tema = agencia_dl._tema_do_dia(marco_zero)
    assert tema == "Segurança Eletrônica (Câmeras e CFTV)"

def test_tema_do_dia_ciclo_completo():
    """Testa que os temas ciclam corretamente ao longo de 4 dias."""
    marco_zero = datetime.date(2026, 3, 1)

    assert agencia_dl._tema_do_dia(marco_zero + datetime.timedelta(days=0)) == "Segurança Eletrônica (Câmeras e CFTV)"
    assert agencia_dl._tema_do_dia(marco_zero + datetime.timedelta(days=1)) == "Elétrica e Máquinas de Automação"
    assert agencia_dl._tema_do_dia(marco_zero + datetime.timedelta(days=2)) == "Energia Solar Fotovoltaica Híbrida (Bateria Ongrid)"
    assert agencia_dl._tema_do_dia(marco_zero + datetime.timedelta(days=3)) == "Sistemas de Prevenção de Incêndio"
    # Dia 4 recomeça o ciclo
    assert agencia_dl._tema_do_dia(marco_zero + datetime.timedelta(days=4)) == "Segurança Eletrônica (Câmeras e CFTV)"

def test_revisor_implacavel_validado():
    """Testa uma mensagem perfeitamente formatada."""
    texto = "Mensagem que pede a avaliação técnica, para o síndico, com responsável crea-rj."
    valido, motivo = agencia_dl.revisor_implacavel(texto)
    assert valido is True
    assert motivo == "Validado."

def test_revisor_implacavel_palavra_proibida():
    """Testa que a palavra 'visita técnica' é proibida."""
    texto = "Venha agendar sua visita técnica hoje mesmo síndico crea-rj!"
    valido, motivo = agencia_dl.revisor_implacavel(texto)
    assert valido is False
    assert "visita técnica" in motivo

def test_revisor_implacavel_falta_avaliacao_tecnica():
    """Testa que é obrigatório pedir 'Avaliação Técnica'."""
    texto = "Mensagem boa para o síndico aprovar, tudo com crea-rj, agende sua análise."
    valido, motivo = agencia_dl.revisor_implacavel(texto)
    assert valido is False
    assert "Avaliação Técnica" in motivo

def test_revisor_implacavel_publico_alvo():
    """Testa que deve focar em síndico ou administradora."""
    texto = "Agende uma avaliação técnica hoje! Responsabilidade crea-rj."
    valido, motivo = agencia_dl.revisor_implacavel(texto)
    assert valido is False
    assert "Síndicos/Administradoras" in motivo

def test_revisor_implacavel_crea_rj():
    """Testa que exige a menção ao crea-rj."""
    texto = "Síndico, marque sua avaliação técnica com nossos especialistas."
    valido, motivo = agencia_dl.revisor_implacavel(texto)
    assert valido is False
    assert "CREA" in motivo
