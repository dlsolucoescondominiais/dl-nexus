import os
import httpx
from fastapi import APIRouter, HTTPException, BackgroundTasks, Header
from pydantic import BaseModel
from typing import Optional
from antigravity.agents.aninha import AninhaAgent

router = APIRouter(prefix="/api/leads", tags=["LEADS", "INTEGRAÇÃO"])
aninha = AninhaAgent()

# Configurações do Supabase (Vêm do root .env ou injetadas)
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://nejdtvkpiclagsnfljsz.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY") # Precisamos para INSERT
DL_API_KEY = os.getenv("N8N_API_KEY", "DL-SECRET-2026") # Chave compartilhada com n8n

class LeadSitePayload(BaseModel):
    origem: str
    nome_contato: str
    telefone: str
    tipo_cliente: str # "sindico", "admin_condominio", etc
    servico: str # "eletrica", "solar", etc
    mensagem: str

@router.post("/site-receptor")
async def site_receptor(
    payload: LeadSitePayload, 
    bg_tasks: BackgroundTasks,
    x_dl_api_key: Optional[str] = Header(None)
):
    """
    Endpoint Gateway: Recebe leads do n8n (que por sua vez recebe do site).
    Faz o mapeamento para o Supabase e dispara a Aninha.
    """
    
    # 1. Validação de Segurança Básica (Header X-DL-API-KEY)
    if x_dl_api_key != DL_API_KEY:
        raise HTTPException(status_code=403, detail="Acesso negado: API Key inválida.")

    # 2. Mapeamento para o Schema do Supabase
    lead_db = {
        "origem": payload.origem,
        "nome_contato": payload.nome_contato,
        "telefone": payload.telefone,
        "persona": payload.tipo_cliente,         # Mapeado conforme Ordem de Comando
        "tipo_servico": payload.servico,
        "historico_das_dores": payload.mensagem, # Mapeado conforme Ordem de Comando
        "status": "novo",
        "prioridade": "alta"
    }

    # 3. Inserção no Supabase (REST API)
    try:
        async with httpx.AsyncClient() as client:
            headers = {
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}",
                "Content-Type": "application/json",
                "Prefer": "return=minimal"
            }
            supabase_endpoint = f"{SUPABASE_URL}/rest/v1/leads"
            resp = await client.post(supabase_endpoint, json=lead_db, headers=headers)
            resp.raise_for_status()
    except Exception as e:
        print(f"Erro ao inserir no Supabase: {e}")
        # Prosseguimos mesmo se o insert falhar para não bloquear o webhook do site, 
        # mas idealmente logamos para correção.
        pass

    # 4. Gatilho da Aninha (Background Task)
    # Reutilizamos a lógica da Aninha para triar e iniciar contato
    lead_para_ia = {
        "nome_condominio": "A definir (Site)", 
        "telefone": payload.telefone,
        "email": "site@contato.com", # Placeholder se não vier do site
        "mensagem_original": payload.mensagem,
        "origem": payload.origem,
        "prioridade_inferida": "alta"
    }
    
    # Adicionamos à fila de execução para não travar o HTTP Response
    # A Aninha fará a triagem e notificará o n8n via callback
    bg_tasks.add_task(aninha.fazer_triagem, lead_para_ia)

    return {
        "status": "sucesso", 
        "mensagem": "Lead processado e encaminhado para Aninha (Avaliação Técnica).",
        "mapeamento": "persona/historico_das_dores"
    }
