import os
import json
import logging
import hmac
import hashlib
import requests
from fastapi import APIRouter, Request, HTTPException, Response, Body, BackgroundTasks

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/meta", tags=["Meta Webhooks"])

META_VERIFY_TOKEN = os.getenv("META_VERIFY_TOKEN", "dl-nexus-default-token")
META_APP_SECRET = os.getenv("META_APP_SECRET", "")
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL", "http://n8n:5678/webhook/meta")

def verify_signature(payload_body: bytes, signature_header: str) -> bool:
    """7. Segurança básica: Validação de assinatura SHA256 do Meta."""
    if not META_APP_SECRET or not signature_header:
        return False
    if not signature_header.startswith('sha256='):
        return False
    signature = signature_header.split('=')[1]
    expected_signature = hmac.new(
        META_APP_SECRET.encode('utf-8'),
        payload_body,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected_signature, signature)

def persist_data_fallback(payload: dict):
    """10. Persistência dos dados: Fallback quando o n8n está indisponível."""
    try:
        logger.info("Executando fallback de persistência de dados.")
        with open("meta_webhook_fallback.log", "a") as f:
            f.write(json.dumps(payload) + "\n")
    except Exception as e:
        logger.error(f"Falha na persistência de fallback: {e}")

def forward_to_n8n(payload: dict):
    """9. Encaminhamento para próximo nó: Roteia o payload para o n8n."""
    try:
        # Usa requests de forma síncrona, executado no threadpool pelo FastAPI BackgroundTasks
        response = requests.post(N8N_WEBHOOK_URL, json=payload, timeout=5)
        response.raise_for_status()
        logger.info("Payload encaminhado com sucesso para n8n.")
    except Exception as e:
        logger.error(f"Erro ao encaminhar para n8n: {e}")
        # Aciona fallback de persistência
        persist_data_fallback(payload)

@router.get("/webhook")
def verify_webhook(request: Request):
    """
    1. URL ativa (GET)
    2. Método correto: GET
    4. Resposta HTTP: Confirmação do Hub Challenge para Meta.
    """
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if mode and token:
        if mode == "subscribe" and token == META_VERIFY_TOKEN:
            logger.info("Webhook Meta verificado com sucesso.")
            return Response(content=challenge, status_code=200)
        else:
            # 6. Tratamento de erro
            logger.warning("Falha na verificação: token inválido.")
            raise HTTPException(status_code=403, detail="Token de verificação inválido")

    raise HTTPException(status_code=400, detail="Parâmetros inválidos")

@router.post("/webhook")
def receive_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    body_bytes: bytes = Body(...)
):
    """
    1. URL ativa (POST)
    2. Método correto: POST
    3. Payload esperado: Mensagens do WhatsApp/Instagram
    5. Tempo de resposta: Rápido (processamento em background)
    """
    # 7. Segurança básica
    signature = request.headers.get("X-Hub-Signature-256")
    if META_APP_SECRET:
        if not signature or not verify_signature(body_bytes, signature):
            logger.error("Assinatura Meta ausente ou inválida.")
            raise HTTPException(status_code=403, detail="Assinatura inválida")

    try:
        payload = json.loads(body_bytes)
    except json.JSONDecodeError:
        # 6. Tratamento de erro
        raise HTTPException(status_code=400, detail="JSON inválido")

    # 8. Registro no log
    logger.info(f"Evento Meta recebido: {payload.get('object', 'unknown')}")

    # 9. Encaminhamento para próximo nó (via background para manter o Tempo de Resposta baixo)
    background_tasks.add_task(forward_to_n8n, payload)

    # 4. Resposta HTTP: Retorna 200 OK rapidamente conforme exigido pelo Meta
    return {"status": "success", "message": "EVENT_RECEIVED"}
