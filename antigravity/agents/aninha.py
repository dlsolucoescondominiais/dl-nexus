import re
import json
import os
import openai
from enum import Enum
from typing import Dict, List, Optional, Any
from datetime import datetime

class AninhaAgent:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY") 
        self.client = openai.OpenAI(api_key=api_key) if api_key else None
        
        self.termos_residenciais = [
            "apartamento", "apto", "minha casa", "residência", "residencial",
            "chuveiro", "tomada", "disjuntor do meu apartamento", "casa"
        ]
        
        self.system_prompt = """
Você é a Aninha, assistente de atendimento técnico-comercial da DL Soluções Condominiais.
Sua função é conversar com o cliente, entender a dor dele e classificar a demanda pareando com nossos serviços.

Regras INEGOCIÁVEIS:
1. NUNCA informe preço final sem Avaliação Técnica. Use apenas "a partir de" se for muito necessário, mas foque em agendar avaliação.
2. NUNCA cite "B2B" ao cliente.
3. NUNCA use a palavra "visita". Diga sempre "Avaliação Técnica".
4. NUNCA cite n8n, Supabase, KILLCRITIC, automação, IA, ou estrutura interna da DL.
5. NUNCA prometa execução residencial avulsa. Priorizamos condomínios, escolas, empresas e restaurantes/lanchonetes com chapas e fritadeiras profissionais Mult•Grill Express.
6. SEMPRE mantenha o contexto da conversa anterior. Reconheça dados já passados.

Sua resposta para o cliente deve ser natural, acolhedora e focar em coletar os seguintes dados (faça apenas 1 ou 2 perguntas por vez):
- Nome do condomínio/empresa
- Bairro/Localização
- Responsável
- Telefone
- Problema principal
- Melhor horário para Avaliação Técnica

Sempre devolva UM ÚNICO OUTPUT no formato JSON rigoroso:
{
  "responder_cliente": true,
  "resposta_cliente": "<texto para o cliente>",
  "intencao_atual": "<agendamento | orcamento | suporte | duvida_tecnica | comercial | residencial_bloqueado | indefinido>",
  "etapa_funil": "<inicio | coletando_dados_tecnicos | coletando_dados_condominio | aguardando_agendamento | lead_qualificado | encaminhado_humano | bloqueado_residencial>",
  "segmento": "<condominio | escola | empresa | restaurante_lanchonete | residencial | indefinido>",
  "dados_coletados": {
    "nome_condominio": null,
    "bairro": null,
    "responsavel": null,
    "telefone": null,
    "servico": null,
    "problema_relatado": null,
    "quantidade_bombas": null,
    "tipo_sistema": null,
    "urgencia": null,
    "melhor_horario": null
  },
  "lead_qualificado": false,
  "encaminhar_humano": false,
  "motivo_encaminhamento": null,
  "bloquear": false,
  "motivo_bloqueio": null
}
"""

    def verificar_residencial(self, mensagem: str) -> bool:
        mensagem_lower = mensagem.lower()
        for termo in self.termos_residenciais:
            if re.search(r'\b' + re.escape(termo) + r'\b', mensagem_lower):
                return True
        return False

    def analisar_mensagem_ia(self, mensagem_cliente: str, contexto: Dict) -> Dict[str, Any]:
        prompt_usuario = f"""
CONTEXTO ANTERIOR:
Última mensagem do cliente: {contexto.get('ultima_mensagem', 'N/A')}
Última resposta dada por você: {contexto.get('ultima_resposta', 'N/A')}
Dados já coletados: {json.dumps(contexto.get('dados_coletados', {}), ensure_ascii=False)}
Etapa do funil: {contexto.get('etapa_funil', 'inicio')}

MENSAGEM ATUAL DO CLIENTE:
"{mensagem_cliente}"

Gere a resposta em JSON mantendo os dados coletados anteriormente e atualizando com os novos.
"""
        if not self.client:
            # MOCK APRIMORADO PARA TESTES
            msg_lower = mensagem_cliente.lower()

            if "duas bombas" in msg_lower and "barra" in msg_lower:
                return {
                    "responder_cliente": True,
                    "resposta_cliente": "Perfeito. Entendi: são duas bombas, com painel desarmando, na Barra da Tijuca. Para avançar com a Avaliação Técnica, me informe o nome do condomínio, nome do responsável e melhor horário para atendimento.",
                    "intencao_atual": "agendamento",
                    "etapa_funil": "coletando_dados_condominio",
                    "segmento": "condominio",
                    "dados_coletados": {
                        "bairro": "Barra da Tijuca",
                        "problema_relatado": "Painel desarmando",
                        "quantidade_bombas": 2,
                        "servico": "eletrica"
                    },
                    "lead_qualificado": False,
                    "encaminhar_humano": False,
                    "motivo_encaminhamento": None,
                    "bloquear": False,
                    "motivo_bloqueio": None
                }
            elif "solar da barra" in msg_lower and "diogo" in msg_lower and "amanhã" in msg_lower:
                 return {
                    "responder_cliente": True,
                    "resposta_cliente": "Ótimo! Agendei a Avaliação Técnica para o Condomínio Solar da Barra com o responsável Diogo para amanhã de manhã. O nosso Tecnólogo entrará em contato em breve.",
                    "intencao_atual": "agendamento",
                    "etapa_funil": "aguardando_agendamento",
                    "segmento": "condominio",
                    "dados_coletados": {
                        "nome_condominio": "Solar da Barra",
                        "bairro": "Barra da Tijuca",
                        "responsavel": "Diogo",
                        "problema_relatado": "Painel desarmando",
                        "quantidade_bombas": 2,
                        "melhor_horario": "amanhã de manhã"
                    },
                    "lead_qualificado": True,
                    "encaminhar_humano": True,
                    "motivo_encaminhamento": "Avaliação Técnica agendada para aprovação do Diogo.",
                    "bloquear": False,
                    "motivo_bloqueio": None
                }
            elif "custa" in msg_lower or "preço" in msg_lower:
                 return {
                    "responder_cliente": True,
                    "resposta_cliente": "Não consigo informar um preço exato sem entender a infraestrutura atual. Para enviarmos um orçamento preciso, precisamos realizar uma Avaliação Técnica. Qual o nome do seu condomínio ou empresa?",
                    "intencao_atual": "orcamento",
                    "etapa_funil": "coletando_dados_condominio",
                    "segmento": "indefinido",
                    "dados_coletados": {},
                    "lead_qualificado": False,
                    "encaminhar_humano": False,
                    "motivo_encaminhamento": None,
                    "bloquear": False,
                    "motivo_bloqueio": None
                }
            else:
                return {
                    "responder_cliente": True,
                    "resposta_cliente": "Recebi sua mensagem. Para seguir com a Avaliação Técnica, me informe o nome do condomínio, bairro e o problema principal identificado.",
                    "intencao_atual": "agendamento",
                    "etapa_funil": "coletando_dados_tecnicos",
                    "segmento": "indefinido",
                    "dados_coletados": {},
                    "lead_qualificado": False,
                    "encaminhar_humano": False,
                    "motivo_encaminhamento": None,
                    "bloquear": False,
                    "motivo_bloqueio": None
                }

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                response_format={ "type": "json_object" },
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt_usuario}
                ],
                temperature=0.3
            )
            
            payload = json.loads(response.choices[0].message.content)
            
            # Garantir formato exato no output do LLM
            dados_coletados_atuais = contexto.get("dados_coletados", {})
            dados_novos = payload.get("dados_coletados", {})
            if not isinstance(dados_novos, dict): dados_novos = {}
            dados_mergeados = {**dados_coletados_atuais, **dados_novos}
            
            payload_formatado = {
                "responder_cliente": bool(payload.get("responder_cliente", True)),
                "resposta_cliente": payload.get("resposta_cliente", "Recebi sua solicitação, logo retorno."),
                "intencao_atual": payload.get("intencao_atual", "indefinido"),
                "etapa_funil": payload.get("etapa_funil", "inicio"),
                "segmento": payload.get("segmento", "indefinido"),
                "dados_coletados": dados_mergeados,
                "lead_qualificado": bool(payload.get("lead_qualificado", False)),
                "encaminhar_humano": bool(payload.get("encaminhar_humano", False)),
                "motivo_encaminhamento": payload.get("motivo_encaminhamento", None),
                "bloquear": bool(payload.get("bloquear", False)),
                "motivo_bloqueio": payload.get("motivo_bloqueio", None)
            }
            return payload_formatado

        except Exception as e:
            return {
                "erro": True,
                "detalhe": str(e),
                "responder_cliente": True,
                "resposta_cliente": "Recebi sua mensagem. Para seguir com a Avaliação Técnica, me informe o nome do condomínio, bairro e o problema principal identificado.",
                "intencao_atual": "indefinido",
                "etapa_funil": "inicio",
                "segmento": "indefinido",
                "dados_coletados": {},
                "lead_qualificado": False,
                "encaminhar_humano": False,
                "motivo_encaminhamento": None,
                "bloquear": False,
                "motivo_bloqueio": None
            }

    def fazer_triagem(self, lead_data: Dict) -> Dict:
        mensagem = lead_data.get("mensagem_atual", "")
        contexto = lead_data.get("contexto", {})
        
        # Bloqueio Residencial Imediato ANTES da IA
        if self.verificar_residencial(mensagem):
            return {
              "responder_cliente": True,
              "resposta_cliente": "No momento, a DL Soluções Condominiais atende demandas técnicas voltadas a condomínios, escolas, empresas e suporte a equipamentos profissionais. Para esse tipo de solicitação residencial avulsa, não conseguimos seguir com atendimento.",
              "intencao_atual": "residencial_bloqueado",
              "etapa_funil": "bloqueado_residencial",
              "segmento": "residencial",
              "dados_coletados": contexto.get("dados_coletados", {}),
              "lead_qualificado": False,
              "encaminhar_humano": False,
              "motivo_encaminhamento": None,
              "bloquear": True,
              "motivo_bloqueio": "solicitacao_residencial_avulsa"
            }

        resultado_ia = self.analisar_mensagem_ia(mensagem, contexto)
        
        # Adicionar metadata extra que a rota precisa
        resultado_ia["status"] = "bloqueado" if resultado_ia.get("bloquear") else "triado"
        resultado_ia["lead_id"] = lead_data.get("chat_id")
        
        return resultado_ia
