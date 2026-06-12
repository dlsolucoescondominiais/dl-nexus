import os
import uuid
import requests
import traceback
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from antigravity.agents.aninha import AninhaAgent

router = APIRouter(prefix="/api/aninha", tags=["ANINHA", "TRIAGEM"])
aninha = AninhaAgent()

WEBHOOK_RETORNO_N8N = os.getenv("N8N_WEBHOOK_URL", "https://n8n.dlsolucoescondominiais.com.br/webhook/dl-automacao-sindicos")
API_KEY_N8N = os.getenv("N8N_API_KEY", "TESTE-123")

# Credenciais Supabase via Env
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://nejdtvkpiclagsnfljsz.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_ANON_KEY")

class ContextoRequest(BaseModel):
    intencao_atual: Optional[str] = None
    etapa_funil: Optional[str] = None
    segmento: Optional[str] = None
    dados_coletados: Dict[str, Any] = Field(default_factory=dict)
    ultima_mensagem: Optional[str] = None
    ultima_resposta: Optional[str] = None

class LeadRequest(BaseModel):
    canal: str = "telegram"
    chat_id: str
    message_id: str
    nome_usuario: Optional[str] = None
    username: Optional[str] = None
    mensagem_atual: str
    contexto: Optional[ContextoRequest] = None

def check_duplicate_message(chat_id: str, message_id: str) -> bool:
    if not SUPABASE_URL or not SUPABASE_KEY: return False
    try:
        headers = {"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}"}
        url = f"{SUPABASE_URL}/rest/v1/mensagens_processadas_aninha?chat_id=eq.{chat_id}&message_id=eq.{message_id}&select=*"
        res = requests.get(url, headers=headers, timeout=5)
        if res.status_code == 200 and len(res.json()) > 0: return True
    except Exception: pass
    return False

def save_processed_message(chat_id: str, message_id: str):
    if not SUPABASE_URL or not SUPABASE_KEY: return
    try:
        headers = {"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}", "Content-Type": "application/json", "Prefer": "return=minimal"}
        url = f"{SUPABASE_URL}/rest/v1/mensagens_processadas_aninha"
        payload = {"chat_id": chat_id, "message_id": message_id}
        requests.post(url, headers=headers, json=payload, timeout=5)
    except Exception: pass

def save_error_log(modulo: str, erro: str):
    if not SUPABASE_URL or not SUPABASE_KEY: return
    try:
        headers = {"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}", "Content-Type": "application/json", "Prefer": "return=minimal"}
        url = f"{SUPABASE_URL}/rest/v1/logs_aninha_erros"
        payload = {"modulo": modulo, "mensagem_erro": erro}
        requests.post(url, headers=headers, json=payload, timeout=5)
    except Exception: pass

def log_event(chat_id: str, message_id: str, mensagem: str, resposta: str):
    if not SUPABASE_URL or not SUPABASE_KEY: return
    try:
        headers = {"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}", "Content-Type": "application/json", "Prefer": "return=minimal"}
        url = f"{SUPABASE_URL}/rest/v1/eventos_aninha"
        payload = {"chat_id": chat_id, "message_id": message_id, "mensagem": mensagem, "resposta": resposta}
        requests.post(url, headers=headers, json=payload, timeout=5)
    except Exception: pass

def save_conversation(chat_id: str, nome_usuario: str, username: str, contexto: dict):
    if not SUPABASE_URL or not SUPABASE_KEY: return
    try:
        headers = {"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}", "Content-Type": "application/json", "Prefer": "resolution=merge-duplicates"}
        url = f"{SUPABASE_URL}/rest/v1/conversas_aninha"
        payload = {
            "chat_id": chat_id,
            "nome_usuario": nome_usuario,
            "username": username,
            "contexto": contexto,
            "updated_at": datetime.now().isoformat()
        }
        requests.post(url, headers=headers, json=payload, timeout=5)
    except Exception as e:
        save_error_log("save_conversation", str(e))

@router.post("/triagem")
def triagem_lead(lead: LeadRequest):
    """
    Endpoint para triagem de leads da DL Soluções usando Aninha Fase 2.
    """
    try:
        # Anti-duplicidade
        if check_duplicate_message(lead.chat_id, lead.message_id):
            return {"status": "ignorado", "motivo": "Mensagem duplicada"}

        # Registrar que estamos processando
        save_processed_message(lead.chat_id, lead.message_id)

        # Preparar os dados para o Motor Aninha
        lead_data = {
            "chat_id": lead.chat_id,
            "message_id": lead.message_id,
            "mensagem_atual": lead.mensagem_atual,
            "contexto": lead.contexto.dict() if lead.contexto else {},
            "nome_usuario": lead.nome_usuario
        }

        # Executar motor Aninha (Trata residencial e IA internamente)
        resultado = aninha.fazer_triagem(lead_data)

        resposta_cliente = resultado.get("resposta_cliente", "Recebi sua solicitação, aguarde nosso contato.")

        # Atualizar Contexto para a API do Chat Bot / N8n
        novo_contexto = lead.contexto.dict() if lead.contexto else {}
        novo_contexto["ultima_mensagem"] = lead.mensagem_atual
        novo_contexto["ultima_resposta"] = resposta_cliente
        novo_contexto["intencao_atual"] = resultado.get("intencao_atual")
        novo_contexto["etapa_funil"] = resultado.get("etapa_funil")
        novo_contexto["segmento"] = resultado.get("segmento")
        novo_contexto["dados_coletados"] = resultado.get("dados_coletados", {})

        # Salvar DB Logs e Contexto
        save_conversation(lead.chat_id, lead.nome_usuario, lead.username, novo_contexto)
        log_event(lead.chat_id, lead.message_id, lead.mensagem_atual, resposta_cliente)

        return resultado

    except Exception as e:
        erro_trace = traceback.format_exc()
        save_error_log("triagem_lead", erro_trace)

        # Fallback rígido em caso de CRASH TOTAL Python
        fallback_msg = "Recebi sua mensagem. Para seguir com a Avaliação Técnica, me informe o nome do condomínio, bairro e o problema principal identificado."

        log_event(lead.chat_id, lead.message_id, lead.mensagem_atual, fallback_msg)
        return {
            "status": "erro",
            "erro": str(e),
            "responder_cliente": True,
            "resposta_cliente": fallback_msg,
            "intencao_atual": "indefinido",
            "etapa_funil": "inicio",
            "segmento": "indefinido",
            "dados_coletados": {},
            "lead_qualificado": False,
            "encaminhar_humano": False,
            "bloquear": False
        }
