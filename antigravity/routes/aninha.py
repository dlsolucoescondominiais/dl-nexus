import os
import uuid
import requests
from supabase import create_client, Client
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from antigravity.agents.aninha import AninhaAgent

# Setup Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://xyz.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "dummy-key")

def get_supabase_client() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

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
def triagem_lead(lead: LeadRequest, bg_tasks: BackgroundTasks):
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

        # 4. Registrar lead no Supabase
        try:
            supabase = get_supabase_client()
            lead_db_data = {
                "id": lead_id,
                "nome": resultado.get("nome", "Não Identificado"),
                "telefone": resultado.get("telefone"),
                "email": resultado.get("email"),
                "nome_condominio": resultado.get("nome_condominio"),
                "status": "triado",
                "motivo": resultado.get("motivo"),
                "urgencia": resultado.get("urgencia"),
                "categoria_servico": resultado.get("categoria_servico"),
                "porte": resultado.get("porte"),
                "origem": resultado.get("origem"),
                "tipo_local": resultado.get("tipo_local"),
                "bairro": resultado.get("bairro"),
                "perfil_cliente": resultado.get("perfil_cliente"),
                "tipo_demanda": resultado.get("tipo_demanda"),
                "tipo_trabalho": resultado.get("tipo_trabalho"),
            }
            supabase.table("leads").upsert(lead_db_data).execute()
        except Exception as db_err:
            print(f"Erro ao salvar lead no Supabase: {db_err}")

        # 5. Envia o callback ao Orquestrador (n8n/Supabase) para o Dashboard atualizar realtime
        # Passa o 'status' alterado (ex: 'triado' ou 'bloqueado')
        bg_tasks.add_task(disparar_webhook_n8n_background, resultado)

        # 6. Retorna o JSON para a interface que chamou
        return resultado
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
