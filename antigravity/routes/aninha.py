import os
import uuid
import requests
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from antigravity.agents.aninha import AninhaAgent

router = APIRouter(prefix="/api/aninha", tags=["ANINHA", "TRIAGEM"])
aninha = AninhaAgent()

# Webhook Oficial do N8N - O orquestrador precisa saber se a Aninha gerou uma proposta
WEBHOOK_RETORNO_N8N = os.getenv("N8N_WEBHOOK_URL", "https://n8n.dlsolucoescondominiais.com.br/webhook/dl-automacao-sindicos")
API_KEY_N8N = os.getenv("N8N_API_KEY", "TESTE-123")

class LeadRequest(BaseModel):
    nome_condominio: str
    telefone: str
    email: str
    mensagem_original: str
    tipo_imovel: str = None
    num_unidades: int = None
    origem: str  # whatsapp, email, site
    prioridade_inferida: str = "baixa"

def disparar_webhook_n8n_background(resultado_triagem: dict):
    """
    Função assíncrona (background) para notificar o Orquestrador
    e a Interface de que a análise da IA foi concluída.
    """
    try:
        headers = {
            "Content-Type": "application/json",
            "X-DL-API-KEY": API_KEY_N8N
        }
        resp = requests.post(WEBHOOK_RETORNO_N8N, json=resultado_triagem, headers=headers, timeout=10)
        print(f"Callback n8n disparado com sucesso: HTTP {resp.status_code}")
    except Exception as e:
        print(f"Falha ao notificar o webhook do n8n: {e}")

@router.post("/triagem")
async def triagem_lead(lead: LeadRequest, bg_tasks: BackgroundTasks):
    """
    Endpoint para triagem de leads da DL Soluções
    Se a análise for complexa, retorna imediato e deixa webhook pra avisar.
    """
    try:
        # 1. Gera ID para o fluxo
        lead_id = str(uuid.uuid4())
        
        # 2. Dados da Mente DL
        lead_data = {
            "lead_id": lead_id,
            "nome_condominio": lead.nome_condominio,
            "telefone": lead.telefone,
            "email": lead.email,
            "mensagem_original": lead.mensagem_original,
            "tipo_imovel": lead.tipo_imovel,
            "num_unidades": lead.num_unidades,
            "origem": lead.origem,
            "prioridade": lead.prioridade_inferida,
        }
        
        # 3. Executar o motor da Aninha
        resultado = aninha.fazer_triagem(lead_data)

        # 4. Envia o callback ao Orquestrador (n8n/Supabase) para o Dashboard atualizar realtime
        # Passa o 'status' alterado (ex: 'triado' ou 'bloqueado')
        bg_tasks.add_task(disparar_webhook_n8n_background, resultado)

        # 5. Retorna o JSON para a interface que chamou
        return resultado
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
