from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from antigravity.agents.aninha import AninhaAgent
import uuid

router = APIRouter(prefix="/api/aninha", tags=["ANINHA", "TRIAGEM"])
aninha = AninhaAgent()

class LeadRequest(BaseModel):
    nome_condominio: str
    telefone: str
    email: str
    mensagem_original: str
    tipo_imovel: str = None
    num_unidades: int = None
    origem: str  # whatsapp, email, site
    prioridade_inferida: str = "baixa"

@router.post("/triagem")
async def triagem_lead(lead: LeadRequest):
    """
    Endpoint para triagem de leads da DL Soluções
    Atuará como Webhook que o n8n ou site direto consumirá.
    """
    try:
        # Gerar ID único para o lead
        lead_id = str(uuid.uuid4())

        # Preparar dados para ANINHA
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

        # Executar triagem com Regras de Negócio DL
        resultado = aninha.fazer_triagem(lead_data)
        return resultado

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
