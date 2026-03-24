import logging
from typing import Dict, Any

class AgenteDeErro:
    """
    Agente responsável por monitorar logs do sistema (FastAPI)
    e potencialmente notificar via n8n/Telegram quando algo falha.
    """

    def __init__(self):
        self.logger = logging.getLogger("ErrorMonitor")
        # Em produção, você poderia configurar o logger para enviar
        # erros diretamente para um webhook do n8n (que manda pro Telegram)

    def registrar_falha(self, contexto: str, erro: Exception, dados: Dict[str, Any] = None):
        """
        Registra o erro e prepara um payload de notificação.
        """
        mensagem_erro = f"ALERTA DE FALHA [{contexto}]: {str(erro)}"

        if dados:
            mensagem_erro += f"\nDados em processamento: {dados}"

        self.logger.error(mensagem_erro)

        # AQUI É ONDE A MÁGICA ACONTECE:
        # Você pode usar a biblioteca requests (import requests) para
        # enviar um POST para um webhook do n8n que você criar.
        # Ex: requests.post("https://seu-n8n.com/webhook/alerta-erro", json={"mensagem": mensagem_erro})

        return {
            "status": "erro_registrado",
            "mensagem": mensagem_erro,
            "acao_sugerida": "Verificar log detalhado e notificar suporte no Telegram."
        }
