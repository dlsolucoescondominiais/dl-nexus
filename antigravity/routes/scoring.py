from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api/nexus", tags=["LEADS", "SCORING"])

class LeadScoringRequest(BaseModel):
    bairro: str
    historico_ticket_regiao: float

@router.post("/score-lead")
async def calculate_lead_score(request: LeadScoringRequest):
    """
    Calcula o Lead Score baseado na região geográfica (RJ) e no ticket médio histórico.
    """
    bairro_lower = request.bairro.lower()
    score_geografico = 0

    # Zonas de alto valor para condomínios
    zonas_sul_oeste = ["barra da tijuca", "recreio", "leblon", "ipanema", "copacabana", "botafogo", "flamengo"]
    zonas_norte_centro = ["tijuca", "vila isabel", "grajau", "maracana", "centro"]

    if any(zona in bairro_lower for zona in zonas_sul_oeste):
        score_geografico += 50
    elif any(zona in bairro_lower for zona in zonas_norte_centro):
        score_geografico += 30
    else:
        score_geografico += 10

    # Ticket score logic
    score_ticket = 0
    if request.historico_ticket_regiao > 5000:
        score_ticket += 50
    elif request.historico_ticket_regiao > 1500:
        score_ticket += 30
    else:
        score_ticket += 10

    total_score = score_geografico + score_ticket

    prioridade = "ALTA"
    if total_score < 40:
        prioridade = "BAIXA"
    elif total_score < 70:
        prioridade = "MEDIA"

    return {
        "score_total": total_score,
        "score_geografico": score_geografico,
        "score_ticket": score_ticket,
        "prioridade": prioridade,
        "mensagem": "Lead classificado com sucesso. Priorize leads ALTA."
    }
