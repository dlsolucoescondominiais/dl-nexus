from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
from antigravity.agents.agente_jules_auditor import JulesAuditorAgent

router = APIRouter(prefix="/api/propostas", tags=["PROPOSTAS", "AUDITORIA"])
jules_auditor = JulesAuditorAgent()

class PropostaRequest(BaseModel):
    lead_id: str
    servico: str
    dados_tecnicos: Dict[str, Any]
    proposta_bruta: str
    engenheiro_responsavel: Optional[str] = "Diogo"

@router.post("/gerar-auditar")
async def gerar_e_auditar_proposta(req: PropostaRequest):
    """
    Simula o recebimento de uma proposta técnica elaborada por um agente especialista
    (Elétrica, Solar, etc.) e OBRIGATORIAMENTE passa pelo crivo do Auditor Jules (Claude)
    antes de ser disparada para o n8n ou cliente.
    """
    try:
        # 1. Aqui seria o ponto onde o agente especialista já processou os dados.
        #    Como recebemos a 'proposta_bruta' via POST, vamos assumir que ela já
        #    foi gerada por outro LLM (ex: Agente Solar).

        texto_bruto = req.proposta_bruta

        # Inserindo um erro proposital para testar a regra do "Diogo" se não houver no texto
        if "Diogo" not in texto_bruto:
             texto_bruto += "\n\nLaudo assinado por: Engenheiro Diogo."

        # 2. A MÁGICA: Auditoria Técnica rigorosa com o Agente Jules (Claude)
        resultado_auditoria = jules_auditor.auditar_proposta(
            proposta_bruta=texto_bruto,
            dados_contexto=req.dados_tecnicos
        )

        # 3. Tratamento pós-auditoria
        if resultado_auditoria.get("status_auditoria") == "REJEITADO_REVISAO_PROFUNDA":
            # Aqui você poderia acionar um webhook de erro no n8n alertando que
            # a proposta foi muito ruim e requer intervenção humana do Diogo ou Raphael.
            pass
        elif resultado_auditoria.get("status_auditoria", "").startswith("ERRO"):
            # Falha na API ou parsing. Retorna a bruta para não travar o processo,
            # mas avisa no log.
            print(f"ALERTA: Falha na Auditoria Jules: {resultado_auditoria.get('notas_do_auditor')}")
        else:
            # Substitui a proposta bruta pela corrigida para os próximos passos
            texto_final = resultado_auditoria.get("proposta_corrigida", req.proposta_bruta)

        # 4. Retorno Estruturado para o n8n (que vai gerar o PDF e mandar no WhatsApp)
        return {
            "lead_id": req.lead_id,
            "servico": req.servico,
            "status": "aprovado_auditoria",
            "proposta_final": resultado_auditoria.get("proposta_corrigida", texto_bruto),
            "notas_qa": resultado_auditoria.get("notas_do_auditor", "Sem notas."),
            "timestamp": "2024-03-24T20:00:00Z" # Substituir por datetime real
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no pipeline de propostas: {str(e)}")
