import os
import requests
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/api/marketing", tags=["MARKETING", "AUTOMAÇÃO"])

# URL do n8n que escuta a sua aprovação manual
WEBHOOK_APROVACAO_N8N = os.getenv("N8N_WEBHOOK_URL", "https://n8n.dlsolucoescondominiais.com.br/webhook/dl-aprovar-post")
API_KEY_N8N = os.getenv("N8N_API_KEY", "dl-nexus-auth-2026")

class PostApprovalRequest(BaseModel):
    post_id: str
    copy_aprovada: str
    imagem_url: str

@router.post("/aprovar")
async def aprovar_post(request: PostApprovalRequest):
    """
    Endpoint chamado pelo Frontend (DL Commander) quando o Diogo
    clica em 'Aprovar e Postar' no rascunho gerado pela IA.
    """
    try:
        headers = {
            "Content-Type": "application/json",
            "X-DL-API-KEY": API_KEY_N8N
        }
        payload = request.model_dump()

        # Dispara o gatilho para o n8n fazer o push final para o Facebook/Instagram API
        resp = requests.post(WEBHOOK_APROVACAO_N8N, json=payload, headers=headers, timeout=15)

        if resp.status_code not in (200, 201):
            raise Exception(f"Orquestrador n8n retornou erro: {resp.text}")

        return {"status": "success", "message": "Postagem encaminhada ao Orquestrador (Meta API)."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
