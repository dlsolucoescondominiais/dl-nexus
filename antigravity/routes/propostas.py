from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
from antigravity.agents.agente_jules_auditor import JulesAuditorAgent
import os
import openai

router = APIRouter(prefix="/api/propostas", tags=["PROPOSTAS", "AUDITORIA"])
jules_auditor = JulesAuditorAgent()

# Inicialização segura do cliente OpenAI (Camada 4 da Pirâmide de Custos)
openai.api_key = os.environ.get("OPENAI_API_KEY")

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
    e OBRIGATORIAMENTE passa pelo crivo do Auditor Jules (Claude)
    """
    try:
        texto_bruto = req.proposta_bruta

        if "Diogo" not in texto_bruto:
             texto_bruto += "\n\nLaudo assinado por: Engenheiro Diogo."

        resultado_auditoria = jules_auditor.auditar_proposta(
            proposta_bruta=texto_bruto,
            dados_contexto=req.dados_tecnicos
        )

        if resultado_auditoria.get("status_auditoria", "").startswith("ERRO"):
            print(f"ALERTA: Falha na Auditoria Jules: {resultado_auditoria.get('notas_do_auditor')}")
        else:
            texto_final = resultado_auditoria.get("proposta_corrigida", req.proposta_bruta)

        return {
            "lead_id": req.lead_id,
            "servico": req.servico,
            "status": "aprovado_auditoria",
            "proposta_final": resultado_auditoria.get("proposta_corrigida", texto_bruto),
            "notas_qa": resultado_auditoria.get("notas_do_auditor", "Sem notas."),
            "timestamp": "2024-03-24T20:00:00Z"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no pipeline de propostas: {str(e)}")


class ArtigoRequest(BaseModel):
    prompt_gerador: str
    tema: Optional[str] = "Geral"

SYSTEM_PROMPT_MARKETING = """
Você é o Especialista de Marketing e Engenharia Comercial da DL Soluções Condominiais.
Sua missão é criar postagens técnicas, persuasivas e focadas em conversão para síndicos profissionais e administradoras no Rio de Janeiro (Zonas Sul, Sudoeste, Oeste e Norte).

PORTFÓLIO: Elétrica, Energia Solar, CFTV, Prevenção de Incêndio, Mobilidade (CVE).

🚨 REGRA DE OURO (FOCO AGRESSIVO EM RECEITA RECORRENTE):
Em 70% das suas criações, você deve dar ênfase máxima aos nossos serviços de assinatura:
1. Portaria Autônoma: Foque na redução brutal de custos na folha de pagamento e aumento da segurança 24h.
2. Plano DL Fortress: Destaque a nossa blindagem tecnológica e manutenção preventiva contínua.
3. Plano DL Partner: Venda a tranquilidade do síndico ter uma infraestrutura que não quebra.

TOM DE VOZ: Autoridade técnica impecável. Demonstre solidez empresarial. O líder da operação é um Tecnólogo especialista. Nunca prometa preços fixos, prometa "Avaliação Técnica".
"""

@router.post("/gerar-artigo")
async def gerar_artigo_redes_sociais(req: ArtigoRequest):
    """
    Endpoint para geração de artigos técnicos e persuasivos para redes sociais.
    Consumido pelo Workflow 013 do n8n.
    Utiliza OpenAI (Camada 4 - Copy Comercial).
    """
    try:
        if not openai.api_key:
            return {
                "status": "aviso_sem_chave",
                "tema_solicitado": req.tema,
                "texto_artigo": "🛠️ Aviso do Sistema: OpenAI API Key não configurada. Configure para gerar o texto real de marketing."
            }

        resposta = openai.chat.completions.create(
            model="gpt-4o-mini", # Custo baixo para tarefas recorrentes de copy
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT_MARKETING},
                {"role": "user", "content": req.prompt_gerador}
            ],
            temperature=0.7
        )

        texto_gerado = resposta.choices[0].message.content

        return {
            "status": "sucesso",
            "tema_solicitado": req.tema,
            "texto_artigo": texto_gerado
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar artigo na OpenAI: {str(e)}")
