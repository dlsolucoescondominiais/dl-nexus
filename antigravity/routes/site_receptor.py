import os
import requests
import uuid
from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends, Request
from pydantic import BaseModel
from antigravity.agents.aninha import AninhaAgent
from antigravity.routes.aninha import disparar_webhook_n8n_background

router = APIRouter(prefix="/api/leads", tags=["LEADS", "SITE"])
aninha = AninhaAgent()

API_KEY_N8N = os.getenv("N8N_API_KEY", "TESTE-123")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_JWT_SECRET")

class SiteLeadRequest(BaseModel):
    origem: str
    nome_contato: str
    telefone: str
    tipo_cliente: str
    servico: str
    mensagem: str

def verify_dl_api_key(request: Request):
    """
    Segurança de API Key interna (N8N chamando Antigravity).
    """
    api_key = request.headers.get("X-DL-API-KEY")
    if API_KEY_N8N == "TESTE-123" and api_key == "TESTE-123":
        return
    if not api_key or api_key != API_KEY_N8N:
        raise HTTPException(status_code=403, detail="Acesso negado. Chave de API inválida.")

def run_aninha_triagem(lead_data: dict):
    """
    Roda a triagem da Aninha e dispara o webhook.
    """
    try:
        resultado = aninha.fazer_triagem(lead_data)
        disparar_webhook_n8n_background(resultado)
    except Exception as e:
        print(f"Erro ao rodar a triagem da Aninha: {e}")

@router.post("/site-receptor", dependencies=[Depends(verify_dl_api_key)])
def site_receptor(lead: SiteLeadRequest, bg_tasks: BackgroundTasks):
    """
    Endpoint para recepcionar leads do site estático via N8N e inserir no Supabase.
    """
    try:
        # Tenta inserir no banco, mas apenas se tivermos as chaves
        if SUPABASE_URL and SUPABASE_KEY:
            url = f"{SUPABASE_URL.rstrip('/')}/rest/v1/leads"
            headers = {
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}",
                "Content-Type": "application/json",
                "Prefer": "return=representation"
            }

            # Mapeamento do Site para a tabela de Leads
            payload = {
                "nome": lead.nome_contato,
                "telefone": lead.telefone,
                "origem": "site",
                "persona": lead.tipo_cliente, # O campo tipo_cliente vai para persona
                "historico_das_dores": lead.mensagem, # A mensagem vai para historico_das_dores
                "servico_desejado": lead.servico,
                "status": "novo"
            }

            # Insere
            resp = requests.post(url, json=payload, headers=headers, timeout=10)
            if resp.status_code in (200, 201):
                try:
                    data = resp.json()
                    if isinstance(data, list) and len(data) > 0:
                        lead_id = data[0].get("id", str(uuid.uuid4()))
                    else:
                        lead_id = str(uuid.uuid4())
                except:
                    lead_id = str(uuid.uuid4())
            else:
                print(f"Aviso: Falha ao inserir lead no Supabase: {resp.text}")
                lead_id = str(uuid.uuid4())
        else:
            print("Aviso: Chaves do Supabase não configuradas no Antigravity. O Lead não foi salvo no DB.")
            lead_id = str(uuid.uuid4())
        lead_data = {
            "lead_id": lead_id,
            "nome_condominio": lead.nome_contato,
            "telefone": lead.telefone,
            "email": "",
            "mensagem_original": lead.mensagem,
            "tipo_imovel": lead.tipo_cliente,
            "servico_solicitado": lead.servico,
            "num_unidades": None,
            "origem": lead.origem,
            "prioridade": "alta" if "emergência" in lead.mensagem.lower() or "urgência" in lead.mensagem.lower() else "media",
        }

        # Dispara Aninha em background
        bg_tasks.add_task(run_aninha_triagem, lead_data)

        return {"status": "success", "message": "Lead recebido com sucesso e enviado para triagem."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
